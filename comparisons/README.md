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

## Shared workload now exists

The comparison no longer lacks a common workload definition or implementation.

`workloads/low-power-local-registry-v0.1/` now contains:

- a bounded C99/POSIX registry service with no runtime dependencies;
- an explicit line protocol (`PING`, `PUT`, `GET`, `COUNT`);
- durable-ack semantics using temp-file fsync + rename + parent-directory fsync;
- a machine-readable 32-record / 30-minute comparison profile;
- a LAN-side benchmark driver;
- a host-CI functional restart-persistence check.

CI proves only the host implementation. It does **not** prove Archer C7 v5, DS220+, or Wyse 3040 compatibility, power use, physical hard-power-loss survival, or device service autostart. Candidate workload runs therefore remain `not_collected` and the comparison still has no ranked winner.

Ranking remains blocked by missing comparable evidence for:

- running the shared registry workload on all three candidates and recording its footprint;
- refreshing/normalizing acquisition cost when a ranking attempt is made, including shipping/accessories/storage;
- comparable wall-power measurements under the shared profile;
- provisioning / repeat-provisioning time;
- hard-power-loss -> boot -> registry-service restart behavior using the shared durable heartbeat;
- replacement availability and remaining-life evidence.

A dated configuration-aware EU market snapshot already exists under `market_snapshots/`; asking/displayed prices remain sample evidence rather than transaction-price truth.

## Validation

`tools/validate_comparisons.py` checks that:

- comparison IDs are unique;
- referenced contracts and device records exist;
- contract paths exist;
- device record paths exist;
- `pass` / `conditional` are not backed entirely by unknown values;
- hard-requirement eligibility matches the individual requirement statuses;
- ranking gaps and blockers remain explicit.

CI runs comparison validation after device/contract validation, then compiles and exercises the shared registry workload with `make test`.

See `COMPARISON_METHOD.md` for the truth rules.

## Rule

> **Passing hard contract fields is eligibility evidence. Ranking requires comparable workload, cost, power, recovery and friction evidence.**
