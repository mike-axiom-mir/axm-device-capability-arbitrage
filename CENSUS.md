# Device Capability Census

**Milestone 01:** 25 evidence-backed devices across at least 8 marketed categories.

Current grounded count:

```text
Devices:    18 / 25
Categories: 18 distinct / 8 required
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
| 11 | Canon imageRUNNER ADVANCE C3530i | Printer / office MFP | Manufacturer-supported MEAP application runtime via administrator SMS install; `.jar` application + license-aware admission without shell/root claim | DOCUMENTED | No | `devices/canon/imagerunner-advance-c3530i.yaml` |
| 12 | Creality K1 | 3D printer / manufacturing appliance | Manufacturer-documented opt-in root SSH on stock Creality OS, plus firmware rollback and official low-level recovery tooling | DOCUMENTED | No | `devices/creality/k1.yaml` |
| 13 | Valve Steam Deck LCD 256 GB | Handheld gaming PC / console | Manufacturer-supported SteamOS/KDE/Flatpak execution, explicit sudo elevation, BIOS/multi-boot/microSD boot, and official recovery; privilege kept separate from update persistence | DOCUMENTED | No | `devices/valve/steam-deck-lcd-256gb.yaml` |
| 14 | Siemens SIMATIC IOT2050 Advanced / 6ES7647-0BA00-1YA2 | Industrial IoT gateway / commercial surplus | Manufacturer-documented Debian-based root SSH/UART + apt execution, external-media boot and U-Boot; exact article number still spans FS-dependent USB capability | DOCUMENTED | No | `devices/siemens/simatic-iot2050-advanced-6es7647-0ba00-1ya2.yaml` |
| 15 | LG OLED55C1PUB / C1 55-inch OLED | Smart TV / display appliance | Manufacturer-supported webOS Developer Mode `.ipk` execution; sandboxed app authority whose renewable developer session can expire and remove Developer Mode-installed apps | DOCUMENTED | No | `devices/lg/oled55c1pub.yaml` |
| 16 | Polestar 2 model year 2026 | Vehicle infotainment / non-safety computer | Manufacturer-supported Google Play installation of car-adapted Android Automotive apps; sandboxed infotainment execution explicitly bounded away from whole-vehicle/safety-control authority | DOCUMENTED | No | `devices/polestar/polestar-2-my2026.yaml` |
| 17 | Grandstream GXV3370 | Enterprise IP video phone / desk endpoint | Manufacturer-supported Android 7 application development/deployment with administrator-controlled third-party app admission; Safe Mode, factory reset and SD-card firmware recovery remain distinct | DOCUMENTED | No | `devices/grandstream/gxv3370.yaml` |
| 18 | Critter & Guitari Organelle S2 | Programmable musical instrument / audio processor | Manufacturer-supported Pure Data patch authoring plus Linux terminal/compile access; OS and patch state live on a removable microSD root disk with destructive official re-image and retainable prior-media path | DOCUMENTED | No | `devices/critter-and-guitari/organelle-s2.yaml` |

## Category coverage

- [x] Consumer camera
- [x] Router / access point
- [x] IP camera / NVR
- [x] Phone / tablet / handheld terminal
- [x] Smart-home / microcontroller appliance
- [x] Media / TV / signage hardware
- [x] Smart TV / display appliance
- [x] NAS / storage appliance
- [x] Robot / autonomous appliance
- [x] E-reader / e-ink device
- [x] Printer / office appliance
- [x] 3D printer / manufacturing appliance
- [x] Console / handheld gaming device
- [x] Thin client / POS / kiosk
- [x] Industrial / commercial surplus
- [x] Vehicle infotainment / non-safety computer
- [x] Enterprise IP video phone / desk endpoint
- [x] Programmable musical instrument / audio processor
- [ ] Other / unknown category

Only eight categories are required for Milestone 01. New records should now optimize for **evidence diversity and model pressure**, not category-count padding.

## High-value next research queue

These are research targets, **not capability claims**.

1. One additional NAS/router/thin-client candidate only if it materially improves the first comparison's price/power/recovery evidence.
2. One device with a persistent-state locality pattern that differs again from camera/relay firmware replacement, if evidence reveals it naturally.
3. One second phone/tablet/handheld only if it pressures a materially different execution, recovery or acquisition-identity boundary.
4. A third admission-controlled application platform only if it adds a materially different signing, licensing, lease, credential or distribution boundary beyond the Canon C3530i and Grandstream GXV3370 cases.
5. One second privileged physical appliance only if it tests whether the K1 host/actuator distinction generalizes rather than merely repeating root access.
6. One device that independently pressures execution-state persistence across vendor updates, if evidence shows a pattern materially different from Steam Deck Flatpak vs system modification.
7. One second vendor-session-gated developer platform only if it independently tests whether the LG webOS execution-lease pattern generalizes.
8. One oddball appliance whose capability creates a genuinely new schema/evidence pressure rather than repeating general Linux/root access.

The industrial/commercial-surplus slot is no longer a queue item: Siemens SIMATIC IOT2050 Advanced fills it with manufacturer-supported local Linux execution, external-media boot/recovery controls, industrial interfaces, and a new exact-article-versus-functional-status identity pressure case.

The console/handheld slot is no longer a queue item: Steam Deck LCD 256 GB fills it with manufacturer-supported Linux application execution, explicit privileged elevation, multi-boot, removable-media boot, and official recovery.

The oddball-manufacturing-appliance slot is no longer a queue item: Creality K1 fills it with manufacturer-documented root SSH on a heated moving appliance plus documented rollback/recovery.

The smart-TV/display slot is now represented by LG OLED55C1PUB. Its value is not just that webOS can run custom applications: LG documents a renewable Developer Mode session whose expiry/disable state removes apps installed through Developer Mode, making execution durability a separate capability question.

The vehicle-infotainment slot is now represented by Polestar 2 model year 2026. Its value is not merely that Android apps run in a car: the evidence forces a parent-system boundary. A sandboxed infotainment application may be valid custom execution while braking, steering, propulsion, safety systems, CAN and arbitrary vehicle-property authority remain outside the proven scope.

The enterprise IP video-phone / desk-endpoint slot is now represented by Grandstream GXV3370. Its value is not simply Android-on-a-phone: Grandstream documents a real custom-application path whose install/uninstall admission can be allowed, administrator-gated, source-sensitive, or prohibited, plus separate Safe Mode, factory-reset and SD-card firmware-recovery layers.

The programmable musical-instrument / audio-processor slot is now represented by Critter & Guitari Organelle S2. Its value is not simply Linux in an instrument: the manufacturer documents user-authored patch execution plus console/compile access while leaving privilege unproven, and the removable microSD root disk creates a recovery case where re-imaging the chosen target is destructive even though an untouched prior OS card can be retained physically.

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

A market listing with carrier/origin unknown therefore must not inherit the custom-OS capability merely from the model name. Future market collection should preserve the capability gate or leave it unknown rather than merging locked and unlockable supply.

One pressure case is enough to record the lesson but not enough to freeze a universal new variant schema.

### 9. An application runtime can be admission-controlled

Canon C3530i first exposed the distinction:

```text
MEAP runtime exists
  -> administrator logs into SMS
  -> compatible MEAP application package is selected
  -> applicable license/admission conditions are satisfied
  -> application can be installed and started
