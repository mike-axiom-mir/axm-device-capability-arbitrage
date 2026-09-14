#!/usr/bin/env python3
"""Validate repository-local artifacts referenced by capability comparisons.

This gate protects link integrity and contract/date coherence between comparison
records and their market/workload artifacts. It does not judge external source
quality or turn an artifact reference into physical-device verification.
"""
from __future__ import annotations

import sys
from datetime import date
from pathlib import Path, PurePosixPath
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
RANKING_READY_STATES = {"evidence_ready", "completed"}
YAML_SUFFIXES = {".yaml", ".yml"}


class ValidationError(Exception):
    pass


def load_yaml(path: Path) -> dict[str, Any]:
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        raise ValidationError(f"{path}: invalid YAML: {exc}") from exc
    if not isinstance(data, dict):
        raise ValidationError(f"{path}: top-level YAML value must be a mapping")
    return data


def require_string(value: Any, context: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValidationError(f"{context} must be a non-empty string")
    return value.strip()


def canonical_date(value: Any, context: str) -> date:
    text = require_string(value, context)
    try:
        parsed = date.fromisoformat(text)
    except ValueError as exc:
        raise ValidationError(f"{context} must be canonical ISO YYYY-MM-DD") from exc
    if parsed.isoformat() != text:
        raise ValidationError(f"{context} must be canonical ISO YYYY-MM-DD")
    return parsed


def repo_artifact_path(value: Any, *, root_dir: str, context: str) -> tuple[Path, str]:
    text = require_string(value, context)
    if "\\" in text:
        raise ValidationError(f"{context} must use repository POSIX separators")

    rel = PurePosixPath(text)
    if rel.is_absolute() or not rel.parts or rel.parts[0] != root_dir:
        raise ValidationError(f"{context} must point beneath {root_dir}/")
    if any(part in {".", ".."} for part in rel.parts):
        raise ValidationError(f"{context} must not contain '.' or '..' path segments")
    if rel.suffix.lower() not in YAML_SUFFIXES:
        raise ValidationError(f"{context} must reference a YAML file")

    path = ROOT.joinpath(*rel.parts)
    try:
        resolved = path.resolve()
        root_resolved = ROOT.resolve()
    except OSError as exc:
        raise ValidationError(f"{context} could not be resolved: {exc}") from exc
    if resolved != root_resolved and root_resolved not in resolved.parents:
        raise ValidationError(f"{context} escapes repository root")
    if not resolved.is_file():
        raise ValidationError(f"{context} references missing artifact {text!r}")
    return resolved, text


def validate_market_refs(
    refs: Any,
    *,
    comparison_id: str,
    contract_id: str,
    comparison_date: date,
) -> int:
    if not isinstance(refs, list) or not refs:
        raise ValidationError(f"{comparison_id}.market_snapshot_refs must be a non-empty list")

    seen_paths: set[str] = set()
    seen_snapshot_ids: set[str] = set()
    for index, raw_ref in enumerate(refs):
        context = f"{comparison_id}.market_snapshot_refs[{index}]"
        path, rel = repo_artifact_path(raw_ref, root_dir="market_snapshots", context=context)
        if rel in seen_paths:
            raise ValidationError(f"{comparison_id}.market_snapshot_refs repeats {rel!r}")
        seen_paths.add(rel)

        snapshot = load_yaml(path)
        snapshot_id = require_string(snapshot.get("snapshot_id"), f"{rel}.snapshot_id")
        if snapshot_id in seen_snapshot_ids:
            raise ValidationError(
                f"{comparison_id}.market_snapshot_refs resolves duplicate snapshot_id {snapshot_id!r}"
            )
        seen_snapshot_ids.add(snapshot_id)

        snapshot_contract = require_string(snapshot.get("contract_id"), f"{rel}.contract_id")
        if snapshot_contract != contract_id:
            raise ValidationError(
                f"{comparison_id} contract_id={contract_id!r} but {rel} "
                f"contract_id={snapshot_contract!r}"
            )

        snapshot_date = canonical_date(snapshot.get("checked_at"), f"{rel}.checked_at")
        if snapshot_date > comparison_date:
            raise ValidationError(
                f"{comparison_id} checked_at predates linked market snapshot {rel}"
            )

    return len(seen_paths)


def validate_workload_ref(
    raw_ref: Any,
    *,
    comparison_id: str,
    contract_id: str,
) -> str:
    context = f"{comparison_id}.workload_ref"
    path, rel = repo_artifact_path(raw_ref, root_dir="workloads", context=context)
    workload = load_yaml(path)
    workload_id = require_string(workload.get("workload_id"), f"{rel}.workload_id")
    workload_contract = require_string(workload.get("contract_id"), f"{rel}.contract_id")
    if workload_contract != contract_id:
        raise ValidationError(
            f"{comparison_id} contract_id={contract_id!r} but {rel} "
            f"contract_id={workload_contract!r}"
        )
    return workload_id


def validate_comparison(path: Path) -> tuple[str, int, bool]:
    rel = path.relative_to(ROOT).as_posix()
    data = load_yaml(path)
    comparison_id = require_string(data.get("comparison_id"), f"{rel}.comparison_id")
    contract_id = require_string(data.get("contract_id"), f"{rel}.contract_id")
    comparison_date = canonical_date(data.get("checked_at"), f"{rel}.checked_at")
    status = require_string(data.get("status"), f"{rel}.status")

    market_refs = data.get("market_snapshot_refs")
    workload_ref = data.get("workload_ref")

    if status in RANKING_READY_STATES:
        if market_refs is None:
            raise ValidationError(
                f"{comparison_id} is {status!r} but has no market_snapshot_refs"
            )
        if workload_ref is None:
            raise ValidationError(f"{comparison_id} is {status!r} but has no workload_ref")

    market_count = 0
    if market_refs is not None:
        market_count = validate_market_refs(
            market_refs,
            comparison_id=comparison_id,
            contract_id=contract_id,
            comparison_date=comparison_date,
        )

    has_workload = workload_ref is not None
    if has_workload:
        validate_workload_ref(
            workload_ref,
            comparison_id=comparison_id,
            contract_id=contract_id,
        )

    return comparison_id, market_count, has_workload


def main() -> int:
    comparison_paths = sorted((ROOT / "comparisons").glob("**/*.yaml"))
    if not comparison_paths:
        print("FAIL no comparison YAML records found", file=sys.stderr)
        return 1

    errors: list[str] = []
    linked_markets = 0
    linked_workloads = 0

    for path in comparison_paths:
        rel = path.relative_to(ROOT)
        try:
            comparison_id, market_count, has_workload = validate_comparison(path)
            linked_markets += market_count
            linked_workloads += int(has_workload)
            print(
                f"PASS {rel}: {comparison_id}; "
                f"{market_count} market snapshot ref(s); workload_ref={has_workload}"
            )
        except (ValidationError, OSError) as exc:
            errors.append(f"FAIL {rel}: {exc}")

    print()
    print(
        f"Checked {len(comparison_paths)} comparison record(s): "
        f"{linked_markets} market snapshot link(s), {linked_workloads} workload link(s)."
    )

    if errors:
        print("\nValidation errors:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(
        "All present comparison artifact references resolve inside the repository, "
        "match the comparison contract, and preserve date coherence."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
