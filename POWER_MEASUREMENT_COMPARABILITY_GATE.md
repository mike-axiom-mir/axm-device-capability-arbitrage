# Power Measurement Comparability Gate

**Status:** Active validation rule.  
**Purpose:** Prevent locally measured power numbers from becoming comparison evidence without enough context to know what was actually measured.

## Why this exists

The first capability-arbitrage comparison is deliberately blocked on comparable physical evidence. Wall power is one of those blockers.

The existing experiment-receipt method already requires a real local instrument, its model, a measurement duration, the tested unit configuration, and workload-profile matching before numeric workload watts are accepted. That prevents many false claims, but two honest measurements can still be materially incomparable when they silently differ in:

- what sits downstream of the meter;
- which power supply, disks, adapters, or peripherals are included;
- how long the device was allowed to settle before measurement;
- whether the reported average came from the meter itself, energy divided by elapsed time, or sampled readings;
- the sample interval used for a sampled mean;
- known or unknown instrument uncertainty/calibration state.

This gate makes those boundaries explicit before a numeric result can enter a receipt.

## External measurement references

This AXM method is intentionally lightweight; it does **not** claim conformance with a laboratory standard. Its direction is grounded by two public primary references:

- NIST Technical Note 1297 explains that measurement results need an uncertainty statement and that uncertainty depends on the measurement process and how the method was implemented: https://www.nist.gov/pml/nist-technical-note-1297
- NIST's discussion of method-defined measurands specifically notes that uncertainty depends on repeatability/reproducibility and on how well the standard measurement method was implemented: https://www.nist.gov/pml/nist-technical-note-1297/nist-tn-1297-appendix-d4-measurand-defined-measurement-method
- IEC 62301:2026 is the current IEC standard for measurement and reporting of standby/non-active electrical power for appliances and equipment. AXM does not claim IEC 62301 compliance; the reference simply reinforces that low-power claims require a defined measurement/reporting method rather than a naked watt number: https://webstore.iec.ch/en/publication/90194

NIST also cautions against using a numerical value as "accuracy"; this repo therefore records an `uncertainty_statement` rather than inventing a precision claim when the meter documentation or calibration evidence is unknown.

## Machine-readable receipt extension

`experiment_receipts/TEMPLATE.yaml` keeps receipt version `0.1` because this is an additive early-schema extension and there are no committed real experiment receipts to migrate yet.

The `measurement_tools.wall_power` block now carries:

```yaml
measurement_boundary: unknown
integration_method: unknown
sample_interval_seconds: unknown
uncertainty_statement: unknown
calibration_status: unknown
```

Allowed `measurement_boundary` values are:

```text
whole_test_setup_at_wall
device_and_required_power_supply_at_wall
other
unknown
```

Allowed `integration_method` values are:

```text
instrument_average
energy_divided_by_time
sample_mean
unknown
```

Allowed `calibration_status` values are:

```text
currently_calibrated
manufacturer_spec_only
self_checked
not_calibrated
unknown
```

`workload_run` also carries:

```yaml
idle_stabilization_seconds: unknown
workload_stabilization_seconds: unknown
```

A zero stabilization period is allowed when that is what was intentionally done. `unknown` is different: it means the operator did not establish the stabilization period.

## Numeric-power gate

When either local idle watts or local workload-average watts is numeric, `tools/validate_power_measurement_comparability.py` requires:

1. a known measurement boundary;
2. a known averaging/integration method;
3. a known stabilization duration for the corresponding measurement;
4. a positive sample interval when `sample_mean` is used;
5. an explicit power-supply description for the tested unit;
6. an explicit attached-peripherals description (`none` is valid when true; `unknown` is not);
7. at least one durable experiment artifact.

The existing receipt validator remains responsible for instrument/model identity, local-instrument source class, measurement duration, workload-profile matching, SHA-256 artifact shape, and local-verification promotion rules.

The two validators are intentionally complementary rather than one pretending to establish everything.

## Uncertainty is allowed to remain unknown

A field being explicit does not mean the underlying fact must be known.

A consumer wall meter may have no trustworthy current calibration evidence available. The receipt may therefore say:

```yaml
uncertainty_statement: unknown
calibration_status: unknown
```

That measurement can still be useful as an observation, but the repo must not use tiny apparent watt differences as a strong ranking signal when the uncertainty is unknown or larger than the difference being discussed.

This gate records the limitation instead of fabricating laboratory confidence.

## Measurement boundary examples

For an always-on node, the useful quantity is usually the power cost of the setup that must actually remain powered.

```text
router + its required AC adapter
  -> include both upstream of the meter

thin client + its required AC adapter
  -> include both upstream of the meter

NAS + required drives + its power supply
  -> a ranking measurement should normally include the drives needed by the compared role
```

A different boundary may still be researched, but it must be named. A chassis-only NAS measurement and a fully provisioned router measurement must not silently look equivalent merely because both fields say `watts`.

## Artifact rule

Any numeric local power value now requires at least one durable artifact in the receipt.

The artifact may be, for example, a meter export, photo, video, test transcript, or logged sample set. The existing experiment-receipt validator checks its location, SHA-256 digest, and `proves` statement.

This does not make the artifact automatically truthful. It makes the observation inspectable and harder to detach from its evidence.

## What this does not prove

Passing this gate does **not** prove:

- that the meter is accurate;
- that its calibration claim is correct;
- that environmental conditions were ideal;
- that one run generalizes to every unit of the model;
- that a manufacturer power figure equals locally measured power;
- that the device wins the comparison;
- that a physical test occurred when the receipt still contains no numeric result.

Local verification still requires the existing receipt/artifact and promotion gates.

## Comparison consequence

The first low-power registry comparison remains unranked.

This change does not manufacture the missing measurements. It improves the protocol so that when the Archer C7 v5, DS220+, and Wyse 3040 are physically tested, their power evidence can preserve the same kind of boundary, stabilization, averaging, configuration, and artifact context.

## Root gate

**Truth:** a watt number cannot hide an unknown measurement boundary, averaging method, stabilization period, or test setup. Uncertainty may remain unknown rather than being invented.  
**Agency / non-domination:** the gate only validates receipts for the existing owned/authorized experiment path; it adds no remote-control or hidden-persistence mechanism.  
**Continuity:** measurement context and durable artifacts survive outside operator memory and chat state.  
**Wisdom before speed:** the comparison stays blocked until power evidence is genuinely comparable; a faster naked number is not treated as a better result.

## One-line rule

> **A local watt value is comparison evidence only when the repo can tell what was powered, how the value was averaged, how the state was stabilized, and which durable artifact preserves the observation.**
