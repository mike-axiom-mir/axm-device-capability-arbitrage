# Evidence Claim Scope Gate

**Status:** Active validation rule.  
**Purpose:** Ensure a positive evidence claim states what its source actually proves and that each device preserves a machine-readable source-check date.

## Why this exists

`EVIDENCE_STANDARD.md` already requires claim scoping:

- what exact claim does the source support;
- which model/revision/firmware does it cover;
- what does it not prove;
- when was it checked.

Before this gate, `tools/validate_records.py` required only `id`, `state`, and `source` for each evidence claim. A syntactically valid positive claim could therefore point at a source without recording any machine-readable statement of what that source was being used to prove.

That is too weak for a repository whose central rule is:

> **A possibility is not a capability record until evidence supports the claim.**

A URL is provenance. It is not, by itself, a scoped claim.

## Required invariant

For every device record:

1. `evidence.last_checked` must exist and use canonical ISO calendar form `YYYY-MM-DD`;
2. every positive evidence claim (`DOCUMENTED`, `COMMUNITY_VERIFIED`, `LOCALLY_VERIFIED`, or `REPRODUCIBLE`) must have a non-empty `proves` list;
3. `proves`, optional `does_not_prove`, and optional `additional_sources` must contain non-empty strings and no duplicate entries within each list;
4. an identical statement may not appear in both `proves` and `does_not_prove`;
5. the primary `source` may not be repeated inside `additional_sources`.

The gate deliberately does **not** require a particular URL host or source class. Local receipts, repository artifacts, manufacturer documentation, upstream projects, and other evidence classes can all be legitimate when they match the claim.

## What this improves

The minimum evidence chain becomes:

```text
truth state
  -> source
  -> explicit statement(s) of what the source proves
  -> record-level checked date
```

That makes a positive evidence claim inspectable even before a human opens the source.

It also catches several forms of silent drift:

```text
source URL exists
+ state = COMMUNITY_VERIFIED
+ proves missing
=> FAIL

proves:
  - exact-model custom execution works
does_not_prove:
  - exact-model custom execution works
=> FAIL

source: https://example.invalid/a
additional_sources:
  - https://example.invalid/a
=> FAIL
```

The last example is only a duplicate-source check. The validator does not treat the example URL as credible or reachable.

## What the gate intentionally does not do

It does **not**:

- decide whether the source is trustworthy;
- fetch sources or declare a URL currently reachable;
- infer source quality from a domain name;
- prove that the wording in `proves` is faithful to the source;
- require every claim to have a `does_not_prove` list;
- impose an arbitrary freshness lifetime;
- promote or demote any truth state;
- replace exact-model/revision review;
- replace structured evidence-strength validation;
- replace local-verification experiment receipts.

`evidence.last_checked` is validated as a canonical date, not as an automatic expiration policy. Different claims age at different rates; a manufacturer connector specification and a cloud-service behavior should not silently receive the same freshness lifetime.

## Non-promoting states

`UNRESEARCHED`, `DEPRECATED`, and `CONTRADICTED` are not positive evidence states.

If one of those claims includes `proves`, the list is structurally validated, but this gate does not require a `proves` list for those states. Their semantics may need a future contradiction/deprecation-specific structure rather than forcing them into the positive-claim shape prematurely.

## Relationship to the evidence-strength gate

This validator answers:

> Does a positive evidence claim explicitly say what its source is being used to prove?

`tools/validate_structured_evidence_strength.py` answers:

> Does a record/structured truth label stay within the evidence strength available to support it?

Those are complementary checks. A claim can be well scoped yet too weak for a promoted truth state; or it can be strong enough in label but poorly scoped. CI now rejects either failure.

## CI

`tools/validate_evidence_claim_scope.py` scans every device YAML record after the base structural validator and before the structured evidence-strength gate.

The ordering is deliberate:

```text
base structure / claim IDs
  -> evidence-claim scope
  -> evidence-strength ceilings
  -> remaining census / market / experiment gates
```

This keeps error messages local: missing base structure fails first; ambiguous positive claim scope fails next; truth-state inflation fails after that.

## Root gate

**Truth:** a positive evidence label must carry an explicit statement of what its source proves, not merely a URL and confidence word.  
**Agency / non-domination:** the gate does not auto-promote claims, rewrite records, or hide uncertainty behind a source link.  
**Continuity:** checked dates and claim scope become executable repository invariants rather than chat-only discipline.  
**Wisdom before speed:** the validator strengthens the existing evidence model without inventing source credibility, freshness, or factual correctness that still requires review.
