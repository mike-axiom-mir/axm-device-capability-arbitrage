#!/usr/bin/env python3
"""Gate Tweakers-derived device evidence against its declared evidence role.

Tweakers is valuable for Dutch discovery, market context, and community leads, but
its different surfaces must not be silently promoted into the same kind of device
truth. This validator is intentionally narrow:

* Vraag & Aanbod is acquisition evidence, not a positive device-capability claim.
* Pricewatch may support bounded variant/specification/retail cross-checks, but it
  may not by itself promote a claim above DOCUMENTED.
* Tweakers community/forum evidence is secondary. When it is the primary source
  of a positive device claim, the record must point to explicit stronger
  corroboration in another positive claim.

The gate does not fetch URLs or decide whether a manufacturer/upstream/source-code
source is factually correct. It preserves the evidence relationship so reviewers
can inspect it instead of inheriting forum anecdotes as machine truth.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

import yaml

ROOT = Path(__file__).resolve().parents[1]

POSITIVE_STATES = {
    "DOCUMENTED",
    "COMMUNITY_VERIFIED",
    "LOCALLY_VERIFIED",
    "REPRODUCIBLE",
}
NON_PROMOTING_STATES = {
    "UNRESEARCHED",
    "DEPRECATED",
    "CONTRADICTED",
}

COMMUNITY_SURFACES = {
    "tweakers_forum_thread",
    "tweakers_user_review",
}
PRICEWATCH_SURFACES = {
    "tweakers_pricewatch_product",
    "tweakers_pricewatch_history",
}
MARKET_SURFACES = {
    "tweakers_vraag_en_aanbod_listing",
}
PRICEWATCH_SCOPES = {
    "variant_crosscheck",
    "specification_crosscheck",
    "retail_context",
    "historical_retail_context",
}
CORROBORATION_KINDS = {
    "manufacturer_documentation",
    "upstream_project_documentation",
    "working_source_code",
    "local_reproduction",
}


class ValidationError(Exception):
    pass


def load_yaml(path: Path) -> dict[str, Any]:
    try:
        raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        raise ValidationError(f"invalid YAML: {exc}") from exc
    if not isinstance(raw, dict):
        raise ValidationError("top-level YAML value must be a mapping")
    return raw


def require_string(value: Any, context: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValidationError(f"{context} must be a non-empty string")
    return value.strip()


def require_string_list(value: Any, context: str) -> list[str]:
    if not isinstance(value, list) or not value:
        raise ValidationError(f"{context} must be a non-empty list")
    result: list[str] = []
    seen: set[str] = set()
    for index, item in enumerate(value):
        text = require_string(item, f"{context}[{index}]")
        if text in seen:
            raise ValidationError(f"{context} contains duplicate entry {text!r}")
        seen.add(text)
        result.append(text)
    return result


def is_tweakers_host(host: str) -> bool:
    return host == "tweakers.net" or host.endswith(".tweakers.net")


def url_surface(url: str, context: str) -> str | None:
    text = require_string(url, context)
    parsed = urlparse(text)
    # This is a Tweakers-specific gate, not a generic source-URL validator.
    # Repository/local evidence references may use another representation and
    # must remain the responsibility of their own gates.
    if parsed.scheme not in {"http", "https"} or not parsed.hostname:
        return None
    host = parsed.hostname.lower().rstrip(".")
    path = parsed.path.lower()
    if not is_tweakers_host(host):
        return None
    if host == "gathering.tweakers.net":
        return "community"
    if path.startswith("/aanbod/"):
        return "market"
    if path.startswith("/pricewatch/"):
        return "pricewatch"
    if path.startswith("/reviews/") or path.startswith("/productreview/"):
        return "community"
    return "other_tweakers"


def declared_surface_kind(claim: dict[str, Any], context: str) -> str | None:
    raw = claim.get("source_surface")
    if raw is None:
        return None
    surface = require_string(raw, f"{context}.source_surface")
    if surface in COMMUNITY_SURFACES:
        return "community"
    if surface in PRICEWATCH_SURFACES:
        return "pricewatch"
    if surface in MARKET_SURFACES:
        return "market"
    if surface.startswith("tweakers_"):
        return "other_tweakers"
    return None


def claim_sources(claim: dict[str, Any], context: str) -> list[str]:
    primary = require_string(claim.get("source"), f"{context}.source")
    sources = [primary]
    additional = claim.get("additional_sources")
    if additional is not None:
        sources.extend(require_string_list(additional, f"{context}.additional_sources"))
    return sources


def build_claim_index(claims: list[Any], record_context: str) -> dict[str, dict[str, Any]]:
    index: dict[str, dict[str, Any]] = {}
    for claim_index, claim in enumerate(claims):
        context = f"{record_context}.evidence.claims[{claim_index}]"
        if not isinstance(claim, dict):
            raise ValidationError(f"{context} must be a mapping")
        claim_id = require_string(claim.get("id"), f"{context}.id")
        if claim_id in index:
            raise ValidationError(f"{record_context}: duplicate evidence claim id {claim_id!r}")
        index[claim_id] = claim
    return index


def validate_corroboration(
    claim: dict[str, Any],
    *,
    claim_id: str,
    context: str,
    claims_by_id: dict[str, dict[str, Any]],
) -> None:
    entries = claim.get("tweakers_corroboration")
    if not isinstance(entries, list) or not entries:
        raise ValidationError(
            f"{context}: positive Tweakers community claim requires a non-empty "
            "tweakers_corroboration list"
        )

    seen_refs: set[str] = set()
    valid = 0
    for index, entry in enumerate(entries):
        entry_context = f"{context}.tweakers_corroboration[{index}]"
        if not isinstance(entry, dict):
            raise ValidationError(f"{entry_context} must be a mapping")
        ref_id = require_string(entry.get("claim_id"), f"{entry_context}.claim_id")
        kind = require_string(entry.get("kind"), f"{entry_context}.kind")
        if kind not in CORROBORATION_KINDS:
            allowed = ", ".join(sorted(CORROBORATION_KINDS))
            raise ValidationError(
                f"{entry_context}.kind {kind!r} is not allowed; expected one of: {allowed}"
            )
        if ref_id == claim_id:
            raise ValidationError(f"{entry_context}.claim_id may not self-reference {claim_id!r}")
        if ref_id in seen_refs:
            raise ValidationError(f"{context}: duplicate corroboration claim {ref_id!r}")
        seen_refs.add(ref_id)

        referenced = claims_by_id.get(ref_id)
        if referenced is None:
            raise ValidationError(
                f"{entry_context}.claim_id references unknown evidence claim {ref_id!r}"
            )
        ref_state = require_string(
            referenced.get("state"), f"{entry_context}.referenced_claim.state"
        )
        if ref_state not in POSITIVE_STATES:
            raise ValidationError(
                f"{entry_context}: corroborating claim {ref_id!r} is {ref_state}, "
                "not positive evidence"
            )

        ref_source = require_string(
            referenced.get("source"), f"{entry_context}.referenced_claim.source"
        )
        ref_surface = url_surface(ref_source, f"{entry_context}.referenced_claim.source")
        if ref_surface in {"community", "market", "pricewatch", "other_tweakers"}:
            raise ValidationError(
                f"{entry_context}: corroborating claim {ref_id!r} must be grounded in "
                "a non-Tweakers primary source"
            )
        valid += 1

    if valid == 0:
        raise ValidationError(f"{context}: no valid corroboration claim remains")


def validate_claim(
    claim: dict[str, Any],
    *,
    claim_index: int,
    record_context: str,
    claims_by_id: dict[str, dict[str, Any]],
) -> tuple[int, int, int]:
    context = f"{record_context}.evidence.claims[{claim_index}]"
    claim_id = require_string(claim.get("id"), f"{context}.id")
    state = require_string(claim.get("state"), f"{context}.state")
    if state not in POSITIVE_STATES and state not in NON_PROMOTING_STATES:
        raise ValidationError(f"{context}.state has unsupported truth state {state!r}")

    sources = claim_sources(claim, context)
    inferred = [url_surface(url, f"{context}.source[{index}]") for index, url in enumerate(sources)]
    declared = declared_surface_kind(claim, context)

    has_community = declared == "community" or "community" in inferred
    has_pricewatch = declared == "pricewatch" or "pricewatch" in inferred
    has_market = declared == "market" or "market" in inferred

    primary_kind = url_surface(sources[0], f"{context}.source")
    if declared is not None:
        # A Tweakers source_surface describes the primary source. A recognized
        # Tweakers label on a non-Tweakers URL (or the wrong Tweakers surface)
        # is provenance drift and must fail explicitly.
        if primary_kind != declared:
            raise ValidationError(
                f"{context}.source_surface declares {declared!r} but primary URL "
                f"classifies as {primary_kind!r}"
            )

    if state in POSITIVE_STATES and primary_kind == "market":
        raise ValidationError(
            f"{context}: Tweakers Vraag & Aanbod may support market snapshots, "
            "not a positive device evidence claim"
        )

    if state in POSITIVE_STATES and primary_kind == "pricewatch":
        if state != "DOCUMENTED":
            raise ValidationError(
                f"{context}: Pricewatch-only primary evidence may not promote a "
                f"device claim above DOCUMENTED (found {state})"
            )
        scope = require_string(claim.get("tweakers_evidence_scope"), f"{context}.tweakers_evidence_scope")
        if scope not in PRICEWATCH_SCOPES:
            allowed = ", ".join(sorted(PRICEWATCH_SCOPES))
            raise ValidationError(
                f"{context}.tweakers_evidence_scope {scope!r} is not allowed for "
                f"Pricewatch evidence; expected one of: {allowed}"
            )

    if state in POSITIVE_STATES and primary_kind == "community":
        validate_corroboration(
            claim,
            claim_id=claim_id,
            context=context,
            claims_by_id=claims_by_id,
        )

    # If a community source is merely additional to a non-Tweakers primary
    # source, the positive claim is already grounded elsewhere. It remains
    # secondary evidence and cannot independently raise the claim's state here.
    return int(has_community), int(has_pricewatch), int(has_market)


def validate_device(path: Path) -> tuple[int, int, int, int]:
    data = load_yaml(path)
    evidence = data.get("evidence")
    if not isinstance(evidence, dict):
        raise ValidationError("evidence must be a mapping")
    claims = evidence.get("claims")
    if not isinstance(claims, list):
        raise ValidationError("evidence.claims must be a list")

    rel = path.relative_to(ROOT).as_posix()
    claims_by_id = build_claim_index(claims, rel)
    community = 0
    pricewatch = 0
    market = 0
    for index, claim in enumerate(claims):
        assert isinstance(claim, dict)
        c, p, m = validate_claim(
            claim,
            claim_index=index,
            record_context=rel,
            claims_by_id=claims_by_id,
        )
        community += c
        pricewatch += p
        market += m
    return len(claims), community, pricewatch, market


def main() -> int:
    device_paths = sorted((ROOT / "devices").glob("**/*.yaml"))
    if not device_paths:
        print("FAIL no device YAML records found", file=sys.stderr)
        return 1

    errors: list[str] = []
    total_claims = 0
    community_claims = 0
    pricewatch_claims = 0
    market_claims = 0

    for path in device_paths:
        rel = path.relative_to(ROOT)
        try:
            count, community, pricewatch, market = validate_device(path)
            total_claims += count
            community_claims += community
            pricewatch_claims += pricewatch
            market_claims += market
            print(
                f"PASS {rel}: {count} claim(s); "
                f"Tweakers community={community}, Pricewatch={pricewatch}, V&A={market}"
            )
        except (ValidationError, OSError) as exc:
            errors.append(f"FAIL {rel}: {exc}")

    print()
    print(
        f"Checked {total_claims} evidence claim(s) across {len(device_paths)} device record(s): "
        f"Tweakers community={community_claims}, Pricewatch={pricewatch_claims}, "
        f"Vraag & Aanbod={market_claims}."
    )

    if errors:
        print("\nValidation errors:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(
        "Tweakers device-evidence roles are bounded: community evidence stays secondary, "
        "Pricewatch stays scoped, and Vraag & Aanbod stays out of positive capability claims."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
