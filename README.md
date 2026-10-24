# REM-APP-CREATE

**It's the end of app development as we know it (and I feel fine).**

Reusable agent skills for reliable Android app development, distilled from real-world engineering and testing experience. This toolkit helps agents design, test, build, diagnose, and maintain apps rather than just generate screens.

## Quick start

```sh
npx skills add cip/rem-app-create
```

Select a skill to install or inspect the `skills/` folders first. GitHub visibility is public; no repository invite is required.

## Skills

- `android-app-bootstrap`: inspect a project and select appropriate workflows.
- `android-clean-architecture`: follow Google's Android architecture guidance and maintain testable boundaries.
- `android-model-testing`: use explicit environment models, deterministic scenarios, virtual time, and independent invariants against production code.
- `android-ci-release`: trace CI verification, app IDs, versions, artifacts, and APK builds.
- `android-agent-workflow`: issue/PR lifecycle, approval gates, and verification handoff.

## Principles

- Real-world failures become reproducible regression scenarios.
- Tests prove only what they actually execute: distinguish JVM, emulator, physical-device and live-provider evidence.
- Use production logic in modeled tests; do not test a second copy of the implementation.
- Do not merge changes or initiate paid provider evaluations without explicit user approval.
- Preserve privacy and provenance when deriving generalized guidance from other repositories.

## Status

Early starter release: five instructional skills and a structural validator. Emulator templates, independent judge evaluations, and fully working sample apps remain follow-up work.

## Licensing and ownership

Licensed under **GNU GPL-3.0-only**. See `LICENSE`, `COPYRIGHT.md` and `CONTRIBUTING.md`. The copyright owner may grant separate licenses or relicense their own work. Outside contributors must explicitly grant relicensing permission before their changes are accepted. A public repository does **not** make it public domain. Already distributed GPL copies retain their licenses.

The R.E.M. reference is a playful tribute, not an endorsement or affiliation.