```

Grandstream GXV3370 now independently repeats the same higher-level pattern through a different mechanism:

```text
Android application runtime exists
  -> administrator install/uninstall policy applies
  -> policy may allow, require administrator authentication, be source-sensitive, or forbid third-party app changes
  -> compatible admitted application can run
```

Neither case proves unrestricted general-purpose host authority.

```text
custom application execution
  !=
arbitrary unsigned package admission
  !=
shell/root/bootloader ownership
```

The two records preserve their platform-specific admission controls locally instead of forcing unlike mechanisms into one rigid universal schema. Two cross-vendor cases are enough to treat admission as a durable capability axis, but not enough to pretend Canon licensing and Grandstream Android policy are the same thing.

The GXV3370 adds a second lesson in the same record: Safe Mode can isolate problematic third-party applications without being confused with factory reset or firmware restoration. Recovery target state matters even when the underlying device is still bootable.

### 10. Root host authority is not physical-actuator suitability

Creality K1 adds the inverse pressure case:

```text
manufacturer-documented root SSH exists
  -> authorized owner has privileged host execution

does not automatically mean

unrelated always-on compute is wise
motion/heater actuation is safe to experiment with
whole-device power is low
custom services survive power loss
printer opportunity cost is zero
```

The K1 is a physically consequential fabrication appliance with documented root SSH. Capability matching must therefore keep host execution authority separate from actuator use, physical safety, workload fit and total useful cost.

This is one pressure case. It is enough to preserve the distinction, not enough to freeze a universal actuator-authority schema.

### 11. Execution privilege is not update persistence

Steam Deck LCD 256 GB adds a software-lifecycle distinction:

```text
Flatpak application on SteamOS
  -> normal-user application path
  -> Valve says it runs from writable storage
  -> Valve says this arrangement avoids breakage from future SteamOS system updates

