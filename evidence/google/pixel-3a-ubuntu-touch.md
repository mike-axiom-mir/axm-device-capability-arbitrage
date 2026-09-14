# Evidence Packet — Google Pixel 3a (`sargo`) / Ubuntu Touch

**Device record:** `devices/google/pixel-3a-sargo.yaml`  
**Checked:** 2026-09-14  
**Local verification:** No  
**Current evidence state:** `COMMUNITY_VERIFIED`

## Why this device matters

The Pixel 3a is the first phone/handheld record in the census. It adds a capability pattern that the first nine devices do not capture:

```text
same marketed model
  -> one acquisition variant permits bootloader unlock
  -> another carrier variant can block the replacement-OS path entirely
```

UBports currently supports Google Pixel 3a (`sargo`) with Ubuntu Touch, but its exact-device install instructions explicitly say the **Verizon model must not be used because its bootloader cannot be unlocked**.

That makes acquisition identity part of capability truth. A market listing that merely says `Pixel 3a` does not prove that the purchasable unit can satisfy a replacement-OS execution contract.

## Source 1 — Google Pixel 3a hardware specification

Manufacturer source:

- https://support.google.com/pixelphone/answer/16043605?hl=en

Checked: 2026-09-14

Google's Pixel hardware specification documents Pixel 3a with:

- Qualcomm Snapdragon 670;
- 64-bit octa-core CPU;
- Adreno 615 GPU;
- 4 GB LPDDR4x RAM;
- 64 GB internal storage;
- 5.6-inch 2220×1080 OLED display.

This establishes the baseline compute/memory/display facts in the record.

It does **not** establish Ubuntu Touch compatibility, bootloader unlockability for every carrier variant, wall-power draw, battery health, or unattended service behavior.

## Source 2 — Exact-device Ubuntu Touch support

Exact-device source:

- https://devices.ubuntu-touch.io/device/sargo/release/noble/

Checked: 2026-09-14

UBports identifies the device as:

```text
Google Pixel 3a
codename: sargo
port base: Halium 9.0
installer: supported
support state: Full community support
```

At the check date the page lists an Ubuntu Touch 24.04 `noble` stable channel (`24.04-1.4`, released 2026-07-13), plus newer RC/daily channels.

The exact-device feature table marks working support for core areas including:

- boot into UI;
- Wi-Fi;
- Bluetooth;
- NFC;
- cellular data;
- cameras;
- touchscreen and common sensors;
- ADB access;
- recovery image;
- reset to factory defaults;
- charging and normal shutdown/reboot.

UBports also preserves known limitations rather than presenting the port as perfect. In particular, VoLTE is a global/partial issue and carrier/region dependent.

### Installation gate

UBports' Pixel 3a instructions require:

1. an unlocked bootloader;
2. the correct Android base before installation;
3. **not** using the Verizon model, because that model does not allow the bootloader to be unlocked;
4. if the device is above Android 9, reverting to factory image `PQ3B.190801.002` first.

This is the most important finding in this activation.

The capability supply is not:

```text
all Pixel 3a units
```

It is closer to:

```text
Pixel 3a / sargo
AND bootloader-unlockable acquisition variant
AND correct install baseline
```

A cheap locked unit is therefore not interchangeable with an unlockable one for this execution contract.

## Source 3 — Ubuntu Touch custom-code surface

Platform sources:

- https://docs.ubports.com/en/latest/appdev/
- https://docs.ubports.com/en/latest/userguide/advanceduse/
- https://docs.ubports.com/en/latest/appdev/guides/writeable-dirs.html

UBports documents user-built Ubuntu Touch applications and the Clickable workflow. Native application backends may use C++, Python, Go, Rust or JavaScript.

UBports also documents shell access through ADB/SSH and local terminal workflows.

The security boundary matters: normal Ubuntu Touch applications are confined, and some advanced operations that make the system image writable can weaken security or interfere with OTA updates.

The record therefore supports real native custom-code and shell capability without silently converting that into unrestricted persistent root.

