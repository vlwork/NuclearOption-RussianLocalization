#!/usr/bin/env python3
"""Offline real-method/Harmony fixtures for the 0.34.6 UI compatibility delta."""
import argparse
import importlib.util
import json
import os
from pathlib import Path
import re
import subprocess
import uuid

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("mission_runtime", Path(__file__).with_name("test-mission-runtime.py"))
runtime = importlib.util.module_from_spec(spec)
spec.loader.exec_module(runtime)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--harmony", type=Path, required=True)
    parser.add_argument("--metadata", type=Path, help="Optional local output of inspect-game-compatibility.ps1")
    args = parser.parse_args()
    if not args.harmony.is_file():
        raise ValueError("Use an existing local Harmony assembly; never downloaded")
    source = (ROOT / "src/LocalizationPatch/Plugin.cs").read_text(encoding="utf-8-sig")
    runtime.regression_check(source)
    baseline = json.loads(subprocess.check_output(["git", "show", "8046c91:localization/ru.json"], cwd=ROOT))
    current = json.loads((ROOT / "localization/ru.json").read_text(encoding="utf-8"))
    manifest = json.loads((ROOT / "config/game-0346-ui.json").read_text(encoding="utf-8"))
    additions = {x["source"]: x["russian"] for x in manifest["translations"]}
    assert len(baseline) == manifest["baselineEntryCount"] == 3729
    assert current == {**baseline, **additions} and not baseline.keys() & additions.keys()
    if args.metadata:
        evidence = json.loads(args.metadata.read_text(encoding="utf-8-sig"))
        assert evidence["build"] == manifest["steamBuild"]
        assert next(x["sha256"] for x in evidence["hashes"] if x["file"].endswith("/Assembly-CSharp.dll")) == manifest["assemblySha256"]
        for item in manifest["translations"]:
            assert any(x["text"] == item["source"] and item["producer"] + "(" in x["method"] for x in evidence["literals"]), item["source"]
        signatures = {x["signature"] for x in evidence["methods"]}
        required = {
            "System.Void TMPro.TMP_Text::set_text(System.String)",
            "System.Void UnityEngine.UI.Text::set_text(System.String)",
            "System.Void TMPro.TextMeshPro::OnEnable()",
            "System.Void TMPro.TextMeshProUGUI::OnEnable()",
            "System.Void TMPro.TMP_Text::SetText(System.String,System.Boolean)",
            "System.Void NuclearOption.Chat.ChatAutocompleteUI::SetHeader(NuclearOption.Chat.ChatAutocompleteEngine,System.Int32)",
            "System.Void MissionMessages::ShowMessgeLocal(System.String,System.Boolean,FactionHQ)",
            "UnityEngine.TextCore.LowLevel.FontEngineError UnityEngine.TextCore.LowLevel.FontEngine::LoadFontFace(UnityEngine.Font,System.Int32)",
        }
        for owner in ("TMPro.TMP_Dropdown", "UnityEngine.UI.Dropdown"):
            for option in ("System.String", owner + "/OptionData"):
                required.add(f"System.Void {owner}::AddOptions(System.Collections.Generic.List`1<{option}>)")
        assert required <= signatures, required - signatures
        assert "System.Void TMPro.TMP_Text::SetText(System.String)" not in signatures
        fields = {(x["type"], x["name"]): x["fieldType"] for x in evidence["fields"]}
        for owner, name in (("NuclearOption.Chat.ChatAutocompleteUI", "headerTitle"),
                            ("NuclearOption.Chat.ChatHoverCardUI", "nameText"),
                            ("NuclearOption.Chat.AllowBanListItem", "nameText"),
                            ("LeaderboardPlayerEntry", "textName"),
                            ("MessageUI", "messageText"), ("MessageUI", "killFeedText")):
            assert fields[(owner, name)] == "TMPro.TextMeshProUGUI"
        print("PASS: exact current-game Harmony/UI signatures and guarded display fields")
    assert (ROOT / "src/LocalizationPatchDropdown/Plugin.cs").read_bytes().replace(b"\r\n", b"\n") == subprocess.check_output(
        ["git", "show", "90e6a96:src/LocalizationPatchDropdown/Plugin.cs"], cwd=ROOT).replace(b"\r\n", b"\n")
    for banned in ("HQMessageInternal", "SetSizeWithCurrentAnchors", "SetParent(", "GetComponentsInChildren"):
        assert banned not in source, banned
    production = []
    for anchor in ("private static readonly Type ChatSuggestionRowType", "private static readonly FieldInfo MessageDisplayField", "private static readonly FieldInfo KillFeedDisplayField",
                   "private static readonly Type ChatAutocompleteType", "private static readonly Type ChatAutocompleteEngineType", "private static readonly FieldInfo ChatHeaderTitleField",
                   "private static readonly Type ChatHoverCardType", "private static readonly FieldInfo ChatHoverNameField", "private static readonly Type AllowBanItemType",
                   "private static readonly FieldInfo AllowBanNameField", "private static readonly Type LeaderboardEntryType", "private static readonly FieldInfo LeaderboardNameField"):
        start = source.index(anchor)
        production.append(source[start:source.index(";", start) + 1])
    for anchor in ("private static MethodInfo FindChatHeaderTarget(", "private bool PatchChatAutocompleteHeader(",
                   "static class ChatAutocomplete_Header_Patch", "private static bool IsOwnedTextField(", "private static bool IsProtectedPlayerText(",
                   "internal bool TranslateTmpComponent(", "private void FastScanTmpTextAndFit(",
                   "internal static string Translate(", "private static string TryPatternMatch(",
                   "static class TMP_OnEnable_Patch", "static class TMP_Text_SetText_Patch", "static class TMP_Text_SetTextMethod_Patch"):
        production.append(runtime.definition(source, anchor))
    harness = (ROOT / "tools/ui-compatibility-fixtures.cs").read_text(encoding="utf-8")
    harness = harness.replace("// @PRODUCTION_DEFINITIONS@", "\n".join(production))
    old_source = subprocess.check_output(["git", "show", "90e6a96:src/LocalizationPatch/Plugin.cs"], cwd=ROOT).decode("utf-8-sig")
    assert baseline["Multiplayer"] == "\u041c\u0443\u043b\u044c\u0442\u0438\u043f\u043b\u0435\u0435\u0440"
    probe = '''public class BaselineProbe {
        internal static bool Enabled = true, FontReady = false, isPatching = false;
        internal static BaselineProbe Instance = new BaselineProbe();
        internal static Dictionary<string,string> Translations = new Dictionary<string,string> { { "Multiplayer", "\\u041c\\u0443\\u043b\\u044c\\u0442\\u0438\\u043f\\u043b\\u0435\\u0435\\u0440" } };
        internal static HashSet<string> TranslationKeys = new HashSet<string> { "Multiplayer" };
        private HashSet<int> translatedInstances = new HashSet<int>();
        internal int translatedCount;
        private void RecordUntranslated(string text) { }
        private static bool IsDialogueBoxTitle(TMP_Text text) { return false; }
        private static bool ContainsKorean(string text) { return true; }
        private static void EnsureKoreanFallback(TMP_Text text) { }
    '''
    for anchor in ("internal void TranslateTmpComponent(", "internal static string Translate(", "private static string TryPatternMatch("):
        probe += runtime.definition(old_source, anchor) + "\n"
    harness = harness.replace("// @BASELINE_PROBE@", probe + "}")
    output = ROOT / ".verification" / ("ui-compatibility-" + uuid.uuid4().hex)
    if any(p.is_symlink() for p in (output, *output.parents)):
        raise ValueError("Refusing linked output")
    output.mkdir()
    generated = output / "UiCompatibilityTests.cs"
    generated.write_text(harness, encoding="utf-8")
    sdks = subprocess.check_output(["dotnet", "--list-sdks"], text=True)
    sdk = re.findall(r"^([^ ]+) \[([^\]]+)\]$", sdks, re.M)[-1]
    compiler = Path(sdk[1]) / sdk[0] / "Roslyn/bincore/csc.dll"
    framework = Path(os.environ["WINDIR"]) / "Microsoft.NET/Framework64/v4.0.30319"
    executable = output / "UiCompatibilityTests.exe"
    subprocess.run(["dotnet", str(compiler), "/nologo", "/warnaserror+", "/optimize+", "/target:exe", "/nostdlib+",
                    f"/out:{executable}", f"/reference:{args.harmony.resolve()}",
                    *[f"/reference:{framework / name}" for name in ("mscorlib.dll", "System.dll", "System.Core.dll")],
                    str(generated)], check=True)
    # Resolve Harmony locally without copying it into the fixture output.
    runner = output / "Run.ps1"
    runner.write_text("param($HarmonyPath, $Executable)\n[void][Reflection.Assembly]::LoadFrom($HarmonyPath)\n"
                      "$assembly=[Reflection.Assembly]::LoadFrom($Executable)\n"
                      "$result=$assembly.EntryPoint.Invoke($null, (, [string[]]@()))\nexit $result\n", encoding="utf-8")
    subprocess.run(["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(runner),
                    str(args.harmony.resolve()), str(executable)], check=True)
    print(f"PASS: all 3729 baseline pairs, {len(additions)} reviewed additions, unchanged dropdown and static regression boundary")


if __name__ == "__main__":
    main()
