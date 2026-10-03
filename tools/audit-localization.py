#!/usr/bin/env python3
"""Offline, deterministic QA. Input data is never rewritten by this tool."""
from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
# Char.IsWhiteSpace used by .NET String.Trim; not Python's extra C0 separators.
DOTNET_WS = "\t\n\v\f\r \u0085\u00a0\u1680\u2000\u2001\u2002\u2003\u2004\u2005\u2006\u2007\u2008\u2009\u200a\u2028\u2029\u202f\u205f\u3000"
SEVERITIES = ("CRITICAL", "HIGH", "MEDIUM", "INFO")


def trim(text):
    return text.strip(DOTNET_WS)


def normalize(text):
    return " ".join(text.split())


def load_pairs(path):
    """Preserve exact duplicate keys instead of accepting the last silently."""
    text = path.read_text(encoding="utf-8-sig")
    if not text.lstrip().startswith("{"):
        raise ValueError("Root must be a JSON object")
    pairs = json.loads(text, object_pairs_hook=list)
    if not isinstance(pairs, list) or any(not isinstance(p, tuple) or len(p) != 2 for p in pairs):
        raise ValueError("Root must be a JSON object of string pairs")
    if any(not isinstance(k, str) or not isinstance(v, str) for k, v in pairs):
        raise ValueError("All source keys and translation values must be strings")
    return dict(pairs), Counter(k for k, _ in pairs)


def placeholders(text):
    # Escaped {{ and }} are literals, not composite-format arguments.
    result = []
    i = 0
    while i < len(text):
        if text[i:i + 2] in ("{{", "}}"):
            i += 2
            continue
        match = re.match(r"\{(\d+)(?:\s*,\s*(-?\d+))?(?::([^{}]*))?\}", text[i:])
        if match:
            result.append((int(match[1]), int(match[2]) if match[2] else None, match[3]))
            i += len(match[0])
        else:
            i += 1
    return Counter(result)


def tags(text, config):
    if text in config["pseudoLabels"]:
        return []
    result = []
    for match in re.finditer(r"</?([A-Za-z][\w-]*)(?:\s[^<>]*|=[^<>]*)?\s*/?>|<#[0-9a-fA-F]{6,8}>", text):
        if match[1] is None or match[1].lower() in config["tmpTags"]:
            tag = re.sub(r"\s+", " ", match[0])
            if match[1]:
                tag = tag.replace(match[1], match[1].lower(), 1)
            result.append(tag)
    return result


def exported_source(line):
    """Decode the quoted key in runtime exports, or accept a plain snapshot line."""
    line = line.strip()
    if not line or line.startswith("//"):
        return None
    if line.startswith('"'):
        try:
            value, _ = json.JSONDecoder().raw_decode(line)
            return value if isinstance(value, str) else None
        except ValueError:
            return None
    return line


def extracted_records(path):
    records, section, runtime_export = defaultdict(set), None, False
    for raw in path.read_text(encoding="utf-8-sig").splitlines():
        line = raw.strip()
        if line.startswith("//") and "==========" in line:
            runtime_export = True
            section = "Hints" if "DID YOU KNOW? HINTS" in line else ("Encyclopedia" if "ENCYCLOPEDIA DESCRIPTIONS" in line else None)
            continue
        header = re.fullmatch(r"\[?(Did you know\??(?: hints?)?|Encyclopedia(?: descriptions?)?)\]?\s*:?", line, re.I)
        if header:
            section = "Hints" if header[1].lower().startswith("did") else "Encyclopedia"
        elif re.match(r"^\[.*\]$", line):
            section = None
        elif section:
            # Runtime exports contain raw CSV too. Count only emitted source keys there.
            if runtime_export and not re.match(r'^"(?:\\.|[^"\\])*"\s*:', line):
                continue
            source = exported_source(line)
            if source:
                records[section].add(source)
    return records


