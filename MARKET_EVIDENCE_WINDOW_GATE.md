# Market Evidence Window Gate

**Status:** Active validation rule.  
**Purpose:** Prevent a comparison from becoming ranking-ready while its acquisition evidence is stale, spread across an undeclared time window, or mixed across currencies.

## Why this exists

The repository already preserves dated market snapshots and requires ranking-ready comparisons to link market evidence for every non-ineligible candidate. That still leaves another failure mode:

```text
candidate A -> recently checked market snapshot
candidate B -> old market snapshot
candidate C -> different currency snapshot
comparison -> evidence_ready
```

Every file can exist and every candidate can be covered while the cost comparison is no longer temporally or monetarily comparable.

A used-hardware market also does not have one universally correct freshness interval. A fixed global threshold would hide a research judgment inside validator code.

The gate therefore requires the comparison to make that judgment explicit before promotion.

## Machine-readable policy

A comparison may declare:

```yaml
market_evidence_policy:
  currency: EUR
  max_snapshot_age_days: 14
  max_cross_snapshot_check_span_days: 7
```

The numbers above are an example only, not a repository default.

`max_snapshot_age_days` means the maximum allowed age of any linked snapshot relative to the comparison `checked_at` date.

`max_cross_snapshot_check_span_days` means the maximum allowed difference between the oldest and newest linked snapshot `checked_at` dates.

`currency` is the single snapshot currency accepted by that comparison policy. Currency conversion is not silently performed by this gate.

## Promotion rule

For `evidence_incomplete` comparisons, the policy may be absent. This keeps early research flexible and avoids inventing a freshness threshold before a ranking attempt exists.

For comparisons marked `evidence_ready` or `completed`, `market_evidence_policy` is mandatory and must contain:

- a three-letter uppercase `currency`;
- positive integer `max_snapshot_age_days`;
- positive integer `max_cross_snapshot_check_span_days`.

Every linked market snapshot must then:

- exist under `market_snapshots/`;
- have a canonical `checked_at` date no later than the comparison date;
- be no older than the declared maximum age;
- use the declared currency;
- remain inside the declared cross-snapshot check-date span when combined with the other linked snapshots.

## What this does not prove

Passing this gate does **not** prove:

- that an asking price became a transaction price;
- that exchange rates were considered;
- that shipping, adapters, storage, taxes, or other acquisition friction were counted;
- that listings are still available;
- that seller descriptions are true;
- that samples are statistically representative;
- that a device is cheaper in total useful cost;
- that any physical workload, power, provisioning, or recovery test has run.

Those remain separate evidence questions.

## Why the policy is declared instead of hard-coded

Market volatility differs by device, region, scarcity, seller class, and the purpose of the comparison. The repository should not pretend there is one scientifically correct freshness interval for all of them.

The durable invariant is instead:

> A ranking-ready comparison must state the market window it is willing to trust, and its linked snapshots must actually satisfy that declaration.

This converts a hidden judgment into inspectable state without fabricating a universal number.

## Current comparison effect

The current low-power local registry comparison remains `evidence_incomplete`, so no freshness threshold is silently invented for it. Its existing 2026-09-14 snapshot remains valid partial market evidence under the existing market-snapshot and artifact-link gates.

When that comparison is eventually promoted to `evidence_ready`, it must first declare a market evidence policy and refresh/restructure the linked snapshots as needed to satisfy it.

## Validation order

The intended CI chain is:

```text
market snapshot structure/arithmetic
  -> comparison artifact links + candidate coverage
  -> ranking-ready market evidence window
  -> comparison readiness semantics
  -> physical experiment / power / local-verification gates
```

The new validator is `tools/validate_market_evidence_window.py`.

## Root gate

**Truth:** ranking-ready cost evidence cannot be silently stale, cross-window, or mixed-currency.  
**Agency / non-domination:** the validator does not choose the acceptable market window on behalf of the comparison author and never rewrites evidence to pass.  
**Continuity:** the freshness/currency judgment lives in machine-readable repository state rather than temporary chat context.  
**Wisdom before speed:** early research can stay incomplete, but promotion requires an explicit comparability policy rather than a rushed price story.

## One-line rule

> **Before market evidence can support ranking readiness, declare the time and currency window you trust, then prove the linked snapshots actually fit it.**
