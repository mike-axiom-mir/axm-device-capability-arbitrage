# Next Build

**Current state:** Initial foundation is in place. Nine census records now exercise nine materially different hardware/execution patterns: a consumer camera with a custom Android application path, a Wi-Fi router with replaceable Linux/OpenWrt firmware, an e-reader with native application/script execution, a mobile robot with rooted Linux/SSH plus local-only control, a NAS with a manufacturer-supported container runtime plus native persistent storage, a thin client with conventional Debian/OpenWrt execution plus PC-class UEFI boot controls, a media stick with manufacturer-supported Android APK sideloading through opt-in ADB but no evidence of root ownership, an IP camera with exact Thingino replacement-firmware targets/root SSH/local RTSP-ONVIF services, and a smart-home ESP8285 relay whose stock eWeLink locality differs materially from its Tasmota replacement-firmware locality. The S5 exposed recovery-by-device-state; the DS220+ added recovery data-impact semantics; the Wyse 3040 exposed configuration identity as a separate problem; the Fire TV AFTKA separated application execution from administrator/root authority; Wyze Cam v2 first exposed state-dependent locality; and SONOFF BASICR2 independently reproduced that locality pattern in a different hardware class. The required 8-category breadth threshold is exceeded at 9 distinct categories, but Milestone 01 still requires 16 more evidence-backed devices and a real arbitrage result. Structural validation now covers both recovery paths and optional state-dependent locality records.

## Completed foundation step — Mechanical record checks

Implemented:

- YAML parsing for device and capability-contract records;
- required identity/evidence fields;
- allowed truth-state validation;
- explicit economics state;
- duplicate record/contract ID detection;
- execution-surface structure checks;
- recovery/evidence state checks;
- structured recovery-path checks with evidence-claim references;
- optional structured locality-state checks with evidence-claim references;
- GitHub Actions validation on pushes to `main` and pull requests.

The validator deliberately does **not** reject unknown capability values or enforce a large rigid schema. New hardware classes still need room to challenge v0.1.

`LOCALITY_STATE_MODEL.md` is now an evidence-backed optional extension. Wyze Cam v2 and SONOFF BASICR2 independently show that persistent firmware state can change cloud/local behavior. The validator enforces the minimal shape only when `locality.states` is present; it does not force old flat records to migrate.

## Priority 1 — Run the first actual arbitrage comparison

The hypothesis is not proven by building a database. The three-category candidate set already exists for the current capability contract:

> **low-power local registry / heartbeat node**

Current candidates:

- TP-Link Archer C7 v5 — router / OpenWrt; tiny RAM/flash; strong network role and TFTP recovery;
- Synology DS220+ — NAS / supported containers; much larger storage/compute platform with manufacturer power data but drive and opportunity cost;
- Dell Wyse 3040 — thin client / full Debian; 2 GB RAM, internal eMMC, Gigabit Ethernet, UEFI USB recovery, configurable AC Recovery and a manufacturer sub-4-W claim.

Do **not** rank them yet. The next valuable comparison work is to collect the same missing evidence for all three so unknowns are not converted into fake scores.

Required comparison state:

- used-market snapshot in one NL/EU date window;
- observed configuration for listings where model variants matter;
- measured or credible power data with source class;
- one tiny common registry workload definition;
- provisioning friction and repeat-provisioning time;
- recovery quality and data impact;
- hard-power-loss -> reboot -> service restart behavior;
- replacement availability;
- workload fit;
- required storage/adapters counted separately from chassis price.

Only then ask whether the non-obvious device is actually cheaper/better.

### Configuration-identity rule learned from Wyse 3040 and reinforced by Wyze Cam v2

A product model can remain exact while still spanning materially different unit configurations.

For Wyse 3040, Dell documents:

```text
same marketed model
  -> 8 GB or 16 GB eMMC
  -> optional WLAN/Bluetooth
```

For Wyze Cam v2, current Thingino support distinguishes:

```text
same marketed model
  -> T20X + JXF22 + RTL8189FTV
  -> T20X + JXF23 + RTL8189FTV
```

Market research, installation and matching must preserve observed unit configuration when it matters. A listing containing only a model name must not inherit the best-known storage/radio/sensor variant silently, and replacement firmware must not be selected from the marketed name alone when hardware variants require separate targets.

A later schema extension may need a more general variant/configuration representation, but do not freeze that shape until more devices pressure it.

### Execution-authority rule learned from Fire TV AFTKA

A documented custom-code path is not automatically an administrator-owned operating system.

For Fire TV Stick 4K Max 1st Gen (`AFTKA`), Amazon documents:

```text
user enables developer options
  -> user authorizes ADB connection
  -> custom APK can be sideloaded and launched
```

That proves a real application execution surface. It does **not** prove:

```text
root
bootloader access
cold-boot custom-app restart
fully offline provisioning/runtime
low-level restore media
```

