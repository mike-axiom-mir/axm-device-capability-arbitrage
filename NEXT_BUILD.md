# Next Build

**Current state:** Initial foundation is in place. Two census records now exercise two very different execution surfaces: a consumer camera with a custom Android application path and a Wi-Fi router with replaceable Linux/OpenWrt firmware.

## Priority 1 — Make the records mechanically checkable

Build the smallest useful validation layer for the v0.1 device schema.

Target:

- YAML parses cleanly;
- required identity/evidence fields exist;
- truth-state values are from the allowed set;
- economics state cannot silently disappear;
- unknown values remain legal;
- evidence source URLs are preserved;
- no scoring requires fields that are still unknown.

Do **not** over-freeze the schema before more device classes challenge it.

## Priority 2 — Expand across genuinely different hardware

Next records should maximize schema pressure rather than collect many similar routers.

Recommended next categories:

1. exact OpenIPC IP camera/model;
2. old Android phone with documented unlock/recovery;
3. Kobo e-reader;
4. Valetudo-supported robot vacuum;
5. ESP8266/ESP32 consumer appliance;
6. container-capable NAS;
7. TV/signage box;
8. thin client / POS terminal.

Each new class should expose something the existing two records do not.

## Priority 3 — Run the first actual arbitrage comparison

The hypothesis is not proven by building a database.

Choose one small real goal, for example:

> **low-power local registry / heartbeat node**

Then compare at least three different product categories against the same capability contract.

Required comparison state:

- used-market snapshot;
- measured or credible power data;
- provisioning friction;
- recovery quality;
- replacement availability;
- workload fit.

Only then ask whether the non-obvious device is actually cheaper/better.

## Near-term experiments

### A. Archer C7 v5

- collect NL/EU used-price samples;
- find credible idle/load power measurements or measure locally later;
- define a tiny registry workload footprint;
- estimate/test whether 128 MB RAM + 16 MB flash is genuinely enough;
- test whether USB storage changes the result positively or only adds fragility.

### B. Sony ILCE-6000

- identify exact SoC/architecture from model-specific evidence;
- identify RAM from reliable evidence;
- map PlayMemories API access to sensor, network, storage and audio;
- document recovery/version constraints;
- collect used-price snapshot;
- decide which non-camera roles are actually rational rather than merely possible.

## Stop conditions

Do not expand the census blindly if:

- records keep requiring exceptions the schema cannot represent;
- evidence quality is too weak to compare devices;
- cost data cannot be time/region scoped;
- a scoring system starts hiding unknowns;
- product category begins acting as an implicit capability claim.

When one of those occurs, repair the model before adding volume.

## Root gate

**Truth:** no fake verification.  
**Agency / non-domination:** owned/authorized hardware only.  
**Continuity:** evidence and recovery live in repo state.  
**Wisdom before speed:** prove the comparison before scaling the catalogue.
