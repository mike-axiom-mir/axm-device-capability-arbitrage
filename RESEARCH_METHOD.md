# Research Method — AXM Device Capability Arbitrage

**Status:** v0.1 working method  
**Purpose:** Turn strange hardware discoveries into comparable, evidence-backed device records without letting product labels define capability.

## 1. Start from a goal, not a product

The primary research question is not "what is this device for?"

It is:

> **What verified capabilities does this device expose, and which goals could those capabilities satisfy?**

For goal-driven research, write the minimum capability contract first. Do not name a preferred product class unless the goal genuinely requires it.

Example:

```yaml
goal: low_power_local_registry
required:
  custom_code_execution: true
  persistent_state: true
  local_networking: true
  unattended_boot: true
preferred:
  power_watts_max: 10
  open_firmware: true
  recovery_path: documented
```

## 2. Discovery phase

For each candidate collect, where evidence exists:

- exact manufacturer and model;
- hardware revision;
- SoC / CPU;
- architecture / instruction set;
- RAM;
- internal persistent storage;
- removable storage;
- operating system / firmware;
- firmware update mechanism;
- network interfaces;
- USB / serial / GPIO / expansion interfaces;
- sensors;
- actuators and outputs;
- power source and approximate power profile;
- normal boot behavior;
- local/offline behavior.

Unknown stays `unknown`. Do not fill gaps from a neighboring model unless the record explicitly marks the inference.

### Integrated-substrate check

Do not value a donor only by CPU/RAM. Ask what integration mass production has already paid for.

Capture useful pre-integrated functions such as:

- battery, charger and power sequencing;
- cellular/Wi-Fi/Bluetooth radios and antennas;
- USB host/device hardware;
- SIM path;
- display, controls, audio and sensors;
- enclosure and thermal solution;
- boot/recovery hardware;
- accessible board-level buses or test pads.

Then capture the adaptation cost required to reuse them:

- helper PCB/components;
- level shifting or power conversion;
- cables/connectors;
- soldering or destructive mechanical work;
- driver/device-tree work;
- signal-integrity constraints;
- variant uncertainty.

The MF800 modem-thing case in `research/MF800_MODEM_THING_ARBITRAGE_CASE.md` is the reference pressure case. It demonstrates why an inexpensive finished consumer device can be a more valuable donor substrate than its product label suggests, while also showing how adapter hardware, physical modification, suspend behavior and unit consistency can erase apparent savings.

## 3. Find the execution surface

A chip inside a box is not enough. Determine how code actually reaches execution.

Look for, in roughly increasing control depth:

1. manufacturer application platform;
2. browser / WebView;
3. scripting or plugin runtime;
4. package manager;
5. custom APK / native application;
6. user shell;
7. administrator/root shell;
8. service / recovery execution mode;
9. replaceable firmware;
10. bootloader execution;
11. bare-metal execution.

Record the actual path. Avoid the vague label `hackable`.

## 4. Separate existence from accessibility

For each capability distinguish:

```text
PRESENT        — hardware/software appears to contain it
ACCESSIBLE     — documented interface reaches it
EXECUTABLE     — custom code can use it
VERIFIED       — evidence shows it working
REPRODUCIBLE   — another operator can repeat it from preserved instructions
```

A camera sensor may be present while unavailable to a custom app. A USB port may exist while exposing only a restricted mode. A Linux kernel may exist while no user-controlled code path is known.

## 5. Evidence capture

Every nontrivial claim should point to evidence.

Prefer sources in this order when practical:

1. local reproduction receipt;
2. source code / build instructions for a working implementation;
3. manufacturer documentation;
4. mature upstream open-source project documentation;
5. independent technical write-up;
6. community report;
7. marketplace listing only for market data, never for execution claims.

Preserve URLs, access/check date, relevant version/revision, and what the source actually proves.

## 6. Recovery research

Before recommending modification, investigate recovery separately from execution.

Check for:

- factory reset;
- official recovery image;
- rescue partition;
- dual-bank firmware;
- removable boot media;
- USB recovery;
- UART console;
- bootloader access;
- JTAG where relevant;
- configuration export;
- known irreversible steps;
- known brick modes.

`custom_code_execution: true` must never silently imply `safe_to_modify: true`.

## 7. Real-cost research

Collect cost as a dated market observation, not an eternal property.

Record separately:

- purchase price;
- shipping;
- power adapter;
- required cables / serial adapters;
- storage media;
- special tools;
- unlocking / provisioning time;
- expected power use;
- maintenance burden;
- failure/replacement difficulty;
- availability in the relevant region.

Do not rank a €5 device above a €20 device until the hidden friction is counted.

## 8. Role mapping

After evidence capture, map the device to useful roles rather than forcing it to run an entire stack.

Examples:

- registry;
- heartbeat/watchdog;
- verifier;
- deterministic worker;
- mesh relay;
- sensor collector;
- actuator bridge;
- local cache;
- provenance logger;
- storage/archive;
- offline data courier;
- lightweight simulation;
- game/server node;
- local inference where realistic.

Role mapping is a hypothesis until tested against an actual capability contract.

## 9. Composition search

Always consider whether multiple cheap devices beat one conventional device.

Evaluate:

- one-device solution;
- role-specialized composition;
- redundant composition;
- battery-backed + mains composition;
- sensor node + storage node + network node combinations.

Composition must count coordination, networking, power, and recovery overhead.

## 10. Verification states

Use the strongest grounded state only:

```text
UNRESEARCHED
DOCUMENTED
COMMUNITY_VERIFIED
LOCALLY_VERIFIED
REPRODUCIBLE
DEPRECATED
CONTRADICTED
```

`COMMUNITY_VERIFIED` means a concrete public implementation exists. It does not mean AXM reproduced it locally.

`LOCALLY_VERIFIED` requires our own test evidence.

`REPRODUCIBLE` requires preserved steps and enough evidence for another operator to repeat the result.

## 11. Contradictions

Do not overwrite contradictory evidence.

Record:

- claim A;
- claim B;
- model/revision/firmware differences;
- what remains unresolved;
- the next test that would resolve it.

Contradiction is useful state.

## 12. First census protocol

Initial falsifiable milestone:

> **25 devices across at least 8 marketed categories.**

A device counts toward the milestone only if it has:

- an exact model identity;
- at least one meaningful execution-surface finding;
- source evidence;
- explicit unknowns;
- recovery status;
- preliminary role mapping;
- cost status, even if the status is `not_collected`.

The milestone succeeds only if capability-first matching surfaces useful options that product-category shopping would plausibly miss.

## 13. Root gate before promotion

Before a record or recommendation is promoted:

**Truth** — Do claims match evidence and uncertainty?  
**Agency / non-domination** — Is use limited to owned/authorized hardware with visible control?  
**Continuity** — Are evidence, setup and recovery preserved outside temporary chat state?  
**Wisdom before speed** — Does the option still make sense after power, friction, fragility and maintenance are counted?

## 14. Output rule

Research should end in machine-readable state plus human-readable evidence.

The preferred chain is:

```text
discovery
→ evidence
→ device record
→ capability contract match
→ cost/recovery score
→ experiment
→ result / contradiction
→ revised record
```

The marketed product category remains metadata throughout.