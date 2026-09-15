#!/usr/bin/env python3
"""Validate every machine-readable `source_claim_ids` link in device records.

The census schema is deliberately extensible. Mature structures such as recovery,
locality, and execution locus have dedicated validators, but exploratory per-device
structures may also preserve provenance through `source_claim_ids`. This guard walks
the whole device record and enforces the common evidence-link contract without
freezing or interpreting the surrounding experimental schema.
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
NON_PROMOTING_STATES = {"UNRESEARCHED", "DEPRECATED", "CONTRADICTED"}
ALL_TRUTH_STATES = set(POSITIVE_TRUTH_RANK) | NON_PROMOTING_STATES


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


def build_claim_states(data: dict[str, Any]) -> dict[str, str]:
    evidence = data.get("evidence")
    if not isinstance(evidence, dict):
        raise ValidationError("evidence must be a mapping")
    claims = evidence.get("claims")
    if not isinstance(claims, list):
        raise ValidationError("evidence.claims must be a list")

    states: dict[str, str] = {}
    for index, claim in enumerate(claims):
        context = f"evidence.claims[{index}]"
        if not isinstance(claim, dict):
            raise ValidationError(f"{context} must be a mapping")
        claim_id = require_nonempty_string(claim.get("id"), f"{context}.id")
        if claim_id in states:
            raise ValidationError(f"duplicate evidence claim id: {claim_id}")
        state = require_nonempty_string(claim.get("state"), f"{context}.state")
        if state not in ALL_TRUTH_STATES:
            raise ValidationError(f"{context}.state has unsupported truth state {state!r}")
        states[claim_id] = state
    return states


def validate_link_container(
    container: dict[str, Any],
    *,
    context: str,
    claim_states: dict[str, str],
) -> int:
    """Validate one mapping that declares `source_claim_ids`."""
    raw_refs = container.get("source_claim_ids")
    if not isinstance(raw_refs, list) or not raw_refs:
        raise ValidationError(f"{context}.source_claim_ids must be a non-empty list")

    refs: list[str] = []
    seen: set[str] = set()
    for index, raw_ref in enumerate(raw_refs):
        ref = require_nonempty_string(raw_ref, f"{context}.source_claim_ids[{index}]")
        if ref in seen:
            raise ValidationError(
                f"{context}.source_claim_ids contains duplicate evidence claim {ref!r}"
            )
        seen.add(ref)
        if ref not in claim_states:
            raise ValidationError(
                f"{context}.source_claim_ids references unknown evidence claim {ref!r}"
            )
        refs.append(ref)

    # Only interpret `state` as evidence strength when it is one of the repository's
    # truth-state tokens. Exploratory structures may legitimately use a domain state
    # such as `active`, `stock`, or `restricted`; this generic gate must not freeze
    # those schemas by pretending every field named `state` is an evidence state.
    state = container.get("state")
    if state not in ALL_TRUTH_STATES:
        return 1

    if state in NON_PROMOTING_STATES:
        return 1

    positive_support = [
        (claim_id, claim_states[claim_id])
        for claim_id in refs
        if claim_states[claim_id] in POSITIVE_TRUTH_RANK
    ]
    if not positive_support:
        linked = ", ".join(f"{claim_id}:{claim_states[claim_id]}" for claim_id in refs)
        raise ValidationError(
            f"{context} claims {state} but its source_claim_ids contain no positive "
            f"support ({linked or 'none'})"
        )

    strongest_claim_id, strongest_claim_state = max(
        positive_support,
        key=lambda item: POSITIVE_TRUTH_RANK[item[1]],
    )
    if POSITIVE_TRUTH_RANK[state] > POSITIVE_TRUTH_RANK[strongest_claim_state]:
        raise ValidationError(
            f"{context}.state claims {state} but strongest linked evidence is "
            f"{strongest_claim_state} ({strongest_claim_id})"
        )

    return 1


def walk_source_claim_links(
    node: Any,
    *,
    context: str,
    claim_states: dict[str, str],
) -> int:
    """Recursively find and validate every mapping that carries source_claim_ids."""
    count = 0
    if isinstance(node, dict):
        if "source_claim_ids" in node:
            count += validate_link_container(
                node,
                context=context,
                claim_states=claim_states,
            )
        for key, value in node.items():
            child_context = f"{context}.{key}" if context else str(key)
            count += walk_source_claim_links(
                value,
                context=child_context,
                claim_states=claim_states,
            )
    elif isinstance(node, list):
        for index, value in enumerate(node):
            child_context = f"{context}[{index}]"
            count += walk_source_claim_links(
                value,
                context=child_context,
                claim_states=claim_states,
            )
    return count


def validate_data(data: dict[str, Any]) -> int:
    claim_states = build_claim_states(data)
    return walk_source_claim_links(data, context="device", claim_states=claim_states)


def validate_device(path: Path) -> int:
    return validate_data(load_yaml(path))


def main() -> int:
    paths = sorted((ROOT / "devices").glob("**/*.yaml"))
    if not paths:
        print("FAIL source-claim links: no device records found", file=sys.stderr)
        return 1

    errors: list[str] = []
    link_containers = 0
    for path in paths:
        rel = path.relative_to(ROOT)
        try:
            count = validate_device(path)
            link_containers += count
            print(f"PASS {rel}: {count} source_claim_ids container(s)")
        except (ValidationError, OSError) as exc:
            errors.append(f"FAIL {rel}: {exc}")

    print()
    print(
        f"Checked generic evidence links across {len(paths)} device record(s): "
        f"{link_containers} source_claim_ids container(s)."
    )

    if errors:
        print("\nSource-claim link validation errors:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(
        "Every machine-readable source_claim_ids list is non-empty, unique, resolvable, "
        "and truth-state-bearing containers stay within their linked evidence strength."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
