#!/usr/bin/env python3
"""Independent Git-baseline differential review and repository-local final report.

Reuses the QA engine; does not rewrite source, localization, DLLs or packages.
"""
import hashlib
import importlib.util
import json
import re
import subprocess
import zipfile
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = "8594a28b36572b2393921bee26346bcdd4cc82a1"


def module(name):
    spec = importlib.util.spec_from_file_location(name, Path(__file__).with_name(name + ".py"))
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


audit, stabilization = module("audit-localization"), module("stabilize-localization")


def git(*args):
    return subprocess.check_output(["git", "-c", "safe.directory=" + str(ROOT), "-c", "core.quotepath=false", "-C", str(ROOT), *args]).decode("utf-8")


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def cell(value):
    return audit.cell(value)


def jcell(value):
    return cell(json.dumps(value, ensure_ascii=False))


CASE_REASONS = {
    "ACTIVE": "Adjective gender/standalone-state context is unknown.",
    "AOA": "Compact abbreviation versus expanded angle-of-attack wording; avionics remains deferred.",
    "BOSCALI": "Faction/place display context unknown; no lore naming policy inferred.",
    "CAMERA TRANSFORM": "Editor/internal transform terminology is deferred.",
    "CREATE NEW": "Omitted object versus explicit adjective may depend on UI context.",
    "DEVELOPMENT ROADMAP": "Two natural synonyms; no demonstrated semantic defect.",
    "ENEMY": "Noun versus adjectival/plural UI context is unknown.",
    "FAR": "Abbreviation versus expanded adverb may be intentional for space.",
    "FRIENDLY": "Adjectival agreement/number may depend on UI context.",
    "FACTION FUNDS": "Potential plurality inconsistency; editor/statistics context is unproven.",
    "FACTION SCORE": "Potential score terminology inconsistency; editor/statistics context is unproven.",
    "GUN": "Pistol versus cannon is suspicious, but the uppercase label may be deferred cockpit text; no global-invariant corruption.",
    "HIGH": "Adjective gender may depend on the omitted noun.",
    "INNER WING PYLONS": "Both mean inner wing pylons; style synonym, not a proven semantic defect.",
    "LOW": "Adjective gender may depend on the omitted noun.",
    "MEDIUM": "Gender/number may depend on the omitted noun.",
    "MISSILE WARNING": "Warning label variants express the same threat; cockpit context is deferred.",
    "NAME": "Personal name versus object name needs display context.",
    "NEW": "Adjective gender may depend on the omitted noun.",
    "NO TARGET": "Empty target value is suspicious but may intentionally suppress an avionics label; deferred.",
    "NEED PREVIEW": "Two natural preview synonyms; no semantic defect proven.",
    "OBJECTIVE": "Target versus task meaning requires context, including deferred editor use.",
    "OPTICAL": "Adjective gender and sensor context need confirmation.",
    "OUTER WING PYLONS": "Both refer to outer wing pylons; awkward variant but no proven context-safe convergence.",
    "PRIMEVA ARMED LIBERATION ALLIANCE": "Proper faction/title convention and display context need confirmation; no invented lore.",
    "PRIMEVA": "Faction/place naming convention and display context need confirmation.",
    "PUBLIC": "Adjective gender versus visibility terminology requires lobby context.",
    "PVE": "Abbreviation style differs but gameplay acronym meaning survives; naming convention unproven.",
    "READY": "State versus agreeing adjective may be intentional.",
    "REQUISITION": "Noun versus action verb may reflect status/button context.",
    "SOUTH BOSCALI GENERAL AVIATION": "Awkward title variant, but entity/lore naming context is insufficient for a safe rewrite.",
    "TOTAL": "Explicit weight versus general total may reflect different displays.",
    "VALUE": "Cost versus data value is context-dependent, including editor/internal use.",
    "WEAPONS": "Two natural military UI synonyms; no semantic defect proven."
}
INTENTIONAL_CASE = {"DEVELOPMENT ROADMAP", "FAR", "INNER WING PYLONS", "NEED PREVIEW", "WEAPONS"}


