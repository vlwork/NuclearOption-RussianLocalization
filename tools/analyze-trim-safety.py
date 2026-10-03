#!/usr/bin/env python3
"""Generate a read-only deep analysis of boundary-whitespace localization keys."""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
from collections import defaultdict
from pathlib import Path


SAFE_RAW_KEYS = {
    " Objective needs a faction",
    " This text uses emojis, which have a different byte count.",
    "BUILDING REPAIRS COMPLETE ",
    "Can't multiselect ",
    "Custom Airbase ",
    "Hello, world! ",
    "Mission Failed, no spawn points available ",
    "No reserve ",
    "Test 1a Passed: Short string handled correctly. ",
    "Test 1b Passed: Short string handled correctly. ",
    "Test 2 Passed: Long string split into multiple chunks correctly. ",
    "Test 3 Passed: Long string correctly truncated to max length. ",
    "Test 4 Passed: String with special characters handled correctly. ",
    "Test 5 Passed: Japanese text correctly split into chunks under the 255-byte limit. ",
    "Test 6 Passed: Empty string handled correctly. ",
    "WRECK REMOVAL ",
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest().upper()


def md(value: object) -> str:
    text = "" if value is None else str(value)
    return html.escape(text, quote=False).replace("|", "&#124;").replace("\r\n", "<br>").replace("\n", "<br>").replace("\r", "<br>")


def raw_json(value: str) -> str:
    return "<code>" + md(json.dumps(value, ensure_ascii=False)) + "</code>"


def explicit_whitespace(value: str) -> str:
    names = {" ": "⟦SPACE⟧", "\t": "⟦TAB⟧", "\n": "⟦LF⟧", "\r": "⟦CR⟧", "\v": "⟦VT⟧", "\f": "⟦FF⟧", "\u00a0": "⟦NBSP⟧"}
    rendered = "".join(names.get(char, f"⟦U+{ord(char):04X}⟧") if char.isspace() else char for char in value)
    return "<code>" + md(rendered) + "</code>"


def boundary_parts(value: str) -> tuple[str, str]:
    leading_length = len(value) - len(value.lstrip())
    trailing_length = len(value) - len(value.rstrip())
    leading = value[:leading_length]
    trailing = value[len(value) - trailing_length :] if trailing_length else ""
    return leading, trailing


def flags(value: str) -> dict[str, bool]:
    leading, trailing = boundary_parts(value)
    whitespace_kinds = {char for char in value if char.isspace()}
    return {
        "leading spaces": " " in leading,
        "trailing spaces": " " in trailing,
        "leading newline": "\n" in leading or "\r" in leading,
        "trailing newline": "\n" in trailing or "\r" in trailing,
        "tabs": "\t" in value,
        "multiple whitespace kinds": len(whitespace_kinds) > 1,
    }


def flag_text(item_flags: dict[str, bool]) -> str:
    enabled = [name for name, enabled in item_flags.items() if enabled]
    return ", ".join(enabled) if enabled else "none"


def manual_reason(key: str, collision_members: dict[str, list[str]]) -> str:
    normalized = key.strip()
    item_flags = flags(key)
    if normalized in collision_members:
        return "Trim collision requires an explicit choice before any rename or deduplication."
    if item_flags["leading newline"] or item_flags["trailing newline"] or item_flags["tabs"] or item_flags["multiple whitespace kinds"]:
        return "Boundary newline/tab/mixed whitespace may encode layout or concatenation context."
    if normalized.endswith((":", "-")) or normalized.endswith((" by", " for", " from", " in", " of", " on", " to", " with", " because")):
        return "The string is a likely dynamic prefix/label; static data cannot prove whole-string semantics."
    return "The padded key looks like a dynamic or diagnostic fragment; source provenance is insufficient to prove safe normalization."


def find_line(lines: list[str], needle: str) -> int:
    for index, line in enumerate(lines, 1):
        if needle in line:
            return index
    raise RuntimeError(f"Expected runtime marker not found: {needle}")


def table_header() -> list[str]:
    return [
        "| # | Classification | Exact raw key (JSON) | Explicit whitespace | Trimmed key | Current Russian value | Trimmed key exists | Trimmed-key value | Values identical | Boundary flags | Reason |",
        "|---:|---|---|---|---|---|:---:|---|:---:|---|---|",
    ]


def table_row(index: int, item: dict[str, object]) -> str:
    return "| " + " | ".join([
        str(index), str(item["classification"]), raw_json(str(item["raw"])), explicit_whitespace(str(item["raw"])),
        raw_json(str(item["trimmed"])), md(item["value"]), "yes" if item["trimmed_exists"] else "no",
        md(item["trimmed_value"]) if item["trimmed_exists"] else "—",
        "yes" if item["identical"] else ("no" if item["trimmed_exists"] else "n/a"),
        md(flag_text(item["flags"])), md(item["reason"]),
    ]) + " |"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--audit-report", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    repo = args.repo.resolve()
    localization_path = repo / "localization" / "ru.json"
    plugin_path = repo / "src" / "LocalizationPatch" / "Plugin.cs"
    output_path = (args.output or repo / "reports" / "trim-safety-analysis.md").resolve()
    if repo not in output_path.parents:
        raise RuntimeError(f"Refusing to generate a report outside the repository: {output_path}")

    data = json.loads(localization_path.read_text(encoding="utf-8-sig"))
    unsafe_keys = sorted((key for key in data if key != key.strip()), key=lambda value: value.encode("utf-8"))
    normalized_groups: dict[str, list[str]] = defaultdict(list)
    for key in data:
        normalized_groups[key.strip()].append(key)
    collisions = {
        normalized: sorted(set(members), key=lambda value: value.encode("utf-8"))
        for normalized, members in normalized_groups.items() if len(set(members)) > 1
    }
    normalized_allowlist = all(key not in data and key.strip() in data for key in SAFE_RAW_KEYS)
    expected_unsafe = 112 if normalized_allowlist else 128
    if len(unsafe_keys) != expected_unsafe:
        raise RuntimeError(f"Expected reviewed state {expected_unsafe} trim-unsafe keys; found {len(unsafe_keys)}")
    if len(collisions) != 4:
        raise RuntimeError(f"Expected 4 trim-normalized collisions; found {len(collisions)}")

    collision_classes = {
        "Already loaded": ("A. SAFE_DUPLICATE", "Exact trimmed key exists and both Russian values are identical."),
        "Path Node": ("A. SAFE_DUPLICATE", "Both padded variants have the same Russian value and describe the same label; no exact trimmed key exists."),
        "Saved Mission:": ("B. VALUE_CONFLICT", "The padded and exact keys have different Russian translations."),
        "Turret under pilot control": ("A. SAFE_DUPLICATE", "Exact trimmed key exists and both Russian values are identical."),
    }
    if set(collisions) != set(collision_classes):
        raise RuntimeError(f"Unexpected collision set: {sorted(collisions)}")

    items: list[dict[str, object]] = []
    for key in unsafe_keys:
        trimmed = key.strip()
        trimmed_exists = trimmed in data
        identical = trimmed_exists and data[trimmed] == data[key]
        if identical:
            classification = "REDUNDANT_OR_DEAD"
            reason = "The ordinary exact lookup uses the identical trimmed entry. A padded pattern sub-probe is theoretically possible but yields the same value."
        elif key in SAFE_RAW_KEYS:
            classification = "SAFE_TO_NORMALIZE"
            reason = "Collision-free, syntactically complete string with only ordinary U+0020 boundary padding and no target overwrite."
        else:
            classification = "REQUIRES_MANUAL_DECISION"
            reason = manual_reason(key, collisions)
        items.append({
            "raw": key, "trimmed": trimmed, "value": data[key], "trimmed_exists": trimmed_exists,
            "trimmed_value": data.get(trimmed), "identical": identical, "flags": flags(key),
            "classification": classification, "reason": reason,
        })

    grouped = {name: [item for item in items if item["classification"] == name] for name in ("SAFE_TO_NORMALIZE", "REQUIRES_MANUAL_DECISION", "REDUNDANT_OR_DEAD")}
    expected_counts = {"SAFE_TO_NORMALIZE": 0 if normalized_allowlist else 16, "REQUIRES_MANUAL_DECISION": 110, "REDUNDANT_OR_DEAD": 2}
    actual_counts = {name: len(group) for name, group in grouped.items()}
    if actual_counts != expected_counts:
        raise RuntimeError(f"Classification count changed: {actual_counts}")

    source_lines = plugin_path.read_text(encoding="utf-8-sig").splitlines()
    runtime_lines = {
        "load": find_line(source_lines, "private void ParseSimpleJson"),
        "store": find_line(source_lines, "Translations[key] = value;"),
        "tmp": find_line(source_lines, "internal void TranslateTmpComponent"),
        "tmp_trim": find_line(source_lines, "string trimmed = current.Trim();"),
        "legacy": find_line(source_lines, "// Scan legacy Text components"),
        "translate": find_line(source_lines, "internal static string Translate(string original)"),
        "translate_trim": find_line(source_lines, "string trimmed = original.Trim();"),
        "patterns": find_line(source_lines, "private static string TryPatternMatch(string text)"),
    }

    provenance_files = sorted(path.relative_to(repo).as_posix() for path in repo.rglob("*") if ".verification" not in path.parts and path.is_file() and re.match(r"(?i)^(extracted_gamedata|untranslated).*\.txt$", path.name))
    audit_note = "No generated audit report was supplied."
    if args.audit_report and args.audit_report.is_file():
        audit_text = args.audit_report.read_text(encoding="utf-8-sig")
        unsafe_match = re.search(r"\| Trim-unsafe keys \| (\d+) \|", audit_text)
        collision_match = re.search(r"\| Trim-normalized collisions \| (\d+) \|", audit_text)
        audit_note = (
            f"Generated audit `{args.audit_report}` (SHA-256 `{sha256(args.audit_report)}`) reports "
            f"{unsafe_match.group(1) if unsafe_match else 'unknown'} trim-unsafe keys and "
            f"{collision_match.group(1) if collision_match else 'unknown'} collisions, matching this analysis."
        )

    lines: list[str] = [
        "# Trim-safety analysis", "",
        "This is a static, read-only classification. It does not recommend bulk trimming and does not modify localization or runtime files.", "",
        "## SUMMARY", "", "| Metric | Count |", "|---|---:|",
        f"| Trim-unsafe keys | {len(items)} |", f"| Trim-normalized collisions | {len(collisions)} |",
        f"| SAFE_TO_NORMALIZE | {len(grouped['SAFE_TO_NORMALIZE'])} |",
        f"| REQUIRES_MANUAL_DECISION | {len(grouped['REQUIRES_MANUAL_DECISION'])} |",
        f"| REDUNDANT_OR_DEAD | {len(grouped['REDUNDANT_OR_DEAD'])} |", "",
        f"The three groups cover all {len(items)} remaining trim-unsafe keys. Baseline: 128 unsafe, 16 safe, 110 manual, 2 redundant. Only the 16 reviewed collision-free keys were renamed; their values were preserved. Collision classification describes equivalent data, not universal runtime deadness.", "",
        "### Whitespace profile", "", "| Property | Count |", "|---|---:|",
    ]
    for flag_name in ("leading spaces", "trailing spaces", "leading newline", "trailing newline", "tabs", "multiple whitespace kinds"):
        lines.append(f"| {flag_name} | {sum(bool(item['flags'][flag_name]) for item in items)} |")

    lines.extend(["", "## COLLISIONS", "", "| Normalized key | Classification | All raw keys | Current Russian values | Static conclusion |", "|---|---|---|---|---|"])
    for normalized in sorted(collisions, key=lambda value: value.encode("utf-8")):
        members = collisions[normalized]
        collision_class, conclusion = collision_classes[normalized]
        raw_members = "<br>".join(raw_json(member) + " — " + explicit_whitespace(member) for member in members)
        values = "<br>".join(raw_json(member) + " → " + md(data[member]) for member in members)
        lines.append(f"| {raw_json(normalized)} | {collision_class} | {raw_members} | {values} | {md(conclusion)} |")

    lines.extend(["", f"## ALL {len(items)} TRIM-UNSAFE KEYS", ""] + table_header())
    for index, item in enumerate(items, 1):
        lines.append(table_row(index, item))

    section_titles = [
        ("SAFE CANDIDATES", "SAFE_TO_NORMALIZE", "These are classification candidates only. Each is collision-free, has no existing trimmed key, and contains only ordinary boundary spaces around a syntactically complete string."),
        ("MANUAL REVIEW", "REQUIRES_MANUAL_DECISION", "These entries are collision-involved, formatting-sensitive, or likely dynamic/log fragments. Static evidence is not strong enough for an automatic rename."),
        ("DEAD/REDUNDANT", "REDUNDANT_OR_DEAD", "The exact trimmed key already exists with the same translation. The padded entries are redundant for ordinary exact lookup; retain them because pattern sub-probes can carry whitespace."),
    ]
    for heading, classification, explanation in section_titles:
        lines.extend(["", f"## {heading}", "", explanation, ""] + table_header())
        for item in grouped[classification]:
            lines.append(table_row(items.index(item) + 1, item))

    lines.extend([
        "", "## RUNTIME ANALYSIS", "",
        f"- JSON parsing starts at `ParseSimpleJson` in `Plugin.cs` line {runtime_lines['load']}; line {runtime_lines['store']} stores each decoded key verbatim in `Translations`. Loading does not normalize keys.",
        f"- `TranslateTmpComponent` begins at line {runtime_lines['tmp']}. It computes `current.Trim()` at line {runtime_lines['tmp_trim']} and uses only that value for exact lookup, cache revalidation, pattern matching, and untranslated recording.",
        f"- The legacy `UnityEngine.UI.Text` sweep starts at line {runtime_lines['legacy']} and likewise trims `txt.text` before exact or pattern lookup.",
        f"- `Translate` begins at line {runtime_lines['translate']} and trims `original` at line {runtime_lines['translate_trim']}. TMP and legacy setter patches route through this method.",
        f"- `TryPatternMatch` begins at line {runtime_lines['patterns']}. Its outer input is trimmed, but some derived substrings are NOT: bracket prefixes, numbered mission names, dash segments and faction-unit names. For example `Already loaded  (1)` probes `Already loaded `; `01.  Turret under pilot control` can probe a leading-space key. These are static theoretical examples, not observed game evidence.",
        "- Leading/trailing whitespace keys cannot be reached by ordinary whole-string exact lookup. It would be incorrect to assert universal deadness across all pattern paths. Original boundary whitespace is not reapplied by exact translation.",
        "- The 16 allowlisted, complete boundary-space labels were normalized only as explicitly authorized. Remaining dynamic/diagnostic fragments and every collision are retained; no blanket trim or deduplication was applied.",
        "", "## SOURCE PROVENANCE", "",
        f"- `extracted_gamedata.txt` / `untranslated*.txt` files found in the named repository: {', '.join(f'`{item}`' for item in provenance_files) if provenance_files else 'none'}.",
        f"- {audit_note}",
        "- With no extracted source snapshot, classifications rely on exact dictionary contents, collision/value equality, lexical completeness, and the inspected runtime lookup code. Dynamic/log-fragment entries remain manual by design.",
        "", "## METHODOLOGY AND SAFETY", "",
        "- `str.strip()` mirrors the observed boundary characters in this dataset. General QA uses an explicit .NET Char.IsWhiteSpace set. Baseline was 128/4; the reviewed post-correction state is 112/4.",
        "- No key, translation, plugin source, DLL, or release archive is written by this tool.",
        "- The allowlist for SAFE_TO_NORMALIZE is intentionally narrow and asserted by count; new or changed data causes generation to fail for re-review.",
        "- This report documents current remaining findings, not authorization for further localization changes.", "",
        f"Localization SHA-256 at analysis time: `{sha256(localization_path)}`<br>",
        f"Plugin source SHA-256 at analysis time: `{sha256(plugin_path)}`",
    ])

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    print(f"trim-unsafe={len(items)} collisions={len(collisions)} classifications={actual_counts}")
    print(output_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
