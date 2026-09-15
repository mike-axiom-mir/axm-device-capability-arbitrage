# Local Verification Promotion Gate — v0.1

**Status:** Active evidence-integrity gate.  
**Purpose:** Prevent a device record from claiming local verification merely because a local experiment format exists or because someone remembers that a test happened.

## 1. Problem

The repository already has a strong local experiment receipt format and validator. That protects the receipt itself.

Before this gate, however, there was still a continuity gap between two independent facts:

```text
experiment receipt exists and validates

and

device record says locally_verified: true
```

Nothing mechanically required the second statement to be backed by the first.

A future edit could therefore promote a device to `LOCALLY_VERIFIED` while accidentally omitting, losing, or never creating the receipt that makes the claim reproducible outside chat/operator memory.

This file closes that gap without promoting any current device.

## 2. Promotion rule

A device record may use:

```yaml
evidence:
  locally_verified: true
```

only when at least one machine-readable receipt under `experiment_receipts/` satisfies all of the following:

```text
receipt_kind == local_experiment
receipt.device_record_id == device.record_id
authorization.owned_or_authorized == true
result.local_verification_claimed == true
result.overall_state == LOCALLY_VERIFIED or REPRODUCIBLE
artifacts is non-empty
```

The `receipt_kind` token is intentionally the same token accepted by `tools/validate_experiment_receipts.py`. The receipt schema has only `template` and `local_experiment`; `actual` is descriptive prose, not a valid on-disk receipt kind.

The existing `tools/validate_experiment_receipts.py` remains the authority for detailed receipt validity, including artifact hashes, measurement semantics, workload bindings, and hard-power-loss trial requirements.

The promotion validator only checks the cross-file truth boundary.

## 3. Local truth states also require the flag

If a device's `evidence.overall_state` or any individual evidence claim is marked:

```text
LOCALLY_VERIFIED
REPRODUCIBLE
```

then `evidence.locally_verified` must also be `true`.

This prevents contradictory state such as:

```yaml
evidence:
  overall_state: LOCALLY_VERIFIED
  locally_verified: false
```

or a locally verified claim hidden inside a record whose summary still denies local verification.

## 4. Necessary, not sufficient

A qualifying receipt is a **promotion prerequisite**, not a universal proof token.

One receipt can prove only what its method and artifacts actually establish. It does not automatically justify promoting every claim in the device record.

Safe review remains:

```text
physical experiment
  -> receipt + artifacts
  -> receipt validator
  -> promotion gate
  -> inspect exact claim scope
  -> promote only the claims actually supported
```

For example, a receipt proving that a registry workload ran locally does not automatically prove:

- every recovery path;
- every sensor or actuator interface;
- all firmware versions;
- every hardware revision;
- long-term reliability;
- reproducibility on another unit.

Those remain separate evidence questions.

## 5. Why receipt discovery uses `device_record_id`

The v0.1 gate does not add another mandatory receipt-ID list to every device record.

Actual experiments are represented on disk by `receipt_kind: local_experiment`, and those receipts already bind to one exact `device_record_id`, so the repository can discover qualifying receipts mechanically. This keeps the early schema small while still making the evidence chain inspectable.

If later pressure shows that individual claims need explicit receipt IDs, add that only when real local experiments demonstrate the need. Do not freeze a finer-grained schema in advance.

## 6. Schema-alignment regression

The receipt validator and the promotion validator form one chain. Their receipt-kind vocabulary must therefore remain aligned.

A previous implementation of the promotion gate accidentally checked for:

```text
receipt_kind == actual
```

while the authoritative receipt validator accepts only:

```text
template
local_experiment
```

That made a positive promotion impossible: every valid physical receipt would be ignored by the promotion gate.

`tools/test_local_verification_promotion.py` now locks the boundary down with regression checks. It proves that a schema-valid `local_experiment` can qualify, while `template`, the invalid legacy label `actual`, a wrong device binding, missing authorization, or missing artifacts cannot.

## 7. Current repository effect

This gate does **not** claim that any current census device has been locally verified.

The current receipt directory contains the unresearched template and no qualifying positive device receipt. Existing device records correctly remain externally documented/community-verified with `locally_verified: false`.

Therefore this change strengthens future truth preservation without changing:

- census count;
- market evidence;
- power evidence;
- compatibility claims;
- recovery claims;
- comparison ranking.

## 8. Failure and contradiction remain first-class

A failed or partial local experiment receipt is still valuable evidence and should remain in the repository.

It simply cannot satisfy this positive promotion gate unless it explicitly reaches a local truth state under the receipt method.

Likewise, committing a positive receipt does not force the device record to promote automatically. The receipt may need review, may cover only one narrow claim, or may expose a contradiction that should instead be preserved.

## 9. CI order

The validation workflow runs:

```text
validate device/contract structure
validate market snapshots
validate comparisons
validate experiment receipts
validate local power comparability
test local-verification promotion discriminator
validate local-verification promotion linkage
build/verify common workload
```

This means the detailed receipt validator checks receipt semantics before the cross-file promotion gate is evaluated, while the regression test prevents the two validators from silently drifting onto incompatible receipt-kind vocabularies.

## 10. Root gate

**Truth** — no `locally_verified: true`, `LOCALLY_VERIFIED`, or `REPRODUCIBLE` device evidence can survive CI without a preserved qualifying `local_experiment` receipt for the same device, and the discriminator is regression-tested against the actual receipt schema.  
**Agency / non-domination** — the qualifying receipt must assert `owned_or_authorized: true`; local verification cannot be earned through unauthorized testing.  
**Continuity** — the promotion depends on repository evidence and artifacts rather than hidden operator/chat memory, and the vocabulary joining the receipt validator to the promotion gate is mechanically preserved.  
**Wisdom before speed** — local evidence is reviewed before promotion; one successful run is not silently generalized to every claim, firmware, or unit.

## 11. One-line rule

> **A device may say it was locally verified only when the repository contains a schema-valid owned/authorized `local_experiment` receipt that lets another reviewer inspect what actually happened.**
