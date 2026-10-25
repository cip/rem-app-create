#!/usr/bin/env python3
"""Contract checks for the pinned official plugin-eval schema v2."""
import tempfile
import unittest
from pathlib import Path

from build_plugin_eval_benchmark import build_config


class ContractTests(unittest.TestCase):
    def test_official_schema_and_isolation_intent(self):
        with tempfile.TemporaryDirectory() as dirname:
            result = build_config("test-model", Path(dirname))
        self.assertEqual(result["kind"], "plugin-eval-benchmark")
        self.assertEqual(result["schemaVersion"], 2)
        self.assertEqual(result["runner"]["type"], "codex-cli")
        self.assertEqual(result["runner"]["approvalPolicy"], "never")
        self.assertEqual(result["runner"]["model"], "test-model")
        self.assertEqual(result["targetProvisioning"]["mode"], "isolated-skill-home")
        self.assertEqual(len(result["scenarios"]), 4)
        for scenario in result["scenarios"]:
            self.assertIn("scripts/fake_github.py", scenario["userInput"])
            self.assertIn("Do not use any real GitHub", scenario["userInput"])
            self.assertTrue(scenario["successChecklist"])
        self.assertEqual(result["verifiers"]["commands"], ["python3 scripts/test_fake_github.py"])


if __name__ == "__main__":
    unittest.main()
