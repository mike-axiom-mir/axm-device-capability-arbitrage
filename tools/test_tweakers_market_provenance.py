#!/usr/bin/env python3
"""Regression tests for Tweakers market-provenance seller-class handling."""

from __future__ import annotations

from copy import deepcopy

from validate_tweakers_market_provenance import (
    ValidationError,
    validate_tweakers_observation,
)


def base_observation() -> dict:
    return {
        "marketplace": "Tweakers_Vraag_En_Aanbod",
        "listed_at": "2026-08-18",
        "price_type": "asking",
        "seller_class": "unknown",
        "seller_class_basis": (
            "The public listing exposes the account and location but does not "
            "explicitly establish private, business, or dealer status."
        ),
        "model_identity": "Example Device",
        "configuration": {"variant": "example"},
        "source": "https://tweakers.net/aanbod/1234567/example-device.html",
        "source_scope": "direct_listing",
    }


def expect_valid(name: str, observation: dict) -> None:
    result = validate_tweakers_observation(name, observation)
    if result is not True:
        raise AssertionError(f"{name}: expected Tweakers observation to validate")


def expect_invalid(name: str, observation: dict, needle: str) -> None:
    try:
        validate_tweakers_observation(name, observation)
    except ValidationError as exc:
        if needle not in str(exc):
            raise AssertionError(
                f"{name}: expected error containing {needle!r}, got {exc!r}"
            ) from exc
    else:
        raise AssertionError(f"{name}: expected validation failure")


def main() -> int:
    unknown = base_observation()
    expect_valid("unknown_seller_with_basis", unknown)

    private = deepcopy(unknown)
    private["seller_class"] = "private"
    private["seller_class_basis"] = "The source explicitly identifies a private seller."
    expect_valid("private_seller_with_basis", private)

    missing_basis = deepcopy(unknown)
    missing_basis.pop("seller_class_basis")
    expect_invalid(
        "missing_seller_class_basis",
        missing_basis,
        "seller_class_basis must be a non-empty string",
    )

    guessed = deepcopy(unknown)
    guessed["seller_class"] = "probably_private"
    expect_invalid(
        "unbounded_seller_class",
        guessed,
        "seller_class 'probably_private' must be one of",
    )

    bad_scope = deepcopy(unknown)
    bad_scope["source_scope"] = "search_result_snapshot"
    expect_invalid(
        "vraag_en_aanbod_capture_scope",
        bad_scope,
        "source_scope must remain the generic capture mode 'direct_listing'",
    )

    pricewatch = deepcopy(unknown)
    pricewatch["source"] = "https://tweakers.net/pricewatch/123456/example.html"
    expect_invalid(
        "pricewatch_not_raw_listing",
        pricewatch,
        "not a raw acquisition listing",
    )

    forum = deepcopy(unknown)
    forum["source"] = "https://gathering.tweakers.net/forum/list_messages/123456"
    expect_invalid(
        "forum_not_market_observation",
        forum,
        "research leads, not raw acquisition-price observations",
    )

    print("Tweakers market-provenance seller-class regression tests passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
