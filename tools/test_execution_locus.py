#!/usr/bin/env python3
"""Regression tests for the optional execution-locus truth boundary."""
from __future__ import annotations

from validate_execution_locus import ValidationError, validate_surface

CLAIM_STATES = {
    "local_documented": "DOCUMENTED",
    "local_community": "COMMUNITY_VERIFIED",
    "remote_documented": "DOCUMENTED",
    "unresearched": "UNRESEARCHED",
    "deprecated": "DEPRECATED",
    "contradicted": "CONTRADICTED",
}


def expect_pass(surface: dict, label: str) -> None:
    validate_surface(surface, label, CLAIM_STATES)


def expect_fail(surface: dict, label: str) -> None:
    try:
        validate_surface(surface, label, CLAIM_STATES)
    except ValidationError:
        return
    raise AssertionError(f"{label} unexpectedly passed")


def main() -> int:
    expect_pass({"custom_code": True}, "legacy_surface_without_locus")
    expect_pass(
        {
            "custom_code": True,
            "locus": "on_device",
            "state": "DOCUMENTED",
            "source_claim_ids": ["local_documented"],
        },
        "on_device_custom_code",
    )
    expect_pass(
        {
            "custom_code": True,
            "locus": "split",
            "state": "COMMUNITY_VERIFIED",
            "source_claim_ids": ["local_community", "remote_documented"],
        },
        "split_custom_code",
    )
    expect_pass(
        {
            "custom_code": False,
            "locus": "remote_service",
            "state": "DOCUMENTED",
            "source_claim_ids": ["remote_documented"],
        },
        "remote_service",
    )
    expect_pass(
        {
            "custom_code": "unknown",
            "locus": "unknown",
            "state": "UNRESEARCHED",
            "source_claim_ids": ["unresearched"],
        },
        "unknown_locus_can_preserve_uncertainty",
    )

    expect_fail(
        {
            "custom_code": True,
            "locus": "remote_service",
            "state": "DOCUMENTED",
            "source_claim_ids": ["remote_documented"],
        },
        "remote_promoted_to_local",
    )
    expect_fail(
        {
            "custom_code": True,
            "locus": "unknown",
            "state": "UNRESEARCHED",
            "source_claim_ids": ["unresearched"],
        },
        "unknown_promoted_to_local",
    )
    expect_fail(
        {
            "custom_code": False,
            "locus": "on_device",
            "state": "DOCUMENTED",
            "source_claim_ids": ["local_documented"],
        },
        "on_device_without_custom_code",
    )
    expect_fail(
        {
            "custom_code": False,
            "locus": "split",
            "state": "DOCUMENTED",
            "source_claim_ids": ["local_documented", "remote_documented"],
        },
        "split_without_local_custom_code",
    )
    expect_fail(
        {
            "custom_code": True,
            "locus": "cloud",
            "state": "DOCUMENTED",
            "source_claim_ids": ["local_documented"],
        },
        "unbounded_locus_token",
    )
    expect_fail(
        {
            "custom_code": "maybe",
            "locus": "on_device",
            "state": "DOCUMENTED",
            "source_claim_ids": ["local_documented"],
        },
        "invalid_custom_code_token",
    )
    expect_fail(
        {"custom_code": True, "locus": "on_device", "state": "DOCUMENTED"},
        "missing_locus_evidence_link",
    )
    expect_fail(
        {
            "custom_code": True,
            "locus": "on_device",
            "state": "DOCUMENTED",
            "source_claim_ids": [],
        },
        "empty_locus_evidence_link",
    )
    expect_fail(
        {
            "custom_code": True,
            "locus": "on_device",
            "state": "DOCUMENTED",
            "source_claim_ids": ["missing_claim"],
        },
        "unknown_locus_evidence_claim",
    )
    expect_fail(
        {
            "custom_code": True,
            "locus": "on_device",
            "state": "DOCUMENTED",
            "source_claim_ids": ["local_documented", "local_documented"],
        },
        "duplicate_locus_evidence_claim",
    )
    expect_fail(
        {
            "custom_code": True,
            "locus": "on_device",
            "state": "DOCUMENTED",
            "source_claim_ids": ["contradicted"],
        },
        "positive_locus_cannot_rest_on_contradicted_claim",
    )
    expect_fail(
        {
            "custom_code": False,
            "locus": "remote_service",
            "state": "DOCUMENTED",
            "source_claim_ids": ["deprecated", "unresearched"],
        },
        "positive_remote_locus_needs_positive_evidence",
    )
    expect_fail(
        {
            "custom_code": True,
            "locus": "on_device",
            "state": "COMMUNITY_VERIFIED",
            "source_claim_ids": ["local_documented"],
        },
        "locus_state_cannot_outrun_linked_evidence",
    )
    expect_fail(
        {
            "custom_code": True,
            "locus": "on_device",
            "state": "CONTRADICTED",
            "source_claim_ids": ["local_documented"],
        },
        "positive_locus_requires_positive_surface_state",
    )

    print("PASS execution-locus regression cases")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
