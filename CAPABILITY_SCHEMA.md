# Capability Schema — v0.1

**Status:** Early schema. Expected to evolve from evidence.  
**Rule:** Unknown values stay unknown. Product category never implies capability.

## 1. Purpose

A device record should describe the machine that actually exists, the execution surfaces actually reachable, the evidence supporting those claims, and the costs/risks relevant to using it.

The schema is intentionally capability-first. It separates:

- identity from capability;
- hardware presence from software accessibility;
- execution from privilege;
- capability from recovery;
- sticker price from total useful cost;
- external documentation from local verification.

## 2. Canonical top-level shape

```yaml
schema_version: "0.1"
record_id: manufacturer-model-revision

identity: {}
compute: {}
memory: {}
execution: {}
connectivity: {}
inputs: {}
outputs: {}
power: {}
boot: {}
recovery: {}
locality: {}
economics: {}
roles: []
evidence: {}
notes: []
```

A field may be absent when not yet researched, but mature records should prefer explicit `unknown` so missing research is visible.

## 3. Identity

```yaml
identity:
  manufacturer: sony
  model: ILCE-6000
  common_name: Sony α6000
  marketed_category: mirrorless_camera
  hardware_revision: unknown
  release_period: unknown
```

`marketed_category` is discovery metadata only. It must never be used as proof of execution, power, networking or safety properties.

## 4. Compute

```yaml
compute:
  soc: unknown
  architecture: unknown
  cpu_cores: unknown
  clock_mhz: unknown
  accelerator:
    gpu: unknown
    npu: unknown
    dsp: unknown
```

Do not copy SoC/RAM claims from a similar product unless the evidence explicitly covers this model/revision.

## 5. Memory and storage

```yaml
memory:
  ram_mb: unknown
  internal_persistent_storage_mb: unknown
  removable_storage:
    present: true
    types:
      - sd
```

Where storage is partitioned, distinguish:

- application-private storage;
- writable system storage;
- removable media;
- read-only firmware;
- external USB/network storage.

## 6. Execution

Execution is a list because one device may expose multiple independent paths.

```yaml
execution:
  surfaces:
    - type: android_apk
      environment: android
      version: "2.3.7"
      custom_code: true
      privilege: application_user
      access_method: community_installer
      state: COMMUNITY_VERIFIED

    - type: adb
      environment: android
      custom_code: true
      privilege: unknown
      access_method: optional_tweak_app
      state: DOCUMENTED
```

Suggested `type` values:

```text
manufacturer_app
browser
webview
script_runtime
plugin
package_manager
android_apk
native_binary
container
jvm
wasm
shell
ssh
adb
telnet
uart
service_mode
recovery_mode
replaceable_firmware
bootloader
bare_metal
other
```

Suggested privilege values:

```text
sandboxed
application_user
normal_user
administrator
root
kernel
bootloader
bare_metal
unknown
```

Never collapse these into a single `hackable: true` field.

## 7. Connectivity

```yaml
connectivity:
  ethernet: false
  wifi:
    present: true
    modes: unknown
  bluetooth: unknown
  nfc: true
  usb:
    present: true
    modes:
      - mass_storage
      - mtp
      - pc_remote
  serial: unknown
  gpio: unknown
```

Record what is externally documented separately from what is accessible to custom code.

## 8. Inputs

```yaml
inputs:
  sensors:
    - type: image_sensor
      accessible_to_custom_code: unknown
  microphones:
    - type: built_in_stereo
      accessible_to_custom_code: unknown
  controls:
    - shutter
    - dpad
    - control_wheel
    - buttons
```

Physical existence is not the same as custom-code accessibility.

## 9. Outputs / actuators

```yaml
outputs:
  display:
    present: true
    custom_rendering_verified: true
  speaker:
    present: true
    custom_audio_verified: false
  leds: unknown
  motors: []
  relays: []
```

Use `actuator` broadly for machine-controllable physical outputs, but preserve safety classification where relevant.

## 10. Power

```yaml
power:
  source:
    battery: true
    external_power: true
  idle_watts: unknown
  active_watts: unknown
  measured: false
  always_on_suitability: unknown
  thermal_notes: unknown
```

Power figures must identify whether they are:

- manufacturer rated;
- independently measured;
- locally measured;
- estimated.

## 11. Boot

```yaml
boot:
  unattended_boot: unknown
  auto_start_custom_code: unknown
  secure_boot: unknown
  boot_from_removable_media: unknown
  bootloader_access: unknown
```