Future matching must preserve sandbox/application-level capability without silently upgrading it to general Linux/root capability.

The Fire TV therefore does not enter the registry comparison merely because it has 2 GB RAM and networking. A candidate must satisfy the contract, not resemble a computer on paper.

### Locality-state rule — now supported by two independent devices

Locality is not always a permanent hardware property.

Wyze Cam v2:

```text
stock Wyze firmware
  -> internet-centred app/live/settings behavior
  -> configured microSD recording can continue offline

Thingino firmware
  -> local RTSP / ONVIF / Web UI / root SSH
  -> vendor cloud is not required for normal local runtime
```

SONOFF BASICR2:

```text
stock eWeLink firmware
  -> same-LAN on/off can survive WAN loss after pairing
  -> stock provisioning and some schedule/scene/share setup remain server/internet dependent

Tasmota firmware
  -> local WebUI / console / LAN MQTT
  -> vendor cloud is not required for normal local runtime
```

These are different hardware and different stock-locality patterns, but both fit the same minimal `locality.states` structure. That is enough to validate the optional structure mechanically.

Do **not** infer from this that replacement firmware is always preferable. State change has cost: modification effort, lost vendor features, physical safety, recovery uncertainty and possible irreversible transitions.

## Priority 2 — Continue census expansion across genuinely different hardware

The breadth threshold is exceeded at 9 distinct categories. Do not pad the remaining 16 records with near-duplicates. New records should maximize schema pressure, evidence diversity, or comparison value.

Recommended next categories/patterns:

1. old Android phone with documented unlock/recovery and offline operation;
2. printer/MFP with an application or embedded Linux/Android execution layer;
3. console/handheld gaming device with a supported homebrew/Linux path;
4. industrial/commercial surplus hardware with non-PC market positioning;
5. non-safety vehicle/infotainment computer only where the execution boundary is clearly separated from safety-critical systems;
6. an additional network/storage/thin-client candidate only if it materially improves the first comparison's price/power/recovery evidence;
7. a new persistent-state pattern that pressures locality, recovery or execution authority differently again;
8. oddball appliance where a different execution/recovery/locality pattern challenges the current schema.

Each new record should expose something the existing nine do not.

### Recovery-state rule learned from the S5

When a persistent modification changes what recovery paths remain available, record recovery by **device state** rather than treating `factory_reset` as a global property.

Example pattern:

```text
stock state
  -> official factory reset may restore stock firmware

modified state
  -> return-to-stock may be unavailable
  -> same modified state may still be reprovisionable
```

Do not let a valid stock recovery claim imply reversibility after modification.

### Recovery-data rule learned from the DS220+

When two recovery methods have different data/configuration effects, preserve that difference explicitly.

Example pattern:

```text
OS/config recovery
  -> system configuration may be cleared
  -> user data may be preserved

factory erase
  -> system returns to defaults
  -> user data is destroyed
```

Do not let `recovery_path: true` hide whether state, configuration or user data survives.

### Physical-safety rule learned from BASICR2

Software freedom can coexist with hardware hazards.

BASICR2 replacement firmware is an interesting local-control capability, but the device contains hazardous mains voltage. The manufacturer warns about electric shock and recommends qualified-professional installation/repair.

Therefore:

```text
firmware is community-flashable
!=
energized hardware is safe to handle casually
```

Safe installation/inspection effort is real friction and belongs in total useful cost. Research notes should not normalize live-mains experimentation merely because a low-voltage programming interface exists.

## Priority 3 — Add scoring only after comparison data exists

Do not invent a universal device score yet.

Once the three registry candidates contain comparable cost, power, provisioning and recovery evidence, introduce only the smallest scoring model needed to answer that concrete capability contract. Unknowns must remain visible and must not be converted into neutral-looking numeric values.

## Near-term experiments

### A. Archer C7 v5

- collect NL/EU used-price samples;
- find credible idle/load power measurements or measure locally later;
- define and deploy the common tiny registry workload;
- estimate/test whether 128 MB RAM + 16 MB flash is genuinely enough;
- test whether USB storage changes the result positively or only adds fragility;
- test hard power loss -> OpenWrt -> registry service restart.

### B. Synology DS220+

- collect NL/EU bare-chassis used-price samples separately from units sold with drives;
- price a minimal supported storage configuration so required drive cost is visible;
- verify a currently compatible Container Manager release on owned hardware;
- run the common tiny registry workload and measure RAM/CPU/storage footprint;
- measure wall power with drives active, idle and hibernated and compare with Synology's manufacturer figures;
- test power loss -> Power Recovery -> DSM -> container restart behavior;
- test Mode 2 recovery on noncritical data and preserve which application/container state must be rebuilt.

### C. Dell Wyse 3040

