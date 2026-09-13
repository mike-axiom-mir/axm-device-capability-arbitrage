# Evidence Standard

**Status:** v0.1  
**Purpose:** Keep capability discovery aggressive while keeping claims conservative.

## 1. Core rule

> **A possibility is not a capability record until evidence supports the claim.**

A product specification can prove that hardware exists. It does not necessarily prove that user-controlled code can access it.

A community hack can prove execution on one model/revision. It does not automatically prove support across an entire product family.

A successful local experiment can prove a result happened once. It does not automatically prove reproducibility.

## 2. Truth states

### `UNRESEARCHED`
The field or claim matters but has not yet been investigated.

### `DOCUMENTED`
A credible source documents the capability, interface or property, but this repo has not found a concrete public reproduction or performed a local test.

### `COMMUNITY_VERIFIED`
A concrete public implementation, reproducible technical project, source code, build, or detailed report demonstrates the capability on the stated target.

This is external verification, not AXM local verification.

### `LOCALLY_VERIFIED`
AXM or an authorized local operator reproduced the claim and preserved evidence of the result.

### `REPRODUCIBLE`
The result has preserved steps, dependencies, versions, evidence and recovery information sufficient for an independent operator to reproduce it with reasonable confidence.

### `DEPRECATED`
The evidence was once valid but is no longer recommended or expected to work because of firmware, service shutdown, tooling age, hardware changes or another documented reason.

### `CONTRADICTED`
Credible evidence conflicts with the current claim. Preserve both sides and stop treating the claim as settled.

## 3. Source hierarchy

Prefer evidence roughly in this order, while matching the source to the claim:

1. local reproduction evidence;
2. source code + working build/instructions targeting the exact device;
3. manufacturer technical documentation;
4. mature upstream project documentation;
5. independent technical reverse-engineering report;
6. community report with concrete model/version details;
7. marketplace material for economics/availability only.

Manufacturer documentation is strong for ports, advertised interfaces and supported application platforms. It is not automatically strong for undocumented privilege or reverse-engineered execution.

Community source code may be stronger than the manufacturer for proving an undocumented execution path.

## 4. Claim scoping

Every evidence item should answer:

- What exact claim does this source support?
- Which model/revision/firmware does it cover?
- What does it **not** prove?
- When was it checked?

Example:

```yaml
claim: custom_apk_execution
state: COMMUNITY_VERIFIED
scope:
  model: Sony ILCE-6000
  firmware: unknown
proves:
  - custom PlayMemories Camera App can execute on tested α6000
  - camera buttons can be read by that app
  - custom framebuffer rendering works
not_proven:
  - root privilege
  - identical behavior on every PlayMemories model
  - unattended auto-start
```

## 5. Exact model first

Do not silently generalize:

```text
ILCE-6000 works
```

into:

```text
all Sony cameras work
```

Family-level records may exist, but they should be derived from explicit model lists or multiple records, not convenience.

Hardware revisions can matter even when the retail model name is identical.

## 6. Local verification receipts

A local test should preserve enough state to reconstruct what happened.

Recommended receipt fields:

```yaml
experiment_id: ...
device_record_id: ...
date: ...
operator: ...
hardware_revision: ...
firmware_version: ...
method: ...
expected: ...
actual: ...
result: pass|fail|partial
artifacts:
  - log
  - photo
  - screen_recording
  - serial_capture
  - checksum
recovery_tested: true|false|unknown
notes: ...
```

A screenshot is useful evidence of visible state. A screen recording may preserve transitions. Logs, checksums and command transcripts may provide stronger machine evidence. Use the artifact that actually proves the claim.

## 7. Negative evidence

Failed experiments are evidence.

Record:

- exact model/revision;
- firmware;
- attempted method;
- failure point;
- whether the method is disproven or merely incomplete;
- recovery outcome.

Do not delete failed paths just because a later path succeeds.

## 8. Contradiction protocol

When credible sources disagree:

1. mark the claim `CONTRADICTED`;
2. preserve both sources;
3. look for model/revision/firmware differences;
4. identify the smallest test that could resolve the conflict;
5. do not average incompatible claims into fake certainty.

## 9. Economics evidence

Price is time- and region-sensitive.

For used-price estimates prefer multiple dated listings or completed sales where available.

Record:

- region;
- date;
- condition;
- included adapters/accessories;
- sample count;
- low/median/high rather than one magic number.

Marketplace listings do not prove hardware capability.

## 10. Security and safety claims

Do not call a modification safe merely because it worked.

Safety/recovery evidence should separately cover:

- reversibility;
- known brick risks;
- electrical hazards;
- physical actuator hazards;
- access/ownership legitimacy;
- impact on original safety functions.

## 11. Source integrity

Do not silently paraphrase a source into a stronger claim.

Where possible preserve:

- source URL;
- repository and commit/release when relevant;
- source title;
- date checked;
- concise statement of what was extracted from it.

If a source disappears, the record should still reveal what claim depended on it.

## 12. Promotion gate

A device may count toward the first 25-device census at `DOCUMENTED` or stronger if it has a meaningful execution-surface finding, but recommendations for real deployment should generally require stronger execution and recovery evidence.

No record becomes trustworthy because it has many fields filled. Trust comes from the evidence chain.

## 13. Foundational evidence rule

> **Unknown is acceptable. Unsupported certainty is not.**