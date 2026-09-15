# Evidence Packet — Critter & Guitari Organelle S2 / Open Patch Platform and Removable Root Disk

**Device record:** `devices/critter-and-guitari/organelle-s2.yaml`  
**Exact scope:** Critter & Guitari Organelle S2  
**Checked:** 2026-09-15  
**Local verification:** No  
**Current evidence state:** `DOCUMENTED`

## Why this device matters

The Organelle S2 adds a genuinely different hardware class to the census: a programmable musical instrument / audio processor whose manufacturer openly documents the machine as a Linux microcomputer and user-programmable patch platform.

Its strongest new model pressure is not merely "Linux inside a synthesizer." The operating system and user patch state live on a removable microSD root disk, and Critter & Guitari documents a recovery method that is destructive to the selected card while also explicitly allowing a new card to be used so the previous OS medium can be retained.

That creates a useful continuity distinction:

```text
restore target is destructively re-imaged
  !=
previous boot state must be destroyed
```

The record also keeps console/compile access separate from root privilege. The official programming documentation provides real coding and build surfaces, but the cited material does not establish root, sudo, bootloader authority or unattended custom-service persistence.

## Source 1 — Official Organelle product specification

Official Critter & Guitari product page:

- https://critterandguitari.com/products/organelle-m

Checked: 2026-09-15

The current Organelle page presents the Organelle S2 and documents:

- a 1.8 GHz quad-core 64-bit ARM Cortex-A53 processor;
- 1 GB RAM;
- a Linux operating system;
- an installed 8 GB microSD card split into approximately 4 GB for the OS and 4 GB for patches/files;
- stereo audio input and output;
- an electret microphone;
- MIDI input/output;
- two USB 2.0 Type-A host ports with MIDI-over-USB and serial-over-USB support;
- HDMI output;
- footswitch input;
- 9 VDC / 1.0 A power requirement.

### Hardware truth boundary

These are manufacturer platform specifications for the current Organelle S2 product presentation.

They do **not** establish:

- the exact SoC part number;
- free RAM or writable storage on a particular acquired unit;
- root or bootloader authority;
- measured idle/active wall power;
- unattended restart behavior;
- NL/EU used-market value;
- AXM local reproduction.

The 9 VDC / 1.0 A figure is a supply requirement. It is not converted into a self-consumption measurement.

## Source 2 — Official Organelle M / S / S2 manual: programmable Linux platform

Official manual:

- https://docs.critterandguitari.com/Organelle/og_sms2/

The currently published documentation is the Organelle M / S / S2 manual and identifies the current OS line as Organelle OS 5.1 in 2026.

The manual describes the Organelle as a modern microcomputer running Linux and an open-source platform. It says users can create their own patches and identifies Pure Data as the environment used by most patches.

The same manual says the microSD card acts as the internal microcomputer's **root disk**. The operating system lives there, while the card also stores patches. On normal power-up the Organelle boots to its menu and can load patches from microSD or USB storage.

### Execution truth boundary

This is sufficient for a manufacturer-supported user-programmable execution surface.

It does **not** establish:

- root privilege;
- sudo availability;
- unrestricted package-manager authority;
- arbitrary bootloader access;
- cold-boot autostart of arbitrary user services;
- persistence of every user modification across OS updates;
- AXM local reproduction.

The device record therefore marks custom patch execution as `DOCUMENTED` while leaving privilege `unknown`.

## Source 3 — Official programming guide: console and compilation

Official programming documentation:

- https://docs.critterandguitari.com/Organelle/organelle_programming/

Critter & Guitari documents a Web editor with two relevant controls:

- **Compile** runs a patch-local `compile.sh`; the guide explicitly says build steps for a Pd external or other source file can be placed there;
- **Terminal** switches to a console and is described as giving low-level access for users who prefer to code that way.

The same documentation describes a VNC workflow for viewing/controlling the Organelle desktop from another computer on the same local Wi-Fi network.

### Console truth boundary

This proves a real manufacturer-supported console/build surface.

It does **not** prove:

- root;
- sudo;
- kernel or bootloader authority;
- arbitrary remote access without owner configuration;
- automatic service startup after reboot/power loss;
- general-purpose server suitability.

