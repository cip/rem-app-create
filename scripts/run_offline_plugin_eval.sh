#!/usr/bin/env bash
# Fully network-disconnected integration test of the official benchmark plumbing.
# A stub stands in for Codex. NEVER report it as a live agent evaluation.
set -euo pipefail
cd "$(dirname "$0")/.."
command -v docker >/dev/null || { echo "Docker is required" >&2; exit 2; }
: "${OPENAI_PLUGIN_EVAL_DIR:?Set OPENAI_PLUGIN_EVAL_DIR to a reviewed openai/plugins checkout}"
test "$(git -C "$OPENAI_PLUGIN_EVAL_DIR" rev-parse HEAD)" = "0722921d5542fc593105c27bd52630babd8b8c2a" || {
  echo "Unexpected upstream plugin-eval commit" >&2; exit 2;
}
mkdir -p reports/plugin-eval-offline
docker build -q -f evals/rem-feedback/Dockerfile.offline -t rem-plugin-eval-offline:local . >/dev/null
docker run --rm --network none --cap-drop ALL --security-opt no-new-privileges \
  --user "$(id -u):$(id -g)" \
  --pids-limit 128 --memory 768m --cpus 2 \
  --read-only --tmpfs /tmp:rw,nosuid,nodev,exec,size=256m \
  --mount "type=bind,source=$(pwd),target=/src,readonly" \
  --mount "type=bind,source=$(realpath "$OPENAI_PLUGIN_EVAL_DIR"),target=/upstream,readonly" \
  --mount "type=bind,source=$(pwd)/reports/plugin-eval-offline,target=/results" \
  --workdir /work rem-plugin-eval-offline:local sh -eu -c '
    mkdir -p /tmp/workspace
    cp -r /src/scripts /src/docs /src/skills /src/evals /tmp/workspace/
    cd /tmp/workspace
    chmod 755 scripts/offline_codex_stub.py
    test -x scripts/offline_codex_stub.py
    scripts/offline_codex_stub.py --version
    python3 scripts/build_plugin_eval_benchmark.py --output /tmp/benchmark.json --workspace /tmp/workspace
    PLUGIN_EVAL_CODEX_EXECUTABLE=/tmp/workspace/scripts/offline_codex_stub.py \
      node /upstream/plugins/plugin-eval/scripts/plugin-eval.js benchmark skills/rem-feedback \
      --config /tmp/benchmark.json --result-out /results/benchmark-run.json --format json \
      --output /results/benchmark-cli.json
    python3 - <<"PY"
import json
from pathlib import Path
p = json.loads(Path("/results/benchmark-run.json").read_text())
assert len(p["scenarios"]) == 4
assert all(s["status"] == "completed" for s in p["scenarios"]), p["summary"]
for scenario in p["scenarios"]:
    source = Path(scenario["rawEventLogPath"])
    assert source.is_file() and source.stat().st_size > 0
    (Path("/results") / (scenario["id"] + ".codex.jsonl")).write_bytes(source.read_bytes())
print("OFFLINE STUB: official runner processed four synthetic scenarios (NO AGENT)")
PY
    printf "OFFLINE_STUB_ONLY=1\\nMODEL_EXECUTED=NO\\nNETWORK=DISABLED\\n" > /results/provenance.txt
  '
echo "Offline official-runner plumbing test completed; NO real Codex/LLM evaluation."
