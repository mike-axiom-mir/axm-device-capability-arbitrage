# Structured Evidence Strength Gate

**Status:** Active validation rule.  
**Purpose:** Prevent structured recovery and locality entries from claiming a stronger positive truth state than their cited evidence claims support.

## Why this exists

`recovery.paths` and `locality.states` already carry `source_claim_ids`, and the base validator already checks that those IDs resolve inside the same device record.

That catches broken references, but it does not by itself prevent this contradiction:

```yaml
recovery:
  paths:
    - id: example
      state: COMMUNITY_VERIFIED
      source_claim_ids:
        - official_manual_only

evidence:
  claims:
    - id: official_manual_only
      state: DOCUMENTED
```

The path says the result was community-verified while its strongest cited evidence says only that it is documented.

`RECOVERY_PATH_MODEL.md` already states the intended rule:

> A path must not gain a stronger truth state than its supporting evidence warrants.

This gate makes that rule mechanical and applies the same evidence discipline to structured locality states.

## Positive evidence ladder

Only the positive/promotable truth states are ordered:

```text
DOCUMENTED
  < COMMUNITY_VERIFIED
  < LOCALLY_VERIFIED
  < REPRODUCIBLE
```

`UNRESEARCHED`, `DEPRECATED`, and `CONTRADICTED` are not weaker rungs on that ladder. They describe a different evidence condition and therefore cannot, by themselves, support promotion of a positive structured state.

## Validation rule

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

## Scope

This gate intentionally does **not**:

- infer missing evidence states;
- promote records automatically;
- rewrite existing records;
- decide that `REPRODUCIBLE` means every sub-claim is locally reproduced;
- rank source quality merely from URL type;
- replace the local-verification receipt gate;
- claim that a valid evidence link proves the real-world fact.

It only enforces that a structured positive state cannot outrun the truth state of the evidence claims it explicitly cites.

## CI

`tools/validate_structured_evidence_strength.py` scans every device YAML record and applies this rule to structured recovery and locality entries.

It runs after the base device/contract validator so structural mistakes are reported first.

## Root gate

**Truth:** a structured claim cannot silently outrun its cited evidence.  
**Agency / non-domination:** no capability or recovery claim is promoted merely because a stronger label would be convenient.  
**Continuity:** the evidence-strength relationship is executable repository policy rather than chat-only interpretation.  
**Wisdom before speed:** conservative states remain valid; the gate blocks unsupported promotion without forcing premature schema migration.
