---
name: android-ci-release
description: Set up traceable Android CI and safe APK versioning, testing and release handoffs.
---
# Android CI and APK handoff

1. Inspect existing application IDs, signing, Gradle modules and CI before changing anything. Keep production ID and signing identity stable.
2. Establish JVM tests and debug assembly as the fast baseline. Compile instrumentation and **execute** emulator tests separately; never conflate the two.
3. Make build metadata observable: source ref, commit, versionName, numeric monotonically compatible versionCode, variant/app ID and test evidence.
4. Preserve installability across CI builds. Read [Android build versioning](../../docs/ANDROID_BUILD_VERSIONING.md) and implement or retain a durable collision-safe code allocator when issuing frequent installable CI APKs. Check previously distributed APK high-water marks, app ID, stable signing identity and persisted-data compatibility. Do not assume branch-local counters or run numbers handle reruns/concurrent builds.
5. Allocate a new code for every executed APK build, including reruns and Quick Rebuild; publication-only retries reuse the validated artifact. Fail closed on allocator/metadata/signature errors. Compare against the built APK before publication and prevent an out-of-order lower-code build replacing a higher-code handoff.
6. Include a discoverable **Settings → About / App info** (or equivalent) view in Android apps by default, showing **installed** `versionName` and `versionCode`; expandable provenance and a copyable diagnostics summary should be included where build metadata is available. Follow the [in-app build identity standard](../../docs/ANDROID_BUILD_VERSIONING.md#default-in-app-build-identity-mandatory-for-toolkit-created-apps). Verify displayed identity against the built APK, not hardcoded Gradle fallbacks.
7. Provide direct links to exact CI run and APK where available. Report status from queued/start through APK-ready and completion.
8. Quick/rebuild modes may skip tests only if labeled explicitly unverified. Real paid LLM/provider validation is opt-in.
9. Keep PR checks, signed releases, artifacts and secrets separate; never commit credentials.

Model-check concurrent allocation, cancellation, retries, counter corruption and out-of-order completion; separately validate signed in-place Android updates preserving data on emulator/device. Do not claim model/unit tests prove installability.

Report exactly which jobs were executed and whether the user can install the resulting artifact without overwriting unrelated variants.
