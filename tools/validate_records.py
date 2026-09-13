#!/usr/bin/env python3
"""Validate AXM Device Capability Arbitrage YAML records.

This intentionally checks only the smallest stable contract. The research schema is
still young; validation should catch accidental structural drift without freezing
unknown fields or preventing new device classes from challenging the model.
"""

from __future__ import annotations

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

REQUIRED_DEVICE_TOP_LEVEL = {
    "schema_version",
    "record_id",
    "identity",
    "execution",
    "recovery",
    "economics",
    "roles",
    "evidence",
}

REQUIRED_IDENTITY = {"manufacturer", "model", "marketed_category"}
REQUIRED_CONTRACT_TOP_LEVEL = {
    "contract_version",
    "contract_id",
    "purpose",
    "required",
    "verification",
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


def require_keys(data: dict[str, Any], keys: set[str], context: str) -> None:
    missing = sorted(keys - set(data))
    if missing:
        raise ValidationError(f"{context} missing required keys: {', '.join(missing)}")


def validate_truth_state(value: Any, context: str) -> None:
    if value not in TRUTH_STATES:
        allowed = ", ".join(sorted(TRUTH_STATES))
        raise ValidationError(f"{context} has invalid truth state {value!r}; allowed: {allowed}")


def validate_device(path: Path, seen_ids: set[str]) -> None:
    data = load_yaml(path)
    require_keys(data, REQUIRED_DEVICE_TOP_LEVEL, "device record")

    record_id = data["record_id"]
    if not isinstance(record_id, str) or not record_id.strip():
        raise ValidationError("record_id must be a non-empty string")
    if record_id in seen_ids:
        raise ValidationError(f"duplicate record_id: {record_id}")
    seen_ids.add(record_id)

    identity = data["identity"]
    if not isinstance(identity, dict):
        raise ValidationError("identity must be a mapping")
    require_keys(identity, REQUIRED_IDENTITY, "identity")

    execution = data["execution"]
    if not isinstance(execution, dict):
        raise ValidationError("execution must be a mapping")
    surfaces = execution.get("surfaces")
    if not isinstance(surfaces, list) or not surfaces:
        raise ValidationError("execution.surfaces must be a non-empty list")

    for index, surface in enumerate(surfaces):
        if not isinstance(surface, dict):
            raise ValidationError(f"execution.surfaces[{index}] must be a mapping")
        for key in ("type", "custom_code", "state"):
            if key not in surface:
                raise ValidationError(f"execution.surfaces[{index}] missing {key}")
        validate_truth_state(surface["state"], f"execution.surfaces[{index}].state")

    recovery = data["recovery"]
    if not isinstance(recovery, dict):
        raise ValidationError("recovery must be a mapping")
    if "recovery_state" not in recovery:
        raise ValidationError("recovery.recovery_state is required")
    validate_truth_state(recovery["recovery_state"], "recovery.recovery_state")

    economics = data["economics"]
    if not isinstance(economics, dict):
        raise ValidationError("economics must be a mapping")
    if not economics.get("market_data_state"):
        raise ValidationError("economics.market_data_state must be explicit")

    roles = data["roles"]
    if not isinstance(roles, list):
        raise ValidationError("roles must be a list")

    evidence = data["evidence"]
    if not isinstance(evidence, dict):
        raise ValidationError("evidence must be a mapping")
    if "overall_state" not in evidence:
        raise ValidationError("evidence.overall_state is required")
    validate_truth_state(evidence["overall_state"], "evidence.overall_state")

    claims = evidence.get("claims", [])
    if not isinstance(claims, list):
        raise ValidationError("evidence.claims must be a list")
    for index, claim in enumerate(claims):
        if not isinstance(claim, dict):
            raise ValidationError(f"evidence.claims[{index}] must be a mapping")
        for key in ("id", "state", "source"):
            if key not in claim:
                raise ValidationError(f"evidence.claims[{index}] missing {key}")
        validate_truth_state(claim["state"], f"evidence.claims[{index}].state")


def validate_contract(path: Path, seen_ids: set[str]) -> None:
    data = load_yaml(path)
    require_keys(data, REQUIRED_CONTRACT_TOP_LEVEL, "capability contract")

    contract_id = data["contract_id"]
    if not isinstance(contract_id, str) or not contract_id.strip():
        raise ValidationError("contract_id must be a non-empty string")
    if contract_id in seen_ids:
        raise ValidationError(f"duplicate contract_id: {contract_id}")
    seen_ids.add(contract_id)

    if not isinstance(data["required"], dict) or not data["required"]:
        raise ValidationError("required must be a non-empty mapping")

    verification = data["verification"]
    if not isinstance(verification, dict):
        raise ValidationError("verification must be a mapping")
    if not verification.get("state"):
        raise ValidationError("verification.state must be explicit")


def validate_group(paths: list[Path], validator) -> tuple[int, list[str]]:
    errors: list[str] = []
    seen_ids: set[str] = set()
    for path in paths:
        rel = path.relative_to(ROOT)
        try:
            validator(path, seen_ids)
            print(f"PASS {rel}")
        except (ValidationError, OSError) as exc:
            errors.append(f"FAIL {rel}: {exc}")
    return len(paths), errors


def main() -> int:
    device_paths = sorted((ROOT / "devices").glob("**/*.yaml"))
    contract_paths = sorted((ROOT / "capability_contracts").glob("**/*.yaml"))

    if not device_paths:
        print("FAIL no device YAML records found", file=sys.stderr)
        return 1

    device_count, device_errors = validate_group(device_paths, validate_device)
    contract_count, contract_errors = validate_group(contract_paths, validate_contract)
    errors = device_errors + contract_errors

    print()
    print(f"Validated {device_count} device record(s) and {contract_count} capability contract(s).")

    if errors:
        print("\nValidation errors:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print("All structural checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
