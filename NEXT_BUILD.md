# Next Build

**Current state:** Initial foundation is in place. Seven census records now exercise seven materially different hardware/execution patterns: a consumer camera with a custom Android application path, a Wi-Fi router with replaceable Linux/OpenWrt firmware, an e-reader with native application/script execution, a mobile robot with rooted Linux/SSH plus local-only control, a NAS with a manufacturer-supported container runtime plus native persistent storage, a thin client with conventional Debian/OpenWrt execution plus PC-class UEFI boot controls, and a media stick with manufacturer-supported Android APK sideloading through opt-in ADB but no evidence of root ownership. The S5 exposed recovery-by-device-state; the DS220+ added recovery data-impact semantics; the Wyse 3040 exposed configuration identity as a separate problem because one marketed model spans multiple eMMC and wireless configurations; the Fire TV AFTKA now shows that real custom application execution must remain distinct from administrator/root authority. A small structural validator and GitHub Actions workflow protect the machine-readable records without freezing the research schema too early.

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
- GitHub Actions validation on pushes to `main` and pull requests.

The validator deliberately does **not** reject unknown capability values or enforce a large rigid schema. New hardware classes still need room to challenge v0.1.

## Priority 1 — Run the first actual arbitrage comparison

The hypothesis is not proven by building a database. The three-category candidate set now exists for the current capability contract:

> **low-power local registry / heartbeat node**

Current candidates:

- TP-Link Archer C7 v5 — router / OpenWrt; tiny RAM/flash; strong network role and TFTP recovery;
- Synology DS220+ — NAS / supported containers; much larger storage/compute platform with manufacturer power data but drive and opportunity cost;
- Dell Wyse 3040 — thin client / full Debian; 2 GB RAM, internal eMMC, Gigabit Ethernet, UEFI USB recovery, configurable AC Recovery and a manufacturer sub-4-W claim.

Do **not** rank them yet. The next valuable step is to collect the same missing evidence for all three so unknowns are not converted into fake scores.

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

### Configuration-identity rule learned from the Wyse 3040

A product model can remain exact while still spanning materially different unit configurations.

For Wyse 3040, Dell documents:

```text
same marketed model
  -> 8 GB or 16 GB eMMC
  -> optional WLAN/Bluetooth
```

Market research and matching must therefore preserve observed unit configuration when it matters. A listing containing only a model name must not inherit the best-known storage/radio variant silently.

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

## Priority 2 — Continue census expansion across genuinely different hardware

Next records should maximize schema pressure rather than collect more routers, NAS boxes, robot vacuums, conventional thin clients or Android media sticks.

Recommended next categories:

1. exact OpenIPC IP camera/model;
2. old Android phone with documented unlock/recovery;
3. ESP8266/ESP32 consumer appliance;
4. printer/MFP with an application or embedded Linux/Android execution layer;
5. console/handheld gaming device with a supported homebrew/Linux path;
6. industrial/commercial surplus hardware with non-PC market positioning;
7. non-safety vehicle/infotainment computer only where the execution boundary is clearly separated from safety-critical systems;
8. oddball appliance where a different execution/recovery/locality pattern challenges the current schema.

Each new class should expose something the existing seven records do not.

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
- treat permanent loss of stock state as setup/recovery cost rather than hiding it.

### F. Fire TV Stick 4K Max 1st Gen / AFTKA

- if an owned unit becomes available, preserve its exact build model and Fire OS version before testing;
- locally verify ADB authorization, APK sideload and removal without assuming root;
- test whether a deliberately local APK works with WAN disconnected after stock provisioning;
- test cold power loss -> Fire OS -> application/service lifecycle rather than assuming auto-start;
- measure wall power at boot, idle, local-app active and media-active states;
- verify factory reset on noncritical state and document exactly what application data survives, if anything;
- collect a dated NL/EU used-market sample only after exact-generation identity can be distinguished from 2nd Gen listings.

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
- an application/developer execution surface is silently promoted to root or unrestricted operating-system authority.

When one of those occurs, repair the model before adding volume.

## Root gate

**Truth:** no fake verification, silent best-variant inheritance or privilege inflation.  
**Agency / non-domination:** owned/authorized hardware only; consent-visible developer access stays consent-visible.  
**Continuity:** evidence, variant caveats, execution boundaries and recovery live in repo state.  
**Wisdom before speed:** compare common evidence before ranking hardware or promoting a device into a workload it has not yet earned.
