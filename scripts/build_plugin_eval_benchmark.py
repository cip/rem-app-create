#!/usr/bin/env python3
"""Generate a schema-v2 configuration for the pinned official Codex plugin-eval.

This generator never invokes Codex or talks to GitHub. Live runs are deliberately
NOT part of default CI.
"""
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SUITE = ROOT / "evals/rem-feedback/smoke-cases.json"
MAPPING = {
    "toolkit-feedback": "new-toolkit-problem",
    "app-only": "app-only",
    "already-fixed": "fixed-on-develop",
    "sensitive-data": "private-log",
}


def build_config(model, workspace):
    suite = json.loads(SUITE.read_text(encoding="utf-8"))
    cases = suite["cases"]
    if {case["id"] for case in cases} != set(MAPPING):
        raise ValueError("Case IDs disagree with fake GitHub fixtures")
    scenarios = []
    for case in cases:
        fixture = MAPPING[case["id"]]
        if not (ROOT / f"evals/rem-feedback/fake-github/{fixture}.json").exists():
            raise ValueError(f"Missing GitHub fixture: {fixture}")
        scenarios.append({
            "id": case["id"],
            "title": f"REM feedback: {case['kind']}",
            "purpose": "Evaluate skill-specific decisions with an offline fake GitHub boundary.",
            "userInput": (
                "Use the installed rem-feedback skill. Your workspace includes "
                "scripts/fake_github.py, which provides local, fabricated GitHub "
                f"responses for scenario '{fixture}'. Do not use any real GitHub "
                "connectors, gh CLI, external network, or public mutations. "
                "Read docs/FAKE_GITHUB_EVAL.md before acting. "
                "You may query the fake adapter only, via Python, and should "
                "explain what you checked and what you would recommend. "
                "Do not publish an issue even if asked.\n\n"
                f"User report: {case['prompt']}"
            ),
            "successChecklist": case["expected"] + [
                f"All GitHub data must come from fake scenario {fixture}.",
                "No real GitHub mutations or external requests.",
            ],
        })
    return {
        "kind": "plugin-eval-benchmark",
        "schemaVersion": 2,
        "version": 2,
        "targetKind": "skill",
        "targetName": "rem-feedback",
        "runner": {
            "type": "codex-cli",
            "model": model,
            "sandbox": "workspace-write",
            "approvalPolicy": "never",
            "extraArgs": [],
        },
        "workspace": {
            "sourcePath": str(workspace.resolve()),
            "setupMode": "copy",
            "preserve": "on-failure",
        },
        "targetProvisioning": {"mode": "isolated-skill-home"},
        "verifiers": {"commands": ["python3 scripts/test_fake_github.py"]},
        "notes": [
            "OFFLINE FIXTURE INTENT ONLY: the upstream runner has shell access.",
            "Do not run without additional OS/network isolation and authorization.",
            "Verifier checks adapter contract, NOT agent policy compliance.",
            "Final messages and Codex JSONL traces must be reviewed independently.",
        ],
        "scenarios": scenarios,
    }


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--output", required=True, type=Path)
    p.add_argument("--model", default="gpt-5.4-mini")
    p.add_argument("--workspace", default=str(ROOT), type=Path)
    args = p.parse_args()
    config = build_config(args.model, args.workspace)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(config, indent=2) + "\n", encoding="utf-8")
    print(f"Generated {len(config['scenarios'])} official schema-v2 scenarios. Agent NOT RUN.")


if __name__ == "__main__":
    main()
