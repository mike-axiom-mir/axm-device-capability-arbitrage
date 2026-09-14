#!/usr/bin/env python3
"""Validate local experiment receipts without inventing device results."""

from __future__ import annotations

import math
import re
import sys
from datetime import date
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
SHA256 = re.compile(r"^[0-9a-fA-F]{64}$")
TRUTH_STATES = {
    "UNRESEARCHED", "DOCUMENTED", "COMMUNITY_VERIFIED", "LOCALLY_VERIFIED",
    "REPRODUCIBLE", "DEPRECATED", "CONTRADICTED",
}
RESULT_STATES = {"pass", "fail", "partial", "unknown"}
AUTOMATION_LEVELS = {"manual", "partial", "automated", "unknown"}
NETWORK_SCOPES = {"lan_only", "lan_with_wan", "isolated", "unknown"}

TOP_KEYS = {
    "receipt_version", "receipt_kind", "receipt_id", "device_record_id",
    "contract_id", "workload_id", "performed_at", "authorization",
    "unit_identity", "software_state", "conditions", "measurement_tools",
    "provisioning", "workload_run", "restart_trials", "artifacts", "result",
    "notes",
}
UNIT_KEYS = {
    "local_unit_label", "observed_manufacturer", "observed_model",
    "hardware_revision", "device_state", "configuration",
}
SOFTWARE_KEYS = {"os_or_firmware", "version", "installation_method", "source_or_image_sha256"}
RUN_KEYS = {
    "profile_matches_workload", "build_or_install_elapsed_seconds",
    "binary_or_package_size_bytes", "state_file_size_bytes_after_seed",
    "process_rss_bytes", "cpu_usage_percent", "wall_power_idle_watts",
    "idle_measurement_seconds", "wall_power_workload_average_watts",
    "measurement_seconds", "service_autostart_config", "notes",
}
RESULT_KEYS = {
    "workload_execution", "restart_reliability", "overall_state",
    "local_verification_claimed",
}
TRIAL_KEYS = {
    "id", "power_removed", "power_restored",
    "service_ready_without_manual_intervention",
    "last_acknowledged_value_readable",
    "elapsed_seconds_power_restore_to_service_ready", "note",
}
ARTIFACT_KEYS = {"type", "location", "sha256", "proves"}


class ValidationError(Exception):
    pass


def load_yaml(path: Path) -> dict[str, Any]:
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        raise ValidationError(f"invalid YAML: {exc}") from exc
    if not isinstance(data, dict):
        raise ValidationError("top-level value must be a mapping")
    return data


def require_keys(data: dict[str, Any], keys: set[str], context: str) -> None:
    missing = sorted(keys - set(data))
    if missing:
        raise ValidationError(f"{context} missing keys: {', '.join(missing)}")


def text(value: Any, context: str, *, known: bool = False) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValidationError(f"{context} must be a non-empty string")
    value = value.strip()
    if known and value == "unknown":
        raise ValidationError(f"{context} may not be 'unknown'")
    return value


def bool_or_unknown(value: Any, context: str) -> None:
    if value not in (True, False, "unknown"):
        raise ValidationError(f"{context} must be true, false, or 'unknown'")


def number(
    value: Any,
    context: str,
    *,
    integer: bool = False,
    allow_negative: bool = False,
    percent: bool = False,
) -> float | int | None:
    if value == "unknown":
        return None
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValidationError(f"{context} must be numeric or 'unknown'")
    if integer and not isinstance(value, int):
        raise ValidationError(f"{context} must be an integer or 'unknown'")
    numeric = float(value)
    if not math.isfinite(numeric) or (numeric < 0 and not allow_negative):
        raise ValidationError(f"{context} must be finite and non-negative")
    if percent and numeric > 100:
        raise ValidationError(f"{context} must not exceed 100")
    return value


def date_or_unknown(value: Any, context: str) -> date | None:
    value = text(value, context)
    if value == "unknown":
        return None
    try:
        return date.fromisoformat(value)
    except ValueError as exc:
        raise ValidationError(f"{context} must be ISO YYYY-MM-DD or 'unknown'") from exc


def string_list(value: Any, context: str) -> None:
    if not isinstance(value, list):
        raise ValidationError(f"{context} must be a list")
    for index, item in enumerate(value):
        text(item, f"{context}[{index}]")


