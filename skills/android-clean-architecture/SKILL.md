---
name: android-clean-architecture
description: Design testable Kotlin and Jetpack Compose Android features using Google's recommended architecture.
---
# Clean Android architecture

Prefer unidirectional data flow, clearly scoped UI state, lifecycle-aware collection, ViewModels where appropriate, repositories and separated domain logic. Keep platform and SDK code behind explicit interfaces and inject clocks, dispatchers and external providers.

1. Identify observable use cases and ownership of state.
2. Separate Android UI and transport adapters from policy, state transitions and persistence decisions.
3. Model cancellation, retries, duplicate callbacks, stale events, process recreation and permission changes.
4. Write deterministic JVM tests against the real production reducer/use case and adapter contract tests at the boundary.
5. Select focused instrumentation/emulator checks for Android behaviors JVM tests cannot prove.

Avoid rigid boilerplate or a domain layer without a concrete reason. Check current official Android guidance for any platform-sensitive choice.
