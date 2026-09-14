# Evidence Packet — Polestar 2 MY2026 / Sandboxed Infotainment Execution Inside a Safety-Critical Parent System

**Device record:** `devices/polestar/polestar-2-my2026.yaml`  
**Exact scope:** Polestar 2, model year 2026 documentation  
**Checked:** 2026-09-14  
**Local verification:** No  
**Current evidence state:** `DOCUMENTED`

## Why this device matters

This record fills the census's vehicle-infotainment / non-safety-computer gap without treating a road vehicle as a generic embedded computer.

The evidence chain is intentionally narrow:

```text
Polestar 2 MY2026
  -> Polestar documents Android Automotive OS in the software lineage
  -> MY2026 manual exposes Google Play in the vehicle
  -> internet-connected vehicle + linked Google account
  -> only car-adapted apps are offered
  -> eligible third-party application can be downloaded and installed
```

That establishes a real third-party application execution surface.

It does **not** establish authority over the whole vehicle.

```text
Google Play app executes on infotainment
  != shell/root/bootloader
  != CAN access
  != arbitrary vehicle-property access
  != braking / steering / propulsion / safety-system control
```

The new capability-model lesson is therefore **nested authority**: a non-safety execution surface can exist inside a safety-critical parent machine while the parent machine's control authority remains explicitly outside the proven scope.

## Source 1 — Polestar 2 MY2026: downloading apps

Official Polestar MY2026 manual:

- https://www.polestar.com/at/manual/polestar-2/2026/article/d61b349459320b5fc0a8015105e15000/

Checked: 2026-09-14

Polestar documents that when the vehicle is connected to the internet, new applications can be downloaded and installed. The manual directs the user to Google Play and says the store contains applications adapted/optimised for vehicle use.

The documented install flow also establishes these admission conditions:

- the vehicle is stationary / in Comfort mode for downloading apps;
- Google Play must be opened from the vehicle;
- a Google account must be linked to the current user profile;
- only apps adapted for the car are available.

### Execution truth boundary

This is strong evidence for a manufacturer-supported application surface, but it is an **admission-controlled store path**.

The source does not establish:

- APK sideloading on this exact Polestar 2 state;
- ADB;
- shell;
- root;
- bootloader access;
- alternative firmware/OS installation;
- CAN-bus access;
- arbitrary vehicle-property access;
- cold-boot third-party-app autostart;
- indefinite background-service execution;
- AXM local reproduction.

Those remain unknown or explicitly outside the claimed scope.

## Source 2 — Polestar 2 MY2026 software-update history

Official Polestar MY2026 software history:

- https://www.polestar.com/au/manual/polestar-2/2026/software-updates/

Checked: 2026-09-14

Polestar's update history explicitly names Android Automotive OS. In the historical P3.0.3 notes Polestar records Android Automotive OS 12 and an enabler for continued Google Automotive Services and third-party app development.

The same page is also a useful model-year warning. It says update functionality can vary by market, model year and options, and newer release notes distinguish behavior for model year 2025-or-older versus model year 2026-or-newer.

### Software-state truth boundary

The record therefore does **not** assign a current Android major version to every MY2026 physical vehicle from the historical AAOS 12 note.

The evidence supports:

```text
Polestar 2 software lineage
  -> Android Automotive OS
  -> Google Automotive Services / third-party app development support
```

It does not support:

```text
every MY2026 unit today == one exact Android major version
```

The current installed software state of an arbitrary acquired car remains a unit-level fact.

## Source 3 — Android Automotive OS Google Play admission and driving restrictions

Official Android developer documentation:

- https://developer.android.com/training/cars/parked/automotive-os
- https://developer.android.com/training/cars/apps/library/car-hardware-api
- https://developer.android.com/guide/topics/permissions/overview

Checked: 2026-09-14

Android documents that applications opting into Android Automotive OS distribution through Google Play have car-specific form-factor requirements and are reviewed for safety/compatibility.

For parked apps, Android documents a strong driver-distraction boundary: ordinary parked activities cannot be launched or used while UX driving restrictions are active; if restrictions become active while the app is running, the OS obscures/pauses the activity and may stop it depending on compatibility behavior.

Android's car hardware documentation separately shows that vehicle information is exposed through bounded APIs and permissions on supporting vehicles. The general Android permission model also distinguishes signature permissions, which are granted only to appropriately signed/system-authorized applications rather than ordinary third-party apps by default.

### Parent-system safety boundary

These platform documents are used only to keep the scope narrow.

They support the statement that:

> A third-party Android Automotive application runs inside a permission- and driving-policy-constrained application environment.

