# Plugin-eval smoke preflight (issue #9)

The official [OpenAI plugin-eval](https://github.com/openai/plugins/tree/main/plugins/plugin-eval) can run live Codex benchmarks, but **this first slice is explicitly a dry-run preflight**. It never invokes a model, does not require credentials, makes no paid API requests, and must not be reported as a real behavior evaluation.

## Manual run

From GitHub Actions select **Official plugin-eval smoke preflight**, choose `rem-feedback`, and optionally enter the **intended** model for provenance. This field does not configure or invoke Codex. No workflow runs on ordinary pull requests. Permissions are `contents: read` only.

The workflow pins official upstream commit `0722921d5542fc593105c27bd52630babd8b8c2a`, uses Node.js 22, validates the checked-in case specification, calls the official `init-benchmark` and `benchmark --dry-run` commands, and uploads generated benchmark starter configuration, dry-run output and provenance. The generated benchmark configuration is **not** equivalent to our test case specification. Review it before use.

Locally validate the four REM-specific proposed prompts with:

```sh
python3 scripts/validate_plugin_eval_smoke.py
```

The case JSON defines activation, near-miss/app-only, duplicate/develop-fix and sensitive-data safety expectations. Validation verifies schema shape only. It does **not** prove agent activation, actual tool calls or outcomes.

## Evidence and non-goals

Record `NOT RUN` for live agent behavior, tool traces, GitHub postconditions and observed costs. The dry-run artifact records the toolkit commit, pinned evaluator commit, declared skill and intended model. It must not be used as a passing agent evaluation.

## Next slices before a real live benchmark

1. Convert the four cases into the official generated benchmark config, after inspecting its actual schema at the pinned revision. Pin prompts, model, reasoning settings and target revision.
2. Provide a fake GitHub tool layer with fixed issue search results, main/develop commits and mutation traps. Assert *observable* tool traces and final state. Forbid network/public mutations; `contents: read` GitHub Actions permissions alone cannot prevent external calls using other credentials.
3. Run `codex exec` only in a reviewed sandbox with explicit spending authorization and securely provisioned credentials, never from normal PR validation. Store outcomes, token usage and costs if reported (otherwise `UNKNOWN`).
4. Compare with/without skill and paraphrases, then calibrate optional judge scoring against deterministic assertions.

Existing automatic static analysis remains in `.github/workflows/plugin-eval.yml`; existing synthetic trace checks are separate. This deliberately small step does not claim to complete issue #9's full live evaluation goal.
