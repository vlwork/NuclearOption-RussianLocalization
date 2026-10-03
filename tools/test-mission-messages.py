#!/usr/bin/env python3
"""Offline synthetic discovery fixtures and curated-data regression checks."""
import importlib.util
import json
from pathlib import Path
import struct
import unittest

spec = importlib.util.spec_from_file_location("mission_audit", Path(__file__).with_name("audit-mission-messages.py"))
audit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit)


def encoded_string(text):
    value = text.encode("utf-8")
    result = struct.pack("<I", len(value)) + value
    return result + b"\0" * (-len(result) % 4)


def fixture(name="13. Reprisal", version=6):
    document = dict(JsonVersion=version, missionSettings={"description": "Mission summary"},
                    objectives=[], outcomes=[dict(Type="ShowMessage", UniqueName="StartMessage",
                    Message="K92 is 3 kilometers away.", PlaySound=True, ObjectiveFactionOnly=False)])
    return name, document


def blob(name, document):
    return b"\0" * 16 + encoded_string(name) + encoded_string(json.dumps(document, indent=2))


def records(name, document):
    return audit.candidates([dict(name=name, offset=20, size=100, data=document)])


class MissionTests(unittest.TestCase):
    def test_named_length_prefixed_mission_only(self):
        name, document = fixture()
        found = list(audit.mission_documents(blob(name, document)))
        self.assertEqual(len(found), 1)
        self.assertEqual(found[0]["name"], name)
        self.assertEqual(found[0]["data"], document)
        self.assertEqual(list(audit.mission_documents(json.dumps(document, indent=2).encode())), [])

    def test_malformed_unknown_and_truncated_sources_rejected(self):
        name, document = fixture()
        self.assertEqual(list(audit.mission_documents(blob(name, document)[:-10])), [])
        document["JsonVersion"] = 5
        self.assertEqual(list(audit.mission_documents(blob(name, document))), [])
        document["JsonVersion"] = 6
        del document["objectives"]
        self.assertEqual(list(audit.mission_documents(blob(name, document))), [])

    def test_editor_and_other_fields_not_message_candidates(self):
        name, document = fixture()
        document["outcomes"].append(dict(Type="SpawnUnit", Message="Internal callback", UniqueName="unit-id"))
        document["editor"] = dict(Type="ShowMessage", Message="Editor label")
        sources = {row["source"] for row in records(name, document)}
        self.assertNotIn("Internal callback", sources)
        self.assertNotIn("Editor label", sources)
        self.assertNotIn("unit-id", sources)

    def test_tutorial_and_identifiers_are_separate_exclusions(self):
        name, document = fixture("Tutorial 9 - Fixture")
        rows = records(name, document)
        self.assertEqual({r["category"] for r in rows}, {"MISSION_HINT", "GAMEPLAY_IDENTIFIER"})

    def test_dynamic_placeholders_and_bind_tags(self):
        for source in ("{0} joined", '<bind="Select">', "[bind Select]"):
            self.assertTrue(audit.dynamic_source(source))
        self.assertFalse(audit.dynamic_source("K92 is 3 kilometers away."))

    def test_reviewed_literals_and_provenance_guard(self):
        name, document = fixture()
        plan = dict(reviewedMission=name, translations=[dict(source=document["outcomes"][0]["Message"], russian="K92 в 3 километрах.")])
        self.assertEqual(len(audit.checked_translations(plan, records(name, document))), 1)
        with self.assertRaises(ValueError):
            audit.checked_translations(plan, records("Another mission", document))
        document["outcomes"][0]["Override"] = {"Message": "dynamic"}
        with self.assertRaises(ValueError):
            audit.checked_translations(plan, records(name, document))

    def test_number_callsign_and_identifier_protection(self):
        name, document = fixture()
        source = document["outcomes"][0]["Message"]
        for russian in ("K92 в 4 километрах.", "К92 в 3 километрах."):
            plan = dict(reviewedMission=name, translations=[dict(source=source, russian=russian)])
            with self.assertRaises(ValueError):
                audit.checked_translations(plan, records(name, document))
        document["outcomes"][0]["UniqueName"] = source
        plan["translations"][0]["russian"] = "K92 в 3 километрах."
        with self.assertRaises(ValueError):
            audit.checked_translations(plan, records(name, document))

    def test_exact_lookup_feed_limitation_not_claimed_as_supported(self):
        manifest = json.loads((audit.ROOT / "config/mission-messages.json").read_text(encoding="utf-8"))
        item = next(x for x in manifest["translations"] if "preparing to seize" in x["source"])
        dictionary = {item["source"]: item["russian"]}
        # A model of whole-string lookup, not a claim that a live game was run.
        lookup = lambda text: dictionary.get(text.strip(), text)
        self.assertEqual(lookup(item["source"]), item["russian"])
        for display in (item["source"] + "\nPlayer joined the game",
                        "<color=#FFFFFFFF>" + item["source"] + "</color>",
                        "arbitrary chat: " + item["source"]):
            self.assertEqual(lookup(display), display)

    def test_current_curated_data_and_entry_count(self):
        manifest = json.loads((audit.ROOT / "config/mission-messages.json").read_text(encoding="utf-8"))
        pairs = json.loads((audit.ROOT / "localization/ru.json").read_text(encoding="utf-8-sig"), object_pairs_hook=list)
        russian = dict(pairs)
        self.assertEqual(len(pairs), len(russian))
        self.assertEqual(len(russian), manifest["baselineEntryCount"] + len(manifest["translations"]))
        for item in manifest["translations"]:
            self.assertEqual(russian[item["source"]], item["russian"])
        for identity in ("IR Flares", "Radar Countermeasures", "Continue", "M12 Jackknife"):
            self.assertEqual(russian[identity], identity)

    def test_output_cannot_overwrite_game_or_localization(self):
        source = audit.ROOT / "localization/ru.json"
        with self.assertRaises(ValueError):
            audit.output_path(source, (source,))
        with self.assertRaises(ValueError):
            audit.output_path(Path("G:/SteamLibrary/steamapps/common/Nuclear Option/new.txt"), ())

    def test_markdown_whitespace_and_tags_are_escaped(self):
        self.assertEqual(audit.cell("Line\nK92\t"), '`"Line\\nK92\\t"`')
        self.assertIn("\\u007c", audit.cell("one|two"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
