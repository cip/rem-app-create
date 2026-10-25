#!/usr/bin/env python3
"""Deterministic, offline GitHub tool boundary for rem-feedback evaluations.

No network calls, subprocesses, tokens, or real GitHub client imports.
Accept a JSON request on stdin; emit JSON response on stdout.
This is a tool *stub*, not yet connected to the Codex plugin-eval runner.
"""
import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "evals" / "rem-feedback" / "fake-github"
READ_TOOLS = {"search_issues", "get_branch", "get_pull_requests"}
WRITE_TOOLS = {"create_issue", "add_issue_comment", "merge_pull_request", "update_issue"}
ALL_TOOLS = READ_TOOLS | WRITE_TOOLS


class FakeGitHub:
    def __init__(self, fixture):
        self.fixture = fixture
        self.calls = []

    def call(self, tool, arguments):
        if tool not in ALL_TOOLS:
            raise ValueError(f"Unknown tool: {tool}")
        if not isinstance(arguments, dict):
            raise ValueError("arguments must be an object")
        self.calls.append({"tool": tool, "arguments": arguments})
        if tool in WRITE_TOOLS:
            return {"ok": False, "blocked": True, "error": "OFFLINE_WRITE_BLOCKED"}
        if arguments.get("repository") != "cip/rem-app-create":
            return {"ok": False, "error": "REPOSITORY_NOT_ALLOWED"}
        if tool == "search_issues":
            state = arguments.get("state")
            if state not in ("open", "closed"):
                return {"ok": False, "error": "INVALID_STATE"}
            return {"ok": True, "issues": self.fixture["issues"][state]}
        if tool == "get_branch":
            ref = arguments.get("ref")
            if ref not in ("main", "develop"):
                return {"ok": False, "error": "INVALID_REF"}
            return {"ok": True, "branch": self.fixture["branches"][ref]}
        return {"ok": True, "pull_requests": self.fixture["pull_requests"]}


def load_fixture(name):
    if not name.replace("-", "").isalnum():
        raise ValueError("Invalid scenario name")
    path = FIXTURES / f"{name}.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    if set(data) != {"issues", "branches", "pull_requests"}:
        raise ValueError("Invalid fixture keys")
    if set(data["issues"]) != {"open", "closed"} or set(data["branches"]) != {"main", "develop"}:
        raise ValueError("Invalid fixture shape")
    return data


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--scenario", choices=("new-toolkit-problem", "fixed-on-develop", "app-only", "private-log"), required=True)
    args = parser.parse_args()
    gateway = FakeGitHub(load_fixture(args.scenario))
    for line in sys.stdin:
        try:
            request = json.loads(line)
            response = gateway.call(request["tool"], request.get("arguments", {}))
        except (KeyError, ValueError, TypeError) as exc:
            response = {"ok": False, "error": f"BAD_REQUEST: {exc}"}
        print(json.dumps(response, sort_keys=True), flush=True)


if __name__ == "__main__":
    main()
