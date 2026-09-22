# AXM Device Capability Arbitrage

> **Human markets price products. Machines consume capabilities.**

AXM Device Capability Arbitrage is a research project for finding, describing, and comparing the **real computational capabilities** hidden inside ordinary consumer, embedded, discarded, and surplus hardware.

The core idea is simple:

> **Search by required capability, not by product category.**

A device sold as a camera, router, printer, robot vacuum, e-reader, TV box, NAS, access point, smart plug, thin client, or something else may contain a useful execution surface that has little to do with the way the product is marketed to humans.

The aim is not to force every device to do everything. The aim is to discover the **smallest, cheapest, safest, most recoverable set of verified capabilities capable of satisfying a goal**.

## Why this exists

Hardware is usually searched for through human product categories:

- need a server → buy a server;
- need compute → buy a PC;
- need a network node → buy networking hardware;
- need a sensor node → buy a purpose-built sensor platform.

But many products already contain combinations of:

- CPU / SoC compute;
- RAM;
- persistent storage;
- Linux, Android, RTOS, browser, VM, scripting, or firmware execution surfaces;
- Ethernet, Wi-Fi, Bluetooth, USB, serial, or other connectivity;
- cameras, microphones, lidar, buttons, relays, motors, LEDs, and other I/O;
- recovery modes, bootloaders, replaceable firmware, removable storage, or factory-reset paths.

The market price of those products is influenced by brand, popularity, age, fashion, original purpose, convenience, and demand. That can create a gap between **what humans think an object is worth** and **what its capabilities are worth for a machine task**.

That gap is what this repo studies.

## Capability arbitrage

**Capability arbitrage** is the practice of matching a machine goal to underpriced hardware whose verified capabilities satisfy the goal, even when that hardware was originally sold for something unrelated.

The important unit is not the product category. It is the capability contract.

A goal might require only:

```text
persistent state
+ local networking
+ custom code execution
+ unattended boot
+ < 10 W
+ recoverable failure path
```

If an old router satisfies that contract better and more cheaply than a mini PC, the router is the better candidate for that goal.

If three tiny devices satisfy the contract more cheaply or robustly than one large device, the solution may be a **capability composition** rather than a single machine.

## What counts as evidence

This repo must distinguish possibility from proof.

Do **not** infer arbitrary code execution from specifications alone.

A useful evidence ladder is:

1. manufacturer-supported application execution;
2. supported scripting or plugin execution;
3. verified third-party package execution;
4. verified custom binary execution;
5. administrator/root-level execution;
6. replaceable firmware;
7. bootloader or bare-metal control.

Each device record should preserve, where known:

- exact model and hardware revision;
- firmware / OS version;
- architecture;
- RAM and storage;
- execution method;
- privilege level;
- networking and I/O;
- power profile;
- recovery method;
- brick/failure risk;
- evidence source;
- verification date;
- whether evidence is externally documented or locally reproduced.

Suggested truth states:

```text
UNRESEARCHED
DOCUMENTED
COMMUNITY_VERIFIED
LOCALLY_VERIFIED
REPRODUCIBLE
DEPRECATED
CONTRADICTED
```

## Total useful cost

Purchase price is not enough.

```text
TOTAL USEFUL COST =
    purchase price
  + required adapters
  + storage upgrades
  + unlocking/provisioning effort
  + expected electricity
  + maintenance burden
  + failure risk
  + replacement difficulty
```

A €5 device that requires twelve hours of fragile reverse engineering may be a worse choice than a €20 device that boots open Linux immediately.

The project should therefore track both **money cost** and **friction cost**.

## Goal-first selection

The intended research flow is:

```text
GOAL
  ↓
MINIMUM CAPABILITY CONTRACT
  ↓
CANDIDATE HARDWARE ACROSS ALL PRODUCT CATEGORIES
  ↓
EXECUTION + RECOVERY EVIDENCE
  ↓
TOTAL USEFUL COST
  ↓
ROLE / COMPOSITION MATCH
  ↓
TEST
  ↓
KEEP, REJECT, OR REVISE
```

## Candidate device classes

The census should intentionally search across categories such as:

- routers, access points, repeaters, modems, firewall appliances;
- IP cameras, action cameras, mirrorless cameras, DVRs/NVRs, dashcams;
- old phones, tablets, rugged handhelds, barcode terminals;
- smart plugs, hubs, relays, thermostats, bulbs, sensor gateways;
- TV boxes, smart TVs, projectors, digital signage players, smart speakers;
- NAS and backup appliances;
- robot vacuums and other consumer robots;
- e-readers and e-ink devices;
- printers, scanners, conference systems;
- old consoles and handhelds;
- infotainment and non-safety vehicle computers;
- thin clients, POS systems, kiosks, industrial gateways;
- anything in e-waste with an SoC, flash, firmware update path, network/USB/serial interface, or recoverable boot process.

Product labels are discovery hints, not technical boundaries.

## Potential AXM node roles

A device does not need to host an entire stack to be useful.

Possible roles include:

