# Next Build

**Current state:** Initial foundation is in place. Five census records now exercise five materially different hardware/execution patterns: a consumer camera with a custom Android application path, a Wi-Fi router with replaceable Linux/OpenWrt firmware, an e-reader with native application/script execution, a mobile robot with rooted Linux/SSH plus local-only control, and a NAS with a manufacturer-supported container runtime plus native persistent storage. The S5 exposed recovery-by-device-state; the DS220+ adds a second recovery dimension by showing that two valid recovery paths can have very different configuration/data impact. A small structural validator and GitHub Actions workflow protect the machine-readable records without freezing the research schema too early.

## Completed foundation step — Mechanical record checks

Implemented:

- YAML parsing for device and capability-contract records;
- required identity/evidence fields;
- allowed truth-state validation;
- explicit economics state;
- duplicate record/contract ID detection;
- execution-surface structure checks;
- recovery/evidence state checks;
- GitHub Actions validation on pushes to `main` and pull requests.

The validator deliberately does **not** reject unknown capability values or enforce a large rigid schema. New hardware classes still need room to challenge v0.1.

## Priority 1 — Expand across genuinely different hardware

Next records should maximize schema pressure rather than collect many similar routers, robot vacuums or NAS devices.

Recommended next categories:

1. exact OpenIPC IP camera/model;
2. old Android phone with documented unlock/recovery;
3. ESP8266/ESP32 consumer appliance;
4. TV/signage box;
5. thin client / POS terminal;
6. printer/MFP with an application or embedded Linux/Android execution layer;
7. console/handheld gaming device with a supported homebrew/Linux path;
8. non-safety vehicle/infotainment computer only where the execution boundary is clearly separated from safety-critical systems.

Each new class should expose something the existing five records do not.

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

Do not let `recovery_path: true` hide whether state, configuration or user data survives. A later schema revision should probably represent recovery operations as structured paths with precondition/state, target state and data impact, but do not freeze that shape until more devices pressure it.

## Priority 2 — Run the first actual arbitrage comparison

The hypothesis is not proven by building a database.

Use the existing capability contract:

> **low-power local registry / heartbeat node**

The comparison now has two promising but very different anchored candidates:

- TP-Link Archer C7 v5 — cheap-network-appliance hypothesis, tiny RAM/flash, strong OpenWrt recovery;
- Synology DS220+ — larger supported container/storage platform, manufacturer power data, but likely higher acquisition/storage opportunity cost.

The third comparison target should ideally be a **thin client / POS terminal**, not another router or NAS, so the first real arbitrage test spans three marketed categories.

Required comparison state:

- used-market snapshot in one region/date window;
- measured or credible power data with source class;
- provisioning friction;
- recovery quality **and data impact**;
- replacement availability;
- workload fit;
- required storage/adapters counted separately from chassis price.

Only then ask whether the non-obvious device is actually cheaper/better.

The Roborock S5 should not be assumed to be a good registry node merely because root SSH exists. Its irreversibility, mobile-actuator coupling and original appliance value are real costs that may make it a poor arbitrage choice despite technical capability.

Likewise, the DS220+ should not automatically win because it is much more capable than the Archer C7. If the workload needs only a tiny registry, drive cost and unused NAS capability may make it economically irrational.

## Priority 3 — Add scoring only after comparison data exists

Do not invent a universal device score yet.

Once several real records contain cost, recovery and workload evidence, introduce only the smallest scoring model needed to answer a concrete capability contract. Unknowns must remain visible and must not be converted into neutral-looking numeric values.

## Near-term experiments

### A. Archer C7 v5

- collect NL/EU used-price samples;
- find credible idle/load power measurements or measure locally later;
- define a tiny registry workload footprint;
- estimate/test whether 128 MB RAM + 16 MB flash is genuinely enough;
- test whether USB storage changes the result positively or only adds fragility.

### B. Synology DS220+

- collect NL/EU bare-chassis used-price samples separately from units sold with drives;
- price a minimal supported storage configuration so required drive cost is visible;
- verify a currently compatible Container Manager release on owned hardware;
- measure a tiny registry container's RAM/CPU/storage footprint;
- measure wall power with drives active, idle and hibernated and compare with Synology's manufacturer figures;
- test power loss -> Power Recovery -> DSM -> container restart behavior;
- test Mode 2 recovery on noncritical data and preserve which application/container state must be rebuilt.

### C. Sony ILCE-6000

- identify exact SoC/architecture from model-specific evidence;
- identify RAM from reliable evidence;
- map PlayMemories API access to sensor, network, storage and audio;
- document recovery/version constraints;
- collect used-price snapshot;
- decide which non-camera roles are actually rational rather than merely possible.

### D. Roborock S5

- collect an NL/EU used-price sample;
- collect credible idle-on-dock / charging / cleaning power data or measure locally;
- verify exact production/recovery firmware before any local modification test;
- enumerate actual S5 Valetudo capabilities rather than inheriting every generic integration feature;
- treat permanent loss of stock state as setup/recovery cost rather than hiding it.

## Stop conditions

Do not expand the census blindly if:

- records keep requiring exceptions the schema cannot represent;
- evidence quality is too weak to compare devices;
- cost data cannot be time/region scoped;
- a scoring system starts hiding unknowns;
- product category begins acting as an implicit capability claim;
- recovery claims stop identifying which device state they apply to;
- recovery claims hide configuration/data destruction behind a single positive boolean.

When one of those occurs, repair the model before adding volume.

## Root gate

**Truth:** no fake verification.  
**Agency / non-domination:** owned/authorized hardware only.  
**Continuity:** evidence and recovery live in repo state.  
**Wisdom before speed:** prove the comparison before scaling the catalogue.
