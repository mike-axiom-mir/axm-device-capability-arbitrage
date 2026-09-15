#!/usr/bin/env python3
"""Regression tests for validate_tweakers_device_evidence.py."""

from __future__ import annotations

import copy
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from validate_tweakers_device_evidence import ValidationError, validate_claim


def base_claims():
    return {
        "forum_lead": {
            "id": "forum_lead",
            "state": "COMMUNITY_VERIFIED",
            "source": "https://gathering.tweakers.net/forum/list_messages/12345",
            "proves": ["bounded device behavior"],
        },
        "official": {
            "id": "official",
            "state": "DOCUMENTED",
            "source": "https://example-manufacturer.invalid/support/device",
            "proves": ["manufacturer-documented device behavior"],
        },
    }


def expect_pass(name: str, claim: dict, claims: dict) -> None:
    try:
        validate_claim(
            claim,
            claim_index=0,
            record_context="synthetic/device.yaml",
            claims_by_id=claims,
        )
    except ValidationError as exc:
        raise AssertionError(f"{name}: expected pass, got {exc}") from exc
    print(f"PASS {name}")


def expect_fail(name: str, claim: dict, claims: dict) -> None:
    try:
        validate_claim(
            claim,
            claim_index=0,
            record_context="synthetic/device.yaml",
            claims_by_id=claims,
        )
    except ValidationError:
        print(f"PASS {name} (rejected as expected)")
        return
    raise AssertionError(f"{name}: expected ValidationError")


def main() -> int:
    claims = base_claims()

    expect_fail(
        "positive forum primary without corroboration",
        claims["forum_lead"],
        claims,
    )

    forum_with_corroboration = copy.deepcopy(claims["forum_lead"])
    forum_with_corroboration["tweakers_corroboration"] = [
        {"claim_id": "official", "kind": "manufacturer_documentation"}
    ]
    claims_with_corroboration = copy.deepcopy(claims)
    claims_with_corroboration["forum_lead"] = forum_with_corroboration
    expect_pass(
        "positive forum primary with explicit stronger corroboration",
        forum_with_corroboration,
        claims_with_corroboration,
    )

    lead_only = copy.deepcopy(claims["forum_lead"])
    lead_only["state"] = "UNRESEARCHED"
    expect_pass("forum lead may remain non-promoting", lead_only, {"forum_lead": lead_only})

    official_plus_forum = copy.deepcopy(claims["official"])
    official_plus_forum["additional_sources"] = [
        "https://gathering.tweakers.net/forum/list_messages/12345"
    ]
    expect_pass(
        "forum may remain secondary to non-Tweakers primary evidence",
        official_plus_forum,
        {"official": official_plus_forum},
    )

    pricewatch = {
        "id": "pricewatch_variant",
        "state": "DOCUMENTED",
        "source": "https://tweakers.net/pricewatch/123/device.html",
        "tweakers_evidence_scope": "variant_crosscheck",
        "proves": ["the Pricewatch entry distinguishes this marketed variant"],
    }
    expect_pass("bounded Pricewatch cross-check", pricewatch, {"pricewatch_variant": pricewatch})

    pricewatch_too_strong = copy.deepcopy(pricewatch)
    pricewatch_too_strong["state"] = "COMMUNITY_VERIFIED"
    expect_fail(
        "Pricewatch primary cannot promote above DOCUMENTED",
        pricewatch_too_strong,
        {"pricewatch_variant": pricewatch_too_strong},
    )

    market_claim = {
        "id": "market_claim",
        "state": "DOCUMENTED",
        "source": "https://tweakers.net/aanbod/123/device.html",
        "proves": ["device capability"],
    }
    expect_fail(
        "Vraag & Aanbod cannot be positive device-capability evidence",
        market_claim,
        {"market_claim": market_claim},
    )

    bad_corroboration = copy.deepcopy(forum_with_corroboration)
    bad_corroboration["tweakers_corroboration"] = [
        {"claim_id": "pricewatch_variant", "kind": "manufacturer_documentation"}
    ]
    mixed = {
        "forum_lead": bad_corroboration,
        "pricewatch_variant": pricewatch,
    }
    expect_fail(
        "Tweakers evidence cannot corroborate Tweakers community evidence",
        bad_corroboration,
        mixed,
    )

    print("All Tweakers device-evidence regression checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
