#!/usr/bin/env python3
"""Regression tests for the generic source_claim_ids continuity gate."""
from __future__ import annotations

from validate_source_claim_links import ValidationError, validate_data

CLAIMS = [
    {"id": "documented", "state": "DOCUMENTED", "source": "https://example.invalid/doc"},
    {"id": "community", "state": "COMMUNITY_VERIFIED", "source": "https://example.invalid/community"},
    {"id": "unresearched", "state": "UNRESEARCHED", "source": "https://example.invalid/unresearched"},
    {"id": "contradicted", "state": "CONTRADICTED", "source": "https://example.invalid/contradicted"},
]


def record(extension: object) -> dict:
    return {
        "evidence": {"claims": CLAIMS},
        "experimental": extension,
    }


def expect_pass(extension: object, label: str, expected_count: int | None = None) -> None:
    count = validate_data(record(extension))
    if expected_count is not None and count != expected_count:
        raise AssertionError(f"{label} validated {count} link container(s), expected {expected_count}")


def expect_fail(extension: object, label: str) -> None:
    try:
        validate_data(record(extension))
    except ValidationError:
        return
    raise AssertionError(f"{label} unexpectedly passed")


def main() -> int:
    expect_pass({"mode": "stock"}, "no_links_remains_schema_free", 0)
    expect_pass(
        {
            "operational_modes": [
                {
                    "id": "normal",
                    "state": "DOCUMENTED",
                    "source_claim_ids": ["documented"],
                },
                {
                    "id": "restricted",
                    "state": "COMMUNITY_VERIFIED",
                    "source_claim_ids": ["documented", "community"],
                },
            ]
        },
        "nested_positive_links",
        2,
    )
    expect_pass(
        {
            "mode": {
                "state": "CONTRADICTED",
                "source_claim_ids": ["contradicted"],
            }
        },
        "non_promoting_state_preserves_contradiction",
        1,
    )
    expect_pass(
        {
            "mode": {
                "state": "restricted",
                "source_claim_ids": ["documented"],
            }
        },
        "domain_state_is_not_reinterpreted_as_truth_state",
        1,
    )
    expect_pass(
        {"mode": {"source_claim_ids": ["unresearched"]}},
        "link_without_truth_state_only_requires_resolution",
        1,
    )

    expect_fail(
        {"mode": {"state": "DOCUMENTED", "source_claim_ids": []}},
        "empty_link_list",
    )
    expect_fail(
        {"mode": {"state": "DOCUMENTED", "source_claim_ids": ["missing"]}},
        "unresolved_claim",
    )
    expect_fail(
        {
            "mode": {
                "state": "DOCUMENTED",
                "source_claim_ids": ["documented", "documented"],
            }
        },
        "duplicate_claim_reference",
    )
    expect_fail(
        {
            "mode": {
                "state": "DOCUMENTED",
                "source_claim_ids": ["contradicted", "unresearched"],
            }
        },
        "positive_state_needs_positive_linked_support",
    )
    expect_fail(
        {
            "mode": {
                "state": "COMMUNITY_VERIFIED",
                "source_claim_ids": ["documented"],
            }
        },
        "container_cannot_outrun_linked_evidence",
    )
    expect_fail(
        {"mode": {"state": "DOCUMENTED", "source_claim_ids": [""]}},
        "blank_claim_reference",
    )

    print("PASS generic source-claim-link regression cases")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