- registry node;
- identity node;
- state mirror;
- heartbeat / watchdog;
- local cache;
- file relay;
- deterministic worker;
- verifier;
- scheduler;
- mesh relay;
- sensor collector;
- actuator bridge;
- logging / provenance node;
- backup / recovery node;
- local API bridge;
- game/server node;
- lightweight simulation node;
- inference node;
- offline data courier.

The better question is therefore not:

> Can this device run AXM?

but:

> **Which capabilities can this device safely and usefully host?**

## First research milestone

Do not try to catalogue the entire world first.

Initial target:

> **25 evidence-backed devices across at least 8 marketed categories.**

For each device, capture enough data to compare real capability, real cost, real friction, and real recovery.

Then test whether capability-first ranking exposes candidates that conventional product-category shopping would miss.

Track progress in [`CENSUS.md`](CENSUS.md).

## Repository direction

Current working structure:

```text
/
├── README.md
├── FOUNDATION.md
├── RESEARCH_METHOD.md
├── CAPABILITY_SCHEMA.md
├── COST_MODEL.md
├── EVIDENCE_STANDARD.md
├── SAFETY_AND_RECOVERY.md
├── CENSUS.md
├── NEXT_BUILD.md
├── research/
├── devices/
├── capability_contracts/
├── evidence/
├── scoring/
├── tools/
└── experiments/
```

The structure should grow only when evidence or use requires it.

## Working research layers

- [`FOUNDATION.md`](FOUNDATION.md) — protects the central hypothesis and root boundary.
- [`RESEARCH_METHOD.md`](RESEARCH_METHOD.md) — discovery → execution surface → evidence → recovery → cost → role mapping.
- [`CAPABILITY_SCHEMA.md`](CAPABILITY_SCHEMA.md) — v0.1 device-record semantics and unknown discipline.
- [`EVIDENCE_STANDARD.md`](EVIDENCE_STANDARD.md) — truth states, source integrity, local verification and contradictions.
- [`COST_MODEL.md`](COST_MODEL.md) — total useful cost instead of sticker-price ranking.
- [`SAFETY_AND_RECOVERY.md`](SAFETY_AND_RECOVERY.md) — modification depth, authorization and recovery boundaries.
- [`research/RESEARCH_SEED_v0.1.md`](research/RESEARCH_SEED_v0.1.md) — preserved origin direction before the split.
- [`research/MF800_MODEM_THING_ARBITRAGE_CASE.md`](research/MF800_MODEM_THING_ARBITRAGE_CASE.md) — external reference case for integrated-substrate arbitrage: a cheap 4G hotspot reused as the compute/radio/battery foundation of a Linux handheld, with its adaptation costs and unresolved boundaries preserved.
- [`NEXT_BUILD.md`](NEXT_BUILD.md) — grounded next-build priorities and stop conditions.

## Current census records

### Sony ILCE-6000 / α6000 — consumer camera

- [`devices/sony/ilce-6000.yaml`](devices/sony/ilce-6000.yaml)
- [`evidence/sony/ilce-6000-doom.md`](evidence/sony/ilce-6000-doom.md)

The record deliberately leaves SoC, RAM, privilege depth, unattended boot, recovery quality and market cost unknown where the current evidence does not establish them.

The important verified finding is the **execution surface**: a working public implementation demonstrates a custom PlayMemories/Android application running native game code on the camera, consuming physical controls, rendering custom frames and reading removable storage.

### TP-Link Archer C7 v5 — Wi-Fi router

- [`devices/tp-link/archer-c7-v5.yaml`](devices/tp-link/archer-c7-v5.yaml)
- [`evidence/tp-link/archer-c7-v5-openwrt.md`](evidence/tp-link/archer-c7-v5-openwrt.md)

The exact v5 hardware is represented as a small general Linux node after OpenWrt installation: QCA9563 / MIPS, 128 MB RAM, 16 MB flash, five Gigabit Ethernet ports, dual-band Wi-Fi, USB, serial, and a documented U-Boot/TFTP recovery path. Market price and measured power remain deliberately unfilled until evidence is collected.

Current census count: **2 / 25 devices, 2 / 8 marketed categories**.

## Example capability contract

[`capability_contracts/examples/low_power_registry_node.yaml`](capability_contracts/examples/low_power_registry_node.yaml) demonstrates the inverse side of the project: start with a goal and required capabilities before looking at product categories.

## Governance roots

Internal AXM work in this repo is evaluated against four constitutional roots:

- **Truth** — evidence before claims; preserve uncertainty and contradictions.
- **Agency / non-domination** — legitimate user control; no hidden control over other people or their devices.
- **Continuity** — evidence, state, configuration, and recovery must survive beyond one chat, operator, vendor service, or temporary runtime.
- **Wisdom before speed** — apparent savings must still make sense after setup effort, power, fragility, recovery, and maintenance are counted.

See [`FOUNDATION.md`](FOUNDATION.md) for the deeper project boundary.

## Status

**Early research. Not canon.**

The project begins with a hypothesis and an evidence discipline. Device records should earn trust through documented and reproducible evidence rather than optimism.