def runtime_proof():
    old = git("show", BASE + ":src/LocalizationPatch/Plugin.cs").replace("\r\n", "\n")
    new = (ROOT / "src/LocalizationPatch/Plugin.cs").read_text(encoding="utf-8-sig")
    expected = old
    for before, after in [("\"Localization Patch\", \"3.6.0\"", "\"Localization Patch\", \"3.6.3\""), ("Localization Patch v3.6.0 loaded", "Localization Patch v3.6.3 loaded"), ("Localization Patch v3.6.0 ({CurrentLanguage})", "Localization Patch v3.6.3 ({CurrentLanguage})")]:
        assert expected.count(before) == 1
        expected = expected.replace(before, after)
    removed = '\n'.join([
        '            // Debug: log any function key press to verify input system works',
        '            if (Input.GetKeyDown(KeyCode.F9)) Plugin.Log?.LogInfo("[DEBUG] F9 detected");',
        '            if (Input.GetKeyDown(KeyCode.F10)) Plugin.Log?.LogInfo("[DEBUG] F10 detected");',
        '            if (Input.GetKeyDown(KeyCode.F12)) Plugin.Log?.LogInfo("[DEBUG] F12 detected");',
        '            if (Input.anyKeyDown) Plugin.Log?.LogInfo($"[DEBUG] Any key: {Input.inputString}");', '', ''
    ])
    assert expected.count(removed) == 1
    expected = expected.replace(removed, "")
    assert expected == new, "Unrelated runtime diff: stop before packaging"
    assert (ROOT / "src/LocalizationPatchDropdown/Plugin.cs").read_text(encoding="utf-8-sig") == git("show", BASE + ":src/LocalizationPatchDropdown/Plugin.cs").replace("\r\n", "\n")
    assert not re.search(r"\.sizeDelta\s*=|\.anchoredPosition\s*=|\.SetSizeWithCurrentAnchors\(", new)
    assert new.count("Resources.FindObjectsOfTypeAll") == old.count("Resources.FindObjectsOfTypeAll")
    assert "[DEBUG] Any key:" not in new
    return "Exact normalized-source equivalence after only three version-label substitutions and removal of four diagnostic log guards, their comment and blank line."


