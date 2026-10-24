---
name: android-ci-release
description: Set up traceable Android CI and safe APK versioning, testing and release handoffs.
---
# Android CI and APK handoff

1. Inspect existing application IDs, signing, Gradle modules and CI before changing anything. Keep production ID and signing identity stable.
2. Establish JVM tests and debug assembly as the fast baseline. Compile instrumentation and **execute** emulator tests separately; never conflate the two.
3. Make build metadata observable: source ref, commit, versionName, numeric monotonically compatible versionCode, variant/app ID and test evidence.
4. Preserve installability across CI builds. Handle parallel builds/versionCode uniqueness according to the repository's established scheme.
5. Provide direct links to exact CI run and APK where available. Report status from queued/start through APK-ready and completion.
6. Quick/rebuild modes may skip tests only if labeled explicitly unverified. Real paid LLM/provider validation is opt-in.
7. Keep PR checks, signed releases, artifacts and secrets separate; never commit credentials.

Report exactly which jobs were executed and whether the user can install the resulting artifact without overwriting unrelated variants.
