# Local Experiment Receipt Method — v0.1

**Status:** Evidence-capture extension for physical/local tests.  
**Purpose:** Turn future power, provisioning, workload and recovery experiments into machine-readable evidence without promoting an observation into a stronger claim than it supports.

## 1. Why this exists

`EVIDENCE_STANDARD.md` already requires a local verification receipt before a claim can become `LOCALLY_VERIFIED`. The first capability-arbitrage comparison now has a common executable workload, but the three candidates still lack comparable physical results.

Without a shared receipt shape, three local tests can silently become incomparable:

```text
one operator reports a meter screenshot
another reports a shell command
another reports "worked after reboot"
```

All three may be honest, but they do not establish the same thing.

This extension therefore standardizes **how an observation is recorded**, not what result should occur.

## 2. Location

Actual receipts belong under:

```text
experiment_receipts/
```

The machine-readable starting point is:

```text
experiment_receipts/TEMPLATE.yaml
```

Copy the template to a new descriptive filename for an actual experiment. Never overwrite the template with results.

## 3. Receipt identity

An actual receipt must bind to:

- one existing `device_record_id`;
- one existing `contract_id`;
- one existing `workload_id`;
- the exact observed physical unit configuration;
- the software/firmware state that was actually tested;
- the date the test was performed.

A model-family name alone is insufficient when unit configuration matters.

Do not commit a raw device serial number merely to prove uniqueness. A local/pseudonymous unit label or non-reversible fingerprint is enough unless a serial is materially necessary.

## 4. Authorization gate

An actual physical receipt must say:

```yaml
authorization:
  owned_or_authorized: true
```

The validator rejects a real receipt when this is not true.

This is not a legal ownership oracle. It is an explicit operator assertion that the experiment is within the AXM agency/non-domination boundary.

## 5. Unknown discipline

Fields use the same truth discipline as device records:

- `unknown` means not established;
- numeric zero means measured/observed zero and must not be used as a placeholder;
- `false` means an observed negative result when the field is boolean;
- an empty trial list means the trial was not run;
- a failed experiment remains evidence.

A template may contain `unknown`. A real receipt may also preserve unknown fields. The validator does not require a complete success story.

## 6. Power measurements

A numeric local wall-power result requires:

- a named measurement instrument;
- instrument model;
- source class `local_instrument`;
- a positive measurement duration;
- the tested configuration and attached peripherals;
- at least one evidence artifact when local verification is claimed.

For the common registry workload, a numeric workload-average wattage also requires:

- `profile_matches_workload: true`;
- a measurement window at least as long as the workload's declared `measurement_seconds`.

A power-adapter rating, manufacturer specification, estimate, or neighboring device measurement must not be written into a local wattage field.

Manufacturer and independent measurements remain valid evidence elsewhere; this receipt format is specifically for a test that actually happened on the identified unit.

## 7. Provisioning time

Keep first-device and repeat-device provisioning separate.

```yaml
provisioning:
  first_device_minutes: unknown
  repeat_device_minutes: unknown
  automation_level: unknown
```

A first reverse-engineering session may be expensive while a preserved repeat recipe is cheap. Do not average the two into one friction number.

## 8. Common workload evidence

For a workload-linked receipt, preserve at least the best available values for:

- build/install elapsed time;
- binary/package size;
- state size after seed;
- process memory;
- runtime CPU/load;
- service autostart configuration;
- idle wall power;
- workload wall power;
- measurement duration.

Unknown is accepted. A missing metric does not become zero.

The current comparison workload is:

```text
workloads/low-power-local-registry-v0.1/workload.yaml
```

Its protocol/profile remains the authority for workload semantics. The receipt records whether the operator actually matched that profile.

## 9. Hard-power-loss trials

The current workload asks for five physical repetitions.

Each trial records:

- whether power was actually removed;
- whether power was restored;
- whether the service returned without manual intervention;
- whether the last acknowledged durable value remained readable;
- elapsed restore-to-service-ready time when observed;
- notes/failure detail.

`restart_reliability: pass` is mechanically rejected unless at least the workload target number of trials are present and every counted trial satisfies the workload pass condition.

A partial set may remain `unknown` or `fail`; it must not be promoted to pass.

CI process-restart testing is not a substitute for physical hard-power-loss evidence.

## 10. Artifacts and local verification

A receipt claiming local verification must preserve at least one artifact entry with:

- artifact type;
- repository path or durable URL/location;
- SHA-256 digest;
- concise statement of what it proves.

Useful artifacts include logs, command transcripts, meter exports, photos, video, serial captures, and checksums.

The digest binds the receipt to a particular artifact. It does not prove that the artifact itself is truthful; the claim boundary still matters.

The validator rejects `local_verification_claimed: true` when evidence state is weaker than `LOCALLY_VERIFIED` or when artifact evidence is absent.

## 11. Promotion boundary

A valid receipt does **not** automatically rewrite the device record.

The safe flow is:

```text
physical experiment
  -> receipt + artifacts
  -> validator
  -> human/machine review of what the receipt actually proves
  -> only then promote relevant device/comparison claims
```

This prevents one successful run from silently becoming a universal device-family fact.

## 12. Negative and contradictory results

Failures are first-class.

Examples:

```text
workload did not compile on target
service did not autostart
last acknowledged state disappeared
power exceeded the preferred ceiling
unit required manual intervention
```

Preserve the receipt and artifacts. Mark the relevant result as `fail`, `partial`, or `CONTRADICTED` rather than deleting the run.

A failed local test can be more valuable than an unsupported pass.

## 13. Privacy / agency

Receipts should contain only the unit identity needed for reproducibility.

Prefer:

- local unit labels;
- exact model/revision/configuration;
- firmware/BIOS version;
- hashes of images/artifacts.

Avoid unnecessarily publishing:

- raw serial numbers;
- account identifiers;
- Wi-Fi credentials;
- private LAN addresses;
- personal names;
- vendor-cloud tokens.

## 14. Root gate

**Truth** — numeric measurements require method/tool context; unknown stays unknown; a pass cannot be synthesized from missing trials.  
**Agency / non-domination** — actual receipts explicitly assert owned/authorized hardware; no hidden persistence or unauthorized device access is normalized.  
**Continuity** — exact unit/software state, workload binding, artifacts, hashes and recovery outcomes survive outside chat state.  
**Wisdom before speed** — power, provisioning, failure and recovery evidence are captured before a candidate is ranked.

## 15. One-line rule

> **A local result becomes comparison evidence only when the repo can tell what exact unit was tested, in what state, with what method, what actually happened, and which artifact proves it.**
