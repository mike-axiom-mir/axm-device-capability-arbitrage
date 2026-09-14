#!/usr/bin/env python3
"""Gate ranking-ready comparisons on explicit market-evidence freshness policy.

This validator does not choose a universal freshness threshold. Instead, any
comparison promoted to evidence_ready/completed must declare the maximum age,
cross-snapshot check-date span, and currency it is willing to treat as a
comparable market window.
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


def positive_int(value: Any, context: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 1:
        raise ValidationError(f"{context} must be a positive integer")
    return value


def market_snapshot_path(value: Any, context: str) -> tuple[Path, str]:
    text = require_string(value, context)
    if "\\" in text:
        raise ValidationError(f"{context} must use repository POSIX separators")
    rel = PurePosixPath(text)
    if rel.is_absolute() or not rel.parts or rel.parts[0] != "market_snapshots":
        raise ValidationError(f"{context} must point beneath market_snapshots/")
    if any(part in {".", ".."} for part in rel.parts):
        raise ValidationError(f"{context} must not contain '.' or '..' path segments")
    if rel.suffix.lower() not in YAML_SUFFIXES:
        raise ValidationError(f"{context} must reference a YAML file")
    path = ROOT.joinpath(*rel.parts)
    if not path.is_file():
        raise ValidationError(f"{context} references missing snapshot {text!r}")
    return path, text


def validate_policy(
    raw_policy: Any,
    *,
    comparison_id: str,
    status: str,
    comparison_date: date,
    refs: Any,
) -> tuple[str, int, int, int]:
    if raw_policy is None:
        if status in RANKING_READY_STATES:
            raise ValidationError(
                f"{comparison_id} is {status!r} but has no market_evidence_policy"
            )
        return "deferred", 0, 0, 0

    if not isinstance(raw_policy, dict):
        raise ValidationError(f"{comparison_id}.market_evidence_policy must be a mapping")

    currency = require_string(
        raw_policy.get("currency"),
        f"{comparison_id}.market_evidence_policy.currency",
    )
    if len(currency) != 3 or currency.upper() != currency:
        raise ValidationError(
            f"{comparison_id}.market_evidence_policy.currency must be a three-letter uppercase code"
        )

    max_age = positive_int(
        raw_policy.get("max_snapshot_age_days"),
        f"{comparison_id}.market_evidence_policy.max_snapshot_age_days",
    )
    max_span = positive_int(
        raw_policy.get("max_cross_snapshot_check_span_days"),
        f"{comparison_id}.market_evidence_policy.max_cross_snapshot_check_span_days",
    )

    if not isinstance(refs, list) or not refs:
        raise ValidationError(
            f"{comparison_id} declares market_evidence_policy but has no market_snapshot_refs"
        )

    snapshot_dates: list[date] = []
    seen_paths: set[str] = set()

    for index, raw_ref in enumerate(refs):
        context = f"{comparison_id}.market_snapshot_refs[{index}]"
        path, rel = market_snapshot_path(raw_ref, context)
        if rel in seen_paths:
            raise ValidationError(f"{comparison_id}.market_snapshot_refs repeats {rel!r}")
        seen_paths.add(rel)

        snapshot = load_yaml(path)
        snapshot_date = canonical_date(snapshot.get("checked_at"), f"{rel}.checked_at")
        snapshot_currency = require_string(snapshot.get("currency"), f"{rel}.currency")

        if snapshot_date > comparison_date:
            raise ValidationError(
                f"{comparison_id} checked_at predates linked market snapshot {rel}"
            )

        age_days = (comparison_date - snapshot_date).days
        if age_days > max_age:
            raise ValidationError(
                f"{comparison_id} links {rel} aged {age_days} day(s), exceeding "
                f"market_evidence_policy.max_snapshot_age_days={max_age}"
            )

        if snapshot_currency != currency:
            raise ValidationError(
                f"{comparison_id} market policy currency={currency!r} but {rel} "
                f"currency={snapshot_currency!r}"
            )

        snapshot_dates.append(snapshot_date)

    span_days = (max(snapshot_dates) - min(snapshot_dates)).days
    if span_days > max_span:
        raise ValidationError(
            f"{comparison_id} linked market snapshots span {span_days} day(s), exceeding "
            f"market_evidence_policy.max_cross_snapshot_check_span_days={max_span}"
        )

    return currency, max_age, max_span, span_days


def validate_comparison(path: Path) -> str:
    rel = path.relative_to(ROOT).as_posix()
    data = load_yaml(path)
    comparison_id = require_string(data.get("comparison_id"), f"{rel}.comparison_id")
    status = require_string(data.get("status"), f"{rel}.status")
    comparison_date = canonical_date(data.get("checked_at"), f"{rel}.checked_at")

    currency, max_age, max_span, span = validate_policy(
        data.get("market_evidence_policy"),
        comparison_id=comparison_id,
        status=status,
        comparison_date=comparison_date,
        refs=data.get("market_snapshot_refs"),
    )

    if currency == "deferred":
        return (
            f"{comparison_id}; status={status}; market freshness policy deferred "
            "until ranking-ready promotion"
        )
    return (
        f"{comparison_id}; status={status}; currency={currency}; "
        f"max_age={max_age}d; max_cross_snapshot_span={max_span}d; observed_span={span}d"
    )


def main() -> int:
    comparison_paths = sorted((ROOT / "comparisons").glob("**/*.yaml"))
    if not comparison_paths:
        print("FAIL no comparison YAML records found", file=sys.stderr)
        return 1

    errors: list[str] = []
    for path in comparison_paths:
        rel = path.relative_to(ROOT)
        try:
            summary = validate_comparison(path)
            print(f"PASS {rel}: {summary}")
        except (ValidationError, OSError) as exc:
            errors.append(f"FAIL {rel}: {exc}")

    print()
    print(f"Checked {len(comparison_paths)} comparison market-evidence window policy record(s).")

    if errors:
        print("\nValidation errors:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(
        "Ranking-ready comparisons cannot rely on undeclared, stale, "
        "cross-window, or mixed-currency market snapshots."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
