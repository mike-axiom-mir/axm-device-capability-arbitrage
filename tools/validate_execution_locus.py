#!/usr/bin/env python3
"""Validate optional per-surface execution-locus annotations.

The field is additive: old device records remain valid without `locus`. When a
surface declares it, the value must use the bounded vocabulary, must not
contradict the physical-device meaning of `custom_code`, and must remain
traceable to evidence claims in the same device record.

Positive locus assertions are also evidence-strength gated: the linked claims
must include positive support at least as strong as the execution surface state.
This prevents an unrelated strong claim elsewhere in the record from masking a
weak, contradicted, deprecated, or unresearched locus citation.
"""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]

ALLOWED_LOCI = {"on_device", "remote_service", "split", "unknown"}
ALLOWED_CUSTOM_CODE = {True, False, "unknown"}
POSITIVE_TRUTH_RANK = {
    "DOCUMENTED": 1,
    "COMMUNITY_VERIFIED": 2,
    "LOCALLY_VERIFIED": 3,
    "REPRODUCIBLE": 4,
}
NON_PROMOTING_STATES = {"UNRESEARCHED", "DEPRECATED", "CONTRADICTED"}
ALL_TRUTH_STATES = set(POSITIVE_TRUTH_RANK) | NON_PROMOTING_STATES
POSITIVE_LOCI = {"on_device", "remote_service", "split"}


class ValidationError(Exception):
    pass


def validate_positive_locus_strength(
    *,
    locus: str,
    surface_state: Any,
    source_claim_ids: list[str],
    claim_states: dict[str, str],
    context: str,
) -> None:
    """Keep an asserted locus within the strength of its explicitly linked claims."""
    if locus not in POSITIVE_LOCI:
        return

    if surface_state not in POSITIVE_TRUTH_RANK:
        raise ValidationError(
            f"{context} declares positive locus {locus!r} but surface state "
            f"{surface_state!r} is not a positive evidence state"
        )

    positive_support = [
        (claim_id, claim_states[claim_id])
        for claim_id in source_claim_ids
        if claim_states[claim_id] in POSITIVE_TRUTH_RANK
    ]
    if not positive_support:
        linked = ", ".join(
            f"{claim_id}:{claim_states[claim_id]}" for claim_id in source_claim_ids
        )
        raise ValidationError(
            f"{context} declares positive locus {locus!r} but its linked claims "
            f"contain no positive support ({linked or 'none'})"
        )

    strongest_claim_id, strongest_claim_state = max(
        positive_support,
        key=lambda item: POSITIVE_TRUTH_RANK[item[1]],
    )
    if POSITIVE_TRUTH_RANK[surface_state] > POSITIVE_TRUTH_RANK[strongest_claim_state]:
        raise ValidationError(
            f"{context}.state claims {surface_state} for locus {locus!r} but strongest "
            f"linked locus evidence is {strongest_claim_state} ({strongest_claim_id})"
        )


