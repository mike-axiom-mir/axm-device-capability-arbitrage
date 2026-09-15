#!/usr/bin/env python3
"""Regression tests for the optional execution-locus truth boundary."""
from __future__ import annotations

from validate_execution_locus import ValidationError, validate_surface


def expect_pass(surface: dict, label: str) -> None:
    validate_surface(surface, label)


def expect_fail(surface: dict, label: str) -> None:
    try:
        validate_surface(surface, label)
    except ValidationError:
        return
    raise AssertionError(f"{label} unexpectedly passed")


def main() -> int:
    expect_pass({"custom_code": True}, "legacy_surface_without_locus")
    expect_pass({"custom_code": True, "locus": "on_device"}, "on_device_custom_code")
    expect_pass({"custom_code": True, "locus": "split"}, "split_custom_code")
    expect_pass({"custom_code": False, "locus": "remote_service"}, "remote_service")
    expect_pass({"custom_code": "unknown", "locus": "unknown"}, "unknown_locus")

    expect_fail({"custom_code": True, "locus": "remote_service"}, "remote_promoted_to_local")
    expect_fail({"custom_code": True, "locus": "unknown"}, "unknown_promoted_to_local")
    expect_fail({"custom_code": False, "locus": "on_device"}, "on_device_without_custom_code")
    expect_fail({"custom_code": False, "locus": "split"}, "split_without_local_custom_code")
    expect_fail({"custom_code": True, "locus": "cloud"}, "unbounded_locus_token")
    expect_fail({"custom_code": "maybe", "locus": "on_device"}, "invalid_custom_code_token")

    print("PASS execution-locus regression cases")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