- collect 5–10 dated NL/EU listings and record 8/16-GB eMMC plus power-adapter inclusion separately;
- record whether each listing identifies optional WLAN/Bluetooth rather than assuming it;
- on owned hardware, record BIOS version and actual eMMC capacity before install;
- install Debian from preserved media and time the complete provisioning flow including the EFI/GRUB workaround;
- run the same tiny registry workload used on Archer/DS220+;
- measure wall power at boot, idle and registry-active state rather than substituting Dell's sub-4-W product claim;
- test AC loss -> AC Recovery -> Debian -> service restart repeatedly;
- test USB reinstall and record exactly which system/user/application state must be recreated;
- inspect eMMC health because soldered used flash is a real replacement/reliability cost.

### D. Sony ILCE-6000

- identify exact SoC/architecture from model-specific evidence;
- identify RAM from reliable evidence;
- map PlayMemories API access to sensor, network, storage and audio;
- document recovery/version constraints;
- collect used-price snapshot;
- decide which non-camera roles are actually rational rather than merely possible.

### E. Roborock S5

- collect an NL/EU used-price sample;
- collect credible idle-on-dock / charging / cleaning power data or measure locally;
- verify exact production/recovery firmware before any local modification test;
- enumerate actual S5 Valetudo capabilities rather than inheriting every generic integration feature;
- treat permanent loss of stock state as setup/recovery cost rather than hiding it;
- only add stock-vs-Valetudo `locality.states` if direct stock-locality evidence is collected rather than inferred.

### F. Fire TV Stick 4K Max 1st Gen / AFTKA

- if an owned unit becomes available, preserve its exact build model and Fire OS version before testing;
- locally verify ADB authorization, APK sideload and removal without assuming root;
- test whether a deliberately local APK works with WAN disconnected after stock provisioning;
- test cold power loss -> Fire OS -> application/service lifecycle rather than assuming auto-start;
- measure wall power at boot, idle, local-app active and media-active states;
- verify factory reset on noncritical state and document exactly what application data survives, if anything;
- collect a dated NL/EU used-market sample only after exact-generation identity can be distinguished from 2nd Gen listings.

### G. Wyze Cam v2

- identify JXF22 vs JXF23 on a physical owned unit before selecting replacement firmware;
- preserve stock firmware/version before modification;
- reproduce Thingino installation using the least invasive supported method for that exact unit;
- measure wall power in stock idle, Thingino idle and active RTSP states;
- test cold power loss -> Thingino -> Wi-Fi -> RTSP/ONVIF/SSH repeatedly;
- test the official stock `demo.bin` flash on noncritical stock state separately from researching a Thingino-to-stock transition;
- collect a dated NL/EU used-market sample with sensor-variant ambiguity recorded rather than guessed;
- do not treat root SSH as proof that the camera is a rational general-purpose registry node until RAM/flash headroom and opportunity cost are known.

### H. SONOFF BASICR2

- only inspect/modify an owned or explicitly authorized unit with mains disconnected;
- follow the manufacturer warning that installation/repair should be handled by a qualified professional;
- identify the exact BASICR2 board/revision before firmware work;
- record stock firmware/app state and test stock LAN on/off with WAN deliberately unavailable after normal pairing;
- determine whether a trustworthy stock-firmware preservation/restore path exists before replacement; do not assume stock factory reset restores overwritten firmware;
- reproduce Tasmota only through an isolated low-voltage programming setup and preserve firmware/tool hashes;
- test local WebUI and local MQTT with outbound internet blocked;
- test repeated hard power loss -> Tasmota -> Wi-Fi -> local control and preserve relay power-on-state behavior;
- measure device self-consumption only using an appropriate safe mains measurement method, not an exposed energized PCB;
- collect a dated NL/EU price sample only if actuator-node comparison becomes useful.

## Stop conditions

Do not expand the census blindly if:

- records keep requiring exceptions the schema cannot represent;
- evidence quality is too weak to compare devices;
- cost data cannot be time/region scoped;
- a scoring system starts hiding unknowns;
- product category begins acting as an implicit capability claim;
- recovery claims stop identifying which device state they apply to;
- recovery claims hide configuration/data destruction behind a single positive boolean;
- a model-family record silently assigns optional or higher-spec unit variants to every physical device;
- an application/developer execution surface is silently promoted to root or unrestricted operating-system authority;
- a single locality label hides materially different persistent-state cloud behavior;
- replacement-firmware capability is treated as free while recovery, lost vendor features or physical hazard are ignored.

When one of those occurs, repair the model before adding volume.

## Root gate

**Truth:** no fake verification, silent best-variant inheritance, privilege inflation, locality flattening, or electrical-rating-as-power-measurement substitution.  
**Agency / non-domination:** owned/authorized hardware only; consent-visible developer access stays consent-visible; cameras add privacy/recording consent; physical actuators remain visibly user-controlled.  
**Continuity:** evidence, variant caveats, execution boundaries, locality states, recovery and safety constraints live in repo state.  
**Wisdom before speed:** compare common evidence before ranking hardware; replacement firmware gains must be weighed against installation, recovery, opportunity cost and physical safety.
