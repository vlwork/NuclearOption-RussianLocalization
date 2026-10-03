#!/usr/bin/env python3
"""Guarded mechanical application of explicitly reviewed changes, never translation generation.

Default is read-only. --apply requires the exact checkpoint and the selected phase.
Each phase is validated in memory before writing; original bytes are retained for rollback.
"""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path


def helper(name):
    spec = importlib.util.spec_from_file_location(name, Path(__file__).with_name(name + ".py"))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


SAFE_RAW_KEYS = helper("analyze-trim-safety").SAFE_RAW_KEYS
audit = helper("audit-localization")
ROOT, load_pairs, trim = audit.ROOT, audit.load_pairs, audit.trim


def phase_trim(before):
    assert len(before) == 3716
    unsafe = [k for k in before if k != trim(k)]
    groups = {}
    for k in before:
        groups.setdefault(trim(k), []).append(k)
    assert len(unsafe) == 128 and sum(len(v) > 1 for v in groups.values()) == 4
    redundant = [k for k in unsafe if trim(k) in before and before[k] == before[trim(k)]]
    assert len(redundant) == 2 and len(SAFE_RAW_KEYS) == 16
    assert len(set(unsafe) - SAFE_RAW_KEYS - set(redundant)) == 110
    assert SAFE_RAW_KEYS <= before.keys()
    assert all(trim(k) not in before for k in SAFE_RAW_KEYS)
    after = {trim(k) if k in SAFE_RAW_KEYS else k: v for k, v in before.items()}
    assert len(after) == 3716 and sum(k != trim(k) for k in after) == 112
    assert len(before.keys() - after.keys()) == len(after.keys() - before.keys()) == 16
    assert all(after[trim(k) if k in SAFE_RAW_KEYS else k] == v for k, v in before.items())
    return after


def planned_values(baseline, manifest):
    changes = []
    for item in manifest["values"]:
        key = item["source"]
        old = baseline[key]
        assert item.get("before", old) == old, key
        new = item.get("after", old)
        for left, right in item.get("replace", []):
            assert new.count(left) == 1, (key, left)
            new = new.replace(left, right)
        assert new != old and item["reason"], key
        changes.append(dict(source=key, before=old, after=new, reason=item["reason"], classification=item["classification"]))
    assert len({v["source"] for v in changes}) == len(changes)
    return changes


def verify(baseline, actual, changes):
    expected = phase_trim(baseline)
    for item in changes:
        expected[item["source"]] = item["after"]
    assert actual == expected, "Unexplained structured difference; do not package"
    return dict(entriesBefore=len(baseline), entriesAfter=len(actual), renamedKeys=[dict(before=k, after=trim(k), reason="Previously reviewed SAFE_TO_NORMALIZE; boundary U+0020 only, no collision or value change.") for k in sorted(SAFE_RAW_KEYS)], addedEntries=[], removedEntries=[], changedValues=changes, unexplainedChanges=[])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("phase", choices=("trim", "values", "verify"))
    parser.add_argument("--baseline", type=Path, required=True)
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    manifest = json.loads((ROOT / "config/stabilization-changes.json").read_text(encoding="utf-8"))
    assert hashlib.sha256(args.baseline.read_bytes()).hexdigest().upper() == manifest["baselineSha256"]
    baseline, counts = load_pairs(args.baseline)
    assert max(counts.values()) == 1
    path = ROOT / "localization/ru.json"
    original = path.read_bytes()
    actual, _ = load_pairs(path)
    changes = planned_values(baseline, manifest)
    trimmed = phase_trim(baseline)
    if args.phase == "verify":
        print(json.dumps(verify(baseline, actual, changes), ensure_ascii=True, indent=2))
        return
    assert actual == (baseline if args.phase == "trim" else trimmed), "Phase starting scope changed"
    expected = trimmed.copy()
    if args.phase == "values":
        for item in changes:
            expected[item["source"]] = item["after"]
    # Exact JSON-token substitutions preserve the minified document's bytes/order otherwise.
    text = original.decode("utf-8-sig")
    if args.phase == "trim":
        replacements = [(json.dumps(k, ensure_ascii=False) + ":", json.dumps(trim(k), ensure_ascii=False) + ":") for k in sorted(SAFE_RAW_KEYS)]
    else:
        replacements = [(json.dumps(item["source"], ensure_ascii=False) + ":" + json.dumps(item["before"], ensure_ascii=False), json.dumps(item["source"], ensure_ascii=False) + ":" + json.dumps(item["after"], ensure_ascii=False)) for item in changes]
    for old, new in replacements:
        assert text.count(old) == 1, old
        text = text.replace(old, new)
    assert json.loads(text) == expected
    print(f"{args.phase}: entries=3716 renames={16 if args.phase == 'trim' else 0} valueChanges={len(changes) if args.phase == 'values' else 0}; apply={args.apply}")
    if args.apply:
        try:
            path.write_bytes((b'\xef\xbb\xbf' if original.startswith(b'\xef\xbb\xbf') else b'') + text.encode("utf-8"))
            written, _ = load_pairs(path)
            assert written == expected
        except BaseException:
            path.write_bytes(original)  # Roll back this phase only / откат только текущего этапа.
            raise


if __name__ == "__main__":
    main()
