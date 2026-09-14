# Comparisons

This directory is Layer C of the repository: evidence-gated device comparisons against explicit capability contracts.

## Current comparison

`low-power-local-registry-node-v0.1.yaml` evaluates:

- TP-Link Archer C7 v5;
- Synology DS220+;
- Dell Wyse 3040.

Current result, checked 2026-09-14:

```text
Archer C7 v5
  -> hard_requirements_pass at current record level

Dell Wyse 3040
  -> conditional
  -> AC Recovery must be configured for unattended restart

Synology DS220+
  -> blocked_by_unknowns
  -> basic-runtime vendor-cloud dependency is still unknown
  -> durable state requires separately counted SATA storage

ranked winner
  -> none
```

The Archer result is **not** a deployment recommendation or a local workload receipt. It means only that every hard field in the current capability contract has a supporting value in the current device record.

Ranking remains blocked by missing comparable evidence for:

- a common registry workload;
- same-window NL/EU used-market snapshots;
- comparable wall-power measurements;
- provisioning / repeat-provisioning time;
- hard-power-loss -> boot -> registry-service restart behavior;
- replacement availability and remaining-life evidence.

## Validation

`tools/validate_comparisons.py` checks that:

- comparison IDs are unique;
- referenced contracts and device records exist;
- contract paths exist;
- device record paths exist;
- `pass` / `conditional` are not backed entirely by unknown values;
- hard-requirement eligibility matches the individual requirement statuses;
- ranking gaps and blockers remain explicit.

CI runs comparison validation after device/contract validation.

See `COMPARISON_METHOD.md` for the truth rules.

## Rule

> **Passing hard contract fields is eligibility evidence. Ranking requires comparable workload, cost, power, recovery and friction evidence.**
