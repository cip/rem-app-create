---
name: android-model-testing
description: Model Android integrations and external-system behavior with reproducible event sequences, virtual time and independent invariants.
---
# Model-based testing

Model the **environment and allowed behavior**, not a duplicate implementation of the system under test. Run generated or table-driven event sequences through production reducers, coordinators and use cases.

1. Enumerate external actor profiles, capabilities, provenance and uncertainties: API successes/failures, delayed/missing callbacks, partial observations, repeats, ordering changes and cross-device/lifecycle events.
2. Represent controllable inputs and virtual clock advances as serializable events. Preserve scenario ID, profile revision, seed and minimal ordered trace.
3. Implement independent, user-observable invariants: no unintended deletes; no duplicate side effects; no stale commands crossing sessions; no unsafe assumption of completion.
4. Exercise variants, concurrent intents, retry/deadline boundaries, pause/resume and recoveries. Assert emitted commands and state ownership, not just screen labels.
5. Keep real provider/device evidence in a calibration ledger. Update models from reproducible observations, retaining older profiles.
6. When a defect occurs, write a failing scenario before correcting production code. Characterization tests are not acceptance tests.

A synthetic adapter satisfying an assumed callback contract cannot validate that the actual SDK satisfies it. A JVM pass is not emulator, device or end-to-end verification.
