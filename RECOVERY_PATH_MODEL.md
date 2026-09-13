# Recovery Path Model — additive v0.1 extension

**Status:** Provisional, evidence-driven extension to `CAPABILITY_SCHEMA.md`.  
**Purpose:** Represent recovery as state transitions with explicit data impact instead of a single positive/negative flag.

## Why this exists

The first five census records exposed two independent failure modes in a flat recovery model:

1. **Roborock S5:** a recovery path that exists from stock state does not imply that the same path exists after a persistent modification.
2. **Synology DS220+:** two valid recovery operations can have materially different effects on configuration, user data, and application state.

Therefore:

> **Recovery is a transition from one device state to another, with an evidence state and an impact on retained state/data.**

The existing scalar recovery fields remain useful summaries. `recovery.paths` is an additive structured layer and does not retroactively make older records invalid.

## Provisional machine-readable shape

```yaml
recovery:
  recovery_state: DOCUMENTED
  paths:
    - id: mode_2_dsm_reinstall
      from_state: operating_dsm
      target_state: reinstalled_dsm
      method: physical_reset_mode_2
      availability: true
      state: DOCUMENTED
      data_impact:
        system_configuration: erased
        user_data: preserved
        application_state: unknown
      source_claim_ids:
        - official_reset_and_dsm_reinstall
      notes:
        - "Stored data is documented as preserved; application/container-state survival is not yet established."
```

## Required path fields

Each structured path should contain:

- `id` — stable identifier unique inside the device record;
- `from_state` — the state in which the path claim applies;
- `target_state` — the state expected after the operation, or the desired target when `availability: false`;
- `method` — concise description of the operation;
- `availability` — `true`, `false`, or `unknown`;
- `state` — one of the repository truth states;
- `data_impact` — effects on configuration/data/application state;
- `source_claim_ids` — one or more claim IDs from the record's `evidence.claims`.

`from_state` and `target_state` are intentionally free strings for now. More hardware classes should pressure the vocabulary before it is frozen into an enum.

## Data-impact vocabulary

The provisional values are:

```text
preserved
erased
partially_reset
must_recreate
unknown
not_applicable
```

Required impact fields:

```yaml
data_impact:
  system_configuration: unknown
  user_data: unknown
  application_state: unknown
```

Use `unknown` when the outcome matters but evidence does not establish it. Use `not_applicable` only when the dimension genuinely does not apply to that path.

## Negative recovery evidence

An unavailable path is still valuable recovery evidence.

Example:

```yaml
- id: return_to_stock_after_valetudo
  from_state: rooted_valetudo
  target_state: stock
  method: return_to_stock
  availability: false
  state: DOCUMENTED
  data_impact:
    system_configuration: not_applicable
    user_data: not_applicable
    application_state: not_applicable
  source_claim_ids:
    - post_modification_irreversibility
```

This prevents a stock-only factory reset from being misread as proof of post-modification reversibility.

## Evidence linkage

Every path must point to claim IDs already present in the same device record. A path must not gain a stronger truth state than its supporting evidence warrants.

The validator checks:

- path IDs are unique;
- required fields are present;
- path truth states are valid;
- availability uses `true`, `false`, or `unknown`;
- data-impact values use the provisional vocabulary;
- every `source_claim_ids` entry resolves to an evidence claim in the same record.

This keeps recovery semantics inspectable without requiring a rigid full-device schema.

## What this model does not claim yet

It does not yet encode:

- estimated recovery duration;
- probability of recovery success;
- tool cost;
- destructive hardware steps;
- backup prerequisites;
- firmware image provenance/checksums;
- whether recovery has been locally rehearsed;
- dependencies between recovery paths.

Those may become necessary after more evidence, but they should not be invented before records pressure the need.

## Root gate

**Truth:** recovery claims stay scoped to the state and evidence that support them.  
**Agency / non-domination:** recovery never authorizes modifying hardware without ownership/consent.  
**Continuity:** path semantics and their evidence linkage live in repository state.  
**Wisdom before speed:** data loss, irreversibility, and rebuild burden remain visible instead of being hidden behind `recovery: true`.
