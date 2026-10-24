# REM-APP-CREATE

**It's the end of app development as we know it (and I feel fine).**

**Build Android apps with AI agents — using reusable skills for architecture, model-based testing, CI, APK delivery and disciplined GitHub workflows.**

REM-APP-CREATE is an open-source collection of **Agent Skills**, not an Android app or a one-click app generator. It gives supported coding agents repeatable engineering practices learned from real-world Android projects.

## Start directly in ChatGPT (no IDE required)

**The simplest way:** paste this URL into a ChatGPT conversation:

```text
https://github.com/cip/rem-app-create
```

You can also paste the link **with an app idea**, such as:

> Use https://github.com/cip/rem-app-create to help me build an Android app that shares family photos using Nextcloud without moving or deleting the original images.

**Just the link?** Start by explaining what the toolkit can do, offering example Android app ideas, and asking what the user wants to create. **Link plus an app idea?** Start with a small feature plan and a step-by-step GitHub account/repository setup (including Public versus Private), then use the appropriate skills.

**[ChatGPT start-here instructions and GitHub setup →](CHATGPT_START_HERE.md)**

Reading a public GitHub URL is **not** the same as installing executable skills, connecting GitHub for write access, or provisioning an Android build system. Agents must be candid about which tools they can actually access. No IDE is needed to discuss or plan an app; GitHub Actions can build APKs once configured.

## What can I do with it?

Imagine building a **family photo-sharing Android app**. A person picks photos in the Android Gallery and shares them to the app. The app publishes a shareable collection backed by Nextcloud **without ever moving or deleting the originals**.

Ask your coding agent:

> **Example prompt**
>
> Build an Android app that receives photos from Android's Share Sheet and prepares a shareable Nextcloud collection. Use the REM-APP-CREATE skills. Start with an architecture proposal and a minimal implementation plan. Model Nextcloud success, network failures, duplicate callbacks, cancellations and Android lifecycle changes. Add reproducible tests proving that original photos are never moved or deleted. Then implement the first vertical slice, run the available checks and show me the APK build workflow. Open a PR; don't merge without my approval.

The agent should use the skills to:

1. **Plan** a small Android feature with clear boundaries and user-visible safety invariants.
2. **Implement** production logic behind testable ports/adapters, using Kotlin and Android-recommended architecture.
3. **Test** external-system variants with deterministic event sequences, virtual time and independent assertions against production logic.
4. **Verify** JVM tests separately from actual emulator/device tests; clearly report anything not executed.
5. **Deliver** a reviewable PR and traceable Android CI/APK handoff without automatically merging.

**Reality check:** These are instructions for an AI coding agent, not a guarantee that one prompt produces a finished app. The agent needs access to the target project and its build environment. Existing skills provide guidance; complete Android templates, sample apps and emulator pipelines are still being developed.

## Optional: install skills in a coding agent

### Option A — Install from this public GitHub repository

From a terminal with Node.js/npm available:

```sh
npx skills add cip/rem-app-create
```

Follow the installer's prompts to select your supported agent and skills. For a targeted install, use:

```sh
npx skills add cip/rem-app-create --skill android-model-testing
```

You **do not need a GitHub invitation or access token to read this public repository**. The installer and your coding agent are separate tools. GitHub credentials may still be required to push code or create PRs in your **own** target repository.

### Option B — Use the skills directly

Browse [skills/](skills/), open the relevant `SKILL.md`, and copy or reference it using the documented custom-skill mechanism of your coding agent. For agents supporting the Agent Skills standard, keep the individual `SKILL.md` directories intact.

## Set up a real Android project on GitHub (CLI-based alternative)

1. Create or open your **Android application repository** (separate from this skills repository).
2. Clone that Android repository locally and open it in your preferred agent-enabled development environment.
3. Install the REM-APP-CREATE skills **for that project or agent** as above.
4. Give your agent the example prompt, adjusted to your use case. Ask it to inspect `README.md`, `AGENTS.md`, Gradle files and existing GitHub Actions before proposing changes.
5. Ensure the agent has the needed local tools (typically JDK, Android SDK, Gradle and optionally an emulator). Installation of skills does **not** install the Android toolchain.
6. To let the agent **push code, open PRs or trigger workflows**, authenticate GitHub in that environment (e.g. `gh auth login` or your agent's GitHub connector) with appropriate repository permissions. For **reading and installing these public skills**, none of that is needed.
7. Review proposed changes and run tests. Inspect the exact source commit, test evidence, build status and APK before installation. Approve merges explicitly.

**Minimal first request for an existing app:**

> Inspect this Android repository using the REM-APP-CREATE bootstrap, architecture and model-testing skills. Don't modify anything yet. Explain the smallest safe improvement, the tests to add, and what GitHub/Android setup is missing.

## Available skills

| Skill | Purpose |
| --- | --- |
| [android-app-bootstrap](skills/android-app-bootstrap/SKILL.md) | Audit a new or existing app and select appropriate workflows. |
| [android-clean-architecture](skills/android-clean-architecture/SKILL.md) | Keep Kotlin/Compose features and provider boundaries testable. |
| [android-model-testing](skills/android-model-testing/SKILL.md) | Reproduce state/event sequences, timing, failures and invariants. |
| [android-ci-release](skills/android-ci-release/SKILL.md) | Trace CI evidence, app IDs, signing, versions and installable APKs. |
| [android-agent-workflow](skills/android-agent-workflow/SKILL.md) | Structure issue → branch → tests → PR → review → merge approval. |
| [rem-feedback](skills/rem-feedback/SKILL.md) | Turn user complaints into privacy-safe, deduplicated toolkit issues with consent. |

### Report a problem with the skills

If an app built using REM-APP-CREATE fails, or the guidance is confusing, tell your ChatGPT agent what happened and ask it to **use the [rem-feedback](skills/rem-feedback/SKILL.md) skill**. It will distinguish app-specific issues from reusable toolkit problems, check for duplicates, sanitize information for a **public** issue, and—after your approval and if GitHub write access is available—create an issue in [this repository](https://github.com/cip/rem-app-create/issues). Otherwise, it can prepare a report for the [new issue form](https://github.com/cip/rem-app-create/issues/new). No IDE required to report a problem.

## Principles

- Learn from actual incidents and turn them into **reproducible regression tests**.
- Exercise the **real production code**, not a second implementation inside fixtures.
- Treat JVM, compiled-only instrumentation, executed emulator, physical device and paid/live-provider checks as different levels of evidence.
- Keep actions reversible where possible and protect user data with explicit invariants.
- Never merge pull requests or start paid provider evaluations without explicit user approval.
- Generalize engineering practices without copying sensitive or incompatibly licensed project contents.

## Project status and validation

This is an **early starter release** with six instructional skills and a structural validator. Validation runs on GitHub Actions in [Validate skills](.github/workflows/validate-skills.yml), and can be run locally:

```sh
python3 scripts/validate_skills.py
```

That validates skill structure, **not** whether a coding agent actually builds a working Android app. End-to-end example projects, emulator/CI templates and agent evaluations remain to be added.

## Licensing and ownership

Licensed under **GNU GPL-3.0-only**. See [LICENSE](LICENSE), [COPYRIGHT.md](COPYRIGHT.md) and [CONTRIBUTING.md](CONTRIBUTING.md). The copyright owner can grant other licenses or relicense their own material; outside contributors must explicitly grant appropriate relicensing rights first. Copies already distributed under GPL keep those rights.

The R.E.M. reference is a playful tribute, not an endorsement or affiliation.
