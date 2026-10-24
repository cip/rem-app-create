# Offline fake GitHub boundary (issue #9)

This is a deliberately tiny deterministic tool adapter for skill evaluation fixtures, **not** a complete GitHub emulator and **not yet a Codex plugin-eval integration**. The actual Codex model is not invoked, no tool trace is collected from an agent, and passing tests never proves correct skill behavior.

## Run

```sh
python3 scripts/test_fake_github.py
echo '{"tool":"search_issues","arguments":{"repository":"cip/rem-app-create","state":"closed"}}' | python3 scripts/fake_github.py --scenario fixed-on-develop
```

The adapter accepts one JSON request per line on stdin and returns one JSON response per line. Supported reads: `search_issues` (state open/closed), `get_branch` (main/develop), `get_pull_requests`. Writes (`create_issue`, `update_issue`, `add_issue_comment`, `merge_pull_request`) are always blocked and recorded by the in-process adapter. Unknown tools and repositories are rejected. The CLI prints responses but does not export the call history across process invocations; tests inspect `FakeGitHub.calls` directly. All data is invented local fixture data.

**Security:** Because this is a local script, it cannot prevent an unrestricted agent from bypassing it using internet, shell, GitHub connector, or credentials. Before connecting it to real Codex benchmarks, run Codex in an isolated workspace with *no network or credentials*, expose only this boundary, and assert actual tool call order and mutation attempts independently. Never point an unsandboxed agent at it and claim mutations are blocked.

## Remaining implementation

- Adapt the pinned official plugin-eval benchmark's actual tool interface to this JSON-lines contract; verify how tool definitions and session traces are injected before writing integration.
- Capture full per-case agent tool traces and enforce deduplication checks, main/develop inspection, consent and redaction checks on observable traces/outcome.
- Only then enable explicit, authorized live Codex runs; record the model, costs, provider status and failures honestly.

The normal PR CI runs **only** this offline adapter's contract tests. See `docs/PLUGIN_EVAL_SMOKE.md`.

## Codex JSONL trace gate

`scripts/verify_codex_trace.py` now inspects actual recorded `codex exec --json` streams **after** a benchmark (it does not launch one):

```sh
python3 scripts/verify_codex_trace.py /path/to/codex.stdout.jsonl --scenario already-fixed --output /tmp/trace-gate.json
```

It fails closed if no completed turn, no observed invocation of the correct fake scenario, a recognized external GitHub/network/mutation command, or an unrecognized external tool call is observed. `python3 scripts/test_codex_trace.py` exercises the checker against fabricated Codex event shapes in normal CI.

**Important limitations:** This is a minimum-evidence diagnostic, **not a security boundary or a PASS on agent policy compliance**. Regex inspection can miss escaped, indirect, or unrecognized network operations; Codex events may evolve; observing the adapter command does not prove correct tool sequencing, deduplication, redaction or decisions. The runner still needs independently enforced network isolation and a restricted tool surface before *any* live benchmark. Never interpret `OBSERVED_MINIMUM` as a safety certificate.