Unattended boot matters for infrastructure roles and should not be inferred from normal consumer startup behavior.

## 12. Recovery

A flat summary remains allowed for early records:

```yaml
recovery:
  factory_reset: unknown
  official_restore: unknown
  rescue_partition: unknown
  dual_firmware: unknown
  removable_media_recovery: unknown
  usb_recovery: unknown
  uart_recovery: unknown
  bootloader_recovery: unknown
  known_brick_risk: unknown
  recovery_state: UNRESEARCHED
```

However, evidence from the Roborock S5 and Synology DS220+ showed that a single positive recovery flag can hide two different facts:

- a path may exist from one device state but not another;
- two valid paths may preserve very different amounts of configuration, user data, or application state.

For records where that distinction matters, add structured `recovery.paths` entries:

```yaml
recovery:
  recovery_state: DOCUMENTED
  paths:
    - id: mode_2_dsm_reinstall
      from_state: operating_dsm
      target_state: reinstalled_dsm
      method: physical_reset_mode_2
      availability: true
      state: DOCUMENTED
      data_impact:
        system_configuration: erased
        user_data: preserved
        application_state: unknown
      source_claim_ids:
        - official_reset_and_dsm_reinstall
```

Structured paths are an additive v0.1 extension. Existing scalar recovery fields may remain as summaries while evidence is migrated gradually.

Path rules and the provisional data-impact vocabulary live in `RECOVERY_PATH_MODEL.md`. The validator checks path IDs, truth states, availability, data-impact values, and evidence-claim references when `recovery.paths` is present.

Recovery is part of capability quality, not an appendix.

## 13. Locality / cloud dependence

```yaml
locality:
  state: unknown
  vendor_cloud_required_for_basic_operation: unknown
  vendor_cloud_required_for_provisioning: unknown
  local_network_operation: unknown
  offline_operation: unknown
```

Suggested locality states:

```text
fully_local
local_after_provisioning
cloud_optional
cloud_required_for_some_functions
cloud_required
unknown
```

## 14. Economics

Market values are snapshots, not permanent facts.

```yaml
economics:
  market_region: NL
  checked_at: unknown
  used_price_eur:
    low: unknown
    median: unknown
    high: unknown
  new_price_eur: unknown
  required_adapters_eur: unknown
  required_storage_eur: unknown
  setup_minutes: unknown
  special_tools: []
  replacement_availability: unknown
  market_data_state: not_collected
```

Never present a single marketplace listing as a stable market price.

## 15. Candidate roles

```yaml
roles:
  - role: sensor_collector
    confidence: medium
    reason: camera hardware plus verified custom application execution
  - role: always_on_registry
    confidence: low
    reason: unattended boot and power behavior not yet verified
```

Role confidence is not device truth. It is a mapping hypothesis.

## 16. Evidence block

```yaml
evidence:
  overall_state: COMMUNITY_VERIFIED
  locally_verified: false
  last_checked: "2026-09-13"
  claims:
    - id: custom_apk_execution
      state: COMMUNITY_VERIFIED
      source: https://example.org/source
      note: exact scope of claim
```

Claim IDs should be unique within a device record. Structured recovery paths may reference them through `source_claim_ids` so recovery semantics remain traceable to their evidence.

Each evidence item should state what it proves. A source supporting Wi-Fi presence must not be used as evidence of arbitrary network socket access from custom code.

## 17. Truth states

```text
UNRESEARCHED
DOCUMENTED
COMMUNITY_VERIFIED
LOCALLY_VERIFIED
REPRODUCIBLE
DEPRECATED
CONTRADICTED
```

Definitions live in `EVIDENCE_STANDARD.md`.

## 18. Unknown / null discipline

Use:

- `unknown` when the fact is relevant but not established;
- `not_applicable` when the field genuinely does not apply;
- `not_collected` for market/test data not yet gathered;
- `false` only when evidence establishes absence;
- omitted fields only in very early records.

This avoids turning missing research into false certainty.

## 19. Versioning

Schema changes that alter the meaning of existing fields should bump `schema_version`.

Additive optional fields may be introduced inside the same early schema version when they preserve the meaning of existing fields and older records remain valid. Such extensions must be documented and mechanically validated where practical.

Device records should not be silently rewritten to fit a new schema. Migration should preserve old evidence and note transformed fields.

## 20. Design rule

> **The schema describes verified machine state. It does not describe what the product box wants humans to believe the object is.**