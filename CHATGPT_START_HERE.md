# Use REM-APP-CREATE directly from ChatGPT

This repository is **chat-first**. A user should be able to paste its public GitHub URL into ChatGPT without installing an IDE, Node.js or the skills CLI. Reading the URL is an entry point for guidance, **not** automatic execution of installed skills or a grant of repository write permissions.

## Suggested starter message

```text
Read https://github.com/cip/rem-app-create, especially CHATGPT_START_HERE.md and the relevant skills. Help me create an Android app following its workflow. If I haven't given an app idea, show examples and ask what I want to build. If I have, guide me through creating the target GitHub repository and proceed with an architecture and testing plan. Explain any tooling or permissions actually needed; never claim you executed a skill, built an APK or changed GitHub unless you did.
```

## Scenario A: User pastes only the link

Start with a short explanation:

> REM-APP-CREATE helps AI coding agents design, implement, model-test, build and release Android apps. For example, you could make a family photo-sharing app using Android's Share Sheet and Nextcloud, a voice-driven multiplayer quiz game, or a travel companion. What app would you like to create?

Do not assume the user has an Android project, access tokens, or a development environment. Offer to explore requirements and a first implementation slice from chat. Explain that full builds require an Android-capable execution environment; chat and linked GitHub do not guarantee one.

## Scenario B: User includes an app idea

1. Restate the goal, identify safety/data-retention invariants, identify platform interfaces, and propose a very small first working vertical slice. Ask only for truly blocking missing details.
2. Give the user a **GitHub repository setup walkthrough**, unless a target repo already exists:
   - Sign in or create a free account at https://github.com/signup.
   - Open https://github.com/new.
   - Enter a concise repository name, such as `family-photo-share` (this is the **app repo**, separate from `cip/rem-app-create`).
   - Pick visibility deliberately:
     - **Public**: anybody can read the source and public build logs; easiest for sharing and for assistants to inspect without access grants. Never publish credentials, user photo contents, real personal logs, or private business data. Standard GitHub-hosted Actions runners are generally free on public repositories, subject to GitHub's current policies and limitations.
     - **Private**: only authorized people and connected tools can access it; better for unreleased or sensitive projects. Free accounts can create private repos, but GitHub-hosted Actions minutes/storage are quota-limited and may incur charges if exceeded. Agent tools must receive access explicitly.
     - **Internal** is an enterprise-only visibility option for eligible organizations, **not** a normal alternative on a personal free account.
   - Initialize with README, choose a suitable license deliberately (or no license until decided), and create the repository.
   - Ask for the new repository URL to continue. Do not ask for passwords or personal access tokens in chat.
3. Inspect the actual project via an authorized GitHub connector/tool if available, or guide the user through providing files. Public read access does not imply write access.
4. Explain whether you can write code/branches/PRs in the current ChatGPT environment. If a required capability is unavailable, be transparent and offer a patch or instructions, rather than pretending a full app was built.
5. Use these skills as guidance: `android-app-bootstrap`, `android-clean-architecture`, `android-model-testing`, `android-ci-release`, `android-agent-workflow`. Propose an issue → short branch → tested code → PR → CI → review sequence. Do not merge without approval or initiate paid checks without permission.
6. Once a build exists, report exact commit/ref, variant, versionCode, versionName, executed checks and the correct APK link. Mark unexecuted emulator tests clearly.

## What the user needs and does *not* need

- **For a discussion or plan:** no IDE, CLI, GitHub login, or repository is required.
- **To create a durable GitHub-hosted app:** a GitHub account and a target repo; repository creation may need to happen in the GitHub UI depending on the agent's capabilities.
- **For automated changes and PRs:** an authorized GitHub connection with appropriate write rights.
- **For an installable APK:** access to an Android build environment, which may be GitHub Actions instead of a locally installed IDE.
- **For public REM-APP-CREATE skills:** anyone can read the repository without permission grants; an installation step is optional and environment-dependent.

## Example app ideas

- **Family photo sharing:** Android Share Sheet + Nextcloud adapter, preserving originals under failures.
- **Voice quiz battle:** generated questions, speech interface, multiple player modes and independent answer evaluation.
- **Travel soundtrack:** location-aware media/narration with lifecycle and external-player behavior modeling.

## Important boundaries

GitHub Actions, permissions and prices change. Verify current details against https://docs.github.com/en/billing and https://docs.github.com/en/actions/concepts/billing-and-usage before giving fixed numbers. Public source does not mean public-domain or zero-cost AI API use. Never place secrets in commits, prompts, exported logs, GitHub Actions output or public issues.
