---
name: skill-tester
description: Plan and evaluate Agent Skill tests using official OpenAI or Anthropic evaluation tools and REM-specific deterministic workflow policies.
---
# Skill tester

Use when creating, revising or debugging an Agent Skill. Keep REM-APP-CREATE toolkit development separate from the development process of Android apps that use the toolkit.

## Prefer official evaluation tools

- For Codex environments, prefer OpenAI's official [plugin-eval](https://github.com/openai/plugins/tree/main/plugins/plugin-eval): `analyze` for static review, `init-benchmark` and `benchmark` for real Codex runs, `compare` for before/after comparisons. The pull-request-triggered (or manually dispatched) `Official skill evaluation` workflow performs pinned, **static** `analyze` runs without credentials; see `docs/PLUGIN_EVAL.md`. The CLI remains external; live `benchmark` is not enabled in CI.
- When using Claude, Anthropic's official [skill-creator](https://github.com/anthropics/skills/tree/main/skills/skill-creator) supports skill evaluations and benchmarks.
- Do not adopt arbitrary community GitHub harnesses without explicit review. Vendor tools may be unavailable or platform-specific. Do not silently substitute static checks for agent evaluations.

## Procedure

1. Pin skill version (branch and commit), model/provider and available tools; distinguish activation, workflow, outcome, negative and safety scenarios.
2. Define test prompts and expected observable tool calls, forbidden actions, final state and evidence. Include paraphrases, near-miss prompts, missing permissions and upstream failure cases.
3. Run `python3 scripts/validate_skills.py` and `python3 scripts/test_skill_scenarios.py`. The latter evaluates **synthetic traces**, not actual agent runs.
4. If an official evaluation runner is available and authorized, execute the skill in an isolated workspace. Capture inputs, versions, tool traces, outputs, failures, costs and comparison baseline. Do not run live or paid evaluations without permission.
5. Independently verify postconditions: issue/PR state and target branch, real CI run, APK artifact existence, consent and private-data safeguards. An LLM judge can supplement but never replace hard assertions.
6. Report PASS, FAIL, or NOT RUN separately for structural tests, synthetic trace tests, real agent evaluations and live integration. Turn real failures into durable scenarios.

## Critical invariant examples

- Before publishing toolkit feedback, search open and closed issues, inspect relevant changes on main and develop, sanitize private information, and obtain authorization unless already explicitly requested.
- Never merge without explicit approval. Do not project toolkit branch rules onto downstream app repositories.
- Never claim green CI or an installable APK without verifying the exact run and artifact.

## Limitations and roadmap

V1 is a thin orchestration skill plus small dependency-free deterministic trace-policy examples. It is not an automatic agent runner, LLM judge or end-to-end integration test. See `docs/SKILL_TESTING.md` and issue #7.
