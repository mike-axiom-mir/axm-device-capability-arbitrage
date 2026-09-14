# Structured Evidence Strength Gate

**Status:** Active validation rule.  
**Purpose:** Prevent record-level evidence summaries and structured recovery/locality entries from claiming a stronger positive truth state than the evidence claims supporting them.

## Why this exists

The repo has two different kinds of evidence-derived truth labels:

1. `evidence.overall_state`, a record-level summary;
2. structured `recovery.paths[*].state` and `locality.states[*].state` entries.

`recovery.paths` and `locality.states` already carry `source_claim_ids`, and the base validator already checks that those IDs resolve inside the same device record. That catches broken references, but it does not by itself prevent a structured state from outrunning its cited evidence.

The record-level summary had a similar gap. Before this gate was extended, a record could theoretically say:

```yaml
evidence:
  overall_state: COMMUNITY_VERIFIED
  claims:
    - id: official_manual_only
      state: DOCUMENTED
```

That would make the convenient summary stronger than every positive claim in the record.

The gate now makes both relationships mechanical.

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

This does **not** mean that the strongest single claim proves every fact in the record. `overall_state` remains only a conservative evidence summary. The validator prevents upward inflation; it does not turn the summary into a substitute for claim-level provenance.

## Rule B — Structured recovery/locality state

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

## What the gate intentionally does not do

It does **not**:

- infer missing evidence states;
- promote records automatically;
- rewrite existing records;
- decide that one `REPRODUCIBLE` claim makes every device property reproducible;
- rank source quality merely from URL type;
- replace the local-verification receipt gate;
- replace claim-specific `source_claim_ids` where the schema already requires them;
- claim that syntactically valid evidence proves the real-world fact.

The gate only prevents a positive state label from being stronger than the evidence state available to support that label.

## CI

`tools/validate_structured_evidence_strength.py` scans every device YAML record.

It now checks:

- `evidence.overall_state` against the strongest positive evidence claim in the same record;
- each structured recovery path against the positive evidence claims it cites;
- each structured locality state against the positive evidence claims it cites.

It runs after the base device/contract validator so structural mistakes are reported first. The separate local-verification promotion gate still decides whether local truth states are backed by preserved owned/authorized experiment receipts.

## Root gate

**Truth:** summary and structured truth labels cannot silently outrun the evidence state available to support them.  
**Agency / non-domination:** no capability, recovery, locality, or whole-record status is promoted merely because a stronger label would be convenient.  
**Continuity:** evidence-strength relationships are executable repository policy rather than chat-only interpretation.  
**Wisdom before speed:** conservative labels remain valid; the gate blocks unsupported promotion without forcing broad schema migration.
