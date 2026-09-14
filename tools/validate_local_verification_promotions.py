#!/usr/bin/env python3
"""Gate device-level local-verification promotion on preserved experiment receipts.

This validator intentionally does not promote any device by itself. It only prevents
LOCALLY_VERIFIED/REPRODUCIBLE device claims from existing without at least one
owned/authorized actual experiment receipt that explicitly claims local verification
for the same device. Receipt scope still has to be reviewed before individual claims
are promoted.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
LOCAL_TRUTH_STATES = {"LOCALLY_VERIFIED", "REPRODUCIBLE"}


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
    return value.strip()


def load_receipts(paths: list[Path]) -> dict[str, dict[str, Any]]:
    receipts: dict[str, dict[str, Any]] = {}
    for path in paths:
        data = load_yaml(path)
        receipt_id = require_string(
            data.get("receipt_id"), f"{path.relative_to(ROOT)}.receipt_id"
        )
        if receipt_id in receipts:
            raise ValidationError(f"duplicate receipt_id: {receipt_id}")
        receipts[receipt_id] = data
    return receipts


def qualifying_receipt(receipt: dict[str, Any], record_id: str) -> bool:
    if receipt.get("receipt_kind") != "actual":
        return False
    if receipt.get("device_record_id") != record_id:
        return False

    authorization = receipt.get("authorization")
    if not isinstance(authorization, dict):
        return False
    if authorization.get("owned_or_authorized") is not True:
        return False

    result = receipt.get("result")
    if not isinstance(result, dict):
        return False
    if result.get("local_verification_claimed") is not True:
        return False
    if result.get("overall_state") not in LOCAL_TRUTH_STATES:
        return False

    artifacts = receipt.get("artifacts")
    if not isinstance(artifacts, list) or not artifacts:
        return False

    return True


def validate_device(
    path: Path,
    receipts: dict[str, dict[str, Any]],
) -> None:
    data = load_yaml(path)
    record_id = require_string(data.get("record_id"), f"{path.relative_to(ROOT)}.record_id")

    evidence = data.get("evidence")
    if not isinstance(evidence, dict):
        raise ValidationError("evidence must be a mapping")

    locally_verified = evidence.get("locally_verified", False)
    if not isinstance(locally_verified, bool):
        raise ValidationError("evidence.locally_verified must be boolean when present")

    overall_state = evidence.get("overall_state")
    local_state_used = overall_state in LOCAL_TRUTH_STATES

    claims = evidence.get("claims", [])
    if not isinstance(claims, list):
        raise ValidationError("evidence.claims must be a list")
    for index, claim in enumerate(claims):
        if not isinstance(claim, dict):
            raise ValidationError(f"evidence.claims[{index}] must be a mapping")
        if claim.get("state") in LOCAL_TRUTH_STATES:
            local_state_used = True

    if local_state_used and locally_verified is not True:
        raise ValidationError(
            "record uses LOCALLY_VERIFIED/REPRODUCIBLE evidence but "
            "evidence.locally_verified is not true"
        )

    if not locally_verified:
        return

    matching_ids = sorted(
        receipt_id
        for receipt_id, receipt in receipts.items()
        if qualifying_receipt(receipt, record_id)
    )
    if not matching_ids:
        raise ValidationError(
            "evidence.locally_verified=true requires at least one actual experiment "
            "receipt for this device with owned_or_authorized=true, "
            "result.local_verification_claimed=true, a local truth state, and artifacts"
        )

    print(f"  local verification receipt(s): {', '.join(matching_ids)}")


def main() -> int:
    device_paths = sorted((ROOT / "devices").glob("**/*.yaml"))
    receipt_paths = sorted((ROOT / "experiment_receipts").glob("**/*.yaml"))

    if not device_paths:
        print("FAIL no device YAML records found", file=sys.stderr)
        return 1
    if not receipt_paths:
        print("FAIL no experiment receipt YAML records found", file=sys.stderr)
        return 1

    try:
        receipts = load_receipts(receipt_paths)
    except (ValidationError, OSError) as exc:
        print(f"FAIL receipt index: {exc}", file=sys.stderr)
        return 1

    errors: list[str] = []
    for path in device_paths:
        rel = path.relative_to(ROOT)
        try:
            validate_device(path, receipts)
            print(f"PASS {rel}")
        except (ValidationError, OSError) as exc:
            errors.append(f"FAIL {rel}: {exc}")

    print()
    print(
        f"Checked local-verification promotion for {len(device_paths)} device record(s) "
        f"against {len(receipt_paths)} receipt file(s)."
    )

    if errors:
        print("\nValidation errors:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print("All local-verification promotion gates passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