def analyze(path, config, extracted=None, untranslated=None):
    findings = []
    metrics = dict.fromkeys(("EntryCount", "DuplicateExactKeys", "ProtectedIdentityViolations", "TrimUnsafeKeys", "TrimCollisions", "DesignationViolations", "ProperNameViolations", "PlaceholderMismatches", "TmpTagMismatches", "NewlineMismatches", "CaseVariantGroups", "InconsistentCaseVariantGroups", "TypographyWarnings", "DynamicNoiseEntries"), 0)

    def add(severity, category, source, value, reason, action, strict=False):
        findings.append(dict(severity=severity, category=category, source=source, value=value,
                             reason=reason, action=action, strict=strict))

    try:
        data, counts = load_pairs(path)
    except (ValueError, OSError) as error:
        add("CRITICAL", "JSON integrity", "(document)", "", str(error), "Repair invalid data before building.", True)
        return dict(metrics=metrics, findings=findings, coverage={})
    metrics["EntryCount"] = len(data)
    if len(data) != config["expectedEntryCount"]:
        add("CRITICAL", "JSON integrity", "(document)", str(len(data)), "Unexpected entry count.", "Review the baseline deliberately.", True)
    for key, count in sorted(counts.items()):
        if count > 1:
            metrics["DuplicateExactKeys"] += 1
            add("CRITICAL", "JSON integrity", key, data[key], f"Exact key occurs {count} times.", "Resolve manually before packaging.", True)
    groups, case_groups = defaultdict(list), defaultdict(list)
    for key in sorted(data):
        groups[trim(key)].append(key)
        case_groups[key.upper()].append(key)
        if key != trim(key):
            metrics["TrimUnsafeKeys"] += 1
            add("HIGH", "Trim safety", key, data[key], "Boundary whitespace prevents ordinary exact runtime lookup.", "Review source/context; never bulk-trim.")
    for key, members in sorted(groups.items()):
        if len(members) > 1:
            metrics["TrimCollisions"] += 1
            add("HIGH", "Trim collision", " || ".join(members), " || ".join(data[k] for k in members), f"All normalize to {key!r}.", "Retain until context and values justify a decision.")
    for key in config["protectedIdentities"]:
        if data.get(key) != key:
            metrics["ProtectedIdentityViolations"] += 1
            add("CRITICAL", "Protected identity", key, data.get(key, "(missing)"), "Required exact identity changed.", "Restore the English identity.", True)
    for key, value in sorted(data.items()):
        for token in sorted(set(re.findall(config["designationPattern"], key))):
            if token not in config["designationExclusions"] and not re.search(r"(?<![A-Za-z0-9_/])" + re.escape(token) + r"(?![A-Za-z0-9_/])", value):
                metrics["DesignationViolations"] += 1
                add("CRITICAL", "Model/designation preservation", key, value, f"Missing exact ASCII designation {token}.", f"Preserve {token} verbatim.", True)
        for item in config["properNames"]:
            pattern = r"(?<![A-Za-z0-9_])" + re.escape(item["name"]) + r"(?![A-Za-z0-9_])"
            if re.search(pattern, key) and not any(re.search(p, key) for p in item.get("excludeSourcePatterns", [])) and not re.search(pattern, value):
                metrics["ProperNameViolations"] += 1
                add("CRITICAL", "Proper name", key, value, f"Proper name {item['name']} disappeared or was transliterated.", "Preserve original spelling; translate generic nouns only.", True)
        if placeholders(key) != placeholders(value):
            metrics["PlaceholderMismatches"] += 1
            add("CRITICAL", "Format placeholders", key, value, "Argument index, alignment, format or multiplicity differs.", "Preserve semantically equivalent format arguments.", True)
        if tags(key, config) != tags(value, config):
            metrics["TmpTagMismatches"] += 1
            add("CRITICAL", "TMP tags", key, value, "Rich-text tag sequence/attributes differ.", "Preserve markup structure and attributes.", True)
        if key.count("\n") != value.count("\n") or key.count("\r") != value.count("\r"):
            metrics["NewlineMismatches"] += 1
            add("MEDIUM", "Newline safety", key, value, "Line break counts differ; formatting may be intentional.", "Check layout/concatenation before editing.")
        issues = []
        if re.search(r"(?<![\w])\d+(?:[.,]\d+)?(?:мм|см|км|м|кг|г|т|с|ч|л|вт|квт)\b", value, re.I):
            issues.append("Number touches a Cyrillic unit.")
        if re.search(r"[^\S\r\n]{2,}", value) and not re.search(r"[^\S\r\n]{2,}", key):
            issues.append("Added duplicate horizontal spaces.")
        if re.search(r"\s+[,.!?;]", value) and not re.search(r"\s+[,.!?;]", key):
            issues.append("Likely stray space before punctuation.")
        if value != trim(value) and key == trim(key):
            issues.append("Added boundary whitespace.")
        if issues:
            metrics["TypographyWarnings"] += 1
            add("MEDIUM", "Russian typography", key, value, " ".join(issues), "Review ordinary prose only; protect telemetry and identifiers.")
        if any(re.search(p, key) for p in config["dynamicPatterns"]):
            metrics["DynamicNoiseEntries"] += 1
            add("INFO", "Dynamic noise", key, value, "Generated telemetry/resolution-like literal.", "Report only; no untested runtime pattern changes.")
    for members in case_groups.values():
        if len(members) > 1:
            metrics["CaseVariantGroups"] += 1
            if len({normalize(data[k]).upper() for k in members}) > 1:
                metrics["InconsistentCaseVariantGroups"] += 1
                add("MEDIUM", "Case variants", " || ".join(members), " || ".join(data[k] for k in members), "Translations differ beyond capitalization/whitespace.", "Verify context; case-only groups are not automatically errors.")
    for key in config["qualityCandidates"]:
        add("MEDIUM", "Translation quality", key, data.get(key, "(missing)"), "Curated terminology/identity review candidate, not an automatic error.", "Record a reviewed decision; retain ambiguity.")
    coverage = {}
    if extracted and extracted.is_file():
        records = extracted_records(extracted)
        normalized = {normalize(k) for k in data}
        for kind in ("Hints", "Encyclopedia"):
            sources = records[kind]
            missing = sorted(k for k in sources if normalize(k) not in normalized)
            coverage[kind] = dict(source=len(sources), exact=sum(k in data for k in sources), normalized=sum(normalize(k) in normalized for k in sources), missing=missing)
            for source in missing:
                add("HIGH", "Coverage", source, "(missing)", f"Missing {kind} source.", "Deferred hints stay deferred; review source provenance.")
    else:
        add("INFO", "Coverage", "extracted_gamedata.txt", "(unavailable)", "No local extracted snapshot: coverage is unknown, not 100%.", "Supply an existing snapshot for an offline comparison.")
    if untranslated and untranslated.is_file():
        for key in sorted({source for line in untranslated.read_text(encoding="utf-8-sig").splitlines() if (source := exported_source(line))}):
            if any(re.search(p, key) for p in config["dynamicPatterns"]):
                add("INFO", "Untranslated noise", key, "(untranslated)", "Generated source pattern.", "Report only; do not add literal numeric entries.")
    findings.sort(key=lambda f: (SEVERITIES.index(f["severity"]), f["category"], f["source"], f["reason"]))
    return dict(metrics=metrics, findings=findings, coverage=coverage)