def load_index(paths: list[Path], id_key: str) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    for path in paths:
        data = load_yaml(path)
        item_id = text(data.get(id_key), f"{path.relative_to(ROOT)}.{id_key}")
        if item_id in result:
            raise ValidationError(f"duplicate {id_key}: {item_id}")
        result[item_id] = data
    return result


def load_workloads(paths: list[Path]) -> dict[str, dict[str, Any]]:
    return load_index(paths, "workload_id")


def workload_seconds(workload: dict[str, Any]) -> int | None:
    profile = workload.get("comparison_profile")
    if not isinstance(profile, dict):
        return None
    value = profile.get("measurement_seconds")
    return value if isinstance(value, int) and not isinstance(value, bool) and value > 0 else None


def restart_target(workload: dict[str, Any]) -> int | None:
    restart = workload.get("restart_trial")
    if not isinstance(restart, dict):
        return None
    value = restart.get("repetitions_target")
    return value if isinstance(value, int) and not isinstance(value, bool) and value > 0 else None


def validate_tooling(tools: Any) -> dict[str, Any]:
    if not isinstance(tools, dict):
        raise ValidationError("measurement_tools must be a mapping")
    wall = tools.get("wall_power")
    elapsed = tools.get("elapsed_time")
    if not isinstance(wall, dict) or not isinstance(elapsed, dict):
        raise ValidationError("measurement_tools requires wall_power and elapsed_time mappings")
    for key in ("instrument", "model", "resolution_watts", "source_class"):
        if key not in wall:
            raise ValidationError(f"measurement_tools.wall_power missing {key}")
    text(wall["instrument"], "measurement_tools.wall_power.instrument")
    text(wall["model"], "measurement_tools.wall_power.model")
    number(wall["resolution_watts"], "measurement_tools.wall_power.resolution_watts")
    if wall["source_class"] not in {"local_instrument", "unknown"}:
        raise ValidationError(
            "measurement_tools.wall_power.source_class must be local_instrument or unknown"
        )
    text(elapsed.get("method"), "measurement_tools.elapsed_time.method")
    return wall


def validate_artifacts(value: Any) -> int:
    if not isinstance(value, list):
        raise ValidationError("artifacts must be a list")
    count = 0
    for index, artifact in enumerate(value):
        context = f"artifacts[{index}]"
        if not isinstance(artifact, dict):
            raise ValidationError(f"{context} must be a mapping")
        require_keys(artifact, ARTIFACT_KEYS, context)
        text(artifact["type"], f"{context}.type", known=True)
        text(artifact["location"], f"{context}.location", known=True)
        digest = text(artifact["sha256"], f"{context}.sha256", known=True)
        if not SHA256.fullmatch(digest):
            raise ValidationError(f"{context}.sha256 must be a 64-character SHA-256 digest")
        text(artifact["proves"], f"{context}.proves", known=True)
        count += 1
    return count


def validate_trials(value: Any, workload: dict[str, Any], restart_result: str, template: bool) -> None:
    if not isinstance(value, dict):
        raise ValidationError("restart_trials must be a mapping")
    target = value.get("repetitions_target")
    if isinstance(target, bool) or not isinstance(target, int) or target <= 0:
        raise ValidationError("restart_trials.repetitions_target must be a positive integer")
    expected_target = restart_target(workload)
    if expected_target is not None and target != expected_target:
        raise ValidationError(
            f"restart target {target} does not match workload target {expected_target}"
        )

    trials = value.get("trials")
    if not isinstance(trials, list):
        raise ValidationError("restart_trials.trials must be a list")
    if template and trials:
        raise ValidationError("template restart_trials.trials must be empty")

    seen: set[str] = set()
    pass_count = 0
    for index, trial in enumerate(trials):
        context = f"restart_trials.trials[{index}]"
        if not isinstance(trial, dict):
            raise ValidationError(f"{context} must be a mapping")
        require_keys(trial, TRIAL_KEYS, context)
        trial_id = text(trial["id"], f"{context}.id", known=True)
        if trial_id in seen:
            raise ValidationError(f"duplicate restart trial id {trial_id!r}")
        seen.add(trial_id)
        for key in (
            "power_removed", "power_restored",
            "service_ready_without_manual_intervention",
            "last_acknowledged_value_readable",
        ):
            if not isinstance(trial[key], bool):
                raise ValidationError(f"{context}.{key} must be boolean")
        number(
            trial["elapsed_seconds_power_restore_to_service_ready"],
            f"{context}.elapsed_seconds_power_restore_to_service_ready",
        )
        text(trial["note"], f"{context}.note")
        if all(
            trial[key]
            for key in (
                "power_removed", "power_restored",
                "service_ready_without_manual_intervention",
                "last_acknowledged_value_readable",
            )
        ):
            pass_count += 1

    if restart_result == "pass" and (len(trials) < target or pass_count < target):
        raise ValidationError(
            f"restart_reliability='pass' requires at least {target} passing physical trials"
        )


