# Standardized Power Evidence Gate

Status: active method + CI gate  
Scope: `power.standardized_measurements` in device records

## Why this exists

A standardized manufacturer or independent power test can be valuable evidence without being a local AXM measurement and without describing the workload AXM ultimately wants to compare.

The first concrete pressure case is Google Nest Mini (2nd gen), exact model H2C. Google's EU ecodesign test summary reports **1.6 W networked standby at 230 V / 50 Hz**, tested under **EN 50564:2011** with the microphone switch set to mute. That is useful exact-model evidence. It does not become generic idle power, active power, Local Home workload power, or a locally reproduced AXM measurement merely because the number is machine-readable.

Source checked 2026-09-15:

- https://support.google.com/product-documentation/answer/9851803?hl=en

The existing H2C record already preserves this distinction. This gate makes the minimum provenance/condition contract mechanical for every future record that uses the same extension.

## Required shape

When `power.standardized_measurements` is present, it must be a non-empty list. Every entry must preserve:

```yaml
- id: stable_measurement_id
  metric: networked_standby_power
  watts: 1.6
  input_condition: "230 V AC, 50 Hz"
  test_condition: "EN 50564:2011; microphone switch set to mute"
  measurement_kind: manufacturer_standardized_test
  locally_measured: false
  state: DOCUMENTED
  source_claim_ids:
    - exact_claim_id
```

The gate validates:

- stable unique measurement IDs;
- finite non-negative numeric watts;
- explicit metric, input condition, and test condition;
- bounded measurement provenance;
- boolean local/non-local identity;
- consistency between provenance and `locally_measured`;
- an explicit AXM truth state;
- non-empty, unique evidence-claim references that resolve inside the same device record.

Allowed `measurement_kind` values are deliberately small:

```text
manufacturer_standardized_test
independent_standardized_test
local_standardized_test
unknown
```

`local_standardized_test` requires `locally_measured: true`. All other kinds require `locally_measured: false`. This prevents a manufacturer or third-party figure from silently becoming an AXM local measurement.

## What the gate does not prove

Passing this validator does **not** establish that:

- the source is factually correct;
- the measurement is representative of the AXM target workload;
- the measurement is comparable to another device with a different test condition;
- the hardware was locally inspected;
- idle or active power was measured by AXM;
- a supply rating equals device consumption;
- a standardized standby figure is sufficient to rank a capability-arbitrage candidate.

Those questions remain evidence- and workload-specific.

## Why conditions are mandatory

A bare number such as `1.6 W` is too easy to reuse outside its original boundary. The useful fact is closer to:

```text
Nest Mini H2C
+ manufacturer standardized test
+ networked standby metric
+ 230 V / 50 Hz input
+ EN 50564:2011
+ microphone muted
= 1.6 W
```

Dropping the condition changes the claim.

## Relationship to existing gates

- `tools/validate_source_claim_links.py` protects generic evidence-link integrity.
- `tools/validate_structured_evidence_strength.py` protects truth-state ceilings.
- `tools/validate_power_measurement_comparability.py` protects **local experiment receipt** comparability for wall-power measurements.
- `tools/validate_standardized_power.py` protects the different case of **device-record standardized power evidence**.

The gates are intentionally complementary rather than interchangeable.

## Root check

- **Truth:** preserves source provenance and the exact test boundary around a numeric power claim.
- **Agency / non-domination:** avoids steering hardware choices with a falsely generalized efficiency number.
- **Continuity:** future records use a stable machine-readable provenance/condition shape.
- **Wisdom before speed:** keeps standardized evidence useful without pretending it replaces the slower common-workload measurement needed for a real ranking.
