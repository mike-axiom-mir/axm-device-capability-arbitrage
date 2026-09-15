# Generic Source-Claim Link Gate

**Status:** Active validation rule.  
**Checked:** 2026-09-15  
**Purpose:** Keep evidence links trustworthy inside experimental device structures without freezing those structures into the core schema too early.

## Why this exists

The device census is intentionally allowed to discover new machine-state patterns before AXM knows the smallest reusable schema for them.

That flexibility has already produced useful local structures such as the TI-Nspire CX II-T `operational_modes` entries. Those entries preserve `source_claim_ids`, but the existing dedicated validators only know the semantics of mature structures such as:

- `recovery.paths`;
- `locality.states`;
- execution-surface `locus` annotations.

Before this gate, a new exploratory structure could therefore contain a machine-readable evidence pointer that was misspelled, duplicated, deleted later, or weaker than the truth state attached to that same structure without any generic repository-wide check catching the drift.

The answer is not to freeze every new hardware lesson into a universal schema. The smallest durable rule is simpler:

> **Whenever a device record chooses to preserve evidence through `source_claim_ids`, those links must remain real and internally coherent.**

## Mechanical rule

`tools/validate_source_claim_links.py` recursively walks every device YAML record.

For every mapping containing `source_claim_ids`, it requires:

1. a non-empty list;
2. non-empty string claim IDs;
3. no duplicate claim IDs in that list;
4. every referenced ID to resolve to an evidence claim in the same device record.

When the same mapping also uses one of the repository's evidence truth-state tokens in its `state` field, the gate additionally requires:

- a positive state (`DOCUMENTED`, `COMMUNITY_VERIFIED`, `LOCALLY_VERIFIED`, `REPRODUCIBLE`) to have at least one positive linked claim;
- the mapping's positive truth state not to outrun the strongest positive linked claim;
- non-promoting states (`UNRESEARCHED`, `DEPRECATED`, `CONTRADICTED`) to remain preservable without artificial promotion.

## What it deliberately does not do

The validator does **not** assume that every field named `state` is an evidence state.

Experimental structures may legitimately use domain states such as:

```text
stock
restricted
active
maintenance
```

If `state` is not one of the repository truth-state tokens, the generic gate checks only the evidence-link integrity. It does not reinterpret the local schema.

The validator also does not decide:

- whether a cited source really supports the local field semantics;
- whether an operational mode, safety boundary, admission rule, or future extension deserves a universal schema;
- whether a source is factually correct or current;
- whether a documented result was locally reproduced.

Those remain research and review questions, with dedicated validators added only when repeated hardware evidence justifies them.

## Current pressure case

The TI-Nspire CX II-T record contains an exploratory `operational_modes` structure with evidence links for normal and Press-to-Test/exam states:

```yaml
operational_modes:
  - id: normal_mode
    state: DOCUMENTED
    source_claim_ids:
      - official_exam_mode_access_boundary

  - id: press_to_test_exam_mode
    state: DOCUMENTED
    source_claim_ids:
      - official_exam_mode_access_boundary
```

The base structural validator intentionally does not know the semantics of `operational_modes`, because one calculator is not enough evidence to freeze that structure universally.

The new generic gate can still verify that the machine-readable provenance survives and that the local `DOCUMENTED` state does not exceed the linked claim's evidence strength.

This preserves both sides of the research boundary:

```text
schema remains open to new hardware lessons
while
evidence links do not become unvalidated free text
```

## Relationship to dedicated validators

Overlap is intentional.

Dedicated validators still own semantic rules for mature structures. For example:

- `validate_execution_locus.py` knows that `on_device` and `split` require endpoint custom code;
- `validate_records.py` knows the required shape of recovery paths and locality states;
- `validate_structured_evidence_strength.py` knows the established recovery/locality evidence-strength rules.

The generic gate does not replace any of those. It provides a lower common floor for every `source_claim_ids` field, including future exploratory structures that do not yet justify their own validator.

## Regression coverage

`tools/test_source_claim_links.py` covers:

- no evidence-link field at all;
- nested valid evidence-link containers;
- positive truth states with sufficient linked evidence;
- preserved non-promoting/contradicted evidence;
- domain-specific `state` values that must not be mistaken for evidence states;
- evidence links on structures without a truth-state field;
- empty, blank, duplicate, and unresolved claim references;
- positive structures backed only by non-promoting claims;
- a positive structure whose state outruns the strength of its linked evidence.

Both the regression test and repository-wide validator run in the normal `Validate capability records` workflow.

## Root gate

**Truth:** a machine-readable evidence pointer cannot silently reference nothing, duplicate itself, or carry a stronger truth state than the evidence it explicitly links to.  
**Agency / non-domination:** this changes validation only and introduces no access, persistence, control, or device modification path.  
**Continuity:** exploratory schema pressure can remain exploratory while its provenance remains machine-checkable across later edits.  
**Wisdom before speed:** AXM does not need to standardize a new hardware pattern merely to validate its evidence links; schema commitment can wait for repeated evidence.

## One-line rule

> **Experimental structure is allowed; ungrounded machine-readable provenance is not.**
