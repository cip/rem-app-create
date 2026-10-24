# Android installable build versioning

This is reusable guidance for Android application repositories using REM-APP-CREATE, not a versioning scheme for this skills repository itself. Adapt it to the app's existing Gradle, signing and CI setup. Inspired by the proven Roadtrip Tunes strategy, without copying app-specific identities or CI secrets.

## Fundamental Android invariants

- An in-place update requires the **same applicationId/package identity**, a compatible **signing identity**, and an installed-compatible **versionCode** (normally strictly increasing). It must also preserve or explicitly migrate persisted user data.
- `versionName` is a human-readable product label, **not** the Android installation ordering key. Keep it separately controlled (e.g. patch bump for product changes); rebuilding unchanged sources can use the same name with a new code.
- Pick the versionCode starting floor **above every previously distributed installable APK** of that application ID/signing lineage. Inspect real artifacts, including historic PR/manual builds. Never reset the counter as a convenient fix.
- Android has a versionCode upper bound. Reject invalid, corrupt or exhausted counter state before publishing; never wrap or fall back to a low code.

## Recommended default for repositories publishing frequent CI debug APKs

1. Keep one stable installable Debug application ID and one stable, secured CI Debug signing certificate across PR/Main builds, so they can replace each other on the device. An applicationSuffix is fine, but make sure it stays consistent. Release uses its own established production ID and signing identity; do **not** silently turn a debug install into the release app.
2. Use a **durable repository-wide counter** rather than branch-local incrementing or GitHub Actions run number. Persist it in protected repository state (e.g. a dedicated counter branch) and give each **actual APK build execution** a unique, increasing code. The counter must survive new commits, branches and workflow reruns.
3. Allocate atomically, via compare-and-swap/non-force fast-forward or an equivalent serialized transaction. Concurrent contenders read, attempt allocation and retry on conflict with bounded backoff. Never use force push. Failed builds may leave harmless gaps. If the allocator cannot safely reserve a number, **fail closed**, do not produce an installable APK with a guessed code.
4. Allocate for fresh normal builds, complete or failed-job reruns **when they execute a new APK build**, and opt-in Quick Rebuilds. Publication-only retries re-use the *already built and verified APK* and its identity, never silently rebuild with a conflicting code.
5. Build source provenance must be recorded independently of the allocator: branch/tag, exact built commit, PR head vs synthetic merge SHA, workflow run ID and attempt, variant, application ID, signing certificate fingerprint, `versionName` and allocated `versionCode`. Use an artifact `build-info.json` / job summary / APK filename; expose provenance in-app and app-open logs when practical.
6. Read back and validate the **built APK** package, code, name and signing certificate against allocation metadata **before publishing**. Do not trust only Gradle source literals. Never publish a failed verification as installable.
7. CI signatures must be stable and handled as secrets; follow repository trust boundaries so untrusted PR code cannot access production signing secrets. If PR signing is unsafe, provide a separately labeled non-updatable artifact rather than weakening secret isolation.

## Builds can complete out of order

Allocated code order is **not** completion order. A slower build with a smaller code can finish after a faster build with a larger code. Do not overwrite the 'latest installable' pointer or PR handoff with an older-code APK. If the intended source's APK code is below the user's installed version, request a fresh build of that exact source. Do not recommend uninstall/reinstall without explicit informed consent and a data-backup/migration plan.

## Product version, releases and variants

- Define one authoritative product-version policy. Avoid accidental `versionName` regressions in tagged releases; validate release tags against APK metadata.
- A Release APK should use the project's stable production app ID and established release signing. Do not assume a CI Debug APK can update a Release installation or vice versa.
- If flavors use distinct IDs, specify which tracks are installable over one another. Treat different signing keys, app IDs and data stores as distinct channels.
- For stores, consider store-specific version-code rules, package version limits, signing key lineage, rollout tracks and previously shipped codes before using a shared strategy. A protected release allocation policy may be more appropriate than the Debug counter.
- A higher code can install older application *source* in Debug, but database/schema compatibility can still break data. State migration or backwards-compatibility limitations and test upgrades with real persisted data.

## Quick Rebuild and test evidence

- Quick Rebuild is opt-in, Debug-only by default, and always gets a new code. It may skip tests for speed, but compilation, metadata verification and signing validation still run.
- Clearly mark quick APKs as **tests skipped / unverified** in CI, metadata, comments and UI. Do not replace the latest **verified** Debug publication with a quick artifact.
- Normal CI distinguishes JVM, instrumentation compile, executed emulator and device evidence. All claims attach to the exact built commit, version and run.
- Temporary PR artifacts and durable Main/Release artifacts have explicit retention; never link another branch's “latest” build as if it belongs to the requested PR.

## Model-based/versioning regression matrix

Test the allocator using concurrent contenders and deterministic/fault-injected mock repository APIs. At minimum:
- two or more concurrent allocations from the same state -> unique increasing codes, retried conflict;
- job reruns and quick builds -> new code; publication-only retry -> same APK/code;
- counter missing/corrupt, permission denied, rate limits, network loss, overflow -> fail closed or explicitly documented recovery;
- CI cancellation after reservation -> gap tolerated; out-of-order completion -> newest eligible pointer never regresses;
- wrong package/signature/code/name compared to built artifact -> fail publication;
- older source rebuilt with higher code -> provenance correct; data upgrade/downgrade compatibility checked separately;
- PR head versus synthetic merge SHA, tags and flavors -> accurately labeled;
- installed Debug replacement -> validated on an Android emulator or device with preserved sample user data and matching signing key.

Structural/unit tests cannot prove install-on-device updates. Keep actual install/update evidence separate.

## Recovery and handoff

- Treat the counter as **persistent release state**: back it up/protect it; do not delete, reseed downward, or force-push it. On loss, determine the highest code **ever distributed**, restore history or restart strictly above that high-water mark with a documented, reviewed recovery procedure.
- Handoff must report source PR/ref, built SHA, product version, code (or **pending** until allocated), run/attempt, test execution evidence, build status and the exact APK/download link. Distinguish **APK available** from **CI completed and passed**. Unknown values stay unknown.
- Never claim compatibility on the basis of a new code alone. If the recipient has a higher-code install or incompatible signing, explain the constraint and provide a safe rebuild or migration path.

## Boundaries

This guide is opt-in **for each Android app repository** when the user or app's existing delivery requirements call for it. Do not impose REM-APP-CREATE's development-branch or agent workflow on target repositories. Do not copy Roadtrip Tunes' IDs, counter seed, workflow names or credentials. Preserve existing working solutions and use the smallest safe migration when adopting these practices.
