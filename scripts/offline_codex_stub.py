#!/usr/bin/env python3
"""Test double for the official plugin-eval runner. NEVER an AI agent."""
import json
import re
import subprocess
import sys
from pathlib import Path

if "--version" in sys.argv:
    print("codex-offline-stub 1.0 (NOT REAL CODEX)")
    raise SystemExit(0)
args = sys.argv[1:]
if not args or args[0] != "exec":
    raise SystemExit("Only codex exec is supported")
try:
    message_path = Path(args[args.index("--output-last-message") + 1])
    workspace = Path(args[args.index("--cd") + 1])
except (ValueError, IndexError):
    raise SystemExit("Missing official CLI arguments")
prompt = args[-1]
match = re.search(r"scenario '([a-z-]+)'", prompt)
if not match:
    raise SystemExit("No fake scenario in benchmark prompt")
scenario = match.group(1)
cmd = ["python3", "scripts/fake_github.py", "--scenario", scenario]
payload = json.dumps({"tool":"search_issues","arguments":{"repository":"cip/rem-app-create","state":"open"}}) + "\n"
run = subprocess.run(cmd, input=payload, cwd=workspace, text=True, capture_output=True, check=True)
response = json.loads(run.stdout)
assert response["ok"] is True, response
message_path.parent.mkdir(parents=True, exist_ok=True)
message_path.write_text("OFFLINE STUB ONLY: fake GitHub contract exercised; no AI model.\n", encoding="utf-8")
print(json.dumps({"type":"thread.started","thread_id":"stub-only"}))
print(json.dumps({"type":"item.completed","item":{"type":"command_execution","command":"python3 scripts/fake_github.py --scenario " + scenario,"exit_code":0}}))
print(json.dumps({"type":"turn.completed","usage":{"input_tokens":0,"output_tokens":0,"total_tokens":0}}))