They do **not** prove which optional car-hardware properties this exact Polestar exposes to a given app, and they do not prove that third-party Play apps can command safety-critical actuators.

The record therefore marks all of the following outside the proven execution scope absent exact-model evidence:

- vehicle motion control;
- braking control;
- steering control;
- propulsion control;
- safety-system control;
- arbitrary vehicle-property read/write;
- CAN-bus access.

This is a capability boundary, not a claim that software vulnerabilities are impossible.

## Source 4 — MY2026 centre-display restart

Official Polestar MY2026 manual:

- https://www.polestar.com/is-is/manual/polestar-2/2026/article/da263fe506b716cec0a8015119c03510/

Checked: 2026-09-14

Polestar documents a restart procedure for the centre display when a function stops working or the system locks:

```text
hold centre-display Home button for 20 seconds
  -> continue holding through the displayed message
  -> release when screen turns black
  -> Polestar 2 logo appears after restart
```

### Recovery truth boundary

This proves a documented **infotainment/display restart**.

It does not prove:

- firmware reflash;
- bootloader recovery;
- rescue partition;
- recovery from failed storage;
- recovery from failed vehicle/infotainment hardware;
- automatic restart of a custom third-party service;
- AXM local reproduction.

The structured recovery path therefore leaves data impact unknown rather than guessing that a restart preserves every form of application state.

## Source 5 — MY2026 factory reset / user-data reset

Official Polestar MY2026 manual:

- https://www.polestar.com/uk/manual/polestar-2/2026/article/96fc5cb24f6b5dbfc0a801514786d063/

Checked: 2026-09-14

Polestar documents:

- app settings can be reset;
- network settings require administrator privilege;
- factory reset requires administrator privilege;
- the owner profile always has administrator privilege;
- all vehicle keys must be inside the car for a factory reset;
- factory reset deletes profiles, user data, connected keys and personal settings.

### Data-impact boundary

The device record models this as a destructive user/profile/settings recovery path.

It intentionally does **not** claim that a factory reset:

- reflashes infotainment firmware;
- repairs a non-booting ECU;
- exposes a bootloader or rescue partition;
- necessarily removes every installed application package.

Polestar lists `app settings` separately from the explicit factory-reset deletion list, so `application_state` remains `unknown` instead of being silently marked erased.

## Compute, RAM and storage boundary

No authoritative exact-MY2026 infotainment SoC, CPU architecture/core count, RAM quantity or writable-storage capacity was collected in this activation.

Android Automotive OS execution does not justify inferring these values from another Polestar model year, a related Volvo implementation, an online parts listing, or generic Android expectations.

They remain `unknown`.

## Locality boundary

The documented app-install path requires:

```text
internet connectivity
+ Google account linked to the current vehicle profile
+ Google Play
```

That establishes a cloud/account dependency for **provisioning this application surface**.

It does not establish that every installed third-party app requires Google cloud connectivity for its own normal runtime logic. Runtime locality remains app-specific and unverified.

## Power and economics boundary

No infotainment-subsystem power measurement was collected.

The record does not transform:

- high-voltage traction-battery capacity;
- charging power;
- whole-vehicle energy consumption;

into a claim about infotainment-computer watts.

Likewise, no used-vehicle market cohort was collected. Treating an embedded infotainment computer as a cheap standalone compute node would hide the overwhelming whole-vehicle acquisition, maintenance, insurance, depreciation and opportunity cost unless the vehicle is already legitimately owned for another purpose.

That opportunity-cost fact is enough to keep the Polestar out of the low-power registry comparison even before a wall-power experiment exists.

## Local verification status

No AXM local verification was performed.

Specifically, AXM did **not**:

- install an application on a physical Polestar 2;
- test Google Play eligibility for a custom AXM package;
- test app permissions;
- test vehicle-property access;
- test driving restrictions;
- test app autostart/background persistence;
- measure power;
- collect acquisition prices;
- restart a physical centre display;
- perform a factory reset.

The strongest state remains `DOCUMENTED`.

## Census lesson

Polestar 2 MY2026 adds a distinction that the earlier appliance records did not fully capture:

```text
safety-critical parent machine
  contains
non-safety application computer

application execution authority
  can be real and useful

without implying
parent-system control authority
```

For future vehicle, industrial, robotics and medical-adjacent research, the repo should preserve **which subsystem a capability belongs to** and should never let a sandboxed subsystem execution claim leak upward into authority over the entire parent machine.

This is one strong vehicle pressure case. Preserve the distinction in the record, but do not freeze a universal parent-system schema until independent hardware demonstrates the same need again.
