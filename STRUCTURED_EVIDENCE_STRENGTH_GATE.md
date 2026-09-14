# Structured Evidence Strength Gate

**Status:** Active validation rule.  
**Purpose:** Prevent record-level evidence summaries, core execution/recovery truth labels, and structured recovery/locality entries from claiming a stronger positive truth state than the evidence claims available to support them.

## Why this exists

The repo now carries several evidence-derived truth labels at different levels:

1. `evidence.overall_state`, a record-level summary;
2. `execution.surfaces[*].state`, the truth state of each claimed execution surface;
3. `recovery.recovery_state`, the flat recovery evidence summary;
4. structured `recovery.paths[*].state` and `locality.states[*].state` entries.

`recovery.paths` and `locality.states` already carry `source_claim_ids`, and the base validator checks that those IDs resolve inside the same device record. That allows an exact cited-evidence ceiling for those structured entries.

The record-level summary, execution surfaces, and flat recovery summary do not yet carry mandatory claim links in schema v0.1. Without a second guard, one of those convenient labels could theoretically claim `COMMUNITY_VERIFIED`, `LOCALLY_VERIFIED`, or `REPRODUCIBLE` even when no positive evidence claim in the record reaches that state.

This gate therefore uses two deliberately different checks:

- **record ceiling** for unlinked summary/core states: they may not be stronger than the strongest positive evidence claim anywhere in that device record;
- **cited ceiling** for structured recovery/locality entries: they may not be stronger than the positive claims they explicitly cite.

The first rule is intentionally weaker than claim-specific provenance. It prevents impossible upward inflation without pretending an unrelated strong claim proves the field being checked.

## Positive evidence ladder

Only the positive/promotable truth states are ordered:

```text
DOCUMENTED
  < COMMUNITY_VERIFIED
  < LOCALLY_VERIFIED
  < REPRODUCIBLE
```

`UNRESEARCHED`, `DEPRECATED`, and `CONTRADICTED` are not weaker rungs on that ladder. They describe different evidence conditions and therefore cannot raise a positive evidence ceiling.

## Rule A — Record-level summary

When `evidence.overall_state` uses a positive truth state:

1. the record must contain at least one positive evidence claim;
2. the strongest positive claim must be equal to or stronger than `evidence.overall_state`;
3. the summary may remain deliberately more conservative than the strongest claim;
4. non-promoting claims do not count as positive support.

Examples:

```text
overall DOCUMENTED
  <- strongest claim COMMUNITY_VERIFIED
  PASS

overall COMMUNITY_VERIFIED
  <- strongest claim COMMUNITY_VERIFIED
  PASS

overall COMMUNITY_VERIFIED
  <- strongest claim DOCUMENTED
  FAIL

overall LOCALLY_VERIFIED
  <- no positive claims
  FAIL
```

This does **not** mean that the strongest single claim proves every fact in the record. `overall_state` remains only a conservative evidence summary.

## Rule B — Core execution and flat recovery ceilings

Every `execution.surfaces[*].state` and `recovery.recovery_state` is now checked against the strongest positive evidence claim in the same record.

Examples:

```text
execution surface DOCUMENTED
  <- strongest claim COMMUNITY_VERIFIED
  PASS

execution surface COMMUNITY_VERIFIED
  <- strongest claim DOCUMENTED
  FAIL

recovery summary COMMUNITY_VERIFIED
  <- strongest claim COMMUNITY_VERIFIED
  PASS

recovery summary REPRODUCIBLE
  <- strongest claim COMMUNITY_VERIFIED
  FAIL
```

This closes a structural truth gap: a core capability label can no longer outrun every positive evidence claim in its record merely because it is not one of the structured fields with `source_claim_ids`.

The limitation is explicit:

> **Record-level ceiling is not claim-specific provenance.**

A strong execution claim does not prove recovery, and a strong recovery claim does not prove execution. Until schema evidence justifies mandatory claim links for every core field, this gate blocks only impossible evidence-strength inflation. Human review and claim text still determine whether the source actually supports the specific fact.

## Rule C — Structured recovery/locality state

For each entry in:

- `recovery.paths`
- `locality.states`

when the entry itself uses a positive truth state:

1. `source_claim_ids` must contain at least one positive evidence claim;
2. the strongest cited positive claim must be equal to or stronger than the entry state;
3. stronger cited evidence may support a deliberately more conservative entry state;
4. unresolved, deprecated, or contradicted citations remain visible but do not raise the positive evidence ceiling.

Examples:

```text
entry DOCUMENTED
  <- cited DOCUMENTED
  PASS

entry DOCUMENTED
  <- cited COMMUNITY_VERIFIED
  PASS

entry COMMUNITY_VERIFIED
  <- cited DOCUMENTED only
  FAIL

entry LOCALLY_VERIFIED
  <- cited COMMUNITY_VERIFIED only
  FAIL

entry DOCUMENTED
  <- cited CONTRADICTED only
  FAIL
```

Entries whose own state is `UNRESEARCHED`, `DEPRECATED`, or `CONTRADICTED` are not promoted by this validator. Their structural references remain governed by the base record validator.

## Why not require claim links on every execution surface yet?

That may become the stronger long-term model, but schema v0.1 is still being pressure-tested across very different hardware classes.

Immediately forcing `source_claim_ids` onto every existing execution surface would be a broad migration. The current evidence does justify a smaller invariant now:

> **No positive core truth label may be stronger than every positive evidence claim in its device record.**

If independent records show that exact execution-to-claim linkage is repeatedly necessary, the schema can add it explicitly and migrate records with preserved provenance rather than silently rewriting them during a validator change.

## What the gate intentionally does not do

It does **not**:

- infer missing evidence states;
- promote records automatically;
- rewrite existing records;
- decide that one `REPRODUCIBLE` claim makes every device property reproducible;
- decide that the strongest claim in a record is relevant to every execution or recovery field;
- rank source quality merely from URL type;
- replace the local-verification receipt gate;
- replace claim-specific `source_claim_ids` where the schema already requires them;
- claim that syntactically valid evidence proves the real-world fact.

The gate only prevents positive state labels from being stronger than the evidence state mechanically available to support them.

## CI

`tools/validate_structured_evidence_strength.py` scans every device YAML record.

It now checks:

- `evidence.overall_state` against the strongest positive evidence claim in the same record;
- every `execution.surfaces[*].state` against that record-level positive evidence ceiling;
- `recovery.recovery_state` against that record-level positive evidence ceiling;
- each structured recovery path against the positive evidence claims it cites;
- each structured locality state against the positive evidence claims it cites.

It runs after the base device/contract validator so structural mistakes are reported first. The separate local-verification promotion gate still decides whether local truth states are backed by preserved owned/authorized experiment receipts.

## Root gate

**Truth:** summary, execution, recovery, and structured truth labels cannot silently outrun the evidence state mechanically available to support them.  
**Agency / non-domination:** no capability or recovery status is promoted merely because a stronger label would be convenient.  
**Continuity:** evidence-strength relationships are executable repository policy rather than chat-only interpretation.  
**Wisdom before speed:** the gate adds a conservative ceiling now without pretending record-level strength is claim-specific provenance or forcing a premature whole-census schema migration.
