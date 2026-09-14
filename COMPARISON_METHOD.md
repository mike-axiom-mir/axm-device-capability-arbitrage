# Comparison Method — Evidence-Gated Capability Arbitrage

**Status:** v0.1 early method  
**Purpose:** Turn capability contracts and device records into comparisons without letting unknowns become scores.

## 1. Comparison is not ranking by resemblance

A device enters a comparison because it is being tested against an explicit capability contract, not because it looks like a computer or belongs to a familiar product category.

The comparison has two separate questions:

1. **Hard-requirement eligibility:** does current evidence satisfy the contract's required fields?
2. **Ranking readiness:** is there enough comparable cost, power, workload, provisioning and recovery evidence to choose among eligible candidates?

A candidate can pass the first question while the comparison still has no defensible winner.

## 2. Requirement statuses

Each hard/preferred requirement uses one of:

```text
pass
conditional
unknown
fail
```

Meaning:

- `pass` — the current device record supports the requirement as written;
- `conditional` — the requirement can be satisfied only after an explicit configuration, accessory, state choice or other stated condition;
- `unknown` — the record does not establish whether the requirement is satisfied;
- `fail` — the record establishes a mismatch.

`unknown` must never be converted to `pass` because a device seems likely to work.

## 3. Hard-requirement eligibility

Eligibility is mechanically derived from hard-requirement statuses:

```text
any fail         -> ineligible
else any unknown -> blocked_by_unknowns
else any conditional -> conditional
else             -> hard_requirements_pass
```

This is deliberately stricter than a recommendation system.

`hard_requirements_pass` means only that the **recorded contract fields** pass. It does not mean the workload has been locally run, measured, or proven reliable.

## 4. Record-path evidence

Comparison entries point back to the device record fields used for each conclusion.

Example:

```yaml
record_paths:
  - memory.ram_mb
  - boot.unattended_boot
```

The comparison validator checks that every referenced path exists in the current device record. This makes silent drift harder: if a record field moves or disappears, the comparison must be repaired.

A `pass` or `conditional` result must not rest entirely on `unknown`, `not_collected`, or null record values.

## 5. Contract-path evidence

Every hard requirement also points at the capability-contract field it evaluates.

Example:

```yaml
contract_path: required.memory.ram_mb_min
```

The validator checks that the path exists in the referenced contract.

This keeps comparison logic attached to an explicit goal instead of becoming a generic hardware score.

## 6. Ranking gate

Do not produce a ranked winner while materially comparable evidence is missing.

For the first low-power registry comparison, ranking remains blocked until the candidates have comparable evidence for at least:

- dated used-market acquisition cost in the same region/window;
- required storage/adapters;
- one common registry workload;
- wall power under comparable conditions;
- provisioning and repeat-provisioning effort;
- hard-power-loss -> boot -> service restart behavior;
- recovery burden and data/configuration impact;
- replacement availability.

Manufacturer claims may remain useful evidence, but a manufacturer power figure in one test condition must not be treated as equivalent to a measured common workload on another device.

### Mechanical readiness semantics

Comparison status is now mechanically tied to the blocker/gap state instead of being a free-form label.

For `evidence_incomplete`:

- at least one `decision_blocker` must remain unresolved;
- every candidate that is not already `ineligible` must retain at least one explicit `ranking_gaps` entry.

For `evidence_ready` or `completed`:

- every candidate's `ranking_gaps` list must be empty;
- every `decision_blocker` must have state `resolved` or `not_applicable`.

The blocker vocabulary is intentionally conservative. Only `resolved` and `not_applicable` clear a blocker. Any other non-empty state — including `partial`, `not_collected`, `unknown`, or a newly invented intermediate state — remains blocking until the repository explicitly resolves it.

`contradicted` is not auto-promoted or auto-demoted by these readiness rules. It exists for comparisons whose underlying evidence or premise has been invalidated and must be repaired explicitly.

The comparison validator also requires the three truth rules to remain explicit and true:

```yaml
truth_rules:
  unknown_is_not_pass: true
  hard_eligibility_is_not_workload_verification: true
  no_numeric_score_before_comparable_evidence: true
```

This does not prove that a blocker was resolved correctly. It prevents a comparison from being relabeled ready while its own machine-readable state still says that ranking evidence is missing.

## 7. No neutral numbers for missing evidence

Do not map unknown values to zero, average, midpoint, or a neutral score.

Bad:

```text
unknown power -> 5/10
unknown price -> €0
unknown recovery -> neutral
```

Good:

```text
unknown power -> ranking blocker
unknown price -> ranking blocker
unknown recovery -> eligibility/risk blocker according to the contract
```

## 8. Conditional devices

Conditions must be visible because they are part of total useful cost.

Examples:

- NAS requires drives before it has durable state;
- thin client must have AC Recovery configured to Power On;
- model family requires a specific hardware revision;
- replacement firmware removes a vendor recovery path;
- extra USB storage is required for the workload.

A condition may be cheap or expensive. The comparison must not decide that before evidence exists.

## 9. First comparison state

The first machine-readable comparison is:

```text
capability contract: low-power-local-registry-node
candidates:
  TP-Link Archer C7 v5
  Synology DS220+
  Dell Wyse 3040
```

Its initial purpose is not to declare a winner. It is to expose exactly which hard requirements are already grounded and which missing observations block a real total-useful-cost result.

## 10. Root gate

**Truth:** unknown never becomes pass; a record-level pass is not inflated into local workload verification.  
**Agency / non-domination:** comparisons describe user-controlled capability and do not justify unauthorized modification.  
**Continuity:** every conclusion points back to inspectable contract/device fields and lives in repository state.  
**Wisdom before speed:** eligibility is separated from ranking, and ranking waits for comparable cost/power/recovery evidence.

## 11. One-line rule

> **First prove that a device satisfies the goal; then prove that the evidence is comparable enough to rank it.**
