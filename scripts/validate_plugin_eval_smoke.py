#!/usr/bin/env python3
"""Check the checked-in smoke case contract; DOES NOT execute an agent."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
path = ROOT / "evals/rem-feedback/smoke-cases.json"
suite = json.loads(path.read_text(encoding="utf-8"))
assert suite["schema_version"] == 1
assert suite["skill"] == "rem-feedback"
assert (ROOT / "skills" / suite["skill"] / "SKILL.md").is_file()
cases = suite["cases"]
assert len(cases) >= 4
assert len({case["id"] for case in cases}) == len(cases)
assert {"activation", "negative", "duplicate", "safety"} <= {case["kind"] for case in cases}
for case in cases:
    assert case["prompt"].strip(), case
    assert case["expected"] and case["forbidden"], case
    assert all(isinstance(item, str) and item.strip() for item in case["expected"] + case["forbidden"])
print(f"PASS: validated {len(cases)} smoke case specifications (agent execution NOT RUN)")
