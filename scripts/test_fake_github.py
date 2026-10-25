#!/usr/bin/env python3
"""Offline contract tests for fake GitHub boundary. No agent execution."""
import unittest
from fake_github import FakeGitHub, load_fixture, WRITE_TOOLS

REPO = {"repository": "cip/rem-app-create"}


class FakeGitHubTests(unittest.TestCase):
    def test_scenarios_are_disjoint_and_deterministic(self):
        new = FakeGitHub(load_fixture("new-toolkit-problem"))
        fixed = FakeGitHub(load_fixture("fixed-on-develop"))
        app = FakeGitHub(load_fixture("app-only"))
        self.assertEqual(new.call("search_issues", {**REPO, "state": "open"})["issues"], [])
        self.assertNotEqual(fixed.call("get_branch", {**REPO, "ref": "main"})["branch"],
                            fixed.call("get_branch", {**REPO, "ref": "develop"})["branch"])
        self.assertEqual(app.call("search_issues", {**REPO, "state": "closed"})["issues"], [])
        self.assertEqual(new.call("get_branch", {**REPO, "ref": "main"}),
                         new.call("get_branch", {**REPO, "ref": "main"}))

    def test_every_mutation_blocked_and_recorded(self):
        gateway = FakeGitHub(load_fixture("private-log"))
        for tool in sorted(WRITE_TOOLS):
            result = gateway.call(tool, {**REPO, "body": "SECRET"})
            self.assertEqual(result, {"ok": False, "blocked": True, "error": "OFFLINE_WRITE_BLOCKED"})
        self.assertEqual(len(gateway.calls), len(WRITE_TOOLS))
        self.assertEqual({call["tool"] for call in gateway.calls}, WRITE_TOOLS)

    def test_unexpected_repository_and_ref_denied(self):
        gateway = FakeGitHub(load_fixture("fixed-on-develop"))
        self.assertEqual(gateway.call("get_branch", {"repository": "private/secret", "ref": "main"})["error"], "REPOSITORY_NOT_ALLOWED")
        self.assertEqual(gateway.call("get_branch", {**REPO, "ref": "feature"})["error"], "INVALID_REF")

    def test_rejects_unknown_tools_and_invalid_arguments(self):
        gateway = FakeGitHub(load_fixture("app-only"))
        with self.assertRaises(ValueError):
            gateway.call("shell", {})
        with self.assertRaises(ValueError):
            gateway.call("get_branch", "main")


if __name__ == "__main__":
    unittest.main()
