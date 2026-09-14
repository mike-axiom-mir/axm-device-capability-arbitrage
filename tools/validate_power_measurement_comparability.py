#!/usr/bin/env python3
"""Validate comparability metadata for local power measurements.

This gate does not create or promote measurements. It only requires enough
measurement context that future wall-power numbers can be compared without
silently changing the test boundary or averaging method.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]

BOUNDARIES = {
    "whole_test_setup_at_wall",
    "device_and_required_power_supply_at_wall",
    "other",
    "unknown",
}
INTEGRATION_METHODS = {
    "instrument_average",
    "energy_divided_by_time",
    "sample_mean",
    "unknown",
}
CALIBRATION_STATES = {
    "currently_calibrated",
    "manufacturer_spec_only",
    "self_checked",
    "not_calibrated",
    "unknown",
}
REQUIRED_WALL_POWER_KEYS = {
    "instrument",
    "model",
    "resolution_watts",
    "source_class",
    "measurement_boundary",
    "integration_method",
    "sample_interval_seconds",
    "uncertainty_statement",
    "calibration_status",
}
REQUIRED_STABILIZATION_KEYS = {
    "idle_stabilization_seconds",
    "workload_stabilization_seconds",
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


def number_or_unknown(value: Any, context: str) -> float | None:
    if value == "unknown":
        return None
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValidationError(f"{context} must be numeric or 'unknown'")
    number = float(value)
    if not math.isfinite(number) or number < 0:
        raise ValidationError(f"{context} must be finite and non-negative")
    return number


def require_known_configuration(value: Any, context: str) -> None:
    if value is None:
        raise ValidationError(f"{context} must be explicit for numeric power measurements")
    if isinstance(value, str):
        if not value.strip() or value.strip() == "unknown":
            raise ValidationError(f"{context} may not be unknown for numeric power measurements")
        return
    if isinstance(value, (list, dict)):
        if not value:
            raise ValidationError(f"{context} may not be empty for numeric power measurements")
        return
    raise ValidationError(
        f"{context} must be a descriptive string, list, or mapping for numeric power measurements"
    )


def validate_receipt(path: Path) -> tuple[bool, bool]:
    data = load_yaml(path)
    tools = data.get("measurement_tools")
    if not isinstance(tools, dict):
        raise ValidationError("measurement_tools must be a mapping")
    wall = tools.get("wall_power")
    if not isinstance(wall, dict):
        raise ValidationError("measurement_tools.wall_power must be a mapping")

    missing = sorted(REQUIRED_WALL_POWER_KEYS - set(wall))
    if missing:
        raise ValidationError(
            "measurement_tools.wall_power missing comparability keys: " + ", ".join(missing)
        )

    boundary = require_text(wall["measurement_boundary"], "measurement_tools.wall_power.measurement_boundary")
    if boundary not in BOUNDARIES:
        raise ValidationError(
            f"measurement boundary must be one of {sorted(BOUNDARIES)}"
        )

    integration = require_text(wall["integration_method"], "measurement_tools.wall_power.integration_method")
    if integration not in INTEGRATION_METHODS:
        raise ValidationError(
            f"integration method must be one of {sorted(INTEGRATION_METHODS)}"
        )

    sample_interval = number_or_unknown(
        wall["sample_interval_seconds"],
        "measurement_tools.wall_power.sample_interval_seconds",
    )
    require_text(wall["uncertainty_statement"], "measurement_tools.wall_power.uncertainty_statement")
    calibration = require_text(wall["calibration_status"], "measurement_tools.wall_power.calibration_status")
    if calibration not in CALIBRATION_STATES:
        raise ValidationError(
            f"calibration status must be one of {sorted(CALIBRATION_STATES)}"
        )

    run = data.get("workload_run")
    if not isinstance(run, dict):
        raise ValidationError("workload_run must be a mapping")
    missing_stabilization = sorted(REQUIRED_STABILIZATION_KEYS - set(run))
    if missing_stabilization:
        raise ValidationError(
            "workload_run missing power comparability keys: " + ", ".join(missing_stabilization)
        )

    idle_w = number_or_unknown(run.get("wall_power_idle_watts"), "workload_run.wall_power_idle_watts")
    workload_w = number_or_unknown(
        run.get("wall_power_workload_average_watts"),
        "workload_run.wall_power_workload_average_watts",
    )
    idle_stabilization = number_or_unknown(
        run["idle_stabilization_seconds"],
        "workload_run.idle_stabilization_seconds",
    )
    workload_stabilization = number_or_unknown(
        run["workload_stabilization_seconds"],
        "workload_run.workload_stabilization_seconds",
    )

    has_numeric_power = idle_w is not None or workload_w is not None
    if not has_numeric_power:
        return False, False

    if boundary == "unknown":
        raise ValidationError("numeric power requires a known measurement_boundary")
    if integration == "unknown":
        raise ValidationError("numeric power requires a known integration_method")
    if integration == "sample_mean" and (sample_interval is None or sample_interval <= 0):
        raise ValidationError("sample_mean power requires positive sample_interval_seconds")

    if idle_w is not None and idle_stabilization is None:
        raise ValidationError("numeric idle watts require explicit idle_stabilization_seconds")
    if workload_w is not None and workload_stabilization is None:
        raise ValidationError("numeric workload watts require explicit workload_stabilization_seconds")

    unit = data.get("unit_identity")
    if not isinstance(unit, dict):
        raise ValidationError("unit_identity must be a mapping")
    config = unit.get("configuration")
    if not isinstance(config, dict):
        raise ValidationError("unit_identity.configuration must be a mapping")
    require_known_configuration(config.get("power_supply"), "unit_identity.configuration.power_supply")
    require_known_configuration(
        config.get("attached_peripherals"),
        "unit_identity.configuration.attached_peripherals",
    )

    artifacts = data.get("artifacts")
    if not isinstance(artifacts, list) or not artifacts:
        raise ValidationError(
            "numeric local power requires at least one durable artifact; "
            "the existing receipt validator checks artifact hashes and shape"
        )

    return idle_w is not None, workload_w is not None


def main() -> int:
    paths = sorted((ROOT / "experiment_receipts").glob("**/*.yaml"))
    if not paths:
        print("FAIL no experiment receipt YAML files found", file=sys.stderr)
        return 1

    errors: list[str] = []
    numeric_idle = 0
    numeric_workload = 0
    for path in paths:
        rel = path.relative_to(ROOT)
        try:
            has_idle, has_workload = validate_receipt(path)
            numeric_idle += int(has_idle)
            numeric_workload += int(has_workload)
            print(
                f"PASS {rel}: numeric_idle={has_idle}; "
                f"numeric_workload={has_workload}"
            )
        except (ValidationError, OSError) as exc:
            errors.append(f"FAIL {rel}: {exc}")

    print()
    print(
        f"Checked {len(paths)} receipt file(s): {numeric_idle} numeric idle-power "
        f"measurement(s), {numeric_workload} numeric workload-power measurement(s)."
    )
    if errors:
        print("\nValidation errors:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print("All local power-measurement comparability checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
