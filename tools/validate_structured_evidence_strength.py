#!/usr/bin/env python3
"""Gate positive record/core/structured truth states against evidence strength.

The base record validator guarantees the required structure and resolves
recovery/locality source_claim_ids. This guard adds semantic strength rules:
positive record summaries, execution surfaces, and flat recovery summaries may
not outrun the strongest positive evidence claim in the record, while structured
recovery/locality states may not outrun the positive claims they explicitly cite.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]

POSITIVE_TRUTH_RANK = {
    "DOCUMENTED": 1,
    "COMMUNITY_VERIFIED": 2,
    "LOCALLY_VERIFIED": 3,
    "REPRODUCIBLE": 4,
}

NON_PROMOTING_STATES = {
    "UNRESEARCHED",
    "DEPRECATED",
    "CONTRADICTED",
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


def evidence_claim_states(data: dict[str, Any]) -> dict[str, str]:
    evidence = data.get("evidence")
    if not isinstance(evidence, dict):
        raise ValidationError("evidence must be a mapping")

    claims = evidence.get("claims")
    if not isinstance(claims, list):
        raise ValidationError("evidence.claims must be a list")

    states: dict[str, str] = {}
    for index, claim in enumerate(claims):
        if not isinstance(claim, dict):
            raise ValidationError(f"evidence.claims[{index}] must be a mapping")
        claim_id = claim.get("id")
        state = claim.get("state")
        if not isinstance(claim_id, str) or not claim_id.strip():
            raise ValidationError(f"evidence.claims[{index}].id must be a non-empty string")
        if claim_id in states:
            raise ValidationError(f"duplicate evidence claim id: {claim_id}")
        if state not in POSITIVE_TRUTH_RANK and state not in NON_PROMOTING_STATES:
            raise ValidationError(
                f"evidence claim {claim_id!r} has unsupported truth state {state!r}"
            )
        states[claim_id] = state
    return states


def strongest_positive_claim(claim_states: dict[str, str]) -> tuple[str, str] | None:
    positive = [
        (claim_id, state)
        for claim_id, state in claim_states.items()
        if state in POSITIVE_TRUTH_RANK
    ]
    if not positive:
        return None
    return max(positive, key=lambda item: POSITIVE_TRUTH_RANK[item[1]])


def gate_state_against_record_claims(
    state: Any,
    *,
    context: str,
    claim_states: dict[str, str],
) -> str | None:
    """Apply a conservative record-level evidence ceiling to an unlinked state."""

    if state in NON_PROMOTING_STATES:
        return None
    if state not in POSITIVE_TRUTH_RANK:
        raise ValidationError(f"{context} has unsupported truth state {state!r}")

    strongest = strongest_positive_claim(claim_states)
    if strongest is None:
        raise ValidationError(
            f"{context} claims {state} but the record contains no positive evidence claim"
        )

    strongest_claim_id, strongest_claim_state = strongest
    if POSITIVE_TRUTH_RANK[state] > POSITIVE_TRUTH_RANK[strongest_claim_state]:
        raise ValidationError(
            f"{context} claims {state} but strongest positive evidence claim is "
            f"{strongest_claim_state} ({strongest_claim_id})"
        )
    return strongest_claim_state


def gate_overall_state(
    data: dict[str, Any],
    *,
    claim_states: dict[str, str],
) -> tuple[str, str | None]:
    evidence = data.get("evidence")
    if not isinstance(evidence, dict):
        raise ValidationError("evidence must be a mapping")

    overall_state = evidence.get("overall_state")
    strongest_claim_state = gate_state_against_record_claims(
        overall_state,
        context="evidence.overall_state",
        claim_states=claim_states,
    )
    return str(overall_state), strongest_claim_state


def validate_execution_surfaces(
    data: dict[str, Any],
    *,
    claim_states: dict[str, str],
) -> int:
    execution = data.get("execution")
    if not isinstance(execution, dict):
        raise ValidationError("execution must be a mapping")

    surfaces = execution.get("surfaces")
    if not isinstance(surfaces, list):
        raise ValidationError("execution.surfaces must be a list")

    for index, surface in enumerate(surfaces):
        context = f"execution.surfaces[{index}]"
        if not isinstance(surface, dict):
            raise ValidationError(f"{context} must be a mapping")
        gate_state_against_record_claims(
            surface.get("state"),
            context=f"{context}.state",
            claim_states=claim_states,
        )
    return len(surfaces)


def validate_recovery_summary(
    data: dict[str, Any],
    *,
    claim_states: dict[str, str],
) -> str:
    recovery = data.get("recovery")
    if not isinstance(recovery, dict):
        raise ValidationError("recovery must be a mapping")

    recovery_state = recovery.get("recovery_state")
    gate_state_against_record_claims(
        recovery_state,
        context="recovery.recovery_state",
        claim_states=claim_states,
    )
    return str(recovery_state)


def gate_entry(
    entry: dict[str, Any],
    *,
    context: str,
    claim_states: dict[str, str],
) -> None:
    entry_state = entry.get("state")
    if entry_state in NON_PROMOTING_STATES:
        return
    if entry_state not in POSITIVE_TRUTH_RANK:
        raise ValidationError(f"{context}.state has unsupported truth state {entry_state!r}")

    source_claim_ids = entry.get("source_claim_ids")
    if not isinstance(source_claim_ids, list) or not source_claim_ids:
        raise ValidationError(f"{context}.source_claim_ids must be a non-empty list")

    positive_support: list[tuple[str, str]] = []
    for claim_id in source_claim_ids:
        if not isinstance(claim_id, str) or not claim_id.strip():
            raise ValidationError(f"{context}.source_claim_ids entries must be non-empty strings")
        if claim_id not in claim_states:
            raise ValidationError(
                f"{context}.source_claim_ids references unknown evidence claim {claim_id!r}"
            )
        claim_state = claim_states[claim_id]
        if claim_state in POSITIVE_TRUTH_RANK:
            positive_support.append((claim_id, claim_state))

    if not positive_support:
        states = ", ".join(
            f"{claim_id}:{claim_states[claim_id]}"
            for claim_id in source_claim_ids
            if claim_id in claim_states
        )
        raise ValidationError(
            f"{context} claims {entry_state} but has no positive supporting evidence "
            f"state among its cited claims ({states or 'none'})"
        )

    strongest_claim_id, strongest_claim_state = max(
        positive_support,
        key=lambda item: POSITIVE_TRUTH_RANK[item[1]],
    )
    if POSITIVE_TRUTH_RANK[entry_state] > POSITIVE_TRUTH_RANK[strongest_claim_state]:
        raise ValidationError(
            f"{context} claims {entry_state} but strongest cited evidence is "
            f"{strongest_claim_state} ({strongest_claim_id})"
        )


def validate_collection(
    data: dict[str, Any],
    *,
    section_name: str,
    collection_name: str,
    claim_states: dict[str, str],
) -> int:
    section = data.get(section_name)
    if not isinstance(section, dict):
        return 0

    entries = section.get(collection_name)
    if entries is None:
        return 0
    if not isinstance(entries, list):
        raise ValidationError(f"{section_name}.{collection_name} must be a list")

    for index, entry in enumerate(entries):
        context = f"{section_name}.{collection_name}[{index}]"
        if not isinstance(entry, dict):
            raise ValidationError(f"{context} must be a mapping")
        gate_entry(entry, context=context, claim_states=claim_states)
    return len(entries)


def validate_device(path: Path) -> tuple[str, str | None, int, str, int, int]:
    data = load_yaml(path)
    claim_states = evidence_claim_states(data)
    overall_state, strongest_claim_state = gate_overall_state(
        data,
        claim_states=claim_states,
    )
    execution_count = validate_execution_surfaces(
        data,
        claim_states=claim_states,
    )
    recovery_state = validate_recovery_summary(
        data,
        claim_states=claim_states,
    )
    recovery_count = validate_collection(
        data,
        section_name="recovery",
        collection_name="paths",
        claim_states=claim_states,
    )
    locality_count = validate_collection(
        data,
        section_name="locality",
        collection_name="states",
        claim_states=claim_states,
    )
    return (
        overall_state,
        strongest_claim_state,
        execution_count,
        recovery_state,
        recovery_count,
        locality_count,
    )


def main() -> int:
    device_paths = sorted((ROOT / "devices").glob("**/*.yaml"))
    if not device_paths:
        print("FAIL no device YAML records found", file=sys.stderr)
        return 1

    errors: list[str] = []
    execution_surfaces = 0
    recovery_entries = 0
    locality_entries = 0
    positive_overall_records = 0
    non_promoting_overall_records = 0

    for path in device_paths:
        rel = path.relative_to(ROOT)
        try:
            (
                overall_state,
                strongest_claim_state,
                execution_count,
                recovery_state,
                recovery_count,
                locality_count,
            ) = validate_device(path)
            execution_surfaces += execution_count
            recovery_entries += recovery_count
            locality_entries += locality_count
            if strongest_claim_state is None:
                non_promoting_overall_records += 1
                evidence_summary = f"overall={overall_state} (non-promoting)"
            else:
                positive_overall_records += 1
                evidence_summary = (
                    f"overall={overall_state}, strongest_claim={strongest_claim_state}"
                )
            print(
                f"PASS {rel}: {evidence_summary}; "
                f"{execution_count} execution surface(s), "
                f"recovery_summary={recovery_state}, "
                f"{recovery_count} recovery path(s), {locality_count} locality state(s)"
            )
        except (ValidationError, OSError) as exc:
            errors.append(f"FAIL {rel}: {exc}")

    print()
    print(
        "Checked evidence strength across "
        f"{len(device_paths)} device record(s): "
        f"{positive_overall_records} positive overall state(s), "
        f"{non_promoting_overall_records} non-promoting overall state(s), "
        f"{execution_surfaces} execution surface(s), "
        f"{recovery_entries} recovery path(s), {locality_entries} locality state(s)."
    )

    if errors:
        print("\nValidation errors:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(
        "All positive record summaries, execution/recovery summaries, and structured "
        "recovery/locality truth states stay within the available positive evidence ceiling."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
