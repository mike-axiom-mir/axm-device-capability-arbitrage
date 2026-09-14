#!/usr/bin/env python3
"""Validate dated market snapshots without treating listing prices as market truth."""

from __future__ import annotations

import math
import statistics
import sys
from datetime import date
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]

PRICE_TYPES = {"asking", "displayed_sold_listing_price", "retailer_offer"}
SOURCE_SCOPES = {
    "direct_listing",
    "search_result_snapshot",
    "direct_retailer_offer",
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
    return value


def parse_iso_or_unknown(value: Any, context: str) -> date | None:
    text = require_string(value, context)
    if text == "unknown":
        return None
    try:
        return date.fromisoformat(text)
    except ValueError as exc:
        raise ValidationError(f"{context} must be ISO YYYY-MM-DD or 'unknown'") from exc


def load_ids(paths: list[Path], id_key: str) -> set[str]:
    result: set[str] = set()
    for path in paths:
        data = load_yaml(path)
        item_id = require_string(data.get(id_key), f"{path.relative_to(ROOT)}.{id_key}")
        if item_id in result:
            raise ValidationError(f"duplicate {id_key}: {item_id}")
        result.add(item_id)
    return result


def numeric(value: Any, context: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValidationError(f"{context} must be a number")
    if not math.isfinite(float(value)) or value < 0:
        raise ValidationError(f"{context} must be a finite non-negative number")
    return float(value)


def same_number(left: float, right: float) -> bool:
    return math.isclose(left, right, rel_tol=0.0, abs_tol=1e-9)


def validate_snapshot(
    path: Path,
    *,
    device_ids: set[str],
    contract_ids: set[str],
    seen_snapshot_ids: set[str],
) -> None:
    data = load_yaml(path)

    for key in (
        "snapshot_version",
        "snapshot_id",
        "contract_id",
        "checked_at",
        "currency",
        "scope",
        "method",
        "candidates",
        "decision_use",
    ):
        if key not in data:
            raise ValidationError(f"missing required key {key}")

    snapshot_id = require_string(data["snapshot_id"], "snapshot_id")
    if snapshot_id in seen_snapshot_ids:
        raise ValidationError(f"duplicate snapshot_id: {snapshot_id}")
    seen_snapshot_ids.add(snapshot_id)

    contract_id = require_string(data["contract_id"], "contract_id")
    if contract_id not in contract_ids:
        raise ValidationError(f"unknown contract_id {contract_id!r}")

    checked_at = parse_iso_or_unknown(data["checked_at"], "checked_at")
    if checked_at is None:
        raise ValidationError("checked_at may not be unknown")

    currency = require_string(data["currency"], "currency")
    if len(currency) != 3 or currency.upper() != currency:
        raise ValidationError("currency must be a three-letter uppercase code")

    scope = data["scope"]
    if not isinstance(scope, dict):
        raise ValidationError("scope must be a mapping")
    countries = scope.get("countries")
    if not isinstance(countries, list) or not countries:
        raise ValidationError("scope.countries must be a non-empty list")
    country_set: set[str] = set()
    for index, country in enumerate(countries):
        code = require_string(country, f"scope.countries[{index}]")
        if len(code) != 2 or code.upper() != code:
            raise ValidationError(f"scope.countries[{index}] must be an uppercase two-letter code")
        country_set.add(code)

    start = parse_iso_or_unknown(scope.get("listing_date_start"), "scope.listing_date_start")
    end = parse_iso_or_unknown(scope.get("listing_date_end"), "scope.listing_date_end")
    if start is None or end is None:
        raise ValidationError("scope listing date window may not be unknown")
    if end < start:
        raise ValidationError("scope.listing_date_end must not precede listing_date_start")

    candidates = data["candidates"]
    if not isinstance(candidates, list) or not candidates:
        raise ValidationError("candidates must be a non-empty list")

    seen_candidate_ids: set[str] = set()
    seen_observation_ids: set[str] = set()

    for candidate_index, candidate in enumerate(candidates):
        context = f"candidates[{candidate_index}]"
        if not isinstance(candidate, dict):
            raise ValidationError(f"{context} must be a mapping")

        record_id = require_string(candidate.get("record_id"), f"{context}.record_id")
        if record_id not in device_ids:
            raise ValidationError(f"{context} references unknown device {record_id!r}")
        if record_id in seen_candidate_ids:
            raise ValidationError(f"duplicate candidate record_id {record_id!r}")
        seen_candidate_ids.add(record_id)

        cohorts = candidate.get("cohorts")
        if not isinstance(cohorts, list) or not cohorts:
            raise ValidationError(f"{context}.cohorts must be a non-empty list")

        seen_cohort_ids: set[str] = set()
        for cohort_index, cohort in enumerate(cohorts):
            cohort_context = f"{context}.cohorts[{cohort_index}]"
            if not isinstance(cohort, dict):
                raise ValidationError(f"{cohort_context} must be a mapping")

            cohort_id = require_string(cohort.get("id"), f"{cohort_context}.id")
            if cohort_id in seen_cohort_ids:
                raise ValidationError(f"{context} has duplicate cohort id {cohort_id!r}")
            seen_cohort_ids.add(cohort_id)

            require_string(cohort.get("condition_scope"), f"{cohort_context}.condition_scope")

            observations = cohort.get("observations")
            if not isinstance(observations, list) or not observations:
                raise ValidationError(f"{cohort_context}.observations must be a non-empty list")

            sample_count = cohort.get("sample_count")
            if not isinstance(sample_count, int) or isinstance(sample_count, bool) or sample_count < 1:
                raise ValidationError(f"{cohort_context}.sample_count must be a positive integer")
            if sample_count != len(observations):
                raise ValidationError(
                    f"{cohort_context}.sample_count={sample_count} but has {len(observations)} observations"
                )

            prices: list[float] = []
            for observation_index, observation in enumerate(observations):
                observation_context = f"{cohort_context}.observations[{observation_index}]"
                if not isinstance(observation, dict):
                    raise ValidationError(f"{observation_context} must be a mapping")

                observation_id = require_string(observation.get("id"), f"{observation_context}.id")
                if observation_id in seen_observation_ids:
                    raise ValidationError(f"duplicate observation id {observation_id!r}")
                seen_observation_ids.add(observation_id)

                require_string(observation.get("marketplace"), f"{observation_context}.marketplace")
                country = require_string(observation.get("country"), f"{observation_context}.country")
                if country not in country_set:
                    raise ValidationError(
                        f"{observation_context}.country {country!r} not declared in scope.countries"
                    )

                listed_at = parse_iso_or_unknown(
                    observation.get("listed_at"), f"{observation_context}.listed_at"
                )
                if listed_at is not None and not (start <= listed_at <= end):
                    raise ValidationError(
                        f"{observation_context}.listed_at falls outside snapshot listing window"
                    )

                observation_checked = parse_iso_or_unknown(
                    observation.get("checked_at"), f"{observation_context}.checked_at"
                )
                if observation_checked is None:
                    raise ValidationError(f"{observation_context}.checked_at may not be unknown")
                if observation_checked > checked_at:
                    raise ValidationError(
                        f"{observation_context}.checked_at is later than snapshot checked_at"
                    )

                prices.append(numeric(observation.get("price_eur"), f"{observation_context}.price_eur"))

                price_type = require_string(
                    observation.get("price_type"), f"{observation_context}.price_type"
                )
                if price_type not in PRICE_TYPES:
                    allowed = ", ".join(sorted(PRICE_TYPES))
                    raise ValidationError(
                        f"{observation_context}.price_type {price_type!r} not in {allowed}"
                    )

                require_string(
                    observation.get("seller_class"), f"{observation_context}.seller_class"
                )
                require_string(
                    observation.get("model_identity"), f"{observation_context}.model_identity"
                )

                configuration = observation.get("configuration")
                if not isinstance(configuration, dict) or not configuration:
                    raise ValidationError(
                        f"{observation_context}.configuration must be a non-empty mapping"
                    )

                source = require_string(observation.get("source"), f"{observation_context}.source")
                if not source.startswith(("https://", "http://")):
                    raise ValidationError(f"{observation_context}.source must be an HTTP(S) URL")

                source_scope = require_string(
                    observation.get("source_scope"), f"{observation_context}.source_scope"
                )
                if source_scope not in SOURCE_SCOPES:
                    allowed = ", ".join(sorted(SOURCE_SCOPES))
                    raise ValidationError(
                        f"{observation_context}.source_scope {source_scope!r} not in {allowed}"
                    )
                require_string(observation.get("note"), f"{observation_context}.note")

            stats = cohort.get("descriptive_statistics")
            if not isinstance(stats, dict):
                raise ValidationError(f"{cohort_context}.descriptive_statistics must be a mapping")

            declared_low = numeric(stats.get("low_eur"), f"{cohort_context}.descriptive_statistics.low_eur")
            declared_median = numeric(
                stats.get("median_eur"), f"{cohort_context}.descriptive_statistics.median_eur"
            )
            declared_high = numeric(
                stats.get("high_eur"), f"{cohort_context}.descriptive_statistics.high_eur"
            )

            actual_low = min(prices)
            actual_median = float(statistics.median(prices))
            actual_high = max(prices)
            if not same_number(declared_low, actual_low):
                raise ValidationError(
                    f"{cohort_context} low_eur={declared_low:g}, expected {actual_low:g}"
                )
            if not same_number(declared_median, actual_median):
                raise ValidationError(
                    f"{cohort_context} median_eur={declared_median:g}, expected {actual_median:g}"
                )
            if not same_number(declared_high, actual_high):
                raise ValidationError(
                    f"{cohort_context} high_eur={declared_high:g}, expected {actual_high:g}"
                )

    decision_use = data["decision_use"]
    if not isinstance(decision_use, dict):
        raise ValidationError("decision_use must be a mapping")
    require_string(decision_use.get("ranking_state"), "decision_use.ranking_state")
    for key in ("facts_supported", "not_supported", "next_evidence"):
        values = decision_use.get(key)
        if not isinstance(values, list) or not values:
            raise ValidationError(f"decision_use.{key} must be a non-empty list")
        for index, value in enumerate(values):
            require_string(value, f"decision_use.{key}[{index}]")


def main() -> int:
    snapshot_paths = sorted((ROOT / "market_snapshots").glob("**/*.yaml"))
    device_paths = sorted((ROOT / "devices").glob("**/*.yaml"))
    contract_paths = sorted((ROOT / "capability_contracts").glob("**/*.yaml"))

    if not snapshot_paths:
        print("FAIL no market snapshot YAML records found", file=sys.stderr)
        return 1

    try:
        device_ids = load_ids(device_paths, "record_id")
        contract_ids = load_ids(contract_paths, "contract_id")
    except (ValidationError, OSError) as exc:
        print(f"FAIL index load: {exc}", file=sys.stderr)
        return 1

    errors: list[str] = []
    seen_snapshot_ids: set[str] = set()

    for path in snapshot_paths:
        rel = path.relative_to(ROOT)
        try:
            validate_snapshot(
                path,
                device_ids=device_ids,
                contract_ids=contract_ids,
                seen_snapshot_ids=seen_snapshot_ids,
            )
            print(f"PASS {rel}")
        except (ValidationError, OSError) as exc:
            errors.append(f"FAIL {rel}: {exc}")

    print()
    print(f"Validated {len(snapshot_paths)} market snapshot(s).")

    if errors:
        print("\nValidation errors:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print("All market snapshot checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
