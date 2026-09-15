#!/usr/bin/env python3
"""Regression tests for the optional execution-locus truth boundary."""
from __future__ import annotations

from validate_execution_locus import ValidationError, validate_surface

KNOWN_CLAIMS = {"local_execution", "remote_execution"}


def expect_pass(surface: dict, label: str) -> None:
    validate_surface(surface, label, KNOWN_CLAIMS)


def expect_fail(surface: dict, label: str) -> None:
    try:
        validate_surface(surface, label, KNOWN_CLAIMS)
    except ValidationError:
        return
    raise AssertionError(f"{label} unexpectedly passed")


def main() -> int:
    expect_pass({"custom_code": True}, "legacy_surface_without_locus")
    expect_pass(
        {
            "custom_code": True,
            "locus": "on_device",
            "source_claim_ids": ["local_execution"],
        },
        "on_device_custom_code",
    )
    expect_pass(
        {
            "custom_code": True,
            "locus": "split",
            "source_claim_ids": ["local_execution", "remote_execution"],
        },
        "split_custom_code",
    )
    expect_pass(
        {
            "custom_code": False,
            "locus": "remote_service",
            "source_claim_ids": ["remote_execution"],
        },
        "remote_service",
    )
    expect_pass(
        {
            "custom_code": "unknown",
            "locus": "unknown",
            "source_claim_ids": ["remote_execution"],
        },
        "unknown_locus",
    )

    expect_fail(
        {
            "custom_code": True,
            "locus": "remote_service",
            "source_claim_ids": ["remote_execution"],
        },
        "remote_promoted_to_local",
    )
    expect_fail(
        {
            "custom_code": True,
            "locus": "unknown",
            "source_claim_ids": ["remote_execution"],
        },
        "unknown_promoted_to_local",
    )
    expect_fail(
        {
            "custom_code": False,
            "locus": "on_device",
            "source_claim_ids": ["local_execution"],
        },
        "on_device_without_custom_code",
    )
    expect_fail(
        {
            "custom_code": False,
            "locus": "split",
            "source_claim_ids": ["local_execution", "remote_execution"],
        },
        "split_without_local_custom_code",
    )
    expect_fail(
        {
            "custom_code": True,
            "locus": "cloud",
            "source_claim_ids": ["local_execution"],
        },
        "unbounded_locus_token",
    )
    expect_fail(
        {
            "custom_code": "maybe",
            "locus": "on_device",
            "source_claim_ids": ["local_execution"],
        },
        "invalid_custom_code_token",
    )
    expect_fail(
        {"custom_code": True, "locus": "on_device"},
        "missing_locus_evidence_link",
    )
    expect_fail(
        {
            "custom_code": True,
            "locus": "on_device",
            "source_claim_ids": [],
        },
        "empty_locus_evidence_link",
    )
    expect_fail(
        {
            "custom_code": True,
            "locus": "on_device",
            "source_claim_ids": ["missing_claim"],
        },
        "unknown_locus_evidence_claim",
    )
    expect_fail(
        {
            "custom_code": True,
            "locus": "on_device",
            "source_claim_ids": ["local_execution", "local_execution"],
        },
        "duplicate_locus_evidence_claim",
    )

    print("PASS execution-locus regression cases")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
