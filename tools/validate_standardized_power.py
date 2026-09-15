#!/usr/bin/env python3
"""Validate machine-readable standardized power evidence on device records.

Standardized manufacturer/independent tests are useful evidence, but they are not
interchangeable with AXM local wall-power measurements or generic idle/workload
figures. This gate preserves provenance and test-condition scope whenever a device
record uses power.standardized_measurements.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]

TRUTH_STATES = {
    "UNRESEARCHED",
    "DOCUMENTED",
    "COMMUNITY_VERIFIED",
    "LOCALLY_VERIFIED",
    "REPRODUCIBLE",
    "DEPRECATED",
    "CONTRADICTED",
}

MEASUREMENT_KINDS = {
    "manufacturer_standardized_test",
    "independent_standardized_test",
    "local_standardized_test",
    "unknown",
}

REQUIRED_KEYS = {
    "id",
    "metric",
    "watts",
    "input_condition",
    "test_condition",
    "measurement_kind",
    "locally_measured",
    "state",
    "source_claim_ids",
}


class ValidationError(Exception):
    pass


def load_yaml(path: Path) -> dict[str, Any]:
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        raise ValidationError(f"invalid YAML: {exc}") from exc
    if not isinstance(data, dict):
        raise ValidationError("top-level YAML value must be a mapping")
    return data


def require_text(value: Any, context: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValidationError(f"{context} must be a non-empty string")
    return value.strip()


def evidence_claim_ids(data: dict[str, Any]) -> set[str]:
    evidence = data.get("evidence")
    if not isinstance(evidence, dict):
        raise ValidationError("evidence must be a mapping")
    claims = evidence.get("claims")
    if not isinstance(claims, list):
        raise ValidationError("evidence.claims must be a list")

    result: set[str] = set()
    for index, claim in enumerate(claims):
        if not isinstance(claim, dict):
            raise ValidationError(f"evidence.claims[{index}] must be a mapping")
        claim_id = require_text(claim.get("id"), f"evidence.claims[{index}].id")
        if claim_id in result:
            raise ValidationError(f"duplicate evidence claim id: {claim_id}")
        result.add(claim_id)
    return result


def validate_claim_refs(value: Any, claim_ids: set[str], context: str) -> None:
    if not isinstance(value, list) or not value:
        raise ValidationError(f"{context} must be a non-empty list")
    seen: set[str] = set()
    for index, raw in enumerate(value):
        claim_id = require_text(raw, f"{context}[{index}]")
        if claim_id in seen:
            raise ValidationError(f"{context} contains duplicate claim id {claim_id!r}")
        seen.add(claim_id)
        if claim_id not in claim_ids:
            raise ValidationError(f"{context} references unknown evidence claim {claim_id!r}")


def validate_watts(value: Any, context: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValidationError(f"{context} must be numeric")
    watts = float(value)
    if not math.isfinite(watts) or watts < 0:
        raise ValidationError(f"{context} must be finite and non-negative")
    return watts


def validate_measurements(data: dict[str, Any]) -> int:
    power = data.get("power")
    if power is None:
        return 0
    if not isinstance(power, dict):
        raise ValidationError("power must be a mapping")

    measurements = power.get("standardized_measurements")
    if measurements is None:
        return 0
    if not isinstance(measurements, list) or not measurements:
        raise ValidationError(
            "power.standardized_measurements must be a non-empty list when present"
        )

    claim_ids = evidence_claim_ids(data)
    seen_ids: set[str] = set()

    for index, measurement in enumerate(measurements):
        context = f"power.standardized_measurements[{index}]"
        if not isinstance(measurement, dict):
            raise ValidationError(f"{context} must be a mapping")
        missing = sorted(REQUIRED_KEYS - set(measurement))
        if missing:
            raise ValidationError(f"{context} missing required keys: {', '.join(missing)}")

        measurement_id = require_text(measurement["id"], f"{context}.id")
        if measurement_id in seen_ids:
            raise ValidationError(f"duplicate standardized power measurement id: {measurement_id}")
        seen_ids.add(measurement_id)

        require_text(measurement["metric"], f"{context}.metric")
        validate_watts(measurement["watts"], f"{context}.watts")
        require_text(measurement["input_condition"], f"{context}.input_condition")
        require_text(measurement["test_condition"], f"{context}.test_condition")

        kind = require_text(measurement["measurement_kind"], f"{context}.measurement_kind")
        if kind not in MEASUREMENT_KINDS:
            raise ValidationError(
                f"{context}.measurement_kind must be one of {sorted(MEASUREMENT_KINDS)}"
            )

        locally_measured = measurement["locally_measured"]
        if not isinstance(locally_measured, bool):
            raise ValidationError(f"{context}.locally_measured must be boolean")
        if kind == "local_standardized_test" and not locally_measured:
            raise ValidationError(
                f"{context} local_standardized_test requires locally_measured: true"
            )
        if kind != "local_standardized_test" and locally_measured:
            raise ValidationError(
                f"{context} locally_measured: true requires measurement_kind local_standardized_test"
            )

        state = measurement["state"]
        if state not in TRUTH_STATES:
            raise ValidationError(f"{context}.state has unsupported truth state {state!r}")

        validate_claim_refs(
            measurement["source_claim_ids"],
            claim_ids,
            f"{context}.source_claim_ids",
        )

    return len(measurements)


def validate_device(path: Path) -> int:
    return validate_measurements(load_yaml(path))


def main() -> int:
    paths = sorted((ROOT / "devices").glob("**/*.yaml"))
    if not paths:
        print("FAIL no device YAML records found", file=sys.stderr)
        return 1

    errors: list[str] = []
    total = 0
    records_with_measurements = 0
    for path in paths:
        rel = path.relative_to(ROOT)
        try:
            count = validate_device(path)
            total += count
            records_with_measurements += int(count > 0)
            print(f"PASS {rel}: {count} standardized power measurement(s)")
        except (ValidationError, OSError) as exc:
            errors.append(f"FAIL {rel}: {exc}")

    print()
    print(
        f"Checked {len(paths)} device record(s): {total} standardized power measurement(s) "
        f"across {records_with_measurements} record(s)."
    )
    if errors:
        print("\nValidation errors:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(
        "All standardized power measurements preserve numeric value, provenance, "
        "test/input conditions, local/non-local identity, truth state, and evidence links."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
