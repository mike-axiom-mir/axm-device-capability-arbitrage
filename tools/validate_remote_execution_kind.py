#!/usr/bin/env python3
"""Validate optional classification of off-endpoint execution.

`execution.surfaces[].locus: remote_service` proves that developer-controlled
logic runs somewhere other than the recorded endpoint. This gate preserves the
material distinction between a local companion host and an internet/cloud
service without widening the core execution-locus vocabulary.
"""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]

ALLOWED_REMOTE_KINDS = {
    "companion_host",
    "cloud_service",
    "other_remote",
    "unknown",
}


class ValidationError(Exception):
    pass


def validate_surface(surface: dict[str, Any], context: str) -> bool:
    """Validate one execution surface.

    Returns True when this surface declares locus: remote_service.
    """
    locus = surface.get("locus")
    has_kind = "remote_kind" in surface

    if locus == "remote_service":
        if not has_kind:
            raise ValidationError(
                f"{context}.remote_kind is required when locus is 'remote_service'"
            )
        kind = surface["remote_kind"]
        if not isinstance(kind, str) or not kind.strip():
            raise ValidationError(f"{context}.remote_kind must be a non-empty string")
        if kind not in ALLOWED_REMOTE_KINDS:
            allowed = ", ".join(sorted(ALLOWED_REMOTE_KINDS))
            raise ValidationError(
                f"{context}.remote_kind has invalid value {kind!r}; allowed: {allowed}"
            )
        return True

    if has_kind:
        raise ValidationError(
            f"{context}.remote_kind is only valid when locus is 'remote_service'"
        )

    return False


def validate_device(path: Path) -> int:
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        raise ValidationError(f"invalid YAML: {exc}") from exc

    if not isinstance(data, dict):
        raise ValidationError("top-level YAML must be a mapping")

    execution = data.get("execution")
    if not isinstance(execution, dict):
        raise ValidationError("execution must be a mapping")

    surfaces = execution.get("surfaces")
    if not isinstance(surfaces, list) or not surfaces:
        raise ValidationError("execution.surfaces must be a non-empty list")

    classified = 0
    for index, surface in enumerate(surfaces):
        context = f"execution.surfaces[{index}]"
        if not isinstance(surface, dict):
            raise ValidationError(f"{context} must be a mapping")
        if validate_surface(surface, context):
            classified += 1

    return classified


def main() -> int:
    paths = sorted((ROOT / "devices").glob("**/*.yaml"))
    if not paths:
        print("FAIL remote execution kind: no device records found", file=sys.stderr)
        return 1

    errors: list[str] = []
    classified_total = 0

    for path in paths:
        rel = path.relative_to(ROOT)
        try:
            classified = validate_device(path)
            classified_total += classified
            print(f"PASS {rel}: {classified} remote-service classification(s)")
        except (ValidationError, OSError) as exc:
            errors.append(f"FAIL {rel}: {exc}")

    print()
    print(
        f"Checked {len(paths)} device record(s); "
        f"validated {classified_total} remote-service classification(s)."
    )

    if errors:
        print("\nRemote execution-kind validation errors:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(
        "Every remote-service execution surface identifies whether its "
        "developer-controlled logic runs on a companion host, in a cloud service, "
        "in another off-endpoint location, or remains unknown."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
