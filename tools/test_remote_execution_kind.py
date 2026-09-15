#!/usr/bin/env python3
"""Regression tests for remote-service execution-kind classification."""
from __future__ import annotations

from validate_remote_execution_kind import ValidationError, validate_surface


def expect_pass(surface: dict, label: str) -> None:
    validate_surface(surface, label)


def expect_fail(surface: dict, label: str) -> None:
    try:
        validate_surface(surface, label)
    except ValidationError:
        return
    raise AssertionError(f"{label} unexpectedly passed")


def main() -> int:
    expect_pass(
        {
            "custom_code": False,
            "locus": "remote_service",
            "remote_kind": "companion_host",
        },
        "stream_deck_style_companion_host",
    )
    expect_pass(
        {
            "custom_code": False,
            "locus": "remote_service",
            "remote_kind": "cloud_service",
        },
        "alexa_style_cloud_service",
    )
    expect_pass(
        {
            "custom_code": False,
            "locus": "remote_service",
            "remote_kind": "other_remote",
        },
        "bounded_other_remote",
    )
    expect_pass(
        {
            "custom_code": "unknown",
            "locus": "remote_service",
            "remote_kind": "unknown",
        },
        "remote_kind_can_preserve_uncertainty",
    )
    expect_pass(
        {
            "custom_code": True,
            "locus": "on_device",
        },
        "on_device_does_not_need_remote_kind",
    )
    expect_pass(
        {
            "custom_code": True,
            "locus": "split",
        },
        "split_is_not_forced_into_one_remote_kind",
    )

    expect_fail(
        {
            "custom_code": False,
            "locus": "remote_service",
        },
        "remote_service_missing_kind",
    )
    expect_fail(
        {
            "custom_code": False,
            "locus": "remote_service",
            "remote_kind": "",
        },
        "blank_remote_kind",
    )
    expect_fail(
        {
            "custom_code": False,
            "locus": "remote_service",
            "remote_kind": "internet",
        },
        "unbounded_remote_kind",
    )
    expect_fail(
        {
            "custom_code": True,
            "locus": "on_device",
            "remote_kind": "companion_host",
        },
        "remote_kind_on_on_device_surface",
    )
    expect_fail(
        {
            "custom_code": "unknown",
            "locus": "unknown",
            "remote_kind": "unknown",
        },
        "remote_kind_on_unknown_locus",
    )

    print("PASS remote execution-kind regression cases")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