sudo / non-Flatpak system modification
  -> higher privilege is manufacturer-documented
  -> Valve warns non-Flatpak software may be wiped by a later SteamOS update
```

Therefore a matcher must not turn `root` or `sudo` into an implicit claim that deployment state survives vendor updates.

The record uses an additive `update_persistence` note on its execution surfaces. One pressure case is enough to preserve the lesson but not enough to freeze a universal schema field.

### 12. Exact manufacturer article number can still span functional-status revisions

Siemens SIMATIC IOT2050 Advanced adds an industrial identity case stronger than a generic family name:

```text
same exact article: 6ES7647-0BA00-1YA2

FS01-FS03
  -> 2 x USB 2.0 Type A

FS04
  -> 1 x USB 3.0 Type A
  -> 1 x USB 2.0 Type A
```

Therefore an exact order number is not always the final hardware-identity boundary. Market observations and local experiment receipts should preserve the observed manufacturer functional status when a capability differs by FS.

The same device also has current software-maintenance pressure: Siemens ProductCERT advisory `SSA-834709` says exact-product Industrial OS deployments below V4.3.4.1 with Node-RED installed are affected by a critical authentication flaw and recommends updating affected deployments. Security-patch state is therefore an acquisition/deployment fact, not something to infer from the model name.

One industrial device is enough to preserve these facts in the record and evidence packet, but not enough to freeze a universal functional-status or security-maintenance schema extension yet.

### 13. Developer execution can be leased by vendor session state

LG OLED55C1PUB adds a continuity distinction that is separate from both application privilege and update persistence:

```text
webOS Developer Mode active
  + valid LG Developer session
  -> custom .ipk applications can be installed and launched

session time expires + TV reboots
  OR TV reboots ten times while offline
  -> Developer Mode is disabled
  -> apps installed through Developer Mode are uninstalled
```

Therefore `custom_code: true` must not silently become a claim of indefinitely durable deployment. Account/session admission, execution authority, runtime locality, cold-boot behavior and deployment persistence are separate questions.

This is one pressure case. The repo preserves the lesson in the device/evidence record but does not freeze a universal execution-lease schema until an independent platform reproduces the pattern.

### 14. Subsystem execution authority is not parent-system authority

Polestar 2 MY2026 adds the first explicit safety-critical-parent case:

```text
road vehicle
  contains
Android Automotive infotainment application environment

car-adapted Google Play app executes
  -> sandboxed infotainment capability is real

does not prove
  -> braking control
  -> steering control
  -> propulsion control
  -> safety-system control
  -> CAN access
  -> arbitrary vehicle-property read/write
```

Android's car application model is admission-, permission- and driving-policy-bounded, and the Polestar evidence packet contains no exact-model evidence granting ordinary third-party Play apps safety-critical authority. The record therefore stores a local `safety_boundary` on the execution surface instead of letting application execution leak upward into a whole-vehicle capability claim.

This is one vehicle pressure case. Preserve the distinction, but do not freeze a universal parent-system schema until independent hardware demonstrates the same need again.

### 15. Destructive restore can still preserve continuity through removable root media

Organelle S2 adds a recovery distinction that does not fit a single destructive/non-destructive label:

```text
microSD root disk selected for factory re-image
  -> target card is completely wiped
  -> factory OS state can be restored

