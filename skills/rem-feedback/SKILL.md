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
5. **Investigate upstream before filing:** identify the exact toolkit revision used by the user (branch/tag/commit if available). Search open **and closed** issues in `cip/rem-app-create`, relevant PRs and changes in both `main` and `develop`. Do not treat a matching issue title as proof: compare symptoms, reproduction and versions.
6. Classify the outcome accurately:
   - **Already fixed in main:** link the fix, explain how to retry or update; avoid a duplicate issue.
   - **Fix in develop only:** link the relevant PR/commit and explain the stable-versus-experimental choice. Do not silently switch the user's project to development instructions.
   - **Existing issue, not fixed:** link the issue and, with permission, add sanitized new evidence if materially useful.
   - **Possible regression:** identify when it worked and which versions might be affected; open or update a regression issue after evidence review.
   - **App-only problem:** direct the report to that app's own issue tracker. Suggest a toolkit issue only if a generalizable missing safeguard or instruction contributed.
   - **New toolkit problem:** prepare a new upstream issue after duplicate checks.
   - **Unable to verify:** disclose that source/issue/branch lookup was unavailable; do not state that no fix exists.
7. Before any public post, remove tokens, credentials, names, email addresses, precise location, private repositories, app content and private logs; prefer minimal anonymized steps. Make the report in English with expected/actual behavior, repro, toolkit ref, app ref (only if public and approved), verification evidence, related issues/PRs, and an explicit unknowns section.
8. **Ask before public submission** unless the user specifically requested issue creation or commenting. Describe the intended report and destination. A frustrated complaint alone does not authorize public disclosure.
9. If authorized GitHub write access exists, create the issue or comment on the existing issue and report its exact URL after confirmation. Otherwise offer a ready-to-paste draft and the GitHub issue URL. Never request an access token in chat.
10. Do not merge, retarget the user's app to `develop`, change its branch policies, or run paid evaluations as part of feedback triage. A fix in toolkit `develop` is not automatically a fix in the generated app.

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
