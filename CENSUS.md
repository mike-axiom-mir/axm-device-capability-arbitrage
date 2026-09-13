# Device Capability Census

**Milestone 01:** 25 evidence-backed devices across at least 8 marketed categories.

Current grounded count:

```text
Devices:    7 / 25
Categories: 7 / 8
```

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
| 3 | Kobo Clara HD / N249 | E-reader | Exact-model KOReader native-app execution plus documented NickelMenu script/process launching and official manual reset path | COMMUNITY_VERIFIED | No | `devices/kobo/clara-hd-n249.yaml` |
| 4 | Roborock S5 | Robot vacuum | Valetudo-supported OTA rooting, root SSH execution and local-only control; stock recovery differs materially from post-root recovery | COMMUNITY_VERIFIED | No | `devices/roborock/s5.yaml` |
| 5 | Synology DiskStation DS220+ | NAS / storage appliance | Manufacturer-supported Container Manager path on exact model; 2 GB RAM, SATA persistence and documented reset/reinstall paths | DOCUMENTED | No | `devices/synology/ds220-plus.yaml` |
| 6 | Dell Wyse 3040 Thin Client | Thin client / endpoint | Exact-model Debian 12 installation plus community OpenWrt execution; UEFI USB/PXE boot, AC Recovery and manufacturer sub-4-W power claim | COMMUNITY_VERIFIED | No | `devices/dell/wyse-3040.yaml` |
| 7 | Amazon Fire TV Stick 4K Max 1st Gen / AFTKA | Media / TV / signage hardware | Manufacturer-documented Fire OS 7 APK sideload/launch path through opt-in ADB; application execution without evidence of root or unattended service startup | DOCUMENTED | No | `devices/amazon/fire-tv-stick-4k-max-1st-gen-aftka.yaml` |

## Category coverage

- [x] Consumer camera
- [x] Router / access point
- [ ] IP camera / NVR
- [ ] Phone / tablet / handheld terminal
- [ ] Smart-home / microcontroller appliance
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

Only eight categories are required for Milestone 01, but the search should not stop there.

## High-value next research queue

These are research targets, **not capability claims**.

1. One OpenIPC-supported IP camera with an exact SoC/model mapping.
2. One old Android phone with unlock/recovery and offline operation.
3. One ESP8266/ESP32 consumer appliance with replaceable local firmware.
4. One printer/MFP that supports applications or an embedded Linux/Android execution layer.
5. One non-safety vehicle/infotainment computer with a documented application execution path.
6. One console/handheld gaming device with a supported homebrew or Linux execution surface.
7. One industrial/commercial surplus device with conventional local execution but non-PC market positioning.
8. One oddball appliance or retired commercial device where the execution surface is materially more useful than the marketed category suggests.
9. One additional media/signage box only if it exposes a materially different execution/recovery/locality pattern from the AFTKA Fire TV record.
10. One additional thin client only if it exposes a materially different execution/recovery/power pattern from the Wyse 3040.

## Schema pressure discovered so far

### Recovery target/state

The fourth record exposed a recovery-model problem worth preserving:

```text
stock device recovery != post-modification recovery
```

For the Roborock S5, manufacturer factory reset is documented for the stock state, while Valetudo documents the rooted/install state as not returnable to stock. A single `factory_reset: true` field would therefore overstate recoverability after modification.

Future records should preserve the device state in which a recovery path applies whenever persistent modification changes reversibility.

### Recovery data impact

The fifth record exposes a second, independent recovery distinction:

```text
recovery path exists != recovery path preserves the same data/state
```

For the Synology DS220+, Synology documents a Mode 2 DSM-reinstallation path that clears system configuration while preserving stored data, while a separate erase-all-data factory-reset path is destructive. Treating both as one `factory_reset: true` property would hide operationally critical data-loss semantics.

Future recovery modeling should preserve at least:

- which state/target the recovery path returns to;
- whether system configuration survives;
- whether user data survives;
- whether application/container state survives or must be recreated.

### Model identity vs purchasable-unit configuration

The sixth record exposes a different truth problem:

```text
exact marketed model != exact physical configuration
```

Dell documents Wyse 3040 units with both 8 GB and 16 GB eMMC and optional WLAN/Bluetooth under the same marketed model. A second-hand listing saying only `Wyse 3040` therefore does not prove which storage/wireless configuration is being sold.

Future market and matching work should preserve variant-sensitive state rather than silently assigning the most capable known configuration to every unit. Where a capability contract depends on a variant, the candidate should remain conditional until the actual unit configuration is observed.

### Developer execution vs operating-system authority

The seventh record exposes another execution-boundary problem:

```text
custom application execution != administrator/root ownership of the operating system
```

Amazon documents an opt-in ADB path for sideloading and launching custom APKs on Fire TV. That is a real custom-code surface. The evidence gathered for AFTKA does **not** establish root privilege, bootloader access, cold-boot application restart, fully offline operation, or low-level restore media.

Future matching must preserve this distinction. A device can be useful as a sandboxed/application runtime without inheriting the capabilities of a general root Linux host.

## First comparison set is now structurally complete

The low-power registry experiment still has three evidence-backed candidates from three marketed categories:

```text
TP-Link Archer C7 v5      -> router / OpenWrt
Synology DS220+           -> NAS / supported containers
Dell Wyse 3040            -> thin client / conventional Debian
```

The Fire TV record is **not** silently added to that comparison merely because it has 2 GB RAM and Wi-Fi. Its unattended-start behavior, power profile, offline runtime and application lifecycle are still unknown.

This does **not** mean the comparison is complete. Used-market snapshots, common workload measurements, provisioning friction and power/restart evidence still need to be collected before ranking the three current candidates.

## What the first milestone must prove

The target is not "25 cool hacks."

The milestone should answer:

1. Can different device classes be represented in one capability schema?
2. Can we distinguish hardware presence from accessible execution?
3. Can capability contracts find unexpected candidates?
4. Do unexpected candidates remain attractive after recovery, power and friction are counted?
5. Can another human or machine follow the evidence trail without relying on hidden chat memory?

If the answer is no, revise the model rather than forcing the hypothesis to win.

## Discovery rule

> **The marketed category tells us where humans shelved the object. The census records what the machine actually is.**
