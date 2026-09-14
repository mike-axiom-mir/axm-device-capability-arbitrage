# Device Capability Census

**Milestone 01:** 25 evidence-backed devices across at least 8 marketed categories.

Current grounded count:

```text
Devices:    10 / 25
Categories: 10 distinct / 8 required
```

The category-breadth threshold is now exceeded. Milestone 01 is **not complete** until the census reaches 25 grounded devices and the first real capability-arbitrage comparison is evidence-ready.

This counter is intentionally conservative. A candidate does not count merely because it looks interesting.

## Counting rule

A device counts when it has:

- an exact model identity;
- a meaningful execution-surface finding;
- source evidence;
- explicit unknowns;
- recovery state;
- economics state, even if `not_collected`;
- preliminary role mapping.

## Current records

| # | Device | Marketed category | Execution finding | Evidence | Local test | Record |
|---|---|---|---|---|---|---|
| 1 | Sony ILCE-6000 / alpha 6000 | Mirrorless camera | Custom Android/PlayMemories APK execution; working DoomCam implementation | COMMUNITY_VERIFIED | No | `devices/sony/ilce-6000.yaml` |
| 2 | TP-Link Archer C7 v5 | Wi-Fi router | Full OpenWrt Linux userspace with root administration/package management and documented U-Boot/TFTP recovery | COMMUNITY_VERIFIED | No | `devices/tp-link/archer-c7-v5.yaml` |
| 3 | Kobo Clara HD / N249 | E-reader | Exact-model KOReader native execution plus NickelMenu local command/script launching | COMMUNITY_VERIFIED | No | `devices/kobo/clara-hd-n249.yaml` |
| 4 | Roborock S5 | Robot vacuum | Valetudo OTA rooting, post-root SSH, persistent local execution and local robot control | COMMUNITY_VERIFIED | No | `devices/roborock/s5.yaml` |
| 5 | Synology DiskStation DS220+ | NAS / storage appliance | Manufacturer-supported Container Manager execution on exact model, with power/recovery evidence | DOCUMENTED | No | `devices/synology/ds220-plus.yaml` |
| 6 | Dell Wyse 3040 | Thin client | Exact-model Debian installation and community OpenWrt path; UEFI USB/PXE boot and AC-recovery controls | COMMUNITY_VERIFIED | No | `devices/dell/wyse-3040.yaml` |
| 7 | Amazon Fire TV Stick 4K Max 1st Gen / AFTKA | Media / TV / signage | Manufacturer-supported opt-in ADB + sideloaded Android APK execution; application authority without proven root | DOCUMENTED | No | `devices/amazon/fire-tv-stick-4k-max-1st-gen-aftka.yaml` |
| 8 | Wyze Cam v2 | IP camera | Thingino replacement firmware with exact JXF22/JXF23 targets, root shell evidence and local RTSP/ONVIF/WebUI/SSH | COMMUNITY_VERIFIED | No | `devices/wyze/cam-v2.yaml` |
| 9 | SONOFF BASICR2 | Smart-home / microcontroller appliance | Exact-device Tasmota replacement-firmware path on ESP8285; stock eWeLink LAN control vs local Tasmota WebUI/MQTT | COMMUNITY_VERIFIED | No | `devices/sonoff/basicr2.yaml` |
| 10 | Google Pixel 3a / `sargo` | Smartphone / handheld | Current Ubuntu Touch replacement OS with native apps/shell; custom-OS capability gated by bootloader-unlockable acquisition variant | COMMUNITY_VERIFIED | No | `devices/google/pixel-3a-sargo.yaml` |

## Category coverage

- [x] Consumer camera
- [x] Router / access point
- [x] IP camera / NVR
- [x] Phone / tablet / handheld terminal
- [x] Smart-home / microcontroller appliance
- [x] Media / TV / signage hardware
- [x] NAS / storage appliance
- [x] Robot / autonomous appliance
- [x] E-reader / e-ink device
- [ ] Printer / office appliance
- [ ] Console / handheld gaming device
- [x] Thin client / POS / kiosk
- [ ] Industrial / commercial surplus
- [ ] Vehicle infotainment / non-safety computer
- [ ] Other / unknown category

Only eight categories are required for Milestone 01. New records should now optimize for **evidence diversity and model pressure**, not category-count padding.

## High-value next research queue

These are research targets, **not capability claims**.

1. One printer/MFP with a documented application, script, plugin or embedded-Linux execution surface.
2. One console/handheld with a maintained exact-model homebrew path and recovery evidence.
3. One industrial/commercial surplus computer, controller or panel with conventional local execution.
4. One non-safety vehicle/infotainment computer with a documented application execution path.
5. One additional NAS/router/thin-client candidate only if it materially improves the first comparison's price/power/recovery evidence.
6. One oddball appliance whose machine capability is clearly under-described by its market category.
7. One device with a state-dependent locality pattern that differs again from camera/relay firmware replacement, if evidence reveals it naturally.
8. One second phone/tablet/handheld only if it pressures a materially different execution, recovery or acquisition-identity boundary.

The old-Android-phone slot is no longer a queue item: Pixel 3a now fills it with an exact `sargo` replacement-OS path plus a carrier/bootloader capability gate.

## Schema pressure learned so far

The census exists partly to break weak assumptions in the schema. Current evidence has produced several durable distinctions.

### 1. Recovery depends on device state

Roborock S5:

```text
stock S5
  -> manufacturer factory reset can restore original stock firmware

rooted / Valetudo S5
  -> upstream says return to stock is unavailable
```

Therefore `factory_reset: true` cannot stand in for global reversibility.

### 2. Recovery has data impact

Synology DS220+:

```text
Mode 1 reset
  -> credential/network recovery
  -> stored data preserved

Mode 2 + DSM reinstall
  -> system configuration cleared
  -> stored data documented as preserved

Erase-all-data reset
  -> destructive
```

