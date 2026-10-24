# Skill testing: first iteration

## Decision: adopt official tools, add REM-specific policy checks

Prefer major-vendor evaluation frameworks instead of cloning a community runner. OpenAI's [plugin-eval](https://github.com/openai/plugins/tree/main/plugins/plugin-eval) provides static analysis and Codex benchmarks/comparison. Anthropic's [skill-creator](https://github.com/anthropics/skills/tree/main/skills/skill-creator) includes skill evaluations and benchmark workflows for supported Claude environments. These are **optional, external, provider-dependent** tools. Their functionality, installation and authentication must be verified where used.

REM needs additional domain-specific assertions for GitHub issue deduplication, develop/main inspection, permissions, merge consent, Android CI outcomes and APK evidence. The first iteration demonstrates these as deterministic **synthetic event trace** tests.

## Official OpenAI static integration

The optional, manually dispatched GitHub Actions workflow [Official skill evaluation](../.github/workflows/plugin-eval.yml) uses a pinned OpenAI plugin-eval checkout to analyze selected skills and uploads JSON reports. This is **static analysis**, not an executed agent benchmark. Setup, exact upstream commands, provenance and live-evaluation restrictions are in [PLUGIN_EVAL.md](PLUGIN_EVAL.md).

## Run locally

```sh
python3 scripts/validate_skills.py
python3 scripts/test_skill_scenarios.py
```

Both commands require only Python 3. The second reads `tests/skill_scenarios/*.json`; each fixture has a descriptive `name`, list of `events` with `type`, and an `expected` outcome of `allow` or `deny`. It checks whether modeled event sequences satisfy minimal safety policies. Negative scenarios must be rejected. A test result is not evidence that a deployed skill will follow the same instructions.

## Layers and evidence

| Layer | Current status | Claim allowed |
| --- | --- | --- |
| SKILL.md structure | Implemented | Structure accepted |
| Synthetic policy trace fixtures | Implemented | Hardcoded modeled traces match invariants |
| Official plugin-eval static scan | Manual workflow implemented; not a live benchmark | Static findings only |
| Real agent activation and execution | Not implemented | Nothing, until recorded run exists |
| Tool mocking/state machine integration | Not implemented | Nothing |
| Real GitHub / Android CI / APK E2E | Not implemented | Nothing |
| Independent LLM judge/benchmark | Available externally where installed, not wired | Nothing until executed |

## Priority regressions

- Snake bootstrap: a failed SDK installation must not produce a claim of successful CI or an available APK; a real artifact needs verification.
- Feedback: search open and closed issues, check main and develop and sanitize before publication. Existing issues should be updated rather than duplicated.
- Permissions: no public posting without authorization, no merges without explicit approval. Read-only GitHub must degrade gracefully.

## Follow-up plan

1. Replace or augment synthetic trace fixtures with **captured real tool traces** through official OpenAI/Anthropic agent evaluation runners where supported. Add adapters that translate tool events into a canonical event schema; pin model/skill/commit.
2. Add a mock GitHub/Android service state machine and assert actual tool transition order and effects, not just presence of labels.
3. Run positive/negative skill-activation prompts and paraphrases repeatedly; compare with no-skill baseline. Save prompts and evidence, never report unexecuted tests as passed.
4. Add independent rubric-based LLM judge with hard gates, cost/latency and trace links.
5. Use disposable repositories and a minimal Android reference app for real E2E tests; occasional fresh-account acceptance testing remains issue #6.

## Boundaries

Do not import third-party code or external dependencies into default CI, run model benchmarks without approval, open real GitHub issues in tests, or apply this repository's branch policies automatically to generated apps. A tester skill does not self-certify: separate deterministic assertions and external evaluation runs must assess its behavior.

Tracking: #7 (v1 and extension plan), #6 (broader acceptance test program), #3 (field failures).
