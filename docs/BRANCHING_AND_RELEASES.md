# Branching and releases

## Branch contracts

- **main**: stable, publicly recommended entry point. Ordinary users paste https://github.com/cip/rem-app-create into ChatGPT; this resolves the default branch. Publish only reviewed and verified changes here.
- **develop**: rolling integration and exploratory testing. Paste https://github.com/cip/rem-app-create/tree/develop into ChatGPT and explicitly request the files from `develop`.
- **feature/*, fix/*, docs/***: short-lived task branches, normally submitted as PRs to `develop`.
- **vX.Y.Z tags**: immutable reference points for reproducing a particular skill revision after the release process is established.

## Important ChatGPT behavior

A branch URL points to GitHub content; it does **not** automatically install skills, execute shell commands, grant repository write permission or ensure a specific assistant has read every instruction. Ask the agent to read `README.md`, `CHATGPT_START_HERE.md` and relevant `SKILL.md` files **from the selected branch**, identify the commit SHA, and report any inaccessible files.

Sample test prompt:

> Read https://github.com/cip/rem-app-create/tree/develop at its current commit. Follow its CHATGPT_START_HERE.md and relevant skill instructions to help me develop a Nokia-style Snake Android app. Tell me which files and commit you actually inspected.

For stable behavior, replace the branch with a release tag or commit URL (after those exist).

## Promotion workflow

1. Put independent changes in a short-lived branch targeting `develop`; require human approval for merges.
2. Run the skill syntax/structure validator and appropriate targeted example or agent scenarios, including fresh-chat link-only onboarding and link-plus-app-idea onboarding.
3. Evaluate real app results (such as generated Android CI) where available. Report untested claims as unverified.
4. Open a **promotion PR from `develop` to `main`** with changed skills, known regressions, evidence, limitations and commit SHA. Never silently promote.
5. After approval and merge, tag a version if appropriate and document any incompatible changes.

## GitHub protection recommendations

Configure in GitHub Settings → Rules → Rulesets (or Branch protection) for `main`: required PR reviews, required skill validation, prevent force push and deletion. Restrict production changes to reviewed promotion PRs. Set up a ruleset on `develop` too if the team needs review gates. Branch protection may require plan/visibility-dependent GitHub capabilities; check current settings rather than assuming they are active.

**Initial status:** this policy describes the intended workflow. It does not itself turn on GitHub branch protection or prove all end-to-end scenarios passed.
