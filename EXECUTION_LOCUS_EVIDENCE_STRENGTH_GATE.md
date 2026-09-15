# Execution Locus Evidence-Strength Gate

**Status:** Active validation rule.  
**Checked:** 2026-09-15  
**Purpose:** Prevent a machine-readable execution-locus assertion from being supported only by weak, contradicted, deprecated, or unrelated evidence.

## Why this exists

`EXECUTION_LOCUS_METHOD.md` introduced an optional per-surface `locus` field and then required every locus annotation to point at evidence claims through `source_claim_ids`.

That fixed provenance loss, but it left one narrower truth gap:

```text
surface says: locus = on_device, state = DOCUMENTED
  -> source_claim_ids points to a CONTRADICTED claim
  -> another unrelated DOCUMENTED claim exists elsewhere in the record
  -> old execution-locus validator could still pass
```

The general structured-evidence gate already prevents an execution surface from outrunning the strongest positive claim anywhere in the record. It does not know whether that strong claim is the claim explicitly linked to the locus classification.

For execution locus, that distinction matters. A machine should not be able to follow a source pointer and discover that the cited locus evidence is non-promoting while unrelated evidence elsewhere accidentally carries the surface state.

## Mechanical rule

`tools/validate_execution_locus.py` now treats these as positive locus assertions:

```text
on_device
remote_service
split
```

For those values:

1. the execution surface itself must have a positive truth state;
2. the explicitly linked `source_claim_ids` must contain at least one positive evidence claim;
3. the strongest linked positive claim must be at least as strong as the execution surface state.

Positive evidence states use the repository's existing ordering:

```text
DOCUMENTED < COMMUNITY_VERIFIED < LOCALLY_VERIFIED < REPRODUCIBLE
```

These states do not promote a positive locus assertion:

```text
UNRESEARCHED
DEPRECATED
CONTRADICTED
```

`locus: unknown` deliberately remains different. It is an uncertainty-preserving classification and may reference non-promoting evidence because the point is to record that the execution location has not been established.

## What this closes

The gate now rejects cases such as:

```yaml
execution:
  surfaces:
    - type: plugin
      custom_code: true
      locus: on_device
      state: DOCUMENTED
      source_claim_ids:
        - old_local_execution_claim

evidence:
  claims:
    - id: old_local_execution_claim
      state: CONTRADICTED
      source: https://example.invalid/old-source
    - id: unrelated_hardware_fact
      state: DOCUMENTED
      source: https://example.invalid/hardware
```

It also rejects a stronger surface state that is backed only by weaker linked locus evidence:

```text
surface state: COMMUNITY_VERIFIED
linked locus evidence: DOCUMENTED only
-> fail
```

This does not say the device cannot have that locus. It says the repository does not currently possess linked evidence strong enough to make that exact machine-readable assertion at that state.

## Existing real record

The current Fire TV Stick 4K Max 1st Gen / `AFTKA` locus annotation remains valid:

```text
surface: Android APK
locus: on_device
surface state: DOCUMENTED
linked claim: documented_apk_sideload_and_launch
linked claim state: DOCUMENTED
```

Amazon's developer documentation is the cited primary evidence for installing and launching the APK on the Fire TV endpoint. The gate still does not infer root, bootloader authority, cold-boot persistence, or offline runtime from that fact.

## Independent research pressure

The Google Nest Mini (2nd gen) Local Home SDK case remains useful independent pressure on the same model. Google's current developer documentation says supported Google Home/Nest devices can load and run a developer TypeScript/JavaScript local-fulfillment app on-device, and its supported-device table explicitly lists Nest Mini with a Chrome runtime:

- https://developers.home.google.com/local-home/overview

Google's exact hardware documentation identifies the second-generation Nest Mini as model `H2C` and separately publishes standardized networked-standby evidence. Those sources remain bounded: a 15 W adapter rating is not device consumption, and the EU networked-standby test is not an AXM workload measurement.

- https://support.google.com/googlehome/answer/7072284?hl=en
- https://support.google.com/product-documentation/answer/9851803?hl=en

This activation does not add the Nest Mini to the census. The research is used as an adversarial cross-vendor check on the locus method rather than as an excuse to add a partially prepared device record.

## Tweakers boundary

Tweakers was rechecked for Dutch market context. Current Pricewatch and Vraag & Aanbod surfaces contain second-generation Nest Mini observations, including a dated 11 August 2026 listing at EUR 45, but the inspected listing does not expose exact model code `H2C`.

- https://tweakers.net/pricewatch/1475630/google-nest-mini-wit.html
- https://tweakers.net/aanbod/4154442/google-nest-mini-wit-gen-2.html

Those remain generation-level market leads. They are not promoted into exact-H2C economics and are not used to prove execution locus.

## Regression coverage

`tools/test_execution_locus.py` now covers:

- valid documented on-device execution;
- valid split execution with sufficient linked evidence;
- valid remote-service execution;
- uncertainty-preserving `locus: unknown`;
- missing, empty, duplicate, and unresolved evidence links;
- positive locus backed only by `CONTRADICTED` evidence;
- positive locus backed only by `DEPRECATED` / `UNRESEARCHED` evidence;
- a surface state stronger than its linked locus evidence;
- a positive locus attached to a non-promoting surface state.

The test already runs in the normal `Validate capability records` workflow before the repository-wide execution-locus validator.

## What this gate does not prove

Passing this gate does **not** prove:

- that the linked claim semantically describes the locus correctly;
- that a manufacturer statement is complete;
- that the endpoint is rootable or administratively owned;
- that local execution survives reboot or vendor updates;
- that the execution path works without WAN/vendor infrastructure;
- that local execution was physically reproduced by AXM.

Those remain separate evidence, persistence, locality, privilege, recovery, and local-verification questions.

## Root gate

**Truth:** a positive locus assertion can no longer borrow evidence strength from an unrelated claim while its own linked evidence is non-promoting or weaker than the surface state.  
**Agency / non-domination:** this changes validation only; it adds no access path, covert control, or persistence mechanism.  
**Continuity:** the relationship between locus, surface truth state, and the exact supporting claims is machine-checkable instead of residing only in researcher intent.  
**Wisdom before speed:** uncertain locus can remain `unknown`; the validator does not force a stronger answer merely to complete a record.

## One-line rule

> **A positive execution-locus claim may be no stronger than the positive evidence claims explicitly linked to that locus.**
