---
name: rem-feedback
description: Triage user feedback about REM-APP-CREATE and, with user consent and authorized GitHub access, open a privacy-safe issue in cip/rem-app-create.
---
# REM-APP-CREATE feedback

Use this skill when someone using REM-APP-CREATE reports confusing instructions, failures, missing capabilities, usability concerns or improvement ideas. Treat complaints as actionable signals, but never assume every app bug is a toolkit bug.

## Intake and triage

1. Listen to the complaint. Identify the user goal, what happened, what they expected, and which REM-APP-CREATE advice or automation was involved.
2. Distinguish **toolkit-wide issue** (bad guidance, broken template, installer instructions, inappropriate defaults) from **project-specific issue** (app's own implementation or configuration). File toolkit issues only for reusable learnings; for app-only issues suggest the app repository.
3. Ask for the smallest helpful reproduction if genuinely needed. An app repo, public CI URL, skill name and commit are useful, but never demand a screenshot if logs already contain the evidence.
4. **Before publishing**, remove tokens, credentials, names, email addresses, exact user locations, private repo URLs, personal app content, proprietary source, private logs and any other confidential details. Public issues are accessible to everybody. Do not copy entire logs or copyrighted code unnecessarily.
5. Check existing open/closed issues in `cip/rem-app-create` for duplicates when tools permit; prefer updating or referring to the matching issue instead of creating another.
6. Prepare a concise English report containing: problem, expected behavior, actual behavior, reproduction, environment and versions if known, impact, evidence link only if suitable for public sharing, and suspected toolkit gap clearly marked as hypothesis. Explicitly indicate unknown fields.
7. **Ask permission before publishing feedback publicly** unless the user has explicitly requested submission. A complaint is not automatically consent to publish. Show or summarize the intended public content and target repository.
8. If GitHub write access is available, create an issue in `cip/rem-app-create`; otherwise provide a ready-to-paste issue and `https://github.com/cip/rem-app-create/issues/new`. **Do not claim an issue was filed until GitHub confirms it.** Never ask users to paste access tokens in chat.
9. Report the resulting exact issue URL. Track observed failure separately from future design decisions; don't auto-merge or implement unrequested fixes.

## Example

A user says: "The Snake app built with these skills fails on GitHub Actions." Verify the CI reason first. If reusable guidance should have covered Android SDK setup, propose a generalized issue:

- Title: `CI bootstrap: document/validate Android SDK setup for generated projects`
- What happened: A new Android app CI setup failed during toolchain setup.
- Expected: Templates/guidance ensure usable SDK and Gradle configuration or flag missing prerequisites.
- Repro: Supply only a public minimal CI URL or sanitized relevant error.
- Improvement: Add a regression fixture, update the CI skill and clarify build verification.
- Scope: Toolkit-level workflow improvement, not an allegation that every generated app has the same bug.

## Chat-first entry

If a person pastes only the REM-APP-CREATE repository URL, explain app possibilities. If they report trouble after attempting one, offer feedback triage and issue submission as a natural next step, rather than requiring them to install a local skill runner.
