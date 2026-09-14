# Experiment Receipts

This directory is for machine-readable receipts from **actual local/physical experiments**.

Start from `TEMPLATE.yaml` and follow `../LOCAL_EXPERIMENT_RECEIPT_METHOD.md`.

Current state:

- no physical candidate receipt is present yet;
- the template is not evidence of a device result;
- CI validates the template shape and will validate future real receipts;
- adding a receipt does not automatically promote the corresponding device record.

For the first registry comparison, actual receipts should bind to:

- `contract_id: low-power-local-registry-node`
- `workload_id: low-power-local-registry-v0.1`

Preserve failures as receipts too. Unknown is preferable to invented certainty.