That distinction matters because "console access" should not silently become "administrator-owned Linux" when the documentation does not establish the privilege level.

## Source 4 — Official microSD factory restore

The same M / S / S2 manual documents **Burning SD Card Disk Image**.

It says:

- the microSD card stores both the Organelle OS and patches;
- burning a new image resets the Organelle to factory state;
- the operation completely wipes the selected microSD card;
- files that matter should be backed up first;
- a brand-new card can instead be used if the owner wants to keep the old OS available;
- the current M/S/S2 image requires an 8 GB or larger microSD card.

### Recovery truth boundary

The target card's data impact is clear enough to record as destructive:

```text
system configuration -> erased on target card
user patch/file state -> erased on target card
application/patch state -> erased on target card
```

But the documented alternate-medium path changes the continuity story:

```text
old root disk retained physically
  +
new card receives factory image
  -> factory-state boot medium can be created without overwriting the old card
```

This does **not** prove automatic rollback, dual-boot, or recovery from mainboard, power, bootloader, connector, or physical microSD-slot failure. No such claims are made.

The device record stores the alternate-medium facts locally on the structured recovery path rather than freezing a new universal schema after one pressure case.

## Source 5 — Stand-alone/local basic operation

Official manual:

- https://docs.critterandguitari.com/Organelle/og_sms2/

The manual describes the Organelle as a fully capable stand-alone instrument. Normal locally stored patch operation uses the device's own microSD/USB patch storage, controls and audio interfaces. Wi-Fi appears as an optional connected state rather than a prerequisite for normal instrument boot/play.

### Locality truth boundary

That is sufficient to say a vendor cloud is **not required for basic locally stored patch operation**.

It does **not** establish that:

- every third-party patch is offline-independent;
- every patch/download source is locally available;
- OS update acquisition is fully offline;
- every network-facing workflow is vendor-service independent.

The device record therefore preserves the narrow basic-operation claim instead of declaring every possible workload cloud-free.

## Power boundary

No independent or AXM-local Organelle S2 self-consumption measurement was collected.

Do not convert:

```text
9 VDC x 1.0 A supply requirement
```

into an idle, average or workload watt figure.

Idle watts, active watts, always-on suitability and comparable registry-workload power remain unknown.

## Economics boundary

No dated NL/EU acquisition cohort was collected in this activation.

The record therefore keeps:

- used price unknown;
- new market value uncollected;
- adapter/storage cost unknown;
- replacement availability unknown;
- setup time unknown;
- `market_data_state: not_collected`.

A current manufacturer shop price, even if visible, would be one displayed retail price rather than a reusable acquisition cohort and is therefore not promoted into device truth.

## Local verification status

No AXM local verification was performed.

AXM did **not**:

- boot a physical Organelle S2;
- inspect an exact hardware revision;
- create or execute a local test patch;
- inspect console privilege;
- compile a local source artifact;
- test VNC/Web access;
- re-image a microSD card;
- verify boot from a fresh replacement card;
- test retention/rollback using the old card;
- test hard power loss or unattended restart;
- measure wall power;
- collect acquisition prices.

The strongest evidence state remains `DOCUMENTED`.

## Census lesson

The Organelle S2 adds two useful boundaries.

First:

```text
manufacturer-supported console + compile workflow
  !=
root / sudo / bootloader ownership
```

Second:

```text
destructive factory restore of selected removable root disk
  !=
irreversible destruction of the previously retained boot medium
```

The second distinction may matter later for continuity/recovery scoring: a system whose root state lives on cheap removable media can have a destructive restore procedure while still allowing the operator to preserve the prior medium untouched.

One device is enough to record that pressure, not enough to freeze a universal removable-root-disk schema.

## Root check

**Truth:** hardware, execution, locality and recovery claims stay within exact manufacturer documentation; privilege, power, market value and local reproduction remain unknown where unproven.  
**Agency / non-domination:** the documented programming and recovery paths are owner-visible manufacturer features; no exploit or hidden persistence is used.  
**Continuity:** source URLs, destructive target-media impact and the documented option to retain the previous root disk are preserved in repo state.  
**Wisdom before speed:** a musical instrument is not treated as a cheap server merely because Linux and a console exist; power, restart behavior, opportunity cost and workload fit remain unverified.
