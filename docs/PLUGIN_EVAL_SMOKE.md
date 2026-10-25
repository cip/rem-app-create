# Official plugin-eval benchmark configuration (issue #9)

The pinned official OpenAI plugin-eval revision `0722921d5542fc593105c27bd52630babd8b8c2a` uses **benchmark schemaVersion 2**, `runner.type=codex-cli`, and actual `codex exec` sessions. Its `benchmark --dry-run` **raises an error**; the earlier documentation suggesting this flag was incorrect.

## Implemented

Generate a deterministic config from four `rem-feedback` smoke cases and fake-GitHub fixtures:

```sh
python3 scripts/validate_plugin_eval_smoke.py
python3 scripts/test_fake_github.py
python3 scripts/test_plugin_eval_config.py
python3 scripts/build_plugin_eval_benchmark.py --output /tmp/rem-feedback-benchmark.json --model gpt-5.4-mini
```

The config has the official `plugin-eval-benchmark` kind, schema 2, a `codex-cli` runner, four prompts, an isolated skill installation, workspace copy, and a Python adapter contract verifier. This is a genuine input **configuration** for the official runner, not a competing runner. The new PR validation tests config structure without invoking Codex. The opt-in smoke workflow produces a configuration artifact and official static analysis rather than an unsupported fake dry run.

## Security and evidence limits

**Do not run the live command on an unisolated machine or with production GitHub credentials.** The upstream benchmark grants the Codex agent shell execution in a workspace, uses a copied Codex auth configuration when present, and may make network calls unless separately restricted. Prompt instructions saying to use fake GitHub are **not** a security boundary. The JSON-lines fake adapter currently is a callable *local process*, not an injected GitHub connector. Its contract tests cannot prove the agent used it, and the official runner's verifier currently checks only that the adapter itself passes. No actual GitHub agent tool trace policy gate exists yet.

Only after an external network-restricted environment is provisioned, credentials are limited to model access, the agent's real tool traces can be independently checked, and explicit API spending approval is given should you run:

```sh
node /path/to/openai/plugins/plugins/plugin-eval/scripts/plugin-eval.js benchmark skills/rem-feedback --config /tmp/rem-feedback-benchmark.json --format json
```

Note: `workspace.sourcePath` is an absolute path written at generation time. Rebuild config on the same host where running it. This command performs real (potentially paid) model calls, unlike the config generation and static PR tests. This repository **does not automate** that live step.

## Next required slice

Expose fake-GitHub through an agent-restricted tool interface, capture the actual Codex JSONL tool traces, apply strict per-scenario decision/postcondition verifiers, add no-network enforcement and appropriate spending controls. Then enable an explicit manual live test and record token use and observed cost. Until then report `AGENT NOT RUN`, not PASS.
