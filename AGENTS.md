# Agent instructions

This is a reusable public Android engineering skills toolkit, not a standalone Android app. Technical documentation and skills are in English.

1. Keep skills independently installable in `skills/<name>/SKILL.md`, with valid name/description frontmatter and actionable instructions.
2. Generalize methods from Roadtrip Tunes: do not copy project-specific secrets, licensed third-party sources, logs or personal information.
3. Follow Android recommended architecture, clear boundaries, and testable injected adapters; prefer deterministic production-code model scenarios with independent invariants.
4. Distinguish JVM tests, compiled-only instrumentation, executed emulator, device and live-provider evidence. Never claim unexecuted checks passed.
5. Preserve repro traces and recorded variant profiles, and turn incidents into failing regression tests before fixes.
6. Identify branch, commit, versionCode/versionName, test status and artifact when handing off an APK.
7. Never merge PRs or run paid evaluations without explicit user authorization.
8. Run `python3 scripts/validate_skills.py` after editing skills.
9. Licensing: GPL-3.0-only. Only accept outside copyrighted contributions after explicit relicensing permissions have been arranged; see `CONTRIBUTING.md` and `COPYRIGHT.md`. Do not change the repository license or add third-party material without verifying rights.
