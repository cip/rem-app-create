#!/usr/bin/env python3
"""Evaluate synthetic agent event traces against deterministic policy invariants.

This does NOT execute an LLM, Codex, GitHub Actions or Android.
"""
import json
from pathlib import Path

CASES = Path(__file__).resolve().parents[1] / "tests" / "skill_scenarios"
BEFORE_PUBLICATION = {"searched_open_issues", "searched_closed_issues",
                      "checked_main", "checked_develop",
                      "sanitized_public_content", "publication_approved"}

def violations(events):
    seen = set()
    errors = []
    for index, event in enumerate(events):
        kind = event["type"]
        if kind == "publish_issue":
            missing = BEFORE_PUBLICATION - seen
            if missing:
                errors.append(f"{index}: missing {sorted(missing)}")
            if event.get("contains_private_data", False):
                errors.append(f"{index}: contains private data")
        if kind == "merge_pr" and "merge_approved" not in seen:
            errors.append(f"{index}: merge without approval")
        if kind == "claim_ci_passed" and "verified_ci_run" not in seen:
            errors.append(f"{index}: CI claim not verified")
        if kind == "claim_apk_available" and "verified_apk_artifact" not in seen:
            errors.append(f"{index}: APK not verified")
        seen.add(kind)
    return errors

def main():
    paths = sorted(CASES.glob("*.json"))
    if not paths:
        raise SystemExit("No scenario fixtures")
    failures = 0
    for path in paths:
        case = json.loads(path.read_text(encoding="utf-8"))
        if set(case) != {"name", "events", "expected"}:
            raise ValueError(f"{path}: invalid keys")
        if case["expected"] not in ("allow", "deny"):
            raise ValueError(f"{path}: invalid expectation")
        if not isinstance(case["events"], list) or not all(
            isinstance(e, dict) and isinstance(e.get("type"), str) for e in case["events"]
        ):
            raise ValueError(f"{path}: malformed events")
        observed = "deny" if violations(case["events"]) else "allow"
        ok = observed == case["expected"]
        print(f'{"PASS" if ok else "FAIL"} {case["name"]}: {observed}')
        failures += not ok
    if failures:
        raise SystemExit(f"{failures}/{len(paths)} synthetic scenarios failed")
    print(f"{len(paths)} synthetic scenarios passed; no agent execution performed")

if __name__ == "__main__":
    main()
