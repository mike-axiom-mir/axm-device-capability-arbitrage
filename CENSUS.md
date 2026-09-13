# Device Capability Census

**Milestone 01:** 25 evidence-backed devices across at least 8 marketed categories.

Current grounded count:

```text
Devices:    5 / 25
Categories: 5 / 8
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

## Category coverage

- [x] Consumer camera
- [x] Router / access point
- [ ] IP camera / NVR
- [ ] Phone / tablet / handheld terminal
- [ ] Smart-home / microcontroller appliance
- [ ] Media / TV / signage hardware
- [x] NAS / storage appliance
- [x] Robot / autonomous appliance
- [x] E-reader / e-ink device
- [ ] Printer / office appliance
- [ ] Console / handheld gaming device
- [ ] Thin client / POS / kiosk
- [ ] Industrial / commercial surplus
- [ ] Vehicle infotainment / non-safety computer
- [ ] Other / unknown category

Only eight categories are required for Milestone 01, but the search should not stop there.

## High-value next research queue

These are research targets, **not capability claims**.

1. One OpenIPC-supported IP camera with an exact SoC/model mapping.
2. One old Android phone with unlock/recovery and offline operation.
3. One ESP8266/ESP32 consumer appliance with replaceable local firmware.
4. One Android TV box or digital-signage device with clean local runtime.
5. One discarded thin client / POS terminal with conventional Linux support.
6. One printer/MFP that supports applications or an embedded Linux/Android execution layer.
7. One non-safety vehicle/infotainment computer with a documented application execution path.
8. One console/handheld gaming device with a supported homebrew or Linux execution surface.
9. One oddball appliance or retired commercial device where the execution surface is materially more useful than the marketed category suggests.
10. One additional NAS only if it exposes a materially different execution/recovery/storage pattern from the DS220+.

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
