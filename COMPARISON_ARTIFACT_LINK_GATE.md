# Comparison Artifact Link Gate

**Status:** Active validation rule.  
**Purpose:** Keep machine-readable comparisons attached to the repository evidence artifacts they say they use.

## Why this exists

A comparison can be structurally valid while its supporting repository links silently rot.

The current low-power registry comparison names:

- a dated market snapshot under `market_snapshots/`; and
- a common workload definition under `workloads/`.

Before this gate, `tools/validate_comparisons.py` checked contract paths, device-record paths, requirement states, and eligibility semantics, but it did not resolve those artifact references. A typo, deleted file, moved workload, or snapshot for the wrong capability contract could therefore leave a comparison looking evidence-linked when the chain was broken.

That is a Truth and Continuity problem.

## What the gate checks

`tools/validate_comparison_artifacts.py` validates every comparison YAML under `comparisons/`.

When `market_snapshot_refs` is present:

1. it must be a non-empty list;
2. every reference must be a repository-relative YAML path beneath `market_snapshots/`;
3. duplicate paths are rejected;
4. the target file must exist and parse as YAML;
5. the target must declare a non-empty `snapshot_id` and `contract_id`;
6. the snapshot `contract_id` must equal the comparison `contract_id`;
7. the snapshot `checked_at` must be canonical `YYYY-MM-DD` and must not be later than the comparison `checked_at`;
8. two references in one comparison may not resolve to the same `snapshot_id`.

When `workload_ref` is present:

1. it must be a repository-relative YAML path beneath `workloads/`;
2. the target file must exist and parse as YAML;
3. the target must declare a non-empty `workload_id` and `contract_id`;
4. the workload `contract_id` must equal the comparison `contract_id`.

For comparisons marked `evidence_ready` or `completed`, both market-snapshot and workload references are required. Earlier `evidence_incomplete` comparisons may still omit them so the early research format remains extensible.

## What this does not prove

This gate does **not**:

- fetch or validate the external marketplace URLs inside a snapshot;
- turn displayed listing prices into transaction prices;
- prove that a physical candidate ran the workload;
- prove power draw, provisioning time, recovery behavior, or remaining hardware life;
- decide that a comparison is ready to rank merely because its links resolve;
- replace the dedicated market, comparison, experiment-receipt, or local-verification validators.

A valid link is only a valid evidence chain pointer.

## Why contract identity is checked twice

The repository already validates market snapshots and comparison records separately. This gate adds a cross-artifact invariant:

```text
comparison.contract_id
  == linked market snapshot.contract_id
  == linked workload.contract_id
```

That prevents a syntactically valid artifact for one goal from being silently attached to another goal.

## Date rule

A comparison cannot claim to have been checked before the market evidence it references existed:

```text
market_snapshot.checked_at <= comparison.checked_at
```

This does not impose an automatic freshness window. Old evidence may remain usable when explicitly accepted; the gate only blocks impossible forward references.

## Path rule

Artifact references must stay inside their intended repository namespaces. Absolute paths, backslash paths, traversal segments such as `..`, missing files, and non-YAML targets fail validation.

This is deliberately local. The comparison remains inspectable and reproducible from repository state without trusting hidden chat state or operator memory.

## Validation order

The CI flow now keeps the evidence chain in this order:

```text
market snapshot structure
  -> comparison artifact links
  -> comparison requirement semantics
  -> physical experiment receipts / local-verification gates
```

The artifact-link gate does not duplicate the deeper validators; it joins their outputs into one coherent repository graph.

## Root gate

**Truth:** a comparison cannot cite missing, wrong-contract, future-dated market evidence or a wrong-contract workload as if the evidence chain were intact.  
**Agency / non-domination:** the gate reports broken references and never invents, rewrites, or promotes evidence to make a comparison pass.  
**Continuity:** market and workload evidence remain resolvable from durable repository paths rather than temporary operator context.  
**Wisdom before speed:** link integrity is required before ranking maturity; resolving a file still does not substitute for comparable physical measurements.
