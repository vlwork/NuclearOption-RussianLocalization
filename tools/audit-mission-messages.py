#!/usr/bin/env python3
"""Offline, read-only mission inventory. Never loads or executes game assemblies.

This is a bounded extractor for named, length-prefixed mission JSON TextAssets,
not a general Unity asset parser. No mission files or binaries are copied to Git.
Reviewed Russian text is curated in config/mission-messages.json, not generated.
"""
import argparse
from collections import Counter, defaultdict
import hashlib
import json
import mmap
from pathlib import Path
import re
import struct

ROOT = Path(__file__).resolve().parents[1]
MARKER = b'{\n  "JsonVersion":'
JOIN_FORMAT = '<color=#{RGBA8}>{PlayerDisplayName} joined the game</color>'


def sha256(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest().upper()


def unique_object(pairs):
    result = dict(pairs)
    if len(result) != len(pairs):
        raise ValueError("Duplicate JSON field; source evidence needs review")
    return result


def mission_documents(blob):
    """Require exact length, alignment, name, schema and JSON validity.

    This recognizes the locally observed format only. Unknown formats are not
    interpreted as mission text / неизвестные форматы не переводятся.
    """
    position = 0
    while (position := blob.find(MARKER, position)) >= 0:
        start = position
        position += len(MARKER)
        if start < 4 or start % 4:
            continue
        size = struct.unpack_from("<I", blob, start - 4)[0]
        if not 1 <= size <= 16 * 1024 * 1024 or start + size > len(blob):
            continue
        names = []
        for name_offset in range(max(0, start - 264), start - 4, 4):
            length = struct.unpack_from("<I", blob, name_offset)[0]
            end = name_offset + 4 + length
            if not 1 <= length <= 256 or (end + 3) // 4 * 4 != start - 4:
                continue
            if any(blob[end:start - 4]):
                continue
            try:
                name = blob[name_offset + 4:end].decode("utf-8")
            except UnicodeDecodeError:
                continue
            if all(c.isprintable() for c in name):
                names.append(name)
        if len(names) != 1:
            continue
        try:
            doc = json.loads(blob[start:start + size].decode("utf-8"), object_pairs_hook=unique_object)
        except (ValueError, UnicodeDecodeError):
            continue
        if (not isinstance(doc, dict) or doc.get("JsonVersion") != 6
                or not isinstance(doc.get("missionSettings"), dict)
                or not isinstance(doc.get("outcomes"), list)
                or not isinstance(doc.get("objectives"), list)):
            continue
        yield dict(name=names[0], offset=start, size=size, data=doc)
        position = start + size


def dynamic_source(text):
    # Conservative classification: these require format/glyph-path review.
    return bool(re.search(r"\{[^{}]*\}|<bind\b|\[bind\b", text, re.I))


def candidates(documents):
    entries = []

    def add(document, node, path, field, route):
        text = node.get(field)
        if not isinstance(text, str) or not text.strip():
            return
        tutorial = document["name"].startswith("Tutorial ")
        if field == "UniqueName":
            category = "GAMEPLAY_IDENTIFIER"
        elif tutorial:
            category = "MISSION_HINT"
        elif dynamic_source(text):
            category = "DYNAMIC_MISSION_MESSAGE"
        else:
            category = "STATIC_MISSION_MESSAGE"
        entries.append(dict(source=text, category=category, route=route,
                            mission=document["name"], offset=document["offset"],
                            path=f"{path}.{field}", field=field,
                            nodeFields=sorted(node)))

    for document in documents:
        doc = document["data"]
        add(document, doc["missionSettings"], "$.missionSettings", "description", "mission summary; display route not reviewed")
        for i, node in enumerate(doc["outcomes"]):
            if isinstance(node, dict) and node.get("Type") == "ShowMessage":
                add(document, node, f"$.outcomes[{i}]", "Message", "ShowMessage -> MessageFeed")
                add(document, node, f"$.outcomes[{i}]", "UniqueName", "outcome ID, not display text")
        for i, node in enumerate(doc["objectives"]):
            if isinstance(node, dict) and node.get("Type") == "DialogueBox":
                for field in ("title", "body", "button", "UniqueName"):
                    add(document, node, f"$.objectives[{i}]", field, "DialogueBox -> glyph helper -> TMP")
    return entries


def checked_translations(manifest, entries):
    planned = {item["source"]: item["russian"] for item in manifest["translations"]}
    if len(planned) != len(manifest["translations"]):
        raise ValueError("Duplicate reviewed source")
    identifiers = {e["source"] for e in entries if e["category"] == "GAMEPLAY_IDENTIFIER"}
    for source, russian in planned.items():
        matches = [e for e in entries if e["source"] == source]
        if (not russian or source in identifiers or not matches or any(
                e["category"] != "STATIC_MISSION_MESSAGE" or e["field"] != "Message"
                or e["mission"] != manifest["reviewedMission"] for e in matches)):
            raise ValueError("Reviewed source has unexpected provenance/category: " + source)
        if any(e["nodeFields"] != ["Message", "ObjectiveFactionOnly", "PlaySound", "Type", "UniqueName"] for e in matches):
            raise ValueError("Non-literal outcome fields require review: " + source)
        if source != source.strip() or source.count("\n") != russian.count("\n"):
            raise ValueError("Reviewed boundary/layout changed")
        if Counter(re.findall(r"\d+", source)) != Counter(re.findall(r"\d+", russian)):
            raise ValueError("Numbers/callsigns changed")
        for name in ("K92", "PALA", "Maris Airport"):
            if source.count(name) != russian.count(name):
                raise ValueError("Proper name/callsign changed: " + name)
    return planned


def build_inventory(resources, assembly, baseline, current, manifest):
    with resources.open("rb") as stream, mmap.mmap(stream.fileno(), 0, access=mmap.ACCESS_READ) as blob:
        documents = list(mission_documents(blob))
    entries = candidates(documents)
    planned = checked_translations(manifest, entries)
    source_hash, assembly_hash = sha256(resources), sha256(assembly)
    if source_hash != manifest["resourcesSha256"] or assembly_hash != manifest["assemblySha256"]:
        raise ValueError("Game build changed: existing runtime review does not authorize this evidence")
    groups = defaultdict(list)
    for entry in entries:
        groups[(entry["category"], entry["source"])].append(entry)
    rows = []
    for (category, source), provenance in sorted(groups.items()):
        fields = {e["field"] for e in provenance}
        action, safety = "MANUAL_REVIEW", "Not selected; display route/context requires separate review"
        if category in ("MISSION_HINT", "GAMEPLAY_IDENTIFIER"):
            action, safety = "KEEP_ENGLISH", "Excluded from new translations; any pre-existing mapping is left untouched"
        elif category == "DYNAMIC_MISSION_MESSAGE":
            action, safety = "NEEDS_RUNTIME_SUPPORT", "Binding/substitution format needs separate review"
        elif source in planned:
            action, safety = "TRANSLATE", "Display-only proven; exact lookup only when feed content matches the whole source"
        elif fields <= {"Message"}:
            safety = "Display-only path traced; translation not language-reviewed; aggregated-feed limitation"
        elif "title" in fields or "button" in fields:
            action, safety = "KEEP_ENGLISH", "Current build uses integer dialogue IDs, but controls/title policy stays conservative"
        rows.append(dict(source=source, category=category, provenance=provenance,
                         alreadyBefore=source in baseline, before=baseline.get(source),
                         current=current.get(source), proposed=planned.get(source),
                         safety=safety, action=action))
    rows.append(dict(source=JOIN_FORMAT, category="DYNAMIC_MISSION_MESSAGE",
                     provenance=[dict(mission="Generic multiplayer notice (not narrative)", offset=None,
                                      path="MessageManager.JoinMessage; StringHelper.AddColor")],
                     alreadyBefore=False, before=None, current=None, proposed=None,
                     safety="Display-only; GetDisplayName + literal suffix + RGBA color; user/chat isolation not available to generic lookup",
                     action="NEEDS_RUNTIME_SUPPORT"))
    return dict(documents=[{k: d[k] for k in ("name", "offset", "size")} for d in documents],
                sourceHash=source_hash, assemblyHash=assembly_hash, rows=rows,
                occurrenceCount=len(entries), counts=dict(sorted(Counter(r["category"] for r in rows).items())),
                translations=manifest["translations"])


RUNTIME = """## Runtime safety and reachability

Local metadata/IL was read with the installed Mono.Cecil; no game assembly was executed.
`MissionGroup.ResourceGroup.TryGetJson` reads named `TextAsset.text`. The inventory extracts only
validated version-6 mission JSON, not arbitrary printable strings or editor labels.

`ShowMessageSavedOutcome.Message` -> `ShowMessageOutcome.Load` copies the source into the runtime
Message field. `Complete` passes it to `MissionMessages.ShowMessage`; faction filtering and sound
flags remain separate. `ShowMessgeLocal` (game spelling), and the RPC client path, call
`GameplayUI.GameMessage` -> `MessageUI.GameMessage`. The latter splits on LF and enqueues original
lines plus expiry times in `MessageFeed`. It computes duration from the original source length.
`RefreshUI` joins queued lines with LF and calls `TMP_Text.SetText(StringBuilder)`.

An exhaustive field-reference scan of Assembly-CSharp (including nested types) found `_display`
only in MessageFeed construction and RefreshUI writes; `MessageUI.messageText` is only passed to
the feed constructor. Neither consumer reads localized TMP text back into objectives, callbacks,
IDs, expiry or faction logic. Source fields are saved/copied independently. The selected Reprisal
outcomes have only the five literal fields Message, PlaySound, ObjectiveFactionOnly, UniqueName,
Type; no variable-binding/override payload. Static data translations do not change these fields.
This is evidence for this pinned local build, not a blanket guarantee for arbitrary custom missions.

The 3.6.3 plugin hooks TMP `.text`, `SetText(string)` and OnEnable; legacy `UI.Text.text` calls
`Translate()` and is also scanned. `TranslateTmpComponent`/`Translate` trim the whole displayed
string, perform exact lookup, then existing UI-oriented patterns. The actual mission feed uses
the unhooked StringBuilder overload: existing active TMP sweeps catch it, rather than guaranteed
setter-time interception. Legacy Text is not the traced mission feed. No new sweep is added.

**Important limitation:** one unformatted message alone can match its complete dictionary key.
Two messages, a concurrent player/chat notice, clipped LF lines, or color wrappers normally cannot.
There is no line-by-line or suffix localization in the current lookup. Newline-count preservation
is necessary but does not solve concatenation. No literal combinations/player-name variants are added.

Dialogue objectives use `ShowDialogue` -> `DialogueBox.Show`, with title/body/button routed through
`ReplaceBindTags` and `UnityUITextMeshProGlyphHelper`. The inspected current build's button callback
uses integer CurrentId, not displayed title/button text; objective completion sets a separate bool.
Nevertheless titles/buttons remain unchanged, particularly protected Continue, because of the
previous read-back regression and the plugin's existing title policy. Glyph/binding substitutions
and tutorial dialogue are deferred. No dialogue translations are added in this pass.

## Unsupported dynamic/composed formats — intermediate runtime review

The join notice is proven: `Player.GetDisplayName(context=0) + \" joined the game\"`, wrapped by
`StringHelper.AddColor` as `<color=#{eight-digit RGBA}>{display name} joined the game</color>`,
then placed in the same feed as narrative/chat. The existing exact lookup cannot handle arbitrary
names, colors or feed combinations. No suffix matcher is added: arbitrary chat can contain the same
words and must not be mistaken for a system notice. Existing exact matching is itself not
context-aware; user text equal to a full dictionary key can still match, a pre-existing limitation.

Proposed future narrow solution (NOT IMPLEMENTED): translate each proven authored ShowMessage
argument locally before feed composition, without mutating mission data/network serialization;
handle JoinMessage only at its proven producer and preserve display-name/tag bytes. Restrict the
authored hook to built-in reviewed outcomes if custom missions must not be affected. Tests would
need to prove queue composition, LF clipping, host/client paths, unchanged identifiers, no chat
interception, exact name preservation and intact color/glyph tags. Risks include Harmony signature
drift, producer call sharing, double translation, client/server divergence and user-generated mission
content. This needs user review before any Plugin.cs edit. No runtime or hierarchy changes made.

## Inventory interpretation and exclusions

Rows are distinct (category, exact source) pairs; a shared literal may appear in multiple categories.
Provenance lists every occurrence in the recognized local TextAssets. Identifiers and tutorial
material are separate exclusion rows, never included in mission-message candidate totals. The
manifest intentionally reviews only Reprisal's 13 literal outcomes; proposed translations for other
rows are absent, not silently machine-generated. Empty fields are not candidates. Mission summaries
are listed but their picker/briefing display path has not been cleared for new translation.

Mission Editor is deferred. Did-you-know hints and tutorial guidance are deferred. Cockpit/HUD/MFD
localization remains incomplete and outside scope. Encyclopedia corrections are retained byte-for-byte
as part of the untouched existing values. The current untranslated.txt and extracted_gamedata.txt
exports contain no exact K92 sentence; resources.assets does, with a single-space sentence separator
(the request's line wrapping is not a separate source).
No copied game files, installed-game writes, network access, commit, push or publishing.
"""


def cell(value):
    # JSON escaping preserves whitespace visibly and avoids Markdown/tag interpretation.
    if value is None:
        return "—"
    return "`" + json.dumps(value, ensure_ascii=False).replace("|", "\\u007c").replace("`", "\\u0060") + "`"


def markdown(inventory):
    counts = inventory["counts"]
    scoped = sum(counts.get(k, 0) for k in ("STATIC_MISSION_MESSAGE", "DYNAMIC_MISSION_MESSAGE", "UNKNOWN"))
    lines = ["# Mission messages audit", "", "## Discovery", "",
             f"Recognized named mission TextAssets: **{len(inventory['documents'])}**. Recognized field occurrences: **{inventory['occurrenceCount']}**.",
             f"Mission-message candidate rows (excluding identifiers/tutorials): **{scoped}**. Generic join notice is counted separately from narrative and is included as one dynamic candidate.", "",
             "| Category | Distinct exact-source rows |", "| --- | ---: |"]
    for category in ("STATIC_MISSION_MESSAGE", "DYNAMIC_MISSION_MESSAGE", "GAMEPLAY_IDENTIFIER", "MISSION_EDITOR", "MISSION_HINT", "UNKNOWN"):
        lines.append(f"| {category} | {counts.get(category, 0)} |")
    lines += ["", f"resources.assets SHA256: `{inventory['sourceHash']}`.",
              f"Assembly-CSharp.dll SHA256: `{inventory['assemblyHash']}`.",
              "Read-only inputs: `G:/SteamLibrary/steamapps/common/Nuclear Option/NuclearOption_Data/`.", "",
              "Scope: recognized named, length-prefixed version-6 mission JSON in resources.assets; not exhaustive across custom/downloaded missions or other Unity formats.", "", RUNTIME, "",
              "## Complete reviewed English → Russian additions", "",
              "| Exact English source | Reviewed Russian |", "| --- | --- |"]
    for item in inventory["translations"]:
        lines.append(f"| {cell(item['source'])} | {cell(item['russian'])} |")
    lines += ["", "## Complete source inventory", "",
              "Each section preserves exact source spelling and whitespace via JSON escaping. Sources are not modified."]
    for index, row in enumerate(inventory["rows"], 1):
        lines += ["", f"### {index}. {row['category']} — {row['action']}", "",
                  ("- Symbolic producer format (not a literal dictionary key): " if row["source"] == JOIN_FORMAT else "- Exact English: ") + cell(row["source"]),
                  "- Already in ru.json before this pass: " + ("yes" if row["alreadyBefore"] else "no"),
                  "- Before Russian: " + cell(row["before"]),
                  "- Current Russian: " + cell(row["current"]),
                  "- Proposed Russian: " + cell(row["proposed"]),
                  "- Runtime safety: " + row["safety"],
                  "- Action: " + row["action"], "- Provenance:"]
        for item in row["provenance"]:
            offset = "" if item["offset"] is None else f"; TextAsset JSON offset {item['offset']}"
            lines.append(f"  - {cell(item['mission'])}; `{item['path']}`{offset}")
    return "\n".join(lines) + "\n"


def output_path(path, inputs):
    path = path.resolve()
    if path in {p.resolve() for p in inputs} or not any(path.is_relative_to(ROOT / name) for name in ("reports", ".verification")):
        raise ValueError("Output must be repo-local reports/ or .verification/, never an input")
    return path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--resources", type=Path, required=True)
    parser.add_argument("--assembly", type=Path, required=True)
    parser.add_argument("--baseline", type=Path, required=True)
    parser.add_argument("--report", type=Path, default=ROOT / "reports/mission-messages-audit.md")
    parser.add_argument("--json-report", type=Path, required=True)
    args = parser.parse_args()
    current_path = ROOT / "localization/ru.json"
    config = ROOT / "config/mission-messages.json"
    manifest = json.loads(config.read_text(encoding="utf-8"), object_pairs_hook=unique_object)
    if sha256(args.baseline) != manifest["baselineSha256"]:
        raise ValueError("Unexpected baseline; preserve existing localization work")
    baseline = json.loads(args.baseline.read_text(encoding="utf-8-sig"), object_pairs_hook=unique_object)
    current = json.loads(current_path.read_text(encoding="utf-8-sig"), object_pairs_hook=unique_object)
    inventory = build_inventory(args.resources, args.assembly, baseline, current, manifest)
    inputs = (args.resources, args.assembly, args.baseline, current_path, config)
    for path, content in ((args.report, markdown(inventory)), (args.json_report, json.dumps(inventory, ensure_ascii=False, indent=2) + "\n")):
        path = output_path(path, inputs)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8", newline="\n")
    print(json.dumps(dict(documents=len(inventory["documents"]), counts=inventory["counts"], reviewed=len(inventory["translations"])), ensure_ascii=True))


if __name__ == "__main__":
    main()
