# Comparison Artifact Link Gate

**Status:** Active validation rule.  
**Purpose:** Keep machine-readable comparisons attached to the repository evidence artifacts they say they use, and prevent ranking-ready comparisons from outrunning their linked market evidence.

## Why this exists

A comparison can be structurally valid while its supporting repository links silently rot or cover only part of the candidate set.

The current low-power registry comparison names:

- a dated market snapshot under `market_snapshots/`; and
- a common workload definition under `workloads/`.

Before this gate, `tools/validate_comparisons.py` checked contract paths, device-record paths, requirement states, and eligibility semantics, but it did not resolve those artifact references. The first version of this gate closed path, contract, and date drift.

A second gap remained:

```text
comparison candidates
  -> Archer C7 v5
  -> DS220+
  -> Wyse 3040

linked market snapshot
  -> could theoretically contain only one of them

comparison status
  -> could still be relabeled evidence_ready
```

A valid snapshot link is not enough if the market evidence omits a candidate that is still eligible to be ranked.

That is a Truth and Continuity problem.

## What the gate checks

`tools/validate_comparison_artifacts.py` validates every comparison YAML under `comparisons/`.

### Comparison candidate identity

The gate reads `candidates[*].record_id` and rejects duplicate or empty candidate IDs before evaluating artifact coverage.

It treats a candidate explicitly marked `hard_requirement_eligibility: ineligible` as excluded from the ranking-ready market-coverage requirement. The deeper eligibility semantics remain owned by `tools/validate_comparisons.py`; this gate does not decide whether a candidate deserves that state.

### Market snapshot links

When `market_snapshot_refs` is present:

1. it must be a non-empty list;
2. every reference must be a repository-relative YAML path beneath `market_snapshots/`;
3. duplicate paths are rejected;
4. the target file must exist and parse as YAML;
5. the target must declare a non-empty `snapshot_id` and `contract_id`;
6. the snapshot `contract_id` must equal the comparison `contract_id`;
7. the snapshot `checked_at` must be canonical `YYYY-MM-DD` and must not be later than the comparison `checked_at`;
8. two references in one comparison may not resolve to the same `snapshot_id`;
9. every linked snapshot must contain a non-empty `candidates` list with unique `record_id` values;
10. every linked snapshot must cover at least one candidate actually present in the comparison.

The union of matching snapshot candidate IDs becomes the comparison's **linked market coverage**.

For comparisons marked `evidence_ready` or `completed`, linked market snapshots must cover **every comparison candidate that is not explicitly ineligible**.

Earlier `evidence_incomplete` comparisons may still have partial market coverage. That preserves honest incremental research without allowing partial evidence to masquerade as ranking-ready evidence.

### Workload link

When `workload_ref` is present:

1. it must be a repository-relative YAML path beneath `workloads/`;
2. the target file must exist and parse as YAML;
3. the target must declare a non-empty `workload_id` and `contract_id`;
4. the workload `contract_id` must equal the comparison `contract_id`.

For comparisons marked `evidence_ready` or `completed`, both market-snapshot and workload references are required.

## Current comparison effect

The present low-power registry comparison contains three non-ineligible candidates:

```text
tp-link-archer-c7-v5
synology-ds220-plus
dell-wyse-3040
```

Its linked 2026-09-14 EU market snapshot contains all three record IDs, so the stronger cross-artifact rule is satisfied.

This does **not** promote the comparison. It remains `evidence_incomplete` because physical common-workload runs, comparable power, provisioning, restart/recovery, and replacement-life evidence are still unresolved elsewhere in the comparison state.

## What this does not prove

This gate does **not**:

- fetch or validate the external marketplace URLs inside a snapshot;
- turn displayed listing prices into transaction prices;
- prove equal listing condition, shipping cost, accessories, or required storage;
- impose a market-freshness window;
- prove that a physical candidate ran the workload;
- prove power draw, provisioning time, recovery behavior, or remaining hardware life;
- decide that a comparison is ready to rank merely because its links and candidate coverage resolve;
- replace the dedicated market, comparison, experiment-receipt, power-comparability, or local-verification validators.

Candidate coverage answers only:

> Does the linked market evidence graph actually include each device the comparison still intends to rank?

It does not answer whether that evidence is already sufficient for a fair cost decision.

## Why contract identity is checked twice

The repository already validates market snapshots and comparison records separately. This gate adds a cross-artifact invariant:

```text
comparison.contract_id
  == linked market snapshot.contract_id
  == linked workload.contract_id
```

That prevents a syntactically valid artifact for one goal from being silently attached to another goal.

## Why candidate identity is checked across artifacts

A matching contract is necessary but not sufficient.

Two comparisons may use the same capability contract while evaluating different candidate sets. Market evidence collected for one subset must not automatically count as acquisition evidence for another subset.

For ranking-ready state, the invariant is:

```text
non-ineligible comparison candidate IDs
  ⊆ union(linked market snapshot candidate IDs)
```

Snapshot files may contain additional candidates because a dated market artifact can legitimately be shared or broader than one comparison. Extras do not satisfy missing comparison candidates.

A linked snapshot with **zero** overlap is rejected because it is not evidence for the candidate set at all.

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

The CI flow keeps the evidence chain in this order:

```text
market snapshot structure
  -> comparison artifact links + candidate coverage
  -> comparison requirement/readiness semantics
  -> physical experiment receipts / power comparability / local-verification gates
```

The artifact-link gate does not duplicate the deeper validators; it joins their outputs into one coherent repository graph.

## Root gate

**Truth:** a ranking-ready comparison cannot cite market evidence that omits a still-rankable candidate, and cannot cite missing, wrong-contract, future-dated, or irrelevant artifacts as if the evidence chain were intact.  
**Agency / non-domination:** the gate reports missing coverage and never invents, rewrites, excludes, or promotes a candidate to make the comparison pass.  
**Continuity:** candidate-to-market links remain mechanically reconstructable from durable repository IDs and paths rather than temporary operator context.  
**Wisdom before speed:** partial market research remains valid as partial research, but it cannot be relabeled ranking-ready until the candidate evidence graph is complete; complete linkage still does not substitute for comparable physical measurements.
