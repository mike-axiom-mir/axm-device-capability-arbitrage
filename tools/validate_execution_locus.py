#!/usr/bin/env python3
"""Validate optional per-surface execution-locus annotations.

The field is additive: old device records remain valid without `locus`. When a
surface declares it, the value must use the bounded vocabulary, must not
contradict the physical-device meaning of `custom_code`, and must remain
traceable to evidence claims in the same device record.
"""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]

ALLOWED_LOCI = {"on_device", "remote_service", "split", "unknown"}
ALLOWED_CUSTOM_CODE = {True, False, "unknown"}


class ValidationError(Exception):
    pass


def validate_surface(
    surface: dict[str, Any],
    context: str,
    claim_ids: set[str],
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
    for index, claim_id in enumerate(source_claim_ids):
        ref_context = f"{context}.source_claim_ids[{index}]"
        if not isinstance(claim_id, str) or not claim_id.strip():
            raise ValidationError(f"{ref_context} must be a non-empty string")
        if claim_id in seen_refs:
            raise ValidationError(f"{context}.source_claim_ids contains duplicate {claim_id!r}")
        seen_refs.add(claim_id)
        if claim_id not in claim_ids:
            raise ValidationError(
                f"{ref_context} references unknown evidence claim {claim_id!r}"
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

    claim_ids: set[str] = set()
    for index, claim in enumerate(claims):
        context = f"evidence.claims[{index}]"
        if not isinstance(claim, dict):
            raise ValidationError(f"{context} must be a mapping")
        claim_id = claim.get("id")
        if not isinstance(claim_id, str) or not claim_id.strip():
            raise ValidationError(f"{context}.id must be a non-empty string")
        if claim_id in claim_ids:
            raise ValidationError(f"duplicate evidence claim id: {claim_id}")
        claim_ids.add(claim_id)

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
        if validate_surface(surface, context, claim_ids):
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

    print("Execution-locus annotations are structurally consistent and evidence-linked.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
