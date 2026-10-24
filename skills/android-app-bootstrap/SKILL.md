---
name: android-app-bootstrap
description: Audit a new or existing Android repository and establish reliable agent-driven engineering foundations.
---
# Android app bootstrap

Use at the beginning of an Android project or when retrofitting agent workflows.

1. Read the existing README, AGENTS.md, Gradle files, CI pipelines and relevant issues. Preserve app identity, versioning, signing and user data.
2. Identify business flows, destructive actions, external providers, lifecycle and background work. List observable invariants and known unknowns.
3. Pick relevant skills: clean architecture, model testing, CI release and agent workflow. Avoid duplicating existing infrastructure.
4. Propose the smallest independent implementation and executable verification slice. Do not change a repository merely because it was inspected.
5. Produce a checklist of what actually ran, what is untested, and next risks.

Never silently overwrite existing project conventions or claim emulator/device validation without execution.