Therefore a recovery path needs target state and data-impact semantics.

### 3. Exact model does not always determine purchasable-unit configuration

Dell Wyse 3040 exists with 8 GB or 16 GB eMMC and optional WLAN/Bluetooth under the same model name. A used listing that only says `Wyse 3040` must not silently inherit the best-known variant.

### 4. Application execution is not operating-system authority

Amazon AFTKA exposes real custom APK execution and ADB through manufacturer developer paths. That does not establish root, bootloader control or unrestricted host administration.

### 5. Locality can depend on persistent device state

Wyze Cam v2 first exposed this:

```text
stock Wyze firmware
  -> internet-centred app lifecycle
  -> configured microSD recording can continue offline

Thingino
  -> local RTSP / ONVIF / WebUI / SSH
```

SONOFF BASICR2 independently reproduces the pattern in a different device class:

```text
stock eWeLink firmware
  -> same-LAN on/off can survive WAN loss after pairing
  -> account/server-backed provisioning and some internet functions remain

Tasmota
  -> local WebUI / console / LAN MQTT
  -> vendor cloud is not required for normal local runtime
```

Because two independent pressure cases now fit the same minimal structure, `tools/validate_records.py` validates the optional `locality.states` extension when a record uses it. Existing flat records are **not** automatically migrated.

### 6. Physical hazard belongs in useful-cost reasoning

BASICR2 adds a mains-voltage constraint. Replacement firmware can increase software agency while simultaneously increasing physical setup/recovery burden. The manufacturer warns of electric-shock risk and recommends qualified-professional installation/repair.

A capability bargain is not a bargain if safe deployment cost is ignored.

### 7. Market observations need configuration-aware cohorts

The first cross-category market snapshot showed that acquisition data has the same identity problem as capability data.

```text
Archer C7 v5
  -> exact hardware revision required

Wyse 3040
  -> private used vs dealer refurbished
  -> 8 GB / 16 GB eMMC and adapter inclusion matter

DS220+
  -> bare chassis must remain separate from drive bundles
  -> RAM upgrades remain attached to observations
```

The repository now stores raw dated listing observations under `market_snapshots/` and mechanically checks sample counts plus low/median/high arithmetic. Asking/displayed listing prices remain evidence about the collected sample, not permanent device prices.

### 8. Execution capability can be gated by acquisition variant

Pixel 3a adds a stronger identity problem than optional RAM/radio/sensor differences:

```text
same marketed model: Pixel 3a

bootloader-unlockable non-Verizon unit
  -> UBports-supported Ubuntu Touch installation path exists

Verizon unit
  -> UBports says bootloader cannot be unlocked
  -> replacement-OS path is unavailable
```

A market listing with carrier/origin unknown therefore must not inherit the custom-OS capability merely from the `Pixel 3a` name. Future market collection should preserve the capability gate or leave it unknown rather than merging locked and unlockable supply.

One pressure case is enough to record the lesson but not enough to freeze a universal new variant schema.

## First arbitrage comparison set

The first comparison remains deliberately cross-category:

```text
low-power local registry contract

TP-Link Archer C7 v5
  marketed as: router
  execution: OpenWrt/root Linux

Synology DS220+
  marketed as: NAS
  execution: supported containers

Dell Wyse 3040
  marketed as: thin client
  execution: Debian/root Linux
```

A first validated EU acquisition snapshot now exists at:

`market_snapshots/low-power-local-registry-node-eu-2026-09-14.yaml`

Observed descriptive cohorts in that snapshot are:

```text
Archer C7 v5 exact-revision private asks
  €20–€40, sample median €32

Dell Wyse 3040 private used asks
  €20–€40, sample median €29.50

Dell Wyse 3040 NL dealer-refurbished offers
  €59–€67, sample median €63

Synology DS220+ bare-chassis/no-drive mixed-RAM listings
  €195–€279, sample median €239.50
```

These are **not transaction-price distributions** and do not produce a winner. Shipping, required storage/adapters, common workload behavior and operational evidence still matter.

Do **not** rank the candidates yet. Comparable evidence is still missing for:

- ranking-ready acquisition cost after shipping, required accessories/storage and market refresh;
- common registry workload footprint;
- wall power under comparable conditions;
- provisioning time/friction;
- hard-power-loss -> service-restart behavior;
- recovery burden and state/data loss;
- replacement availability and remaining hardware life.

The SONOFF BASICR2 is not added to this comparison merely because it runs replacement firmware. Its 1 MB flash, unknown RAM, mains-coupled actuator role and absent registry workload evidence make it a different contract candidate.

The Pixel 3a is also not added merely because it has 4 GB RAM and a Linux-phone OS. Unattended boot/service lifecycle, battery wear, charging behavior, wall power and acquisition-variant unlockability are not yet comparable with the infrastructure candidates.

## What Milestone 01 must prove

The target is not "25 cool hacks."

The milestone should answer:

1. Can different device classes be represented in one capability schema?
2. Can we distinguish hardware presence from accessible execution?
3. Can capability contracts find unexpected candidates?
4. Do unexpected candidates remain attractive after recovery, power, friction, physical safety and opportunity cost are counted?
5. Can another human or machine follow the evidence trail without relying on hidden chat memory?
6. Can persistent firmware/software state be represented without flattening recovery or locality into false global booleans?
7. Can dated market observations remain configuration-aware without turning asking prices into permanent device truth?
8. Can acquisition variants that gate the execution surface stay distinct instead of being silently merged into one model-level capability claim?

If the answer is no, revise the model rather than forcing the hypothesis to win.

## Discovery rule

> **The marketed category tells us where humans shelved the object. The census records what the machine actually is.**