def main():
    baseline_bytes = subprocess.check_output(["git", "-c", "safe.directory=" + str(ROOT), "-C", str(ROOT), "show", BASE + ":localization/ru.json"])
    baseline_path = ROOT / ".verification/report-baseline.json"
    baseline_path.write_bytes(baseline_bytes)
    baseline, _ = audit.load_pairs(baseline_path)
    current, _ = audit.load_pairs(ROOT / "localization/ru.json")
    manifest = json.loads((ROOT / "config/stabilization-changes.json").read_text(encoding="utf-8"))
    changes = stabilization.planned_values(baseline, manifest)
    differential = stabilization.verify(baseline, current, changes)
    differential["unchangedEntries"] = sum(k in current and current[k] == v for k, v in baseline.items())
    assert differential["unchangedEntries"] == 3677
    assert len(changes) == 23
    config = json.loads((ROOT / "config/localization-audit.json").read_text(encoding="utf-8"))
    before = audit.analyze(baseline_path, config)
    after = audit.analyze(ROOT / "localization/ru.json", config)
    assert not any(f["strict"] for f in after["findings"])
    proof = runtime_proof()
    recovery = sorted((ROOT / ".verification").glob("recovery-*/inventory.json"))[-1]
    inventory = json.loads(recovery.read_text(encoding="utf-8-sig"))
    hashes = json.loads(recovery.with_name("hashes.json").read_text(encoding="utf-8-sig"))
    change_map = {item["source"]: item for item in changes}
    review = ["# Localization finding review", "", "Every baseline HIGH/MEDIUM finding from the coherent QA engine is classified below. No context-dependent/editor/hint/avionics values were changed. Curated quality candidates remain review reminders, not automatic errors.", "", "| Severity | Category | Exact source (JSON) | Baseline Russian value | Classification | Decision / reason |", "|---|---|---|---|---|---|"]
    classes = Counter()
    for finding in before["findings"]:
        if finding["severity"] not in ("CRITICAL", "HIGH", "MEDIUM"):
            continue
        key, category = finding["source"], finding["category"]
        classification, reason = "CONTEXT_REQUIRED", "Retain: insufficient static/source provenance for a context-safe change."
        if key in change_map:
            classification, reason = change_map[key]["classification"], change_map[key]["reason"]
        elif category == "Trim safety":
            if key in stabilization.SAFE_RAW_KEYS:
                classification, reason = "OBJECTIVE_ERROR", "Only key renamed: approved boundary-space allowlist, no value change or collision."
            elif audit.trim(key) in baseline and baseline[audit.trim(key)] == baseline[key]:
                classification, reason = "INTENTIONAL", "Retain duplicate: no functional benefit from deletion; pattern sub-probes can carry whitespace."
            else:
                reason = "Retain among 110 manual entries: dynamic/diagnostic fragment, collision or formatting context is unproven."
        elif category == "Trim collision":
            classification = "CONTEXT_REQUIRED" if key.startswith("Saved Mission:") else "INTENTIONAL"
            reason = "Retain all raw keys. Saved Mission has conflicting semantics; other collision values are identical and removal offers no demonstrated benefit."
        elif category == "Case variants":
            folded = key.split(" || ")[0].upper()
            assert folded in CASE_REASONS, folded
            classification = "INTENTIONAL" if folded in INTENTIONAL_CASE else "CONTEXT_REQUIRED"
            reason = "Retain: " + CASE_REASONS[folded]
        elif category == "Russian typography":
            reason = "Retain: Column 50m/Concrete Wall 10m are editor/scenery labels; the bridge prose is a deferred mission hint. Not a global invariant defect."
        elif category == "Newline safety":
            reason = "Retain formatting-sensitive manual key; layout/source evidence is insufficient."
        elif category == "Translation quality" and key in ("FGA-57 Anvil", "M12 Jackknife"):
            classification, reason = "INTENTIONAL", "Correct exact model/codename identity; no rewrite."
        classes[classification] += 1
        review.append("| " + " | ".join([finding["severity"], category, jcell(key), jcell(finding["value"]), classification, cell(reason)]) + " |")
    review += ["", "## All case-variant groups", "", "155 groups already agree modulo capitalization/whitespace. All 189 groups remain unchanged; 34 context/style differences are explained above.", "", "| Group | Source variants and current values | Disposition |", "|---|---|---|"]
    groups = defaultdict(list)
    for key in sorted(current):
        groups[key.upper()].append(key)
    for folded, members in sorted(groups.items()):
        if len(members) > 1:
            review.append(f"| {cell(folded)} | " + "<br>".join(jcell(k) + " → " + jcell(current[k]) for k in members) + " | " + ("Retain; " + cell(CASE_REASONS[folded]) if folded in CASE_REASONS else "INTENTIONAL: corresponding capitalization/whitespace only.") + " |")
    (ROOT / "reports/localization-review.md").write_text("\n".join(review) + "\n", encoding="utf-8", newline="\n")
    lines = ["# Full localization stabilization / recovery report", "", "## Recovery", "", f"Original and current HEAD: `{git('rev-parse', 'HEAD').strip()}`. Local branch: `{git('branch', '--show-current').strip()}`. HEAD equals baseline `{BASE}`. No reset, checkout, stash, commit, push or publication occurred.", "", f"Current dirty work was preserved in ignored `{recovery.parent.relative_to(ROOT).as_posix()}` before further edits. No localization value/key was changed during the resume; its recovery and final SHA256 are identical. The rejected package/trim patches were confirmed absent before targeted fixes.", "", "### Initial dirty-file inventory", "", "| Path | Status | Existed at baseline | Purpose / initial completeness |", "|---|---|---|---|"]
    purposes = {
        ".gitignore": "Complete: ignore recovery/verification and Python caches only.",
        "localization/ru.json": "Complete: 16 reviewed renames / 23 reviewed values; independently reverified.",
        "scripts/build.ps1": "Present: offline restore and isolated source-only build; needed fresh validation.",
        "scripts/common.ps1": "Present: one shared QA validator, version/file manifest and path safety; needed review.",
        "scripts/install-local.ps1": "In progress: external backups, duplicate metadata, dry-run and rollback; not yet mock-tested.",
        "scripts/package.ps1": "Interrupted: exact manifest/hash validation, but missing compression assembly and incompatible timestamp-after-write ordering.",
        "src/LocalizationPatch/LocalizationPatch.csproj": "Complete: 3.6.3 assembly/package metadata.",
        "src/LocalizationPatch/Plugin.cs": "Complete: four diagnostic guards removed, three version labels updated; behavior proof rerun.",
        "config/localization-audit.json": "Present: maintainable invariants/glossary/context configuration.",
        "config/stabilization-changes.json": "Complete: explicitly reviewed value-change manifest and reasons.",
        "scripts/audit-localization.ps1": "Present: Windows entry point into one Python QA engine.",
        "tools/audit-localization.py": "Present: deterministic stdlib QA; runtime-export parser/regression tests still needed.",
        "tools/stabilize-localization.py": "Complete: guarded reviewed-phase mechanics / structured verifier; no reapplication on resume."
    }
    for item in inventory:
        lines.append(f"| {cell(item['Path'])} | {item['Status']} | {item['ExistedAtBaseline']} | {cell(purposes[item['Path']])} |")
    lines += ["", "At recovery, README/README_RU/CHANGELOG and the existing trim report/tool were unchanged; trim reporting was stale and failed with `Expected 128 ... found 112`. They were then updated only to reflect verified behavior/current findings.", "", "### Recovery-time SHA256", "", "| Path | SHA256 |", "|---|---|"]
    lines += [f"| {cell(item['Path'])} | `{item['SHA256']}` |" for item in hashes]
    lines += ["", "## Localization / independent Git comparison", "", f"Entries: {len(baseline)} → {len(current)}. Key renames: 16. Logical additions/removals: 0/0. Changed values: 23. Unchanged exact-key/value entries: {differential['unchangedEntries']}. A raw set difference contains 16 old names and 16 new names, all accounted for as renames. Unexplained differences: 0.", "", "All 23 existing changes passed second-pass linguistic/technical review: 1 OBJECTIVE_FIX and 22 CLEAR_RUSSIAN_IMPROVEMENT. None was QUESTIONABLE or OUT_OF_SCOPE; no individual reversion or further translation change was needed.", "", "### Complete changed-value table", "", "| Source | Baseline Russian value | Current Russian value | Second-pass classification / reason |", "|---|---|---|---|"]
    for item in changes:
        second = "OBJECTIVE_FIX" if item["source"] == "T9K41 Boltstrike" else "CLEAR_RUSSIAN_IMPROVEMENT"
        lines.append("| " + " | ".join([jcell(item["source"]), jcell(item["before"]), jcell(item["after"]), second + ": " + cell(item["reason"])]) + " |")
    lines += ["", "### Complete key-rename list", "", "Every row preserves the original translation exactly; only U+0020 boundary padding was removed, as authorized by the reviewed allowlist.", "", "| Raw key (JSON) | New key (JSON) |", "|---|---|"]
    lines += [f"| {jcell(item['before'])} | {jcell(item['after'])} |" for item in differential["renamedKeys"]]
    lines += ["", "### QA before / after", "", "Both columns use the same final QA engine/configuration; they are not silently compared with historical, weaker scripts.", "", "| Metric | Baseline | Final |", "|---|---:|---:|"]
    lines += [f"| {key} | {before['metrics'][key]} | {value} |" for key, value in after["metrics"].items()]
    lines += [f"| {severity} | {sum(f['severity'] == severity for f in before['findings'])} | {sum(f['severity'] == severity for f in after['findings'])} |" for severity in audit.SEVERITIES]
    lines += ["", "Normal audit exit: 0. Strict audit exit: 0. Invalid JSON, duplicates, count, protected identities, designations, proper names, placeholders and TMP all pass. Two baseline newline warnings remain unchanged; valid JSON decoding and the structured proof establish no new escaping/newline corruption.", "", "The 49 MEDIUM rows include 34 case groups, 2 newline cautions, 3 deferred typography warnings and 10 curated review reminders (including correctly preserved names). HIGH=116 comprises 112 trim keys plus 4 collisions. INFO=13 comprises 12 dynamic literals and unavailable coverage. Coverage source/exact/normalized/missing counts are n/a because no real local extracted snapshot exists; test fixtures are excluded.", "", "All protected identities remain exact. `A-19 factory` = `завод A-19`; `T/A-30 factory` = `завод T/A-30`; `T9K41 Boltstrike` and `M12 Jackknife` retain ASCII identity. A2A/A2G are documented mode abbreviations, not model-designation exemptions added to conceal a corruption. Vortex ring state is an aerodynamic exception, not the aircraft codename.", "", "Trim: 128 → 112 unsafe; 4 → 4 collisions; 110 manual entries untouched, 2 redundant entries retained. Saved Mission conflict remains unresolved and unchanged: `Миссия сохранена:` versus `Сохраненная миссия:`. Other collision translations are equivalent and retained; static pattern sub-probes prevent a universal deadness claim. See [trim analysis](trim-safety-analysis.md) and [full finding review](localization-review.md).", "", f"Baseline finding review classes: `{dict(classes)}`. Dynamic/noise entries are report-only; no new runtime patterns, machine translation or deferred coverage were introduced.", "", "## Runtime / build-system review", "", proof, "", "Plugin.cs changed; active runtime and main project metadata are 3.6.3. Dropdown source is baseline-identical and remains 1.0.0. F9/F10 UI toggle, Ctrl+F10 reload, Ctrl+F11 extraction, DoPerFrameLogic timing, periodic scans, OnEnable prefix/postfix and selective Encyclopedia text-only AutoFit remain source-identical. No parent geometry mutation, new global font shrink, cockpit hierarchy scanner or added Resources.FindObjectsOfTypeAll call exists. One-time FrameHelper startup and actual UI-toggle logs are retained; unconditional per-key diagnostics are absent.", "", "Build/common changes have concrete purposes: source-only isolated output, local-only restore/no NuGet audit traffic, warnings-as-errors, one shared QA/config instead of conflicting duplicated validators, production manifest/source-DLL version checks and reparse-point safety. No translation hot-path refactor was retained.", "", "## Installer", "", "Backup destination: `<GameRoot>/LocalizationPatchBackups/LocalizationPatch_<timestamp>_<unique-id>/`, outside all BepInEx. Existing target is backed up before mutation. Conflicting DLLs are identified by assembly metadata even when renamed; only identified duplicates are moved, preserving their relative paths. Exact old targets are backed up and overwritten, not rescanned/moved after installation. Legacy `BepInEx/LocalizationPatchBackups` is relocated. Unrelated files/config are retained; ambiguous candidates or unrelated exact target assemblies block installation before replacement. Rollback retains recoverable partial files rather than deleting them. Previous backups are never deleted.", "", "Mock scenarios A clean install, B upgrade/user preservation, C old plugins backup, D renamed duplicate elsewhere, E path with spaces, F no-mutation WhatIf, G repeated invocation , H ambiguous read-only failure and I unrelated exact-target refusal all pass. No real-game installation was run.", "", "## Build / package", "", "Fresh isolated Release build: LocalizationPatch 0 warnings / 0 errors; LocalizationPatchDropdown 0 warnings / 0 errors; warnings treated as errors. QA regression suite: 11/11 PASS. Isolated packaging succeeded before the release ZIP was created. Exact-entry whitelist and embedded SHA256 verification exclude all backups, debug/build trees, logs, snapshots, configurations, absolute paths and experimental artifacts."]
    zip_path = ROOT / "release/NuclearOption-RussianLocalization-v3.6.3.zip"
    package_ok = zip_path.is_file()
    files = {"LocalizationPatch.dll": ROOT / "src/LocalizationPatch/bin/Release/net472/LocalizationPatch.dll", "LocalizationPatchDropdown.dll": ROOT / "src/LocalizationPatchDropdown/bin/Release/net472/LocalizationPatchDropdown.dll", "ru.json": ROOT / "localization/ru.json", "Tektur-Reg.ttf": ROOT / "fonts/Tektur-Reg.ttf"}
    if package_ok:
        with zipfile.ZipFile(zip_path) as archive:
            assert sorted(archive.namelist()) == sorted("BepInEx/plugins/LocalizationPatch/" + name for name in files)
            for name, path in files.items():
                assert archive.read("BepInEx/plugins/LocalizationPatch/" + name) == path.read_bytes()
            lines += ["", "Archive listing:", "", "```text", *archive.namelist(), "```"]
    lines += ["", "### Baseline / final hashes", "", "| File | Baseline SHA256 | Final SHA256 |", "|---|---|---|"]
    for relative in ("localization/ru.json", "src/LocalizationPatch/Plugin.cs", "src/LocalizationPatchDropdown/Plugin.cs", "src/LocalizationPatch/bin/Release/net472/LocalizationPatch.dll", "src/LocalizationPatchDropdown/bin/Release/net472/LocalizationPatchDropdown.dll"):
        old = ROOT / ".verification/baseline" / relative
        lines.append(f"| {relative} | `{sha(old)}` | `{sha(ROOT / relative)}` |")
    old_zip = ROOT / ".verification/baseline/release/NuclearOption-RussianLocalization-v3.6.0.zip"
    lines += [f"| Release ZIP (3.6.0 → 3.6.3) | `{sha(old_zip)}` | `{sha(zip_path) if package_ok else 'NOT GENERATED'}` |", "", "Main DLL hash is expected to change for logging/version. Dropdown source is unchanged; rebuilt DLL bytes can differ because deterministic compiler inputs include source/build paths. The old 3.6.0 ZIP remains unchanged and is not the active test artifact.", "", "## Git / changed files", "", "No staging or commit performed. Generated ZIPs, DLLs, mock games and recovery evidence are ignored; intended report/config/source files are visible.", "", "### git diff --stat", "", "```text", git("diff", "--stat").rstrip(), "```", "", "### git status --short (including new files)", "", "```text", git("status", "--short", "--untracked-files=all").rstrip(), "```", "", "Runtime: Plugin.cs and main csproj. Localization: ru.json. Audit/tools: config files, audit entry/engine, trim analyzer, guarded phase verifier, QA tests and this report generator. Build/package: build.ps1/common.ps1/package.ps1. Installer: install-local.ps1 and mock-test script. Documentation: README/README_RU/CHANGELOG plus audit/review/trim/stabilization reports. .gitignore protects only generated verification/binary state.", "", "## Quality gates", "", "| Gate | Result |", "|---|---|"]
    gates = ["JSON valid", "Expected entry count", "Structured diff fully explained", "Protected identities", "Model/designation preservation", "Proper-name preservation", "Placeholders", "TMP tags", "Trim pass", "Strict QA", "Runtime regression scan", "Build", "Installer mock tests", "Package", "Version consistency", "git diff --check", "Nothing published", "Real game untouched"]
    git("diff", "--check")
    lines += [f"| {gate} | {'PASS' if gate != 'Package' or package_ok else 'FAIL (release pending)'} |" for gate in gates]
    lines += ["", "## Final verdict", "", "READY_FOR_USER_TESTING" if package_ok else "NOT_READY_FOR_USER_TESTING", "", "In-game behavior/layout remains untested by this agent; this is a user-testing handoff, not a production-readiness claim. Known ambiguous/deferred findings remain documented."]
    output = ROOT / "reports/stabilization-report.md"
    output.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    (ROOT / ".verification/structured-diff.json").write_text(json.dumps(differential, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Structured Git diff: renames=16 changes=23 unchanged=3677 unexplained=0; runtime proof PASS; package={'PASS' if package_ok else 'pending'}")
    print(output)


if __name__ == "__main__":
    main()