def validate_template(
    data: dict[str, Any],
    contract_index: dict[str, dict[str, Any]],
    workload_index: dict[str, dict[str, Any]],
) -> None:
    if data["receipt_id"] != "TEMPLATE":
        raise ValidationError("template receipt_id must be TEMPLATE")
    if data["device_record_id"] != "unknown" or data["performed_at"] != "unknown":
        raise ValidationError("template device_record_id/performed_at must remain unknown")
    contract_id = text(data["contract_id"], "contract_id")
    workload_id = text(data["workload_id"], "workload_id")
    if contract_id not in contract_index or workload_id not in workload_index:
        raise ValidationError("template references unknown contract/workload")
    workload = workload_index[workload_id]
    if workload.get("contract_id") != contract_id:
        raise ValidationError("template workload/contract binding is inconsistent")
    result = data["result"]
    if result["overall_state"] != "UNRESEARCHED" or result["local_verification_claimed"] is not False:
        raise ValidationError("template must remain UNRESEARCHED with no local verification claim")
    if data["artifacts"]:
        raise ValidationError("template artifacts must remain empty")
    validate_trials(data["restart_trials"], workload, result["restart_reliability"], True)


def validate_actual(
    data: dict[str, Any],
    device_index: dict[str, dict[str, Any]],
    contract_index: dict[str, dict[str, Any]],
    workload_index: dict[str, dict[str, Any]],
) -> None:
    device_id = text(data["device_record_id"], "device_record_id", known=True)
    contract_id = text(data["contract_id"], "contract_id", known=True)
    workload_id = text(data["workload_id"], "workload_id", known=True)
    if device_id not in device_index:
        raise ValidationError(f"unknown device_record_id {device_id!r}")
    if contract_id not in contract_index:
        raise ValidationError(f"unknown contract_id {contract_id!r}")
    if workload_id not in workload_index:
        raise ValidationError(f"unknown workload_id {workload_id!r}")
    workload = workload_index[workload_id]
    if workload.get("contract_id") != contract_id:
        raise ValidationError("receipt workload does not belong to receipt contract")
    if date_or_unknown(data["performed_at"], "performed_at") is None:
        raise ValidationError("actual receipt performed_at may not be unknown")

    auth = data["authorization"]
    if not isinstance(auth, dict) or auth.get("owned_or_authorized") is not True:
        raise ValidationError("actual receipt requires authorization.owned_or_authorized=true")

    unit = data["unit_identity"]
    if not isinstance(unit, dict):
        raise ValidationError("unit_identity must be a mapping")
    require_keys(unit, UNIT_KEYS, "unit_identity")
    for key in ("local_unit_label", "observed_manufacturer", "observed_model", "device_state"):
        text(unit[key], f"unit_identity.{key}", known=True)
    text(unit["hardware_revision"], "unit_identity.hardware_revision")
    if not isinstance(unit["configuration"], dict) or not unit["configuration"]:
        raise ValidationError("unit_identity.configuration must be a non-empty mapping")

    software = data["software_state"]
    if not isinstance(software, dict):
        raise ValidationError("software_state must be a mapping")
    require_keys(software, SOFTWARE_KEYS, "software_state")
    for key in ("os_or_firmware", "version", "installation_method"):
        text(software[key], f"software_state.{key}", known=True)
    image_hash = text(software["source_or_image_sha256"], "software_state.source_or_image_sha256")
    if image_hash != "unknown" and not SHA256.fullmatch(image_hash):
        raise ValidationError("software_state.source_or_image_sha256 must be unknown or SHA-256")

    conditions = data["conditions"]
    if not isinstance(conditions, dict):
        raise ValidationError("conditions must be a mapping")
    network_scope = text(conditions.get("network_scope"), "conditions.network_scope")
    if network_scope not in NETWORK_SCOPES:
        raise ValidationError(f"conditions.network_scope must be one of {sorted(NETWORK_SCOPES)}")
    bool_or_unknown(conditions.get("wan_available"), "conditions.wan_available")
    number(
        conditions.get("ambient_temperature_c"),
        "conditions.ambient_temperature_c",
        allow_negative=True,
    )
    string_list(conditions.get("notes"), "conditions.notes")

    wall_tool = validate_tooling(data["measurement_tools"])

    provisioning = data["provisioning"]
    if not isinstance(provisioning, dict):
        raise ValidationError("provisioning must be a mapping")
    for key in ("first_device_minutes", "repeat_device_minutes"):
        number(provisioning.get(key), f"provisioning.{key}")
    automation = text(provisioning.get("automation_level"), "provisioning.automation_level")
    if automation not in AUTOMATION_LEVELS:
        raise ValidationError(f"provisioning.automation_level must be one of {sorted(AUTOMATION_LEVELS)}")
    string_list(provisioning.get("notes"), "provisioning.notes")

    run = data["workload_run"]
    if not isinstance(run, dict):
        raise ValidationError("workload_run must be a mapping")
    require_keys(run, RUN_KEYS, "workload_run")
    bool_or_unknown(run["profile_matches_workload"], "workload_run.profile_matches_workload")
    number(run["build_or_install_elapsed_seconds"], "workload_run.build_or_install_elapsed_seconds")
    for key in ("binary_or_package_size_bytes", "state_file_size_bytes_after_seed", "process_rss_bytes"):
        number(run[key], f"workload_run.{key}", integer=True)
    number(run["cpu_usage_percent"], "workload_run.cpu_usage_percent", percent=True)
    idle_w = number(run["wall_power_idle_watts"], "workload_run.wall_power_idle_watts")
    idle_s = number(run["idle_measurement_seconds"], "workload_run.idle_measurement_seconds", integer=True)
    load_w = number(
        run["wall_power_workload_average_watts"],
        "workload_run.wall_power_workload_average_watts",
    )
    load_s = number(run["measurement_seconds"], "workload_run.measurement_seconds", integer=True)
    text(run["service_autostart_config"], "workload_run.service_autostart_config")
    string_list(run["notes"], "workload_run.notes")

    if idle_w is not None and (idle_s is None or idle_s <= 0):
        raise ValidationError("numeric idle watts require positive idle_measurement_seconds")
    if idle_s is not None and idle_s > 0 and idle_w is None:
        raise ValidationError("idle duration without idle watts is ambiguous; keep both unknown")
    if load_w is not None:
        if run["profile_matches_workload"] is not True:
            raise ValidationError("numeric workload watts require profile_matches_workload=true")
        required = workload_seconds(workload)
        if load_s is None or load_s <= 0 or (required is not None and load_s < required):
            raise ValidationError("workload power measurement window is shorter than workload profile")
    if idle_w is not None or load_w is not None:
        if wall_tool["source_class"] != "local_instrument":
            raise ValidationError("numeric local watts require wall_power.source_class=local_instrument")
        text(wall_tool["instrument"], "measurement_tools.wall_power.instrument", known=True)
        text(wall_tool["model"], "measurement_tools.wall_power.model", known=True)

    result = data["result"]
    if not isinstance(result, dict):
        raise ValidationError("result must be a mapping")
    require_keys(result, RESULT_KEYS, "result")
    for key in ("workload_execution", "restart_reliability"):
        if result[key] not in RESULT_STATES:
            raise ValidationError(f"result.{key} must be one of {sorted(RESULT_STATES)}")
    if result["overall_state"] not in TRUTH_STATES:
        raise ValidationError(f"result.overall_state must be one of {sorted(TRUTH_STATES)}")
    if not isinstance(result["local_verification_claimed"], bool):
        raise ValidationError("result.local_verification_claimed must be boolean")

    validate_trials(
        data["restart_trials"],
        workload,
        result["restart_reliability"],
        False,
    )
    artifact_count = validate_artifacts(data["artifacts"])

    if result["local_verification_claimed"]:
        if result["overall_state"] not in {"LOCALLY_VERIFIED", "REPRODUCIBLE"}:
            raise ValidationError(
                "local_verification_claimed=true requires LOCALLY_VERIFIED or REPRODUCIBLE"
            )
        if artifact_count < 1:
            raise ValidationError("local verification requires at least one SHA-256-bound artifact")
        if result["workload_execution"] == "pass" and run["profile_matches_workload"] is not True:
            raise ValidationError("verified workload pass requires profile_matches_workload=true")


