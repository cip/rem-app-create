# Official OpenAI plugin-eval integration

This integration uses **OpenAI's own source**, not a copied or community-maintained evaluation engine: [openai/plugins / plugin-eval](https://github.com/openai/plugins/tree/main/plugins/plugin-eval).

## Verified upstream interface

At upstream revision `0722921d5542fc593105c27bd52630babd8b8c2a`, `plugins/plugin-eval/README.md` specifies Node.js >=20 and the local entry point `scripts/plugin-eval.js`. The package is private to the monorepo, so **do not use `npx plugin-eval` or assume an npm-published package**.

- `analyze <skill-path> --format json --output <file>`: static local inspection, no model call.
- `init-benchmark <skill-path>`: generates an editable local benchmark configuration.
- `benchmark <skill-path> --config <file>`: executes real Codex CLI sessions and saves run artifacts.
- `report` and `compare`: render and compare saved evaluation outputs.

The checked-in workflow [Official skill evaluation](../.github/workflows/plugin-eval.yml) is **manual** (`workflow_dispatch`) and intentionally performs **only static analysis**. It has no GitHub write permissions and uses a pinned upstream commit. GitHub Actions artifact `official-plugin-eval-static` contains the JSON files and provenance.

## Run the official CLI locally

```sh
git clone https://github.com/openai/plugins.git /tmp/rem-openai-plugins
git -C /tmp/rem-openai-plugins checkout 0722921d5542fc593105c27bd52630babd8b8c2a
node /tmp/rem-openai-plugins/plugins/plugin-eval/scripts/plugin-eval.js analyze skills/rem-feedback --format markdown
```

Node.js >=20 required. Do not blindly execute a new upstream commit: review upstream changes before updating the pin.

## Live Codex agent benchmark: deliberate next step

The CLI supports real `codex exec` evaluations, but **this workflow does not run them**. To run locally in a controlled, user-authorized environment:

```sh
CLI=/tmp/rem-openai-plugins/plugins/plugin-eval/scripts/plugin-eval.js
node "$CLI" init-benchmark skills/rem-feedback
# Review/edit the generated .plugin-eval/benchmark.json and isolate any tools.
# Ensure Codex CLI authentication and spending authorization before continuing.
node "$CLI" benchmark skills/rem-feedback --format markdown
```

The generated benchmark is a **starter**, not a ready-to-run safety regression. Real tests of feedback should use disposable/mocked GitHub tooling with no public write access and require scenario-specific verifiers. No live benchmark is executed in normal CI; this workflow never requires API secrets.

## Evidence levels and follow-up

1. Existing `validate-skills.yml`: structure and synthetic trace policy tests.
2. New manually triggered `plugin-eval.yml`: official **static** skill analysis, machine-readable artifacts and pinned provenance.
3. **Not implemented:** reproducible live Codex smoke benchmark, controlled fake GitHub tools, deterministic trace assertions on actual tool activity, before/after comparisons, LLM judge or cost metrics. Track this in issue #9.

An official static report is **not proof that an agent activated a skill or obeyed the instructions**. Treat CI failure and warnings accurately; do not present a static scan as an E2E result.
