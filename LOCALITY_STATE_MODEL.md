# Locality State Model — evidence-backed v0.1 extension

**Status:** Accepted optional extension; structurally validated when used.  
**Pressure case 1:** Wyze Cam v2 — stock Wyze firmware vs Thingino.  
**Pressure case 2:** SONOFF BASICR2 — stock eWeLink firmware vs Tasmota.  
**Rule:** Cloud/local behavior belongs to the persistent device state that actually exposes it.

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

That remains correct for devices whose relevant software state is stable or whose evidence does not justify multiple states.

Two independent device classes now show that flattening can lose truth.

### Pressure case 1 — Wyze Cam v2

```text
same physical camera
  + stock Wyze firmware
      -> internet-centred app lifecycle
      -> configured microSD recording can continue offline

  + Thingino firmware
      -> local RTSP / ONVIF / Web UI / SSH
      -> vendor cloud is not required for normal local runtime
```

### Pressure case 2 — SONOFF BASICR2

```text
same physical Wi-Fi relay
  + stock eWeLink firmware
      -> same-LAN on/off control can survive WAN loss after pairing
      -> account/server-backed provisioning and some internet functions remain

  + Tasmota firmware
      -> direct local WebUI / console / LAN MQTT
      -> vendor cloud is not required for normal local runtime
```

These cases are materially different. One is an IP camera whose replacement firmware exposes a local camera/Linux stack. The other is a tiny ESP8285 mains relay whose stock firmware is already partly local. The common state structure therefore appears general enough to validate without pretending every device needs it.

This is the locality equivalent of the recovery-state lesson learned from the Roborock S5.

## Representation

When locality materially changes with persistent device state, use:

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
      provisioning_cloud_requirement: required
      source_claim_ids:
        - stock_locality_claim

    - id: replacement_firmware
      device_state: replacement_firmware
      locality_state: fully_local
      state: COMMUNITY_VERIFIED
      offline_capabilities:
        - local_service
        - local_admin
      internet_required_capabilities: []
      provisioning_cloud_requirement: no_vendor_cloud_required_for_runtime
      source_claim_ids:
        - replacement_locality_claim
```

`state_dependent` is a summary/meta-state. It does not mean locality is unknowable; it means the structured entries are the truth-bearing unit.

## Required fields for each state entry

When `locality.states` is present, every entry must preserve:

- `id` — unique within the device record;
- `device_state` — the persistent software/firmware state being described;
- `locality_state` — grounded locality classification for that state;
- `state` — evidence truth state;
- `source_claim_ids` — references to evidence claims in the same record.

Useful optional fields include:

- `offline_capabilities`;
- `internet_required_capabilities`;
- `provisioning_cloud_requirement`;
- notes describing LAN scope, one-time setup dependencies, or optional internet services.

The validator does not require the optional fields because different device classes may express locality with different capability granularity.

## Per-state locality vocabulary

Valid `locality_state` values are:

```text
fully_local
local_after_provisioning
cloud_optional
cloud_required_for_some_functions
cloud_required
unknown
```

Do not use `state_dependent` inside an individual state entry. That value belongs only at the summary level.

## Capability scope matters

One offline capability does not make the whole device fully local.

Examples:

```text
offline recording works
!=
full local administration works
```

and:

```text
same-LAN relay on/off works
!=
all schedules, scenes, sharing and provisioning are cloud-independent
```

When a state is only partly local, preserve the capability split instead of collapsing it to `offline_operation: true`.

## Provisioning vs runtime

Keep these separate:

```text
internet used to download/install software
!=
vendor cloud required for normal runtime
```

Likewise:

```text
vendor cloud/account required for initial stock pairing
!=
public internet required for every post-pairing LAN action
```

A replacement firmware can be downloaded from the internet during setup and still be fully local at runtime. A stock device can use a cloud/account path for provisioning while retaining narrower local behavior afterwards.

## Matching rule

Capability matching evaluates the locality of the **target device state**, not an average of all known states.

Example:

```text
contract requires fully local camera streaming

Wyze stock state
  -> does not satisfy from gathered evidence

Wyze Thingino state
  -> can satisfy locality requirement
  -> modification/recovery cost must also count
```

For a relay contract:

```text
contract requires basic same-LAN on/off during WAN outage

BASICR2 stock eWeLink state
  -> may satisfy that narrow locality requirement after pairing

contract additionally requires no vendor account/cloud provisioning

BASICR2 stock state
  -> does not satisfy
BASICR2 Tasmota state
  -> can satisfy locality requirement
  -> firmware replacement + mains/recovery burden must count
```

Changing state is never free. Installation effort, recovery burden, irreversible/uncertain reversion, lost vendor features, physical safety, and consent implications belong in total useful cost.

## Evidence rule

A state-dependent locality claim must not be inferred merely because alternative firmware exists.

Evidence should establish the relevant behavior, for example:

- documented local service interfaces;
- documented internet/cloud requirements;
- community reproduction on the exact device/target;
- manufacturer LAN/offline behavior;
- local verification receipts when available.

Unknown stays unknown.

## Relationship to recovery

Locality and recovery are related but independent axes.

A replacement firmware state may improve locality while worsening recovery. A stock state may retain cloud dependence while offering a stronger official reset path.

Examples already in the census:

- Wyze Cam v2: Thingino improves local control; Thingino-to-stock recovery remains unknown in the current evidence.
- SONOFF BASICR2: Tasmota improves local ownership; current gathered evidence does not establish a tested return-to-stock path.
- Roborock S5: Valetudo is local-first while upstream documents return to stock as unavailable.

Do not let a gain on one axis erase cost on another.

## Validator behavior

`tools/validate_records.py` now validates `locality.states` **only when a device record chooses to use it**.

It checks:

- summary `locality.state` is `state_dependent`;
- `locality.states` is a non-empty list;
- state-entry IDs are unique;
- `device_state` is explicit;
- `locality_state` uses the bounded vocabulary above;
- evidence `state` uses the repository truth-state vocabulary;
- every `source_claim_ids` reference resolves to an evidence claim in the same record;
- optional offline/internet capability lists are actually lists of non-empty strings;
- optional provisioning requirement is an explicit non-empty string.

It intentionally does **not**:

- require every device to migrate to this model;
- guess missing states;
- require exactly two states;
- force stock/replacement naming;
- decide which firmware state is preferable;
- convert partial locality into a binary score.

The validator therefore catches structural drift without turning a young evidence model into a rigid ontology.

## Migration rule

Do not rewrite existing records automatically.

Migrate a flat record only when direct evidence shows that persistent states materially differ in locality. For example, the Roborock S5 may eventually justify separate stock/Valetudo locality entries, but the stock state should not be backfilled from assumption merely because Valetudo is local-first.

When migrating:

1. preserve the old evidence claims;
2. add direct evidence for every new state distinction;
3. keep unresolved capabilities `unknown`;
4. do not silently change overall truth level;
5. record recovery/modification cost separately.

## Root check

**Truth:** locality belongs to evidenced device state; partial offline behavior is not inflated into full locality.  
**Agency / non-domination:** alternative firmware does not justify hidden modification; owned/authorized hardware and visible operator control remain required.  
**Continuity:** both pressure cases, state distinctions, source links and validator semantics live in repository state.  
**Wisdom before speed:** the model became mechanically enforced only after a second independent device class reproduced the need, and state change costs remain part of matching.
