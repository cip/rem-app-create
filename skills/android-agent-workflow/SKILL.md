---
name: android-agent-workflow
description: Coordinate Android development agents, issue-to-PR delivery and evidence-based review.
---
# Agent engineering workflow

1. Verify the target repository and current main branch. Match the user request to issue, branch and intended pull request; do not guess from a nearby PR.
2. Distinguish question/assessment from explicit implementation approval.
3. Keep increments small, reviewable and testable; use short-lived branches.
4. Delegate architecture, modeling, implementation, emulator validation and independent review only where useful. Identify a single owner for integration and results.
5. Write regression coverage before code changes for reported bugs. Run local available checks before publishing and CI for the exact new commit.
6. Record outputs: changed behavior, trace or scenario, executed tests, CI status, app version/ref and remaining risks.
7. Never autonomously merge without user approval; do not run paid provider calls without opt-in.

Treat agents' conclusions as hypotheses until supported by executable or observed evidence.
