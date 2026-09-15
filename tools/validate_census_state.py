#!/usr/bin/env python3
"""Validate that human census state matches the machine-readable device records.

This guard intentionally validates synchronization, not research quality. Device
record structure/evidence semantics remain the responsibility of validate_records.py
and the other evidence-specific validators.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
CENSUS_PATH = ROOT / "CENSUS.md"
NEXT_BUILD_PATH = ROOT / "NEXT_BUILD.md"
MILESTONE_DEVICE_TARGET = 25
MILESTONE_CATEGORY_TARGET = 8


class ValidationError(Exception):
    pass


def load_device(path: Path) -> dict[str, Any]:
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        raise ValidationError(f"{path.relative_to(ROOT)} invalid YAML: {exc}") from exc
    if not isinstance(data, dict):
        raise ValidationError(f"{path.relative_to(ROOT)} top-level YAML must be a mapping")
    return data


def require_match(pattern: str, text: str, context: str, flags: int = 0) -> re.Match[str]:
    match = re.search(pattern, text, flags)
    if not match:
        raise ValidationError(f"could not parse {context}")
    return match


def parse_devices() -> tuple[list[Path], set[str]]:
    paths = sorted((ROOT / "devices").glob("**/*.yaml"))
    if not paths:
        raise ValidationError("no device YAML records found")

    categories: set[str] = set()
    for path in paths:
        data = load_device(path)
        identity = data.get("identity")
        if not isinstance(identity, dict):
            raise ValidationError(f"{path.relative_to(ROOT)} identity must be a mapping")
        category = identity.get("marketed_category")
        if not isinstance(category, str) or not category.strip():
            raise ValidationError(
                f"{path.relative_to(ROOT)} identity.marketed_category must be a non-empty string"
            )
        categories.add(category.strip())

    return paths, categories


def validate_census(census_text: str, device_paths: list[Path], categories: set[str]) -> None:
    milestone = require_match(
        r"\*\*Milestone 01:\*\*\s*(\d+)\s+evidence-backed devices across at least\s+(\d+)\s+marketed categories\.",
        census_text,
        "CENSUS.md Milestone 01 declaration",
    )
    milestone_devices = int(milestone.group(1))
    milestone_categories = int(milestone.group(2))
    if milestone_devices != MILESTONE_DEVICE_TARGET or milestone_categories != MILESTONE_CATEGORY_TARGET:
        raise ValidationError(
            "CENSUS.md milestone declaration drifted: "
            f"expected {MILESTONE_DEVICE_TARGET} devices / {MILESTONE_CATEGORY_TARGET} categories, "
            f"found {milestone_devices} / {milestone_categories}"
        )

    count_match = require_match(
        r"Devices:\s*(\d+)\s*/\s*(\d+).*?Categories:\s*(\d+)\s+distinct\s*/\s*(\d+)\s+required",
        census_text,
        "CENSUS.md current grounded count",
        flags=re.DOTALL,
    )
    declared_devices = int(count_match.group(1))
    declared_device_target = int(count_match.group(2))
    declared_categories = int(count_match.group(3))
    declared_category_target = int(count_match.group(4))

    actual_devices = len(device_paths)
    actual_categories = len(categories)

    if declared_device_target != MILESTONE_DEVICE_TARGET:
        raise ValidationError(
            f"CENSUS.md device target says {declared_device_target}; expected {MILESTONE_DEVICE_TARGET}"
        )
    if declared_category_target != MILESTONE_CATEGORY_TARGET:
        raise ValidationError(
            f"CENSUS.md category target says {declared_category_target}; expected {MILESTONE_CATEGORY_TARGET}"
        )
    if declared_devices != actual_devices:
        raise ValidationError(
            f"CENSUS.md declares {declared_devices} devices but devices/ contains {actual_devices} YAML records"
        )
    if declared_categories != actual_categories:
        raise ValidationError(
            f"CENSUS.md declares {declared_categories} distinct categories but device records contain {actual_categories}"
        )

    row_pattern = re.compile(
        r"^\|\s*(\d+)\s*\|.*?\|\s*`(devices/[^`]+\.yaml)`\s*\|\s*$",
        re.MULTILINE,
    )
    rows = [(int(number), path) for number, path in row_pattern.findall(census_text)]
    if len(rows) != actual_devices:
        raise ValidationError(
            f"CENSUS.md current-records table has {len(rows)} device rows; expected {actual_devices}"
        )

    row_numbers = [number for number, _ in rows]
    expected_numbers = list(range(1, actual_devices + 1))
    if row_numbers != expected_numbers:
        raise ValidationError(
            f"CENSUS.md row numbering must be contiguous 1..{actual_devices}; found {row_numbers}"
        )

    listed_paths = [path for _, path in rows]
    if len(set(listed_paths)) != len(listed_paths):
        raise ValidationError("CENSUS.md current-records table contains duplicate device paths")

    actual_paths = {path.relative_to(ROOT).as_posix() for path in device_paths}
    listed_set = set(listed_paths)
    missing = sorted(actual_paths - listed_set)
    extra = sorted(listed_set - actual_paths)
    if missing or extra:
        details: list[str] = []
        if missing:
            details.append("missing from CENSUS.md: " + ", ".join(missing))
        if extra:
            details.append("listed but absent from devices/: " + ", ".join(extra))
        raise ValidationError("; ".join(details))

    coverage_match = require_match(
        r"## Category coverage\s*(.*?)(?:\n## |\Z)",
        census_text,
        "CENSUS.md category coverage section",
        flags=re.DOTALL,
    )
    checked_count = len(
        re.findall(r"^- \[x\] ", coverage_match.group(1), flags=re.MULTILINE | re.IGNORECASE)
    )
    if checked_count != actual_categories:
        raise ValidationError(
            f"CENSUS.md category checklist has {checked_count} checked entries; "
            f"device records contain {actual_categories} distinct marketed categories"
        )


def validate_next_build(next_build_text: str, actual_devices: int, actual_categories: int) -> None:
    state = require_match(
        r"\*\*Current state:\*\*.*?contains\s+([\w-]+)\s+grounded records across\s+([\w-]+)\s+marketed categories\..*?Milestone 01 still requires\s+(\d+)\s+more evidence-backed devices",
        next_build_text,
        "NEXT_BUILD.md current-state census summary",
        flags=re.DOTALL,
    )

    number_words = {
        "zero": 0,
        "one": 1,
        "two": 2,
        "three": 3,
        "four": 4,
        "five": 5,
        "six": 6,
        "seven": 7,
        "eight": 8,
        "nine": 9,
        "ten": 10,
        "eleven": 11,
        "twelve": 12,
        "thirteen": 13,
        "fourteen": 14,
        "fifteen": 15,
        "sixteen": 16,
        "seventeen": 17,
        "eighteen": 18,
        "nineteen": 19,
        "twenty": 20,
        "twenty-one": 21,
        "twenty-two": 22,
        "twenty-three": 23,
        "twenty-four": 24,
        "twenty-five": 25,
    }

    def parse_word_or_int(value: str, context: str) -> int:
        if value.isdigit():
            return int(value)
        parsed = number_words.get(value.lower())
        if parsed is None:
            raise ValidationError(f"NEXT_BUILD.md {context} uses unsupported number word {value!r}")
        return parsed

    declared_devices = parse_word_or_int(state.group(1), "device count")
    declared_categories = parse_word_or_int(state.group(2), "category count")
    declared_remaining = int(state.group(3))
    expected_remaining = MILESTONE_DEVICE_TARGET - actual_devices

    if declared_devices != actual_devices:
        raise ValidationError(
            f"NEXT_BUILD.md says {declared_devices} grounded records; actual device count is {actual_devices}"
        )
    if declared_categories != actual_categories:
        raise ValidationError(
            f"NEXT_BUILD.md says {declared_categories} marketed categories; actual distinct count is {actual_categories}"
        )
    if declared_remaining != expected_remaining:
        raise ValidationError(
            f"NEXT_BUILD.md says {declared_remaining} records remain; expected {expected_remaining}"
        )


def main() -> int:
    try:
        device_paths, categories = parse_devices()
        census_text = CENSUS_PATH.read_text(encoding="utf-8")
        next_build_text = NEXT_BUILD_PATH.read_text(encoding="utf-8")
        validate_census(census_text, device_paths, categories)
        validate_next_build(next_build_text, len(device_paths), len(categories))
    except (ValidationError, OSError) as exc:
        print(f"FAIL census state: {exc}", file=sys.stderr)
        return 1

    print(
        "PASS census state: "
        f"{len(device_paths)} device records, {len(categories)} distinct marketed categories, "
        f"{MILESTONE_DEVICE_TARGET - len(device_paths)} device slots remaining."
    )
    print("CENSUS.md table/counts and NEXT_BUILD.md current-state summary are synchronized.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