def validate_surface(
    surface: dict[str, Any],
    context: str,
    claim_states: dict[str, str],
) -> bool:
    """Validate one surface. Return True when it carries a locus annotation."""
    if "locus" not in surface:
        return False

    locus = surface["locus"]
    if locus not in ALLOWED_LOCI:
        allowed = ", ".join(sorted(ALLOWED_LOCI))
        raise ValidationError(f"{context}.locus has invalid value {locus!r}; allowed: {allowed}")

    custom_code = surface.get("custom_code")
    if custom_code not in ALLOWED_CUSTOM_CODE:
        raise ValidationError(
            f"{context}.custom_code must be true, false, or 'unknown' when locus is present"
        )

    if locus in {"on_device", "split"} and custom_code is not True:
        raise ValidationError(
            f"{context} declares locus {locus!r} but does not declare custom_code: true"
        )

    if locus in {"remote_service", "unknown"} and custom_code is True:
        raise ValidationError(
            f"{context} declares locus {locus!r}; this surface cannot promote endpoint custom_code to true"
        )

    source_claim_ids = surface.get("source_claim_ids")
    if not isinstance(source_claim_ids, list) or not source_claim_ids:
        raise ValidationError(
            f"{context}.source_claim_ids must be a non-empty list when locus is present"
        )

    seen_refs: set[str] = set()
    resolved_claim_ids: list[str] = []
    for index, claim_id in enumerate(source_claim_ids):
        ref_context = f"{context}.source_claim_ids[{index}]"
        if not isinstance(claim_id, str) or not claim_id.strip():
            raise ValidationError(f"{ref_context} must be a non-empty string")
        if claim_id in seen_refs:
            raise ValidationError(f"{context}.source_claim_ids contains duplicate {claim_id!r}")
        seen_refs.add(claim_id)
        if claim_id not in claim_states:
            raise ValidationError(
                f"{ref_context} references unknown evidence claim {claim_id!r}"
            )
        resolved_claim_ids.append(claim_id)

    validate_positive_locus_strength(
        locus=locus,
        surface_state=surface.get("state"),
        source_claim_ids=resolved_claim_ids,
        claim_states=claim_states,
        context=context,
    )

    return True


def validate_device(path: Path) -> int:
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        raise ValidationError(f"invalid YAML: {exc}") from exc

    if not isinstance(data, dict):
        raise ValidationError("top-level YAML must be a mapping")

    evidence = data.get("evidence")
    if not isinstance(evidence, dict):
        raise ValidationError("evidence must be a mapping")
    claims = evidence.get("claims")
    if not isinstance(claims, list):
        raise ValidationError("evidence.claims must be a list")

    claim_states: dict[str, str] = {}
    for index, claim in enumerate(claims):
        context = f"evidence.claims[{index}]"
        if not isinstance(claim, dict):
            raise ValidationError(f"{context} must be a mapping")
        claim_id = claim.get("id")
        if not isinstance(claim_id, str) or not claim_id.strip():
            raise ValidationError(f"{context}.id must be a non-empty string")
        if claim_id in claim_states:
            raise ValidationError(f"duplicate evidence claim id: {claim_id}")
        claim_state = claim.get("state")
        if claim_state not in ALL_TRUTH_STATES:
            raise ValidationError(
                f"{context}.state has unsupported truth state {claim_state!r}"
            )
        claim_states[claim_id] = claim_state

    execution = data.get("execution")
    if not isinstance(execution, dict):
        raise ValidationError("execution must be a mapping")

    surfaces = execution.get("surfaces")
    if not isinstance(surfaces, list) or not surfaces:
        raise ValidationError("execution.surfaces must be a non-empty list")

    annotated = 0
    for index, surface in enumerate(surfaces):
        context = f"execution.surfaces[{index}]"
        if not isinstance(surface, dict):
            raise ValidationError(f"{context} must be a mapping")
        if validate_surface(surface, context, claim_states):
            annotated += 1
    return annotated


def main() -> int:
    paths = sorted((ROOT / "devices").glob("**/*.yaml"))
    if not paths:
        print("FAIL execution locus: no device records found", file=sys.stderr)
        return 1

    errors: list[str] = []
    annotated_total = 0

    for path in paths:
        rel = path.relative_to(ROOT)
        try:
            annotated = validate_device(path)
            annotated_total += annotated
            print(f"PASS {rel}: {annotated} locus annotation(s)")
        except (ValidationError, OSError) as exc:
            errors.append(f"FAIL {rel}: {exc}")

    print()
    print(
        f"Checked {len(paths)} device record(s); "
        f"validated {annotated_total} optional execution-locus annotation(s)."
    )

    if errors:
        print("\nExecution-locus validation errors:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(
        "Execution-locus annotations are structurally consistent, evidence-linked, "
        "and positive locus claims stay within their linked evidence strength."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
