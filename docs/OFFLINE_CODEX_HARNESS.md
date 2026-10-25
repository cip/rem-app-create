# Network-disabled plugin-eval runner integration test

Issue #9 now includes a **Docker-based offline plumbing test** of the pinned official OpenAI plugin-eval Codex benchmark path. It invokes the actual upstream `benchmark` command with a **fake executable replacing Codex**, so it cannot evaluate skill behavior, make any model/API calls, or incur model charges.

## Use locally

Requirements: Docker, Git, Bash and a manually reviewed checkout of `openai/plugins` at commit `0722921d5542fc593105c27bd52630babd8b8c2a`. No authentication secrets are needed.

```sh
git clone https://github.com/openai/plugins.git /tmp/rem-plugins
git -C /tmp/rem-plugins checkout 0722921d5542fc593105c27bd52630babd8b8c2a
OPENAI_PLUGIN_EVAL_DIR=/tmp/rem-plugins bash scripts/run_offline_plugin_eval.sh
```

The script builds `evals/rem-feedback/Dockerfile.offline`, validates upstream revision, and runs a container with `--network none`, a read-only root filesystem, no added capabilities, a PID/memory/CPU limit, and a temporary scratch filesystem. The repo and upstream are mounted read-only. Only `reports/plugin-eval-offline` is a writable bind mount. The runner gets a fresh scratch workspace and an **offline stub** at `PLUGIN_EVAL_CODEX_EXECUTABLE`. The stub itself calls `scripts/fake_github.py` and emits synthetic Codex JSONL events. The upstream benchmark config is generated using the real schema v2.

Expected result: four upstream scenario records and four synthetic JSONL event files under `reports/plugin-eval-offline`, plus provenance. This verifies that the upstream runner, workspace preparation, verifier, fake CLI, and artifacts can communicate through the real interface.

## Security and remaining work

**This does not launch a real Codex agent.** In particular, no model reasoning, autonomous tool choice, actual agent policy adherence or fake GitHub tool routing is assessed. Output files and zero token usage are **stub artifacts**, not real agent measurements. The container network restriction is suitable for the stub, but **blocks a real Codex model connection**. Do not weaken network isolation or inject GitHub credentials simply to run real Codex. A safe real-agent environment still requires a narrowly scoped model-network egress proxy or equivalent enforced separation, model credentials with spending limits, verified tool controls, and a strict, independently audited policy verifier.

The test is intentionally **manual**, not a mandatory PR job: Docker availability and building images are environment-dependent. CI continues to run deterministic validations. Do not call a successful offline stub run an end-to-end agent PASS.