owner instead uses a new microSD card
  -> new card receives factory image
  -> prior OS/root disk can remain physically retained
```

The recovery action is destructive to its selected target, but removable-media choice can preserve the previous boot state outside that target. A recovery model therefore may need to keep **target-medium data impact** separate from **whether prior boot media can be retained**.

This is one pressure case. The Organelle record stores the distinction locally on its recovery path instead of freezing a universal removable-root-medium schema after a single device.

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

The C3530i is not added merely because it has 3 GB RAM and an embedded application runtime. MEAP admission/licensing, workload compatibility, transport/mechanical cost, restart behavior and comparable power evidence are not established; Canon's approximately 44.1 W standby claim already makes the low-power contract a poor fit to assume without a workload-specific reason.

The Creality K1 is not added merely because it exposes manufacturer-documented root SSH. RAM, comparable wall power, harmless-service restart behavior, printer opportunity cost and the wisdom of tying registry availability to a heated moving fabrication appliance are unproven.

The Steam Deck LCD 256 GB is not added merely because it has 16 GB RAM, x86 Linux and documented sudo. Whole-device wall power, battery/charging behavior, service autostart, hard-power-loss recovery, update-stable service deployment, used-unit cost and handheld opportunity cost are not comparable with the current infrastructure candidates.

The Siemens IOT2050 Advanced is not added merely because it has manufacturer-documented root Linux execution, two Gigabit Ethernet ports and external-media recovery. Its exact functional status, used acquisition cost, power-supply inclusion, measured registry-workload power, eMMC health, software/security state, service autostart and hard-power-loss behavior are not yet comparable with the three current candidates. The manual's 12 W typical basic-device figure remains manufacturer context, not a common-workload wall-power measurement.

The LG OLED55C1PUB is not added merely because it can run custom webOS applications and has Ethernet/Wi-Fi. The documented Developer Mode path is renewable-session-gated, RAM/storage headroom is unknown, cold-boot app/service autostart is unproven, active wall power is unmeasured, and tying infrastructure availability to a large display has significant opportunity cost.

The Polestar 2 MY2026 is not added merely because it can run car-adapted Android Automotive applications. It is a road vehicle with an admission-controlled sandboxed infotainment surface, not a proven general-purpose/root host; infotainment power, service persistence, exact hardware resources and standalone acquisition economics are unknown, while whole-vehicle opportunity cost dominates any speculative registry-node value.

The Grandstream GXV3370 is not added merely because it has 2 GB RAM, Gigabit Ethernet and manufacturer-supported Android application execution. Its application admission policy is state-dependent, privilege remains unknown, cold-boot service persistence is unverified, wall power is unmeasured, and no dated acquisition cohort or registry workload evidence exists.

The Organelle S2 is not added merely because it has Linux, 1 GB RAM, local networking through a USB adapter and a real console/compile surface. Root privilege, service autostart, hard-power-loss restart, measured wall power, acquisition cost and opportunity cost as a musical instrument remain unverified, so registry-node suitability is not inferred from programmability alone.

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
9. Can real but administrator/license/policy-gated application runtimes remain distinct from unrestricted general-purpose execution?
10. Can privileged host execution remain distinct from physical-actuator suitability and total-useful-cost fit?
11. Can execution privilege remain distinct from the persistence of installed state across vendor OS updates?
12. Can exact manufacturer order numbers remain revision-aware when a functional-status change alters real capability?
13. Can a vendor-session-gated developer surface remain distinct from indefinitely durable deployment without hiding account/network renewal dependency?
14. Can execution authority inside one subsystem remain distinct from authority over a safety-critical parent machine?
15. Can recovery distinguish destructive impact on the selected removable boot medium from the separate ability to retain an earlier boot medium intact?

If the answer is no, revise the model rather than forcing the hypothesis to win.

## Discovery rule

> **The marketed category tells us where humans shelved the object. The census records what the machine actually is.**
