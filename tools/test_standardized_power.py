#!/usr/bin/env python3
"""Regression tests for the standardized-power provenance gate."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import validate_standardized_power as gate


def base_record() -> dict:
    return {
        "power": {
            "standardized_measurements": [
                {
                    "id": "networked_standby",
                    "metric": "networked_standby_power",
                    "watts": 1.6,
                    "input_condition": "230 V AC, 50 Hz",
                    "test_condition": "EN 50564:2011; microphone muted",
                    "measurement_kind": "manufacturer_standardized_test",
                    "locally_measured": False,
                    "state": "DOCUMENTED",
                    "source_claim_ids": ["power_claim"],
                }
            ]
        },
        "evidence": {
            "claims": [
                {
                    "id": "power_claim",
                    "state": "DOCUMENTED",
                    "source": "https://example.invalid/power",
                }
            ]
        },
    }


def expect_pass(name: str, record: dict) -> None:
    try:
        gate.validate_measurements(record)
    except gate.ValidationError as exc:
        raise AssertionError(f"{name} unexpectedly failed: {exc}") from exc


def expect_fail(name: str, record: dict, fragment: str) -> None:
    try:
        gate.validate_measurements(record)
    except gate.ValidationError as exc:
        if fragment not in str(exc):
            raise AssertionError(f"{name} failed for wrong reason: {exc}") from exc
        return
    raise AssertionError(f"{name} unexpectedly passed")


def main() -> int:
    expect_pass("manufacturer scoped measurement", base_record())

    local = base_record()
    local["power"]["standardized_measurements"][0]["measurement_kind"] = "local_standardized_test"
    local["power"]["standardized_measurements"][0]["locally_measured"] = True
    expect_pass("local standardized measurement", local)

    missing_condition = base_record()
    del missing_condition["power"]["standardized_measurements"][0]["test_condition"]
    expect_fail("missing test condition", missing_condition, "missing required keys")

    bad_kind = base_record()
    bad_kind["power"]["standardized_measurements"][0]["measurement_kind"] = "manufacturer_guess"
    expect_fail("unknown invented kind", bad_kind, "measurement_kind must be one of")

    fake_local = base_record()
    fake_local["power"]["standardized_measurements"][0]["locally_measured"] = True
    expect_fail("manufacturer result cannot become local", fake_local, "requires measurement_kind local_standardized_test")

    local_false = base_record()
    local_false["power"]["standardized_measurements"][0]["measurement_kind"] = "local_standardized_test"
    expect_fail("local kind requires local flag", local_false, "requires locally_measured: true")

    missing_claim = base_record()
    missing_claim["power"]["standardized_measurements"][0]["source_claim_ids"] = ["missing"]
    expect_fail("unresolved evidence link", missing_claim, "unknown evidence claim")

    duplicate_claim = base_record()
    duplicate_claim["power"]["standardized_measurements"][0]["source_claim_ids"] = ["power_claim", "power_claim"]
    expect_fail("duplicate evidence link", duplicate_claim, "duplicate claim id")

    negative = base_record()
    negative["power"]["standardized_measurements"][0]["watts"] = -0.1
    expect_fail("negative watts", negative, "finite and non-negative")

    empty = base_record()
    empty["power"]["standardized_measurements"] = []
    expect_fail("empty collection", empty, "non-empty list")

    no_extension = {"power": {}, "evidence": {"claims": []}}
    expect_pass("extension remains optional", no_extension)

    print("PASS standardized power regression suite")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
