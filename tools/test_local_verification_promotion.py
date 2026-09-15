#!/usr/bin/env python3
"""Regression checks for the local-verification promotion receipt discriminator."""

from __future__ import annotations

import copy
import importlib.util
import unittest
from pathlib import Path

MODULE_PATH = Path(__file__).with_name("validate_local_verification_promotions.py")
SPEC = importlib.util.spec_from_file_location("local_promotion_gate", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
GATE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(GATE)


class QualifyingReceiptTests(unittest.TestCase):
    def setUp(self) -> None:
        self.receipt = {
            "receipt_kind": "local_experiment",
            "device_record_id": "example-device",
            "authorization": {"owned_or_authorized": True},
            "result": {
                "local_verification_claimed": True,
                "overall_state": "LOCALLY_VERIFIED",
            },
            "artifacts": [
                {
                    "type": "log",
                    "location": "artifacts/example.log",
                    "sha256": "0" * 64,
                    "proves": "synthetic regression fixture only",
                }
            ],
        }

    def test_schema_valid_local_experiment_can_qualify(self) -> None:
        self.assertTrue(GATE.qualifying_receipt(self.receipt, "example-device"))

    def test_non_schema_actual_label_does_not_qualify(self) -> None:
        receipt = copy.deepcopy(self.receipt)
        receipt["receipt_kind"] = "actual"
        self.assertFalse(GATE.qualifying_receipt(receipt, "example-device"))

    def test_template_never_qualifies(self) -> None:
        receipt = copy.deepcopy(self.receipt)
        receipt["receipt_kind"] = "template"
        self.assertFalse(GATE.qualifying_receipt(receipt, "example-device"))

    def test_wrong_device_never_qualifies(self) -> None:
        self.assertFalse(GATE.qualifying_receipt(self.receipt, "different-device"))

    def test_missing_authorization_or_artifact_never_qualifies(self) -> None:
        unauthorized = copy.deepcopy(self.receipt)
        unauthorized["authorization"]["owned_or_authorized"] = False
        self.assertFalse(GATE.qualifying_receipt(unauthorized, "example-device"))

        no_artifacts = copy.deepcopy(self.receipt)
        no_artifacts["artifacts"] = []
        self.assertFalse(GATE.qualifying_receipt(no_artifacts, "example-device"))


if __name__ == "__main__":
    unittest.main()
