#!/usr/bin/env python3
"""Validate narrative evidence packets against machine-readable device evidence metadata.

This gate protects continuity between evidence/*.md and devices/**/*.yaml. It does not
judge whether an external source is trustworthy, reachable, current, or factually
correct; source/claim semantics remain the responsibility of the other evidence gates.
"""
from __future__ import annotations

import re
import sys
from datetime import date
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
DEVICE_REF_RE = re.compile(r"`(devices/[^`\n]+\.yaml)`")
CHECKED_RE = re.compile(r"^\*\*Checked:\*\*\s*(\d{4}-\d{2}-\d{2})\s*$", re.MULTILINE)
YES_NO_RE = re.compile(r"\b(Yes|No)\b", re.IGNORECASE)


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


def require_string(value: Any, context: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValidationError(f"{context} must be a non-empty string")
    return value.strip()


def canonical_date(value: Any, context: str) -> str:
    text = require_string(value, context)
    try:
        parsed = date.fromisoformat(text)
    except ValueError as exc:
        raise ValidationError(f"{context} must be canonical ISO YYYY-MM-DD") from exc
    if parsed.isoformat() != text:
        raise ValidationError(f"{context} must be canonical ISO YYYY-MM-DD")
    return text


def load_devices(paths: list[Path]) -> dict[str, dict[str, Any]]:
    devices: dict[str, dict[str, Any]] = {}
    seen_record_ids: set[str] = set()

    for path in paths:
        rel = path.relative_to(ROOT).as_posix()
        data = load_yaml(path)
        record_id = require_string(data.get("record_id"), f"{rel}.record_id")
        if record_id in seen_record_ids:
            raise ValidationError(f"duplicate device record_id {record_id!r}")
        seen_record_ids.add(record_id)

        evidence = data.get("evidence")
        if not isinstance(evidence, dict):
            raise ValidationError(f"{rel}.evidence must be a mapping")

        state = require_string(evidence.get("overall_state"), f"{rel}.evidence.overall_state")
        if state not in TRUTH_STATES:
            raise ValidationError(
                f"{rel}.evidence.overall_state {state!r} is not a known truth state"
            )

        checked = canonical_date(evidence.get("last_checked"), f"{rel}.evidence.last_checked")
        locally_verified = evidence.get("locally_verified")
        if not isinstance(locally_verified, bool):
            raise ValidationError(f"{rel}.evidence.locally_verified must be boolean")

        devices[rel] = {
            "record_id": record_id,
            "overall_state": state,
            "last_checked": checked,
            "locally_verified": locally_verified,
        }

    return devices


def packet_metadata_header(text: str) -> str:
    """Return only the front metadata block before the first level-2 section."""
    return text.split("\n## ", 1)[0]


def parse_packet(path: Path) -> dict[str, Any]:
    rel = path.relative_to(ROOT).as_posix()
    text = path.read_text(encoding="utf-8")
    header = packet_metadata_header(text)

    device_refs = list(dict.fromkeys(DEVICE_REF_RE.findall(header)))
    if len(device_refs) != 1:
        raise ValidationError(
            f"{rel} metadata must reference exactly one `devices/...yaml` record; "
            f"found {device_refs or 'none'}"
        )

    checked_matches = CHECKED_RE.findall(header)
    if len(checked_matches) != 1:
        raise ValidationError(
            f"{rel} metadata must contain exactly one **Checked:** YYYY-MM-DD line"
        )
    checked = canonical_date(checked_matches[0], f"{rel}.Checked")

    state_matches: list[str] = []
    local_matches: list[bool] = []
    for line in header.splitlines():
        stripped = line.strip()
        if not stripped.startswith("**"):
            continue
        lowered = stripped.lower()

        # Existing packets use labels such as Evidence state, Current evidence
        # state, and Current overall state. Restrict matching to metadata lines
        # that actually name a state so ordinary prose cannot satisfy the gate.
        if "state" in lowered:
            found = [
                state
                for state in TRUTH_STATES
                if re.search(rf"\b{re.escape(state)}\b", stripped)
            ]
            state_matches.extend(found)

        # Existing packets use Local verification, Local hardware test, and
        # Locally reproduced by AXM. All are explicit Yes/No metadata.
        if "local" in lowered or "reproduced" in lowered:
            yes_no = YES_NO_RE.search(stripped)
            if yes_no:
                local_matches.append(yes_no.group(1).lower() == "yes")

    unique_states = list(dict.fromkeys(state_matches))
    if len(unique_states) != 1:
        raise ValidationError(
            f"{rel} metadata must declare exactly one truth state; "
            f"found {unique_states or 'none'}"
        )
    if len(local_matches) != 1:
        raise ValidationError(
            f"{rel} metadata must declare exactly one local-verification Yes/No value"
        )

    return {
        "device_path": device_refs[0],
        "checked": checked,
        "overall_state": unique_states[0],
        "locally_verified": local_matches[0],
    }


def validate_packet(
    packet_path: Path,
    metadata: dict[str, Any],
    devices: dict[str, dict[str, Any]],
) -> str:
    rel = packet_path.relative_to(ROOT).as_posix()
    device_path = metadata["device_path"]
    if device_path not in devices:
        raise ValidationError(f"{rel} references missing device record {device_path!r}")

    device = devices[device_path]
    mismatches: list[str] = []
    if metadata["checked"] != device["last_checked"]:
        mismatches.append(
            f"Checked={metadata['checked']} vs evidence.last_checked={device['last_checked']}"
        )
    if metadata["overall_state"] != device["overall_state"]:
        mismatches.append(
            f"packet state={metadata['overall_state']} vs "
            f"evidence.overall_state={device['overall_state']}"
        )
    if metadata["locally_verified"] != device["locally_verified"]:
        mismatches.append(
            "packet local verification="
            f"{metadata['locally_verified']} vs "
            f"evidence.locally_verified={device['locally_verified']}"
        )
    if mismatches:
        raise ValidationError(f"{rel} disagrees with {device_path}: " + "; ".join(mismatches))

    return device_path


def main() -> int:
    device_paths = sorted((ROOT / "devices").glob("**/*.yaml"))
    packet_paths = sorted((ROOT / "evidence").glob("**/*.md"))

    if not device_paths:
        print("FAIL no device YAML records found", file=sys.stderr)
        return 1
    if not packet_paths:
        print("FAIL no evidence packet Markdown files found", file=sys.stderr)
        return 1

    try:
        devices = load_devices(device_paths)
    except (ValidationError, OSError) as exc:
        print(f"FAIL evidence packet sync index: {exc}", file=sys.stderr)
        return 1

    errors: list[str] = []
    packet_by_device: dict[str, str] = {}

    for path in packet_paths:
        rel = path.relative_to(ROOT).as_posix()
        try:
            metadata = parse_packet(path)
            device_path = validate_packet(path, metadata, devices)
            if device_path in packet_by_device:
                raise ValidationError(
                    f"{rel} duplicates device packet already provided by "
                    f"{packet_by_device[device_path]}"
                )
            packet_by_device[device_path] = rel
            print(f"PASS {rel} -> {device_path}")
        except (ValidationError, OSError) as exc:
            errors.append(f"FAIL {rel}: {exc}")

    missing_packets = sorted(set(devices) - set(packet_by_device))
    if missing_packets:
        errors.append(
            "FAIL devices without exactly one evidence packet: " + ", ".join(missing_packets)
        )

    print()
    print(
        f"Checked {len(packet_paths)} evidence packet(s) against "
        f"{len(device_paths)} device record(s)."
    )

    if errors:
        print("\nValidation errors:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(
        "All evidence packets have one-to-one device coverage and synchronized "
        "checked date, overall truth state, and local-verification status."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
