#!/usr/bin/env python3
"""Unit tests using fabricated Codex JSONL-shape events, NOT live Codex evidence."""
import unittest
from verify_codex_trace import check_trace

def command(value):
    return {"type": "item.completed", "item": {"type": "command_execution", "command": value}}

class TraceGateTests(unittest.TestCase):
    def test_accepts_only_minimum_observable_adapter_usage(self):
        events = [command("python3 scripts/fake_github.py --scenario fixed-on-develop"), {"type": "turn.completed"}]
        self.assertEqual(check_trace(events, "already-fixed"), [])
    def test_missing_fake_rejected(self):
        self.assertTrue(check_trace([{"type": "turn.completed"}], "already-fixed"))
    def test_network_rejected(self):
        events = [command("curl https://api.github.com"), command("python3 scripts/fake_github.py --scenario app-only"), {"type": "turn.completed"}]
        self.assertTrue(any("network" in e for e in check_trace(events, "app-only")))
    def test_wrong_fixture_rejected(self):
        self.assertIn("wrong fake scenario", check_trace([command("python3 scripts/fake_github.py --scenario private-log"), {"type": "turn.completed"}], "already-fixed"))
    def test_missing_completion_rejected(self):
        self.assertTrue(check_trace([command("python3 scripts/fake_github.py --scenario app-only")], "app-only"))
    def test_unknown_external_tool_rejected(self):
        self.assertTrue(check_trace([{"type":"item.started","item":{"type":"mcp_tool_call","name":"github.search"}}, {"type":"turn.completed"}], "app-only"))
    def test_no_events_rejected(self):
        self.assertTrue(check_trace([], "app-only"))

if __name__ == "__main__":
    unittest.main()