def cell(value):
    return html.escape(str(value), quote=False).replace("|", "&#124;").replace("\r", "\\r").replace("\n", "\\n")


def report(result):
    lines = ["# Localization quality audit", "", "Deterministic offline report. Localization/package inputs are read-only. Review candidates are not automatically defects.", "", "## Summary", "", "| Metric | Count |", "|---|---:|"]
    lines += [f"| {key} | {value} |" for key, value in result["metrics"].items()]
    lines += [f"| {severity} | {sum(f['severity'] == severity for f in result['findings'])} |" for severity in SEVERITIES]
    lines += ["", "Strict mode fails on objective invariants (JSON/schema/count/duplicates, identities, codes, proper names, placeholders and TMP). Style, trim and context warnings do not fail strict mode.", "", "## Coverage", ""]
    lines += [cell(result["coverage"]) if result["coverage"] else "Unavailable: no extracted source snapshot. No coverage percentage can be established."]
    for severity in SEVERITIES:
        lines += ["", f"## {severity}", "", "| Category | Source key (JSON-escaped) | Current Russian value | Reason | Suggested action |", "|---|---|---|---|---|"]
        for item in result["findings"]:
            if item["severity"] == severity:
                lines.append("| " + " | ".join(cell(json.dumps(item[k], ensure_ascii=False)) if k in ("source", "value") else cell(item[k]) for k in ("category", "source", "value", "reason", "action")) + " |")
    return "\n".join(lines) + "\n"


def output_path(path, inputs=()):
    resolved = path.resolve()
    if ROOT not in resolved.parents or resolved.relative_to(ROOT).parts[0] not in ("reports", ".verification"):
        raise ValueError("Audit outputs must stay under repository reports/ or .verification/")
    if resolved in {p.resolve() for p in inputs}:
        raise ValueError("Refusing to overwrite an audit input")
    resolved.parent.mkdir(parents=True, exist_ok=True)
    return resolved


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--strict", action="store_true")
    parser.add_argument("--check-only", action="store_true")
    parser.add_argument("--localization", type=Path, default=ROOT / "localization/ru.json")
    parser.add_argument("--config", type=Path, default=ROOT / "config/localization-audit.json")
    parser.add_argument("--report", type=Path, default=ROOT / "reports/localization-audit.md")
    parser.add_argument("--json-report", type=Path)
    parser.add_argument("--extracted", type=Path, default=ROOT / "extracted_gamedata.txt")
    parser.add_argument("--untranslated", type=Path, default=ROOT / "untranslated.txt")
    args = parser.parse_args()
    result = analyze(args.localization, json.loads(args.config.read_text(encoding="utf-8-sig")), args.extracted, args.untranslated)
    result["sha256"] = hashlib.sha256(args.localization.read_bytes()).hexdigest().upper() if args.localization.is_file() else None
    result["severityCounts"] = {s: sum(f["severity"] == s for f in result["findings"]) for s in SEVERITIES}
    result["strictFailures"] = sum(f["strict"] for f in result["findings"])
    if not args.check_only:
        inputs = (args.localization, args.config, args.extracted, args.untranslated)
        report_path = output_path(args.report, inputs)
        json_path = output_path(args.json_report, inputs) if args.json_report else None
        if json_path == report_path:
            raise ValueError("Markdown and JSON outputs must be distinct")
        report_path.write_text(report(result), encoding="utf-8", newline="\n")
        if args.json_report:
            json_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({k: result[k] for k in ("metrics", "severityCounts", "strictFailures")}, ensure_ascii=True))
    return int(args.strict and result["strictFailures"] > 0)


if __name__ == "__main__":
    raise SystemExit(main())
