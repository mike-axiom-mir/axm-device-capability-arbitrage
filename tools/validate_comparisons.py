#!/usr/bin/env python3
"""Validate machine-readable capability-arbitrage comparisons.

The comparison layer is intentionally small. It checks references and truth-preserving
status semantics without inventing a universal scoring model.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]

REQUIREMENT_STATUSES = {"pass", "conditional", "unknown", "fail"}
ELIGIBILITY_STATES = {
    "hard_requirements_pass",
    "conditional",
    "blocked_by_unknowns",
    "ineligible",
}
COMPARISON_STATES = {
    "evidence_incomplete",
    "evidence_ready",
    "completed",
    "contradicted",
}
UNKNOWNISH_STRINGS = {"unknown", "not_collected"}


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


def require_nonempty_string(value: Any, context: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValidationError(f"{context} must be a non-empty string")


def resolve_path(data: Any, dotted_path: str, context: str) -> Any:
    require_nonempty_string(dotted_path, context)
    current = data
    for part in dotted_path.split("."):
        if not isinstance(current, dict) or part not in current:
            raise ValidationError(f"{context} references missing path {dotted_path!r}")
        current = current[part]
    return current


def is_unknownish(value: Any) -> bool:
    if value is None:
        return True
    if isinstance(value, str):
        return value.strip().lower() in UNKNOWNISH_STRINGS
    if isinstance(value, list):
        return not value or all(is_unknownish(item) for item in value)
    if isinstance(value, dict):
        return not value or all(is_unknownish(item) for item in value.values())
    return False


def load_index(paths: list[Path], id_key: str) -> dict[str, dict[str, Any]]:
    index: dict[str, dict[str, Any]] = {}
    for path in paths:
        data = load_yaml(path)
        item_id = data.get(id_key)
        require_nonempty_string(item_id, f"{path.relative_to(ROOT)}.{id_key}")
        if item_id in index:
            raise ValidationError(f"duplicate {id_key}: {item_id}")
        index[item_id] = data
    return index


def expected_eligibility(statuses: list[str]) -> str:
    if "fail" in statuses:
        return "ineligible"
    if "unknown" in statuses:
        return "blocked_by_unknowns"
    if "conditional" in statuses:
        return "conditional"
    return "hard_requirements_pass"


def validate_requirement_list(
    items: Any,
    *,
    context: str,
    contract: dict[str, Any],
    device: dict[str, Any],
) -> list[str]:
    if not isinstance(items, list) or not items:
        raise ValidationError(f"{context} must be a non-empty list")

    seen_ids: set[str] = set()
    statuses: list[str] = []

    for index, item in enumerate(items):
        item_context = f"{context}[{index}]"
        if not isinstance(item, dict):
            raise ValidationError(f"{item_context} must be a mapping")

        for key in ("id", "contract_path", "status", "record_paths", "note"):
            if key not in item:
                raise ValidationError(f"{item_context} missing required key {key}")

        requirement_id = item["id"]
        require_nonempty_string(requirement_id, f"{item_context}.id")
        if requirement_id in seen_ids:
            raise ValidationError(f"{context} has duplicate requirement id {requirement_id!r}")
        seen_ids.add(requirement_id)

        contract_path = item["contract_path"]
        resolve_path(contract, contract_path, f"{item_context}.contract_path")

        status = item["status"]
        if status not in REQUIREMENT_STATUSES:
            allowed = ", ".join(sorted(REQUIREMENT_STATUSES))
            raise ValidationError(
                f"{item_context}.status has invalid value {status!r}; allowed: {allowed}"
            )
        statuses.append(status)

        record_paths = item["record_paths"]
        if not isinstance(record_paths, list) or not record_paths:
            raise ValidationError(f"{item_context}.record_paths must be a non-empty list")

        resolved_values: list[Any] = []
        for path_index, record_path in enumerate(record_paths):
            value = resolve_path(
                device,
                record_path,
                f"{item_context}.record_paths[{path_index}]",
            )
            resolved_values.append(value)

        if status in {"pass", "conditional"} and all(
            is_unknownish(value) for value in resolved_values
        ):
            raise ValidationError(
                f"{item_context} is {status!r} but every referenced device value is unknown"
            )

        require_nonempty_string(item["note"], f"{item_context}.note")

    return statuses


def validate_comparison(
    path: Path,
    device_index: dict[str, dict[str, Any]],
    contract_index: dict[str, dict[str, Any]],
    seen_comparison_ids: set[str],
) -> None:
    data = load_yaml(path)

    for key in (
        "comparison_version",
        "comparison_id",
        "contract_id",
        "checked_at",
        "status",
        "decision",
        "candidates",
        "decision_blockers",
        "provisional_findings",
    ):
        if key not in data:
            raise ValidationError(f"comparison missing required key {key}")

    comparison_id = data["comparison_id"]
    require_nonempty_string(comparison_id, "comparison_id")
    if comparison_id in seen_comparison_ids:
        raise ValidationError(f"duplicate comparison_id: {comparison_id}")
    seen_comparison_ids.add(comparison_id)

    contract_id = data["contract_id"]
    require_nonempty_string(contract_id, "contract_id")
    if contract_id not in contract_index:
        raise ValidationError(f"comparison references unknown contract_id {contract_id!r}")
    contract = contract_index[contract_id]

    status = data["status"]
    if status not in COMPARISON_STATES:
        allowed = ", ".join(sorted(COMPARISON_STATES))
        raise ValidationError(f"invalid comparison status {status!r}; allowed: {allowed}")

    require_nonempty_string(data["decision"], "decision")

    truth_rules = data.get("truth_rules")
    if not isinstance(truth_rules, dict) or truth_rules.get("unknown_is_not_pass") is not True:
        raise ValidationError("truth_rules.unknown_is_not_pass must be true")

    candidates = data["candidates"]
    if not isinstance(candidates, list) or not candidates:
        raise ValidationError("candidates must be a non-empty list")

    seen_candidate_ids: set[str] = set()
    for index, candidate in enumerate(candidates):
        context = f"candidates[{index}]"
        if not isinstance(candidate, dict):
            raise ValidationError(f"{context} must be a mapping")

        for key in (
            "record_id",
            "hard_requirement_eligibility",
            "hard_requirements",
            "preferred_evidence",
            "ranking_gaps",
        ):
            if key not in candidate:
                raise ValidationError(f"{context} missing required key {key}")

        record_id = candidate["record_id"]
        require_nonempty_string(record_id, f"{context}.record_id")
        if record_id in seen_candidate_ids:
            raise ValidationError(f"duplicate candidate record_id {record_id!r}")
        seen_candidate_ids.add(record_id)
        if record_id not in device_index:
            raise ValidationError(f"{context} references unknown device record {record_id!r}")
        device = device_index[record_id]

        hard_statuses = validate_requirement_list(
            candidate["hard_requirements"],
            context=f"{context}.hard_requirements",
            contract=contract,
            device=device,
        )
        validate_requirement_list(
            candidate["preferred_evidence"],
            context=f"{context}.preferred_evidence",
            contract=contract,
            device=device,
        )

        eligibility = candidate["hard_requirement_eligibility"]
        if eligibility not in ELIGIBILITY_STATES:
            allowed = ", ".join(sorted(ELIGIBILITY_STATES))
            raise ValidationError(
                f"{context}.hard_requirement_eligibility has invalid value {eligibility!r}; "
                f"allowed: {allowed}"
            )
        derived = expected_eligibility(hard_statuses)
        if eligibility != derived:
            raise ValidationError(
                f"{context}.hard_requirement_eligibility is {eligibility!r} but statuses derive {derived!r}"
            )

        ranking_gaps = candidate["ranking_gaps"]
        if not isinstance(ranking_gaps, list) or not ranking_gaps:
            raise ValidationError(f"{context}.ranking_gaps must be a non-empty list")
        for gap_index, gap in enumerate(ranking_gaps):
            require_nonempty_string(gap, f"{context}.ranking_gaps[{gap_index}]")

    blockers = data["decision_blockers"]
    if not isinstance(blockers, list) or not blockers:
        raise ValidationError("decision_blockers must be a non-empty list")
    for index, blocker in enumerate(blockers):
        context = f"decision_blockers[{index}]"
        if not isinstance(blocker, dict):
            raise ValidationError(f"{context} must be a mapping")
        for key in ("id", "state", "note"):
            if key not in blocker:
                raise ValidationError(f"{context} missing required key {key}")
        require_nonempty_string(blocker["id"], f"{context}.id")
        require_nonempty_string(blocker["state"], f"{context}.state")
        require_nonempty_string(blocker["note"], f"{context}.note")

    findings = data["provisional_findings"]
    if not isinstance(findings, list) or not findings:
        raise ValidationError("provisional_findings must be a non-empty list")
    for index, finding in enumerate(findings):
        require_nonempty_string(finding, f"provisional_findings[{index}]")


def main() -> int:
    device_paths = sorted((ROOT / "devices").glob("**/*.yaml"))
    contract_paths = sorted((ROOT / "capability_contracts").glob("**/*.yaml"))
    comparison_paths = sorted((ROOT / "comparisons").glob("**/*.yaml"))

    if not device_paths:
        print("FAIL no device YAML records found", file=sys.stderr)
        return 1
    if not contract_paths:
        print("FAIL no capability-contract YAML records found", file=sys.stderr)
        return 1
    if not comparison_paths:
        print("FAIL no comparison YAML records found", file=sys.stderr)
        return 1

    try:
        device_index = load_index(device_paths, "record_id")
        contract_index = load_index(contract_paths, "contract_id")
    except (ValidationError, OSError) as exc:
        print(f"FAIL index load: {exc}", file=sys.stderr)
        return 1

    errors: list[str] = []
    seen_comparison_ids: set[str] = set()
    for path in comparison_paths:
        rel = path.relative_to(ROOT)
        try:
            validate_comparison(
                path,
                device_index,
                contract_index,
                seen_comparison_ids,
            )
            print(f"PASS {rel}")
        except (ValidationError, OSError) as exc:
            errors.append(f"FAIL {rel}: {exc}")

    print()
    print(f"Validated {len(comparison_paths)} comparison record(s).")

    if errors:
        print("\nValidation errors:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print("All comparison checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
