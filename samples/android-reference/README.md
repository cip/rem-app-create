# Verified Android reference app (Issue #3)

This is a **real Java Android application** (AGP 8.9.2, Gradle 8.11.1, JDK 17, compileSdk 35). It deliberately has no Compose or third-party Android runtime dependencies: the goal is an extremely small, reliably compilable baseline.

The app opens a screen showing a greeting and its installed version name/code. Pure JVM logic is tested with JUnit. The CI workflow at `.github/workflows/android-reference.yml` runs `:app:testDebugUnitTest`, compiles `:app:assembleDebug`, asserts the APK exists and uploads `rem-android-reference-debug-apk`.

## Fresh repository bootstrap

Copy `samples/android-reference/` into a new Android app repository root (including `settings.gradle`, `build.gradle`, and the `app` module). Rename the application ID and package to match the app; configure proper versionCode/signing and adopt the toolkit's versioning guidance before distributing updates. Copy/adapt the workflow and change `gradle -p samples/android-reference` to `gradle`, update the APK artifact path accordingly. Do not blindly reuse debug signing for release.

**Evidence levels:** committed source ≠ CI queued ≠ JVM tests passed ≠ APK compiled ≠ installed on emulator/device. A green GitHub Actions run and its uploaded APK artifact are required before claiming a verified reference build; this README alone is not that evidence.

**CI trigger policy:** PR checks use `pull_request` only; `push` runs only for `main`, avoiding duplicate runs on feature-branch pushes. An intentional new `main` build is distinct from its prior PR validation.

**SDK regression:** never install obsolete `tools` SDK package and never assume `sdkmanager` is on PATH. The workflow discovers the actual executable and installs a known platform/build-tools pair. If the hosted runner layout changes, fail visibly and inspect the job logs.

## Local commands

With Android SDK and JDK 17 installed and Gradle 8.11.1 available:

```sh
gradle -p samples/android-reference :app:testDebugUnitTest :app:assembleDebug
```
