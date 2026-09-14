#!/usr/bin/env python3
"""Validate evidence-claim scope and machine-readable source-check metadata.

The base record validator checks claim IDs, truth states, and primary-source presence.
This guard closes a different gap: a positive evidence claim must say what the source
actually proves, and device evidence must preserve a parseable date for when the
source packet was checked.
"""

from __future__ import annotations

import sys
from datetime import date
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]

POSITIVE_TRUTH_STATES = {
    "DOCUMENTED",
    "COMMUNITY_VERIFIED",
    "LOCALLY_VERIFIED",
    "REPRODUCIBLE",
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


def require_nonempty_string(value: Any, context: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValidationError(f"{context} must be a non-empty string")
    return value.strip()


def validate_unique_string_list(
    value: Any,
    context: str,
    *,
    allow_empty: bool = False,
) -> list[str]:
    if not isinstance(value, list):
        raise ValidationError(f"{context} must be a list")
    if not value and not allow_empty:
        raise ValidationError(f"{context} must be a non-empty list")

    normalized: list[str] = []
    seen: set[str] = set()
    for index, item in enumerate(value):
        text = require_nonempty_string(item, f"{context}[{index}]")
        if text in seen:
            raise ValidationError(f"{context} contains duplicate entry {text!r}")
        seen.add(text)
        normalized.append(text)
    return normalized


def validate_last_checked(evidence: dict[str, Any]) -> str:
    raw = require_nonempty_string(evidence.get("last_checked"), "evidence.last_checked")
    try:
        parsed = date.fromisoformat(raw)
    except ValueError as exc:
        raise ValidationError(
            "evidence.last_checked must use ISO calendar date format YYYY-MM-DD"
        ) from exc

    # date.fromisoformat is intentionally used only as a syntax/type guard. This
    # validator does not declare evidence stale after an arbitrary age or make
    # source freshness depend on the CI runner's wall clock.
    if parsed.isoformat() != raw:
        raise ValidationError(
            "evidence.last_checked must use canonical ISO calendar date format YYYY-MM-DD"
        )
    return raw


def validate_claim(claim: dict[str, Any], index: int) -> None:
    context = f"evidence.claims[{index}]"

    claim_id = require_nonempty_string(claim.get("id"), f"{context}.id")
    state = require_nonempty_string(claim.get("state"), f"{context}.state")
    primary_source = require_nonempty_string(claim.get("source"), f"{context}.source")

    proves_raw = claim.get("proves")
    if state in POSITIVE_TRUTH_STATES:
        if proves_raw is None:
            raise ValidationError(
                f"{context} ({claim_id}) is {state} but has no proves list"
            )
        proves = validate_unique_string_list(proves_raw, f"{context}.proves")
    elif proves_raw is None:
        proves = []
    else:
        proves = validate_unique_string_list(
            proves_raw,
            f"{context}.proves",
            allow_empty=True,
        )

    does_not_prove_raw = claim.get("does_not_prove")
    if does_not_prove_raw is None:
        does_not_prove: list[str] = []
    else:
        does_not_prove = validate_unique_string_list(
            does_not_prove_raw,
            f"{context}.does_not_prove",
            allow_empty=True,
        )

    overlap = sorted(set(proves) & set(does_not_prove))
    if overlap:
        raise ValidationError(
            f"{context} ({claim_id}) lists the same statement in proves and "
            f"does_not_prove: {overlap[0]!r}"
        )

    additional_sources_raw = claim.get("additional_sources")
    if additional_sources_raw is None:
        return

    additional_sources = validate_unique_string_list(
        additional_sources_raw,
        f"{context}.additional_sources",
    )
    if primary_source in additional_sources:
        raise ValidationError(
            f"{context} ({claim_id}) repeats its primary source in additional_sources"
        )


def validate_device(path: Path) -> tuple[str, int, int]:
    data = load_yaml(path)
    evidence = data.get("evidence")
    if not isinstance(evidence, dict):
        raise ValidationError("evidence must be a mapping")

    checked_at = validate_last_checked(evidence)

    claims = evidence.get("claims")
    if not isinstance(claims, list):
        raise ValidationError("evidence.claims must be a list")

    positive_claims = 0
    for index, claim in enumerate(claims):
        if not isinstance(claim, dict):
            raise ValidationError(f"evidence.claims[{index}] must be a mapping")
        validate_claim(claim, index)
        if claim.get("state") in POSITIVE_TRUTH_STATES:
            positive_claims += 1

    return checked_at, len(claims), positive_claims


def main() -> int:
    device_paths = sorted((ROOT / "devices").glob("**/*.yaml"))
    if not device_paths:
        print("FAIL no device YAML records found", file=sys.stderr)
        return 1

    errors: list[str] = []
    total_claims = 0
    positive_claims = 0

    for path in device_paths:
        rel = path.relative_to(ROOT)
        try:
            checked_at, claim_count, positive_count = validate_device(path)
            total_claims += claim_count
            positive_claims += positive_count
            print(
                f"PASS {rel}: checked={checked_at}; "
                f"{claim_count} claim(s), {positive_count} positive scoped claim(s)"
            )
        except (ValidationError, OSError) as exc:
            errors.append(f"FAIL {rel}: {exc}")

    print()
    print(
        f"Checked evidence-claim scope across {len(device_paths)} device record(s): "
        f"{total_claims} claim(s), {positive_claims} positive claim(s)."
    )

    if errors:
        print("\nValidation errors:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(
        "All positive evidence claims explicitly state what they prove, "
        "claim boundary/source lists are structurally coherent, and every "
        "device evidence packet has a canonical ISO check date."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
