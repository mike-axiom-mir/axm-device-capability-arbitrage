# AXM Device Capability Arbitrage — Research Seed v0.1

**Origin date:** 2026-09-13  
**Status:** Working research seed; not canon.  
**Purpose:** Preserve the originating direction before later schemas, scoring systems and device records evolve it.

## Core observation

A device's marketed purpose describes how humans are expected to use it.

It does **not** define its computational capabilities.

A camera can contain an application runtime. A router can contain a general-purpose Linux environment. A robot vacuum can combine compute, storage, networking, sensors and motors. A smart-home product can contain a programmable microcontroller. A NAS can be a container host.

The screen, enclosure, buttons and product category are primarily human-facing packaging.

For machine use, ask instead:

- what processor/architecture exists;
- how much memory is available;
- what persistent storage exists;
- what execution surface exists;
- what privilege is reachable;
- what network and physical interfaces exist;
- what sensors and actuators exist;
- what power profile exists;
- whether unattended operation is possible;
- how the device recovers from failure;
- what it costs after provisioning friction is included.

## Core principle

> **Search by required capability, not by product category.**

Instead of asking:

> What computer should we buy for this task?

ask:

> **What is the smallest, cheapest, safest, most recoverable hardware or hardware composition that satisfies the capability contract?**

Possible answers may include:

- used routers;
- old phones;
- IP cameras;
- consumer cameras;
- TV boxes;
- NAS devices;
- e-readers;
- robot vacuums;
- printers;
- smart-home devices;
- thin clients;
- POS terminals;
- industrial surplus;
- embedded boards hidden inside unrelated products;
- combinations of several devices.

## Capability arbitrage

Working definition:

> **Capability arbitrage is matching a goal to hardware whose useful verified capabilities are priced below conventional alternatives because humans value the product according to category, brand, age, fashion, popularity, convenience or original purpose rather than the machine capability needed for the goal.**

This is not an argument to buy random cheap hardware.

The target is underpriced **useful capability**.

## Trigger example — Sony alpha 6000 / DoomCam

The original trigger for this research was seeing Doom run on a Sony α6000 camera.

The important question was not "how can a camera show Doom?"

The important question was:

> **Why can code like this execute on an object sold as a camera?**

Public evidence showed that compatible Sony PlayMemories cameras expose an Android application environment, with community tooling capable of installing custom applications and exposing debugging/execution paths.

A working DoomCam implementation then demonstrated custom code, physical controls, display output and removable-storage access on the α6000.

The visual game is human-readable proof.

The deeper machine fact is:

```text
processor
+ memory
+ storage
+ execution surface
+ I/O
= potential node
```

That observation immediately extends beyond cameras.

## Human interface is not the capability boundary

Separate:

### Human-facing

- display;
- touchscreen;
- keyboard;
- enclosure;
- branded UI;
- expected consumer workflow.

### Machine-facing

- architecture;
- RAM;
- storage;
- runtime;
- privilege;
- boot chain;
- network;
- serial/USB/GPIO;
- sensors;
- actuators;
- power;
- thermal limits;
- unattended boot;
- recovery;
- deterministic behavior;
- local/offline capability.

A headless object may be a better machine node than an expensive device with a beautiful screen.

## Goal-first pipeline

```text
GOAL
  ↓
MINIMUM CAPABILITY CONTRACT
  ↓
SEARCH ALL DEVICE CLASSES
  ↓
VERIFY EXECUTION + I/O + RECOVERY
  ↓
CALCULATE TOTAL USEFUL COST
  ↓
MAP DEVICE OR COMPOSITION TO ROLE
  ↓
TEST
  ↓
KEEP / REJECT / REVISE
```

## Total useful cost

```text
TOTAL USEFUL COST =
    acquisition
  + adapters
  + required storage
  + provisioning effort
  + electricity
  + maintenance
  + failure risk
  + recovery burden
  + replacement difficulty
```

A €5 object that requires fragile undocumented work may lose to a €20 object that boots an open runtime immediately.

A slightly more expensive low-power device may win over years of operation.

## Capability composition

A goal does not have to fit on one device.

Example:

```text
router
  → registry
  → mesh relay
  → heartbeat

old phone
  → camera
  → microphone
  → battery-backed compute

NAS
  → durable state
  → snapshots
  → archive

microcontroller node
  → sensor
  → relay
  → tiny deterministic state
```

The cheapest grounded solution may be a composition rather than one conventional computer.

## Device classes to investigate

The initial census should deliberately cross human categories:

- network hardware;
- consumer and IP cameras;
- phones/tablets/handheld terminals;
- smart-home hardware;
- media/TV/signage devices;
- NAS/storage appliances;
- robots;
- e-readers/e-ink hardware;
- printers/scanners/conference systems;
- consoles/handhelds;
- non-safety vehicle computers;
- thin clients/POS/kiosks;
- industrial/commercial surplus;
- miscellaneous e-waste with SoCs, flash, firmware or communication interfaces.

## Evidence discipline

Do not claim:

- arbitrary execution from specifications alone;
- root because a shell exists;
- safe flashing because one person succeeded;
- family-wide compatibility from one model;
- recovery without a recovery path;
- stable market price from one listing.

Suggested states:

```text
UNRESEARCHED
DOCUMENTED
COMMUNITY_VERIFIED
LOCALLY_VERIFIED
REPRODUCIBLE
DEPRECATED
CONTRADICTED
```

Unknown should remain unknown.

## Local/offline value

Track whether a node is:

```text
fully_local
local_after_provisioning
cloud_optional
cloud_required_for_some_functions
cloud_required
unknown
```

On-device compute does not automatically mean local control.

## First practical milestone

> **25 evidence-backed devices across at least 8 marketed categories.**

Each should contain:

- exact identity;
- execution-surface evidence;
- important compute/storage facts where known;
- I/O;
- recovery state;
- economic state;
- candidate roles;
- explicit unknowns;
- source evidence.

Then test whether capability-first matching actually exposes unexpected winners.

## Long-term direction

```text
human research
→ machine-readable device census
→ local hardware probe
→ capability contracts
→ device/composition matching
→ cost optimization
→ reproducible provisioning
→ distributed capability fabric
```

The mature system should be able to receive a goal and reason across hardware without being trapped by retail categories.

That capability is not assumed. This repository exists to earn it.

## Roots

### Truth
Evidence before claims. Preserve uncertainty and contradiction.

### Agency / non-domination
Owned/authorized hardware, visible control, no hidden persistence over others.

### Continuity
Preserve evidence, state, configuration and recovery outside temporary chat/operator/vendor state.

### Wisdom before speed
Count power, fragility, labor, maintenance, recovery and long-term fit before calling something cheap or useful.

## One-line seed

> **Ignore what the box says the device is. Measure what the hardware can actually do, then match verified capabilities to goals at the lowest real cost.**

## Split working documents

This seed is intentionally preserved as an origin snapshot. Current working details are split into:

- `FOUNDATION.md`
- `RESEARCH_METHOD.md`
- `CAPABILITY_SCHEMA.md`
- `EVIDENCE_STANDARD.md`
- `COST_MODEL.md`
- `SAFETY_AND_RECOVERY.md`

Later changes should evolve those documents without silently rewriting this origin snapshot.