def validate_receipt(
    path: Path,
    device_index: dict[str, dict[str, Any]],
    contract_index: dict[str, dict[str, Any]],
    workload_index: dict[str, dict[str, Any]],
    seen_ids: set[str],
) -> None:
    data = load_yaml(path)
    require_keys(data, TOP_KEYS, "receipt")
    if data["receipt_version"] != "0.1":
        raise ValidationError("receipt_version must be '0.1'")
    kind = text(data["receipt_kind"], "receipt_kind")
    if kind not in {"template", "local_experiment"}:
        raise ValidationError("receipt_kind must be template or local_experiment")
    receipt_id = text(data["receipt_id"], "receipt_id")
    if receipt_id in seen_ids:
        raise ValidationError(f"duplicate receipt_id {receipt_id!r}")
    seen_ids.add(receipt_id)

    auth = data["authorization"]
    if not isinstance(auth, dict):
        raise ValidationError("authorization must be a mapping")
    bool_or_unknown(auth.get("owned_or_authorized"), "authorization.owned_or_authorized")

    unit = data["unit_identity"]
    if not isinstance(unit, dict):
        raise ValidationError("unit_identity must be a mapping")
    require_keys(unit, UNIT_KEYS, "unit_identity")
    if not isinstance(unit["configuration"], dict) or not unit["configuration"]:
        raise ValidationError("unit_identity.configuration must be a non-empty mapping")

    software = data["software_state"]
    if not isinstance(software, dict):
        raise ValidationError("software_state must be a mapping")
    require_keys(software, SOFTWARE_KEYS, "software_state")

    conditions = data["conditions"]
    if not isinstance(conditions, dict):
        raise ValidationError("conditions must be a mapping")
    for key in ("network_scope", "wan_available", "ambient_temperature_c", "notes"):
        if key not in conditions:
            raise ValidationError(f"conditions missing {key}")

    validate_tooling(data["measurement_tools"])

    provisioning = data["provisioning"]
    if not isinstance(provisioning, dict):
        raise ValidationError("provisioning must be a mapping")
    for key in ("first_device_minutes", "repeat_device_minutes", "automation_level", "notes"):
        if key not in provisioning:
            raise ValidationError(f"provisioning missing {key}")

    run = data["workload_run"]
    if not isinstance(run, dict):
        raise ValidationError("workload_run must be a mapping")
    require_keys(run, RUN_KEYS, "workload_run")

    restart = data["restart_trials"]
    if not isinstance(restart, dict):
        raise ValidationError("restart_trials must be a mapping")
    if "repetitions_target" not in restart or "trials" not in restart:
        raise ValidationError("restart_trials requires repetitions_target and trials")

    if not isinstance(data["artifacts"], list):
        raise ValidationError("artifacts must be a list")
    string_list(data["notes"], "notes")

    result = data["result"]
    if not isinstance(result, dict):
        raise ValidationError("result must be a mapping")
    require_keys(result, RESULT_KEYS, "result")

    if kind == "template":
        validate_template(data, contract_index, workload_index)
    else:
        validate_actual(data, device_index, contract_index, workload_index)


def main() -> int:
    receipt_paths = sorted((ROOT / "experiment_receipts").glob("**/*.yaml"))
    if not receipt_paths:
        print("FAIL no experiment receipt YAML/template found", file=sys.stderr)
        return 1
    try:
        device_index = load_index(sorted((ROOT / "devices").glob("**/*.yaml")), "record_id")
        contract_index = load_index(
            sorted((ROOT / "capability_contracts").glob("**/*.yaml")),
            "contract_id",
        )
        workload_index = load_workloads(sorted((ROOT / "workloads").glob("**/workload.yaml")))
    except (ValidationError, OSError) as exc:
        print(f"FAIL index load: {exc}", file=sys.stderr)
        return 1

    errors: list[str] = []
    seen_ids: set[str] = set()
    for path in receipt_paths:
        rel = path.relative_to(ROOT)
        try:
            validate_receipt(path, device_index, contract_index, workload_index, seen_ids)
            print(f"PASS {rel}")
        except (ValidationError, OSError) as exc:
            errors.append(f"FAIL {rel}: {exc}")

    print()
    print(f"Validated {len(receipt_paths)} experiment receipt file(s).")
    if errors:
        print("\nValidation errors:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print("All experiment receipt checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
