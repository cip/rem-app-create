"""Portable Android build-versioning primitives.

This module is deliberately provider-neutral: repositories must implement a durable
compare-and-swap CounterStore backed by protected state (not this process's memory).
"""
from dataclasses import dataclass

MAX_VERSION_CODE = 2_100_000_000


class AllocationError(RuntimeError):
    pass


@dataclass(frozen=True)
class Snapshot:
    revision: str
    code: int


def allocate(store, *, retries=12):
    """Reserve one fresh code with optimistic concurrency; never force overwrite.

    store.read() -> Snapshot
    store.compare_and_swap(expected_revision, new_code) -> bool
    """
    if retries < 1:
        raise ValueError("retries must be positive")
    for _ in range(retries):
        state = store.read()
        if not isinstance(state, Snapshot) or not isinstance(state.code, int) or isinstance(state.code, bool):
            raise AllocationError("Invalid counter state")
        if not (0 <= state.code < MAX_VERSION_CODE) or not state.revision:
            raise AllocationError("Counter corrupted or exhausted")
        next_code = state.code + 1
        if store.compare_and_swap(state.revision, next_code):
            return next_code
    raise AllocationError("Version allocation contention: bounded retry exhausted")


def validate_apk_identity(expected, actual):
    """Compare parsed APK identity to allocated build identity before publication."""
    required = ("applicationId", "versionCode", "versionName", "signingFingerprint")
    if not all(k in expected and k in actual for k in required):
        raise AllocationError("Missing APK identity")
    for key in required:
        if expected[key] != actual[key]:
            raise AllocationError(f"APK {key} mismatch")
    if not isinstance(actual["versionCode"], int) or isinstance(actual["versionCode"], bool):
        raise AllocationError("Invalid built code")
    if not (1 <= actual["versionCode"] <= MAX_VERSION_CODE):
        raise AllocationError("Built code out of range")
    return True


def runtime_version_label(installed_name, installed_code):
    """The version shown in an About screen must use *installed* package data."""
    if not installed_name or not isinstance(installed_code, int) or isinstance(installed_code, bool) or installed_code < 1:
        raise ValueError("Missing installed version")
    return f"Version {installed_name} ({installed_code})"


def may_replace_latest(existing, candidate):
    """Only promote a verified APK within the same installable distribution channel.

    Callers must serialize pointer updates or use conditional writes: this predicate
    alone does not make concurrent publication atomic.
    """
    required = ("applicationId", "signingFingerprint", "channel", "versionCode")
    if not isinstance(candidate, dict) or candidate.get("verified") is not True:
        return False
    if any(not candidate.get(key) for key in required[:-1]):
        return False
    code = candidate.get("versionCode")
    if type(code) is not int or not 1 <= code <= MAX_VERSION_CODE:
        return False
    if existing is None:
        return True
    if not isinstance(existing, dict):
        return False
    if any(existing.get(key) != candidate[key] for key in required[:-1]):
        return False
    previous = existing.get("versionCode")
    if type(previous) is not int or not 1 <= previous <= MAX_VERSION_CODE:
        return False
    return code > previous
