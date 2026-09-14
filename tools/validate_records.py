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

RECOVERY_IMPACT_VALUES = {
    "preserved",
    "erased",
    "partially_reset",
    "must_recreate",
    "unknown",
    "not_applicable",
}

LOCALITY_STATES = {
    "fully_local",
    "local_after_provisioning",
    "cloud_optional",
    "cloud_required_for_some_functions",
    "cloud_required",
    "unknown",
}

REQUIRED_RECOVERY_PATH = {
    "id",
    "from_state",
    "target_state",
    "method",
    "availability",
    "state",
    "data_impact",
    "source_claim_ids",
}

REQUIRED_RECOVERY_IMPACT = {
    "system_configuration",
    "user_data",
    "application_state",
}

REQUIRED_LOCALITY_STATE = {
    "id",
    "device_state",
    "locality_state",
    "state",
    "source_claim_ids",
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


def require_nonempty_string(value: Any, context: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValidationError(f"{context} must be a non-empty string")


def validate_truth_state(value: Any, context: str) -> None:
    if value not in TRUTH_STATES:
        allowed = ", ".join(sorted(TRUTH_STATES))
        raise ValidationError(f"{context} has invalid truth state {value!r}; allowed: {allowed}")


def validate_claim_references(
    values: Any,
    claim_ids: set[str],
    context: str,
) -> None:
    if not isinstance(values, list) or not values:
        raise ValidationError(f"{context} must be a non-empty list")
    for claim_id in values:
        require_nonempty_string(claim_id, f"{context}[]")
        if claim_id not in claim_ids:
            raise ValidationError(
                f"{context} references unknown evidence claim {claim_id!r}"
            )


def validate_recovery_paths(recovery: dict[str, Any], claim_ids: set[str]) -> None:
    paths = recovery.get("paths")
    if paths is None:
        return
    if not isinstance(paths, list) or not paths:
        raise ValidationError("recovery.paths must be a non-empty list when present")

    seen_path_ids: set[str] = set()

    for index, path in enumerate(paths):
        context = f"recovery.paths[{index}]"
        if not isinstance(path, dict):
            raise ValidationError(f"{context} must be a mapping")
        require_keys(path, REQUIRED_RECOVERY_PATH, context)

        path_id = path["id"]
        require_nonempty_string(path_id, f"{context}.id")
        if path_id in seen_path_ids:
            raise ValidationError(f"duplicate recovery path id: {path_id}")
        seen_path_ids.add(path_id)

        for key in ("from_state", "target_state", "method"):
            require_nonempty_string(path[key], f"{context}.{key}")

        availability = path["availability"]
        if availability not in (True, False, "unknown"):
            raise ValidationError(
                f"{context}.availability must be true, false, or 'unknown'"
            )

        validate_truth_state(path["state"], f"{context}.state")

        impact = path["data_impact"]
        if not isinstance(impact, dict):
            raise ValidationError(f"{context}.data_impact must be a mapping")
        require_keys(impact, REQUIRED_RECOVERY_IMPACT, f"{context}.data_impact")
        for key in REQUIRED_RECOVERY_IMPACT:
            value = impact[key]
            if value not in RECOVERY_IMPACT_VALUES:
                allowed = ", ".join(sorted(RECOVERY_IMPACT_VALUES))
                raise ValidationError(
                    f"{context}.data_impact.{key} has invalid value {value!r}; "
                    f"allowed: {allowed}"
                )

        validate_claim_references(
            path["source_claim_ids"],
            claim_ids,
            f"{context}.source_claim_ids",
        )


def validate_string_list(value: Any, context: str) -> None:
    if not isinstance(value, list):
        raise ValidationError(f"{context} must be a list")
    for index, item in enumerate(value):
        require_nonempty_string(item, f"{context}[{index}]")


def validate_locality_states(locality: dict[str, Any], claim_ids: set[str]) -> None:
    states = locality.get("states")
    if states is None:
        return
    if locality.get("state") != "state_dependent":
        raise ValidationError(
            "locality.state must be 'state_dependent' when locality.states is present"
        )
    if not isinstance(states, list) or not states:
        raise ValidationError("locality.states must be a non-empty list when present")

    seen_state_ids: set[str] = set()

    for index, entry in enumerate(states):
        context = f"locality.states[{index}]"
        if not isinstance(entry, dict):
            raise ValidationError(f"{context} must be a mapping")
        require_keys(entry, REQUIRED_LOCALITY_STATE, context)

        entry_id = entry["id"]
        require_nonempty_string(entry_id, f"{context}.id")
        if entry_id in seen_state_ids:
            raise ValidationError(f"duplicate locality state id: {entry_id}")
        seen_state_ids.add(entry_id)

        require_nonempty_string(entry["device_state"], f"{context}.device_state")

        locality_state = entry["locality_state"]
        if locality_state not in LOCALITY_STATES:
            allowed = ", ".join(sorted(LOCALITY_STATES))
            raise ValidationError(
                f"{context}.locality_state has invalid value {locality_state!r}; "
                f"allowed: {allowed}"
            )

        validate_truth_state(entry["state"], f"{context}.state")
        validate_claim_references(
            entry["source_claim_ids"],
            claim_ids,
            f"{context}.source_claim_ids",
        )

        for key in ("offline_capabilities", "internet_required_capabilities"):
            if key in entry:
                validate_string_list(entry[key], f"{context}.{key}")

        if "provisioning_cloud_requirement" in entry:
            require_nonempty_string(
                entry["provisioning_cloud_requirement"],
                f"{context}.provisioning_cloud_requirement",
            )


def validate_device(path: Path, seen_ids: set[str]) -> None:
    data = load_yaml(path)
    require_keys(data, REQUIRED_DEVICE_TOP_LEVEL, "device record")

    record_id = data["record_id"]
    require_nonempty_string(record_id, "record_id")
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

    claim_ids: set[str] = set()
    for index, claim in enumerate(claims):
        if not isinstance(claim, dict):
            raise ValidationError(f"evidence.claims[{index}] must be a mapping")
        for key in ("id", "state", "source"):
            if key not in claim:
                raise ValidationError(f"evidence.claims[{index}] missing {key}")

        claim_id = claim["id"]
        require_nonempty_string(claim_id, f"evidence.claims[{index}].id")
        if claim_id in claim_ids:
            raise ValidationError(f"duplicate evidence claim id: {claim_id}")
        claim_ids.add(claim_id)

        validate_truth_state(claim["state"], f"evidence.claims[{index}].state")
        require_nonempty_string(claim["source"], f"evidence.claims[{index}].source")

    validate_recovery_paths(recovery, claim_ids)

    locality = data.get("locality")
    if locality is not None:
        if not isinstance(locality, dict):
            raise ValidationError("locality must be a mapping when present")
        validate_locality_states(locality, claim_ids)


def validate_contract(path: Path, seen_ids: set[str]) -> None:
    data = load_yaml(path)
    require_keys(data, REQUIRED_CONTRACT_TOP_LEVEL, "capability contract")

    contract_id = data["contract_id"]
    require_nonempty_string(contract_id, "contract_id")
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
