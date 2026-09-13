# Device Capability Census

**Milestone 01:** 25 evidence-backed devices across at least 8 marketed categories.

Current grounded count:

```text
Devices:    1 / 25
Categories: 1 / 8
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

## Category coverage

- [x] Consumer camera
- [ ] Router / access point
- [ ] IP camera / NVR
- [ ] Phone / tablet / handheld terminal
- [ ] Smart-home / microcontroller appliance
- [ ] Media / TV / signage hardware
- [ ] NAS / storage appliance
- [ ] Robot / autonomous appliance
- [ ] E-reader / e-ink device
- [ ] Printer / office appliance
- [ ] Console / handheld gaming device
- [ ] Thin client / POS / kiosk
- [ ] Industrial / commercial surplus
- [ ] Vehicle infotainment / non-safety computer
- [ ] Other / unknown category

Only eight categories are required for Milestone 01, but the search should not stop there.

## High-value next research queue

These are research targets, **not capability claims**.

1. One common OpenWrt-supported used router with strong recovery documentation.
2. One OpenIPC-supported IP camera with an exact SoC/model mapping.
3. One old Android phone with unlock/recovery and offline operation.
4. One Kobo e-reader with a documented local execution path.
5. One Valetudo-supported robot vacuum with exact rooting/recovery evidence.
6. One ESP8266/ESP32 consumer appliance with replaceable local firmware.
7. One Synology/QNAP-class NAS with supported container execution.
8. One Android TV box or digital-signage device with clean local runtime.
9. One discarded thin client / POS terminal with conventional Linux support.
10. One printer/MFP that supports applications or an embedded Linux/Android execution layer.

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
