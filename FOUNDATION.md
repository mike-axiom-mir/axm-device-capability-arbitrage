# FOUNDATION — AXM Device Capability Arbitrage

**Status:** Foundational research boundary, early-stage.  
**Purpose:** Preserve the meaning of this repository as the device census and scoring systems grow.

---

## 1. Founding observation

A product category is a human description of expected use.

It is not a complete description of the machine inside the product.

A camera may contain an application runtime. A router may be a Linux computer. A robot vacuum may combine compute, networking, storage, sensors, and actuators. A smart plug may contain a programmable microcontroller. A NAS may be a container host.

The important question is not what the box calls the object.

The important question is:

> **What verified capabilities exist, and what goals can they satisfy?**

---

## 2. Central hypothesis

> **Human markets price products. Machines consume capabilities.**

Those two valuation systems are not identical.

Commercial price is influenced by factors such as:

- brand;
- popularity;
- fashion;
- product age;
- consumer demand;
- convenience;
- intended audience;
- ecosystem lock-in;
- original marketed purpose.

A machine workload may care about none of those things.

A workload may only require:

- a certain instruction set;
- enough RAM;
- persistent state;
- a network interface;
- a particular sensor;
- a particular actuator;
- an execution surface;
- an uptime profile;
- a recovery path;
- a power ceiling.

This mismatch can create **capability arbitrage**: useful capability available for less money than conventional category-based purchasing would suggest.

---

## 3. What this repo is trying to build

This repository should evolve toward three connected layers.

### Layer A — Evidence-backed device census

A machine-readable catalogue of real devices and the capabilities they expose.

### Layer B — Capability contracts

Machine-readable descriptions of what a goal minimally requires.

### Layer C — Matching and scoring

A way to compare devices or device combinations against a capability contract using total useful cost rather than sticker price alone.

Long-term conceptual flow:

```text
GOAL
  ↓
CAPABILITY CONTRACT
  ↓
DEVICE / COMPOSITION CANDIDATES
  ↓
EVIDENCE FILTER
  ↓
COST + POWER + RECOVERY + FRICTION SCORE
  ↓
BEST GROUNDED OPTIONS
```

The system should remain useful even if AXM itself is not the eventual consumer.

---

## 4. Product category is metadata, not authority

The marketed category of a device is worth recording because it helps humans find and discuss it.

It must not become a hard boundary in the search system.

Examples of categories:

```text
camera
router
printer
phone
robot vacuum
TV box
NAS
e-reader
smart plug
thin client
industrial gateway
```

These categories should never imply capability by themselves.

A record saying `marketed_category: camera` does **not** prove:

- custom-code execution;
- Android;
- Linux;
- network access;
- root;
- useful compute;
- safe modification.

Likewise, a category should not prevent discovery of unexpected capability.

---

## 5. Execution surface is a first-class capability

A processor existing inside a product is not enough.

The research must ask how software can actually reach it.

Possible execution surfaces include:

- manufacturer application platform;
- browser / WebView;
- scripting runtime;
- plugin system;
- package manager;
- Android APK;
- Linux userspace binary;
- container runtime;
- JVM;
- WebAssembly;
- RTOS task / SDK;
- SSH / shell;
- ADB;
- UART;
- bootloader;
- replaceable firmware;
- bare-metal execution.

These have different privilege, portability, recovery, and safety characteristics. They must not be collapsed into one boolean such as `hackable: true`.

---

## 6. Human interface is not machine capability

Displays, touchscreens, keyboards, enclosures, and polished interfaces are useful for people.

They are not necessarily useful for the target workload.

A headless device may be an excellent node.

A visually impressive device may be a poor node.

The census should therefore separate human-facing properties from machine-facing properties.

### Human-facing examples

- screen size;
- touch support;
- physical keyboard;
- product UI;
- enclosure design.

### Machine-facing examples

- architecture;
- RAM;
- storage;
- execution environment;
- privilege level;
- boot chain;
- networking;
- USB / serial / GPIO;
- sensors;
- actuators;
- power use;
- thermal limits;
- unattended boot;
- recoverability;
- deterministic behavior;
- local/offline operation.

This distinction is foundational.

---

## 7. Capability composition

A goal does not have to fit on one device.

The cheapest or strongest solution may be a composition.

Example:

```text
used router
  → registry
  → mesh relay
  → heartbeat

old phone
  → camera
  → microphone
  → battery-backed compute

NAS
  → durable state
  → archive
  → snapshots

microcontroller device
  → sensor
  → relay
  → deterministic edge state
```

A future matcher should therefore be able to rank:

- one-device solutions;
- multi-device solutions;
- redundant solutions;
- role-specialized solutions.

Do not assume bigger integration is automatically better.

---

## 8. Total useful cost

This project must resist misleading cheapness.

The relevant cost is not only purchase price.

At minimum, consider:

```text
purchase
+ adapters
+ required storage
+ unlocking / provisioning time
+ electricity
+ maintenance
+ failure risk
+ recovery difficulty
+ replacement difficulty
```

Potential future additions:

- shipping;
- tool requirements;
- firmware availability;
- regional availability;
- documentation quality;
- hardware-revision uncertainty;
- expected remaining lifetime.

A device is not a bargain if the hidden friction destroys the advantage.

---

## 9. Evidence before possibility

The project should be aggressive in discovery and conservative in claims.

Interesting hardware is not the same as verified hardware.

A claim should preserve the strongest evidence actually available.

Suggested evidence states:

```text
UNRESEARCHED
DOCUMENTED
COMMUNITY_VERIFIED
LOCALLY_VERIFIED
REPRODUCIBLE
DEPRECATED
CONTRADICTED
```

Where possible preserve:

- primary source;
- independent source;
- exact hardware revision;
- exact firmware version;
- date checked;
- method used;
- commands / build steps;
- failure notes;
- recovery notes;
- local test receipt.

Unknown should remain unknown.

Conflicting evidence should remain visible rather than being silently normalized into certainty.

---

## 10. Recovery is part of capability

A device that performs a task but cannot be safely recovered is not equivalent to a device that performs the same task with a strong recovery path.

Recovery properties may include:

- factory reset;
- rescue partition;
- dual firmware;
- removable storage boot;
- bootloader access;
- UART recovery;
- signed official restore image;
- configuration export;
- reproducible provisioning.

Recovery quality should eventually affect scoring.

---

## 11. Local and offline value

A device that depends on a vendor cloud for basic operation is materially different from one that can operate locally.

Record this difference explicitly.

Possible states may include:

```text
fully_local
local_after_provisioning
cloud_optional
cloud_required_for_some_functions
cloud_required
unknown
```

Do not call a device local merely because some computation happens on-device.

---

## 12. Root merge gate

The internal constitutional merge gate for this AXM work is the four roots.

### Truth

Claims must not outrun evidence.

- No fake verification.
- No collapsing hardware revisions without evidence.
- No claiming arbitrary execution from specifications alone.
- No pretending a one-off hack is a stable deployment path.
- Preserve contradictions and uncertainty.

### Agency / non-domination

Capability discovery must not become an excuse for hidden control.

- Prefer user-owned hardware.
- Require legitimate authority over devices.
- Preserve visible user control.
- No unauthorized access.
- No hidden persistence.
- Shared devices require consent appropriate to the modification.

### Continuity

Useful knowledge must survive beyond a temporary operator or chat.

- Store evidence in the repo.
- Store schemas and scoring logic in inspectable form.
- Preserve recovery instructions.
- Prefer reproducible provisioning.
- Avoid making vendor cloud state the only surviving copy of critical state.

### Wisdom before speed

Fast reuse is not automatically wise reuse.

Count:

- electricity;
- fragility;
- maintenance;
- setup effort;
- safety;
- replacement supply;
- recovery burden;
- long-term operational fit.

A cheap device can still be the wrong device.

---

## 13. Safety boundary

The project should freely investigate powerful capability while maintaining grounded boundaries around deployment.

Particular care is required for:

- safety-critical vehicle systems;
- mains-voltage devices;
- medical equipment;
- security/alarm infrastructure;
- machinery capable of physical injury;
- devices not owned or authorized by the operator.

The existence of an execution surface does not itself justify using it.

Research records may describe capability while still marking a deployment path inappropriate or unverified.

---

## 14. What this project should not become

Do not let the repo drift into:

- a generic gadget database;
- a list of cool hacks without evidence;
- a rooting tutorial collection with no goal matching;
- a shopping-price scraper with no capability model;
- an AXM-only compatibility list;
- a reason to accumulate e-waste without use;
- a system that treats every possible capability as automatically desirable.

The differentiator is the full chain:

> **goal → capability contract → verified hardware state → total useful cost → grounded match**

---

## 15. First falsifiable test

The first useful milestone is not a huge database.

Build a small evidence-backed comparison set:

> **25 devices across at least 8 marketed categories.**

Then ask:

1. Can we represent them consistently?
2. Can we define real goals as capability contracts?
3. Does capability-first matching surface unexpected candidates?
4. Do those candidates remain better after friction, power, and recovery are counted?
5. Can another person or machine reproduce the evidence trail?

If not, revise the hypothesis or schema.

---

## 16. Long-term direction

A mature form of this work could support:

```text
human research
→ machine-readable census
→ local hardware probing
→ capability contracts
→ automatic matching
→ cost optimization
→ reproducible provisioning recipes
→ distributed capability fabric
```

The future system should be able to look at a goal and reason over hardware without being trapped by human retail categories.

That future is not assumed to exist yet.

This repository exists to earn it through evidence.

---

## 17. Foundational one-line rule

> **Ignore what the box says the device is. Measure what the hardware can actually do, then match verified capabilities to goals at the lowest real cost.**
