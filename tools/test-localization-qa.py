#!/usr/bin/env python3
"""Offline regression fixtures live only in the ignored repository verification tree."""
import copy
import importlib.util
import json
import subprocess
import unittest
import uuid
from pathlib import Path

spec = importlib.util.spec_from_file_location("audit", Path(__file__).with_name("audit-localization.py"))
audit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit)


class AuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.directory = audit.ROOT / ".verification" / ("qa-tests-" + uuid.uuid4().hex)
        cls.directory.mkdir(parents=True)
        cls.config = json.loads((audit.ROOT / "config/localization-audit.json").read_text(encoding="utf-8"))

    def fixture(self, pairs, raw=None):
        path = self.directory / (uuid.uuid4().hex + ".json")
        path.write_text(raw if raw is not None else json.dumps(pairs, ensure_ascii=False), encoding="utf-8")
        config = copy.deepcopy(self.config)
        config["expectedEntryCount"] = len(pairs)
        config["protectedIdentities"] = []
        config["qualityCandidates"] = []
        return path, config

    def test_json_schema_duplicates_and_invalid(self):
        for raw in ("[]", '{"a":1}', '{"a":"x",}', '{"a":"x","a":"y"}'):
            path, config = self.fixture({"a": "x"}, raw)
            self.assertTrue(any(f["strict"] for f in audit.analyze(path, config)["findings"]))

    def test_identity_failure(self):
        path, config = self.fixture({"Continue": "Продолжить"})
        config["protectedIdentities"] = ["Continue"]
        self.assertEqual(audit.analyze(path, config)["metrics"]["ProtectedIdentityViolations"], 1)

    def test_future_ascii_designations_and_names(self):
        path, config = self.fixture({"X/A-123 Mk": "Х/А-123 Mk", "Q9Z42 Boltstrike": "Q9Z42 Болтстрайк", "T/A-30 factory": "завод T/A-30"})
        result = audit.analyze(path, config)
        self.assertEqual(result["metrics"]["DesignationViolations"], 1)
        self.assertEqual(result["metrics"]["ProperNameViolations"], 1)

    def test_vortex_context(self):
        path, config = self.fixture({"Vortex ring state": "Режим вихревого кольца", "FS-20 Vortex": "FS-20 Vortex"})
        self.assertEqual(audit.analyze(path, config)["metrics"]["ProperNameViolations"], 0)

    def test_formats_escaped_braces_and_reordering(self):
        self.assertEqual(audit.placeholders("{{0}} {0} {2, 10:N0}"), audit.placeholders("{2,10:N0} {{0}} {0}"))
        path, config = self.fixture({"{2:N0} {1}": "{2} {1}"})
        self.assertEqual(audit.analyze(path, config)["metrics"]["PlaceholderMismatches"], 1)

    def test_tmp_attribute_case_loss_and_pseudo_labels(self):
        path, config = self.fixture({'<font="MyFont"><b>Hi</b></font>': '<font="myfont"><b>Привет</b></font>', "<no filter>": "<без фильтра>", "<select a mission>": "<выбрать миссию>"})
        self.assertEqual(audit.analyze(path, config)["metrics"]["TmpTagMismatches"], 1)

    def test_trim_case_and_style_are_nonfatal(self):
        path, config = self.fixture({" Label ": "20мм", "Label": "Метка", "LABEL": "Название", "Line\nTwo": "Строка"})
        result = audit.analyze(path, config)
        self.assertEqual(result["metrics"]["TrimCollisions"], 1)
        self.assertEqual(result["metrics"]["NewlineMismatches"], 1)
        self.assertFalse(any(f["strict"] for f in result["findings"]))

    def test_dotnet_trim_not_python_extra_control(self):
        self.assertEqual(audit.trim("\u00a0label\t"), "label")
        self.assertEqual(audit.trim("\x1clabel\x1c"), "\x1clabel\x1c")

    def test_actual_runtime_export_coverage_and_noise(self):
        path, config = self.fixture({"Hint one": "Подсказка", "Description here": "Описание"})
        extracted = self.directory / "extracted_gamedata.txt"
        extracted.write_text('// ========== DID YOU KNOW? HINTS ==========\n// Raw CSV\nid,type,text\n"Hint one": "",\n"Missing hint": "",\n// ========== ENCYCLOPEDIA DESCRIPTIONS ==========\n"Description  here": "",\n// ========== UNIT DEFINITION STRUCTURE ==========\n"not a description": "",\n', encoding="utf-8")
        untranslated = self.directory / "untranslated.txt"
        untranslated.write_text('// exported\n"AFTERBURNER 84%": "",\n"R1": "",\n', encoding="utf-8")
        result = audit.analyze(path, config, extracted, untranslated)
        self.assertEqual(result["coverage"]["Hints"]["source"], 2)
        self.assertEqual(result["coverage"]["Hints"]["exact"], 1)
        self.assertEqual(result["coverage"]["Encyclopedia"]["normalized"], 1)
        self.assertEqual(sum(f["category"] == "Untranslated noise" for f in result["findings"]), 2)

    def test_cli_read_only_deterministic_and_exit_modes(self):
        path, config = self.fixture({"A-99": "А-99"})
        config_path = self.directory / "config.json"
        config_path.write_text(json.dumps(config), encoding="utf-8")
        report = self.directory / "report.md"
        command = ["python", str(Path(__file__).with_name("audit-localization.py")), "--localization", str(path), "--config", str(config_path), "--report", str(report)]
        before = path.read_bytes()
        self.assertEqual(subprocess.run(command, capture_output=True).returncode, 0)
        first = report.read_bytes()
        self.assertEqual(subprocess.run(command + ["--strict"], capture_output=True).returncode, 1)
        self.assertEqual(first, report.read_bytes())
        self.assertEqual(before, path.read_bytes())

    def test_cannot_redirect_report_over_inputs_or_source(self):
        path, _ = self.fixture({"a": "b"})
        with self.assertRaises(ValueError):
            audit.output_path(path, (path,))
        with self.assertRaises(ValueError):
            audit.output_path(audit.ROOT / "localization/ru.json")


if __name__ == "__main__":
    unittest.main(verbosity=2)
