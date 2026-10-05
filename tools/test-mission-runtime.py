#!/usr/bin/env python3
"""Compile real production-method extracts and exercise the Harmony prefix offline.

Only repository-local ignored fixtures are generated. Unity/game code is not executed.
The fake producer models the separately inspected IL, not a live multiplayer session.
"""
import argparse
import json
import os
from pathlib import Path
import re
import subprocess
import uuid

ROOT = Path(__file__).resolve().parents[1]
BASELINE = "fde844a62ed6b19e2c24d10931c0b54530a6d41b"


def definition(source, anchor, field=False):
    """Extract a complete C# definition, ignoring braces inside literals/comments."""
    if source.count(anchor) != 1:
        raise ValueError(f"Expected one production definition: {anchor}")
    start = source.index(anchor)
    opening = source.index("{", start)
    depth, state, escape = 0, "code", False
    i = opening
    while i < len(source):
        ch = source[i]
        following = source[i:i + 2]
        if state == "line":
            if ch == "\n":
                state = "code"
        elif state == "comment":
            if following == "*/":
                state = "code"
                i += 1
        elif state in ("string", "char"):
            if escape:
                escape = False
            elif ch == "\\":
                escape = True
            elif ch == ('"' if state == "string" else "'"):
                state = "code"
        elif following == "//":
            state = "line"
            i += 1
        elif following == "/*":
            state = "comment"
            i += 1
        elif ch in ('"', "'"):
            state = "string" if ch == '"' else "char"
        elif ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                end = i + 1
                if field:
                    if source[end:end + 1] != ";":
                        raise ValueError("Unexpected field initializer terminator")
                    end += 1
                return source[start:end]
        i += 1
    raise ValueError(f"Unterminated production definition: {anchor}")


def regression_check(source):
    baseline = subprocess.check_output(
        ["git", "-c", f"safe.directory={ROOT.as_posix()}", "show", f"{BASELINE}:src/LocalizationPatch/Plugin.cs"],
        cwd=ROOT).decode("utf-8-sig").replace("\r\n", "\n")
    provenance = (
        "// Derived from 9138noms/NuclearOption-LocalizationPatch.\n"
        "// Upstream permission and attribution: ../../THIRD_PARTY_NOTICES.md.\n"
        "// Repository-authored modifications do not relicense the inherited source.\n\n"
    )
    if not source.startswith(provenance):
        raise AssertionError("Expected plugin provenance header is missing or changed")
    stripped = source[len(provenance):].replace("3.6.4", "3.6.3")
    for first, next_anchor in (
        ("        // Reviewed literal ShowMessage", "        internal static bool FontReady"),
        ("        private bool PatchMissionMessageProducer()", "        private void OnDestroy()"),
        ("        internal static string TranslateMissionMessage(", "        internal static string Translate(string original)"),
        ("        static class MissionMessages_Local_Patch", "        /// <summary>\n        /// CRITICAL: Redirect"),
    ):
        start = stripped.index(first)
        end = stripped.index(next_anchor, start)
        stripped = stripped[:start] + stripped[end:]
    addition = "            if (PatchMissionMessageProducer()) applied++;\n\n"
    if stripped.count(addition) != 1:
        raise AssertionError("Producer registration count changed")
    stripped = stripped.replace(addition, "")
    if stripped != baseline:
        raise AssertionError("Unexpected Plugin.cs change outside version and reviewed mission hook")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--harmony", type=Path, default=Path("G:/SteamLibrary/steamapps/common/Nuclear Option/BepInEx/core/0Harmony.dll"))
    parser.add_argument("--output-dir", type=Path)
    args = parser.parse_args()
    output = (args.output_dir or ROOT / ".verification" / ("mission-runtime-tests-" + uuid.uuid4().hex)).resolve()
    if not output.is_relative_to(ROOT / ".verification") or output.exists():
        raise ValueError("Use a NEW ignored repo-local .verification directory; no overwrite")
    if any(p.is_symlink() for p in (output, *output.parents)):
        raise ValueError("Refusing a linked output directory")
    compiler = Path(os.environ["WINDIR"]) / "Microsoft.NET/Framework64/v4.0.30319/csc.exe"
    if not compiler.is_file() or not args.harmony.is_file():
        raise ValueError("Local .NET Framework compiler and BepInEx Harmony are required; never downloaded")
    source = (ROOT / "src/LocalizationPatch/Plugin.cs").read_text(encoding="utf-8-sig")
    regression_check(source)
    print("PASS: Plugin.cs regression boundary (all old logic byte-for-text unchanged)", flush=True)
    manifest = json.loads((ROOT / "config/mission-messages.json").read_text(encoding="utf-8"))
    allowlist = definition(source, "private static readonly HashSet<string> ReviewedMissionMessages", field=True)
    literals = re.findall(r'"(?:\\.|[^"\\])*"', allowlist)
    reviewed = [json.loads(s) for s in literals]
    if reviewed != [item["source"] for item in manifest["translations"]]:
        raise AssertionError("Compiled allowlist differs from reviewed manifest")
    production = [allowlist]
    for anchor in ("private bool PatchMissionMessageProducer()", "internal static string TranslateMissionMessage(",
                   "internal static string Translate(string original)", "private static string TryPatternMatch(",
                   "private void ParseSimpleJson(", "private string ReadJsonString(", "static class MissionMessages_Local_Patch"):
        production.append(definition(source, anchor))
    pairs = ",\n".join("new string[] { " + json.dumps(item["source"], ensure_ascii=True) + ", " +
                         json.dumps(item["russian"], ensure_ascii=True) + " }" for item in manifest["translations"])
    harness = (ROOT / "tools/mission-runtime-fixtures.cs").read_text(encoding="utf-8")
    harness = harness.replace("// @PRODUCTION_DEFINITIONS@", "\n".join(production)).replace("// @REVIEWED_PAIRS@", pairs)
    output.mkdir(parents=True)
    generated = output / "ProductionExtractTests.cs"
    generated.write_text(harness, encoding="utf-8", newline="\n")
    executable = output / "MissionRuntimeTests.exe"
    subprocess.run([str(compiler), "/nologo", "/warnaserror+", "/optimize+", "/target:exe",
                    f"/out:{executable}", f"/reference:{args.harmony.resolve()}", str(generated)], check=True)
    subprocess.run([str(executable), str(args.harmony.resolve()), str(ROOT / "localization/ru.json")], check=True)
    print(f"PASS: generated runtime fixtures retained at {output}")


if __name__ == "__main__":
    main()
