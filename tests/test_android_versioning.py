"""Executable deterministic contracts for the toolkit's versioning reference."""
import pathlib
import sys
import threading
import unittest
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from scripts.android_versioning import (
    AllocationError, Snapshot, allocate, may_replace_latest,
    runtime_version_label, validate_apk_identity, MAX_VERSION_CODE,
)


class InMemoryCas:
    """Thread-safe fake ONLY for deterministic tests, never a production counter."""
    def __init__(self, initial=999):
        self.lock = threading.Lock()
        self.version = 0
        self.code = initial

    def read(self):
        with self.lock:
            return Snapshot(str(self.version), self.code)

    def compare_and_swap(self, revision, new_code):
        with self.lock:
            if revision != str(self.version):
                return False
            self.code = new_code
            self.version += 1
            return True


class VersioningTests(unittest.TestCase):
    def test_concurrent_builds_allocate_unique_codes(self):
        store = InMemoryCas()
        with ThreadPoolExecutor(max_workers=12) as pool:
            codes = list(pool.map(lambda _: allocate(store, retries=1000), range(100)))
        self.assertEqual(len(set(codes)), 100)
        self.assertEqual(sorted(codes), list(range(1000, 1100)))

    def test_reruns_and_quick_builds_reserve_new_code(self):
        store = InMemoryCas()
        initial = allocate(store)
        full_rerun = allocate(store)
        quick = allocate(store)
        self.assertEqual((initial, full_rerun, quick), (1000, 1001, 1002))
        self.assertEqual(store.code, 1002)  # publication-only retry: no allocate()

    def test_conflict_retry(self):
        class Conflicted(InMemoryCas):
            def __init__(self):
                super().__init__()
                self.fail_first = True
            def compare_and_swap(self, revision, code):
                if self.fail_first:
                    self.fail_first = False
                    return False
                return super().compare_and_swap(revision, code)
        self.assertEqual(allocate(Conflicted()), 1000)

    def test_bounded_failure(self):
        class Rejected(InMemoryCas):
            def compare_and_swap(self, revision, code):
                return False
        with self.assertRaises(AllocationError):
            allocate(Rejected(), retries=2)

    def test_corrupt_or_exhausted_counter(self):
        for state in (-1, MAX_VERSION_CODE, MAX_VERSION_CODE + 1, True, "999"):
            with self.subTest(state=state):
                with self.assertRaises(AllocationError):
                    allocate(InMemoryCas(state))

    def test_cancelled_job_leaves_a_gap_not_a_reused_code(self):
        store = InMemoryCas()
        cancelled_code = allocate(store)
        successor = allocate(store)
        self.assertEqual(successor, cancelled_code + 1)

    def test_out_of_order_completion_and_unverified_build(self):
        latest = dict(applicationId="example.debug", versionCode=1002, verified=True)
        self.assertFalse(may_replace_latest(latest, dict(applicationId="example.debug", versionCode=1001, verified=True)))
        self.assertFalse(may_replace_latest(latest, dict(applicationId="example.debug", versionCode=1003, verified=False)))
        self.assertTrue(may_replace_latest(latest, dict(applicationId="example.debug", versionCode=1003, verified=True)))
        self.assertFalse(may_replace_latest(latest, dict(applicationId="other.app", versionCode=9999, verified=True)))

    def test_built_apk_metadata_must_match_all_fields(self):
        expected = dict(applicationId="app.debug", versionCode=1001, versionName="0.8.12", signingFingerprint="ABC")
        self.assertTrue(validate_apk_identity(expected, expected.copy()))
        for field, new_value in (("applicationId", "other"), ("versionCode", 999), ("versionName", "0.8.11"), ("signingFingerprint", "XYZ")):
            wrong = {**expected, field: new_value}
            with self.subTest(field=field), self.assertRaises(AllocationError):
                validate_apk_identity(expected, wrong)

    def test_about_version_uses_installed_identity(self):
        installed = dict(versionName="0.8.12", versionCode=1002)
        label = runtime_version_label(installed["versionName"], installed["versionCode"])
        self.assertEqual(label, "Version 0.8.12 (1002)")
        with self.assertRaises(ValueError):
            runtime_version_label("", 1002)


if __name__ == "__main__":
    unittest.main()
