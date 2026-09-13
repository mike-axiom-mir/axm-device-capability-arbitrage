# Locality State Model — provisional v0.1 extension

**Status:** Evidence-driven provisional extension.  
**First pressure case:** Wyze Cam v2 — stock Wyze firmware vs Thingino replacement firmware.  
**Rule:** Cloud/local behavior belongs to the device state that actually exposes it.

## Why this exists

The original capability schema treated locality as a flat device-level summary:

```yaml
locality:
  state: unknown
  vendor_cloud_required_for_basic_operation: unknown
  vendor_cloud_required_for_provisioning: unknown
  local_network_operation: unknown
  offline_operation: unknown
```

That remains useful for devices whose relevant software state is stable.

The Wyze Cam v2 shows a case where flattening loses truth:

```text
same physical camera
  + stock Wyze firmware
      -> internet-centred app lifecycle
      -> configured microSD recording can continue offline

  + Thingino firmware
      -> local RTSP / ONVIF / Web UI / SSH
      -> vendor cloud is not required for normal local runtime
```

A single `fully_local`, `cloud_required`, or boolean value would describe one state while silently misdescribing the other.

This is the locality equivalent of the recovery-state lesson learned from the Roborock S5.

## Provisional representation

When locality materially changes with persistent device state, a record may use:

```yaml
locality:
  state: state_dependent
  vendor_cloud_required_for_basic_operation: state_dependent
  vendor_cloud_required_for_provisioning: state_dependent
  local_network_operation: state_dependent
  offline_operation: state_dependent

  states:
    - id: stock_firmware
      device_state: stock_firmware
      locality_state: cloud_required_for_some_functions
      state: DOCUMENTED
      offline_capabilities:
        - local_recording_after_prior_configuration
      internet_required_capabilities:
        - remote_live_view
        - cloud_notifications
      provisioning_cloud_requirement: required
      source_claim_ids:
        - stock_locality_claim

    - id: replacement_firmware
      device_state: replacement_firmware
      locality_state: fully_local
      state: COMMUNITY_VERIFIED
      offline_capabilities:
        - local_rtsp
        - local_admin
      internet_required_capabilities: []
      provisioning_cloud_requirement: no_vendor_cloud_required_for_runtime
      source_claim_ids:
        - replacement_locality_claim
```

`state_dependent` is a meta-state, not a claim that locality is unknowable. It means the record must be read through the structured state entries.

## Required meaning

A structured locality-state entry should preserve at least:

- `id` — unique within the device record;
- `device_state` — the persistent software/firmware state being described;
- `locality_state` — the best grounded locality classification for that state;
- `state` — evidence truth state;
- `source_claim_ids` — evidence claims in the same device record.

Useful optional fields include:

- `offline_capabilities`;
- `internet_required_capabilities`;
- `provisioning_cloud_requirement`;
- notes on local-network scope or one-time setup dependencies.

Do not force every device to populate these fields. The extension exists for evidence that actually needs it.

## Per-state locality vocabulary

Use the existing locality vocabulary for `locality_state`:

```text
fully_local
local_after_provisioning
cloud_optional
cloud_required_for_some_functions
cloud_required
unknown
```

Do not use `state_dependent` inside an individual state entry. That value belongs only at the summary level when multiple states differ materially.

## Capability scope matters

A device can perform one useful function offline while other functions remain cloud-dependent.

For example:

```text
offline recording works
!=
full local administration works
```

Therefore, when a state is only partly local, preserve which capabilities survive without the internet instead of converting partial operation into `offline_operation: true` and stopping there.

## Provisioning vs runtime

Keep these separate:

```text
internet needed to install/download firmware
!=
vendor cloud required for normal runtime
```

A local-first replacement firmware may be downloaded from the internet during setup while still having no vendor-cloud dependency once installed.

Likewise, a stock device may need vendor-cloud provisioning before a narrow offline function remains available.

## Matching rule

Capability matching should evaluate the locality of the **target device state**, not average all known states together.

Example:

```text
contract requires fully local RTSP

stock Wyze state
  -> does not satisfy from gathered evidence

Thingino state
  -> can satisfy locality requirement
  -> but modification/recovery cost must also be counted
```

Changing state is not free. Installation effort, recovery burden, irreversible changes, loss of vendor features, and consent implications belong in total useful cost.

## Evidence rule

A state-dependent locality claim must not be inferred merely because replacement firmware exists.

Evidence should establish the relevant behavior, such as:

- documented local service interfaces;
- documented internet/cloud requirements;
- community reproduction on the exact device or hardware target;
- local test receipts when available.

Unknown stays unknown.

## Relationship to recovery

Locality and recovery are related but independent.

A replacement firmware state may be more local while being harder to recover from. A stock state may be cloud-dependent while offering a stronger official restore path.

Do not let improvement on one axis erase cost on the other.

## Validator status

`tools/validate_records.py` currently validates the stable core plus structured recovery paths. It intentionally does **not** yet enforce `locality.states`.

Reason: this structure has one strong pressure case so far. Freeze the mechanical contract only after at least one additional device demonstrates whether these fields generalize cleanly. Until then:

- document the extension;
- preserve evidence claim IDs;
- keep unknowns explicit;
- do not silently reinterpret existing records.

This is deliberate schema restraint, not an invitation to use arbitrary locality fields.

## Migration note

Existing records should not be rewritten automatically.

Potential candidates such as the Roborock S5 may also have stock-vs-replacement locality differences, but migrate them only after the stock state has direct evidence. Do not backfill a second state from assumption.

## Root check

**Truth:** locality belongs to evidenced device state; partial offline capability is not inflated into full locality.  
**Agency / non-domination:** replacement firmware does not justify hidden modification; ownership/authorization and visible operator control remain required.  
**Continuity:** state distinctions and source links live in repository data rather than temporary chat context.  
**Wisdom before speed:** the model is documented now but mechanical enforcement waits for a second pressure case before the shape is frozen.