## Source 4 — Google factory-image recovery

Manufacturer source:

- https://developers.google.com/android/images

Checked: 2026-09-14

Google documents factory images for Nexus and Pixel devices as a way to restore the device to original factory firmware after custom builds.

Google explicitly warns that:

- installing a factory image erases device data;
- unlocking the bootloader reduces security;
- the bootloader should be relocked after factory-image use when appropriate;
- full OTA images are normally safer/easier when they fit the recovery situation.

For this record the important transition is:

```text
bootloader-unlockable Pixel 3a
  + Ubuntu Touch/custom build
  -> Google factory-image restore
  -> stock Android factory firmware
  -> system/user/application state erased/recreated
```

This is a real documented return-to-stock path for the evaluated custom-OS-capable state.

It does **not** prove recovery from failed flash hardware, physical damage, every bootloader corruption state, or a locked carrier unit that never entered the custom-OS state.

## New schema pressure — acquisition-variant-gated execution

Earlier records already showed that one marketed model can contain different storage, radio, or sensor configurations.

Pixel 3a adds a more consequential variation:

```text
variant difference
  -> can change whether the primary execution surface is obtainable at all
```

For a future market snapshot this means that these observations must not be merged blindly:

```text
Pixel 3a, carrier/origin unknown
Pixel 3a, verified bootloader-unlockable
Pixel 3a, Verizon / bootloader locked
```

They are not equivalent capability supply even if the hardware name and asking price look identical.

A later schema extension may need a generic way to model acquisition-time capability gates. This single record is evidence for the problem, not enough reason by itself to freeze a new universal structure.

## Power and economics truth boundary

No AXM power measurement was performed.

The phone has a 3000 mAh battery according to the exact-device UBports data, but battery capacity is not a wall-power measurement and says nothing about the condition of a used battery.

No dated NL/EU used-market sample was collected. UBports' approximate device-price label is not converted into a market observation.

Current unknowns therefore include:

- idle/active wall power;
- battery health and wear on used units;
- always-on charging behavior;
- replacement availability by unlockable/locked variant;
- current NL/EU price distribution;
- setup time;
- hard-power-loss recovery;
- background service/autostart behavior.

## Candidate roles

Evidence supports further testing for:

- battery-backed local field node;
- human-machine terminal;
- mobile sensor gateway;
- offline/local application host.

The record does **not** yet justify calling the phone a good always-on registry node. Unattended boot, background-service behavior, battery aging, charging policy and measured power all remain unresolved.

## Next falsifiable tests

1. Collect a dated NL/EU Pixel 3a market sample that records carrier/origin or verified bootloader unlockability where listings provide it.
2. Do not treat unknown-origin units as unlockable by default.
3. On an owned/authorized non-Verizon unit, preserve exact stock build, bootloader state and device identity before modification.
4. Reproduce the UBports Installer path from the documented Android 9 baseline and preserve tool/image hashes.
5. Verify native app execution plus ADB/SSH shell without promoting normal app authority to root.
6. Test WAN-disconnected local operation for one deliberately local application.
7. Test hard power loss -> boot -> Wi-Fi -> chosen service/application recovery.
8. Restore stock Android with the documented Google factory-image path on noncritical data and preserve a recovery receipt.
9. Measure wall power and battery behavior only after a specific always-on/mobile workload is defined.

## Root gate

**Truth:** the current Ubuntu Touch path is exact-device evidence, while local verification, power, market price and unattended behavior remain unknown.  
**Agency / non-domination:** bootloader unlock and OS replacement apply only to owned/authorized devices and retain the user's visible choice; no lock bypass is claimed.  
**Continuity:** the exact `sargo` target, Android baseline, Verizon exclusion, source URLs and destructive recovery semantics are stored in repository state.  
**Wisdom before speed:** a cheap listing is not counted as equivalent capability supply until the unit's unlockability gate is known, and the phone is not ranked as infrastructure before power/autostart/battery evidence exists.
