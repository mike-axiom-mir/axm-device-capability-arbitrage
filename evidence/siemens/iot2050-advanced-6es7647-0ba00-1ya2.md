# Evidence Packet — Siemens SIMATIC IOT2050 Advanced / Industrial Linux Execution and Functional-Status Identity

**Device record:** `devices/siemens/simatic-iot2050-advanced-6es7647-0ba00-1ya2.yaml`  
**Exact article / order number:** `6ES7647-0BA00-1YA2`  
**Checked:** 2026-09-14  
**Local verification:** No  
**Current evidence state:** `DOCUMENTED`

## Why this device matters

The SIMATIC IOT2050 Advanced is the first industrial/commercial-surplus class record in the census.

Unlike many consumer appliances, its manufacturer already exposes a conventional local computing path:

```text
industrial gateway
  -> AM6548 HS quad-core SoC
  -> 2 GB DDR4
  -> 16 GB eMMC
  -> microSD / USB boot
  -> Debian-based Siemens example image
  -> root SSH / UART shell
  -> apt package management
  -> U-Boot boot selection
```

That makes it a useful industrial counterexample to the idea that unusual retail categories require exploit-based execution.

The more important schema pressure is identity:

> **Even one exact Siemens order number can span different manufacturer functional-status revisions with different interface capability.**

For `6ES7647-0BA00-1YA2`, Siemens documents:

```text
FS01-FS03
  -> 2 x USB 2.0 Type A

FS04
  -> 1 x USB 3.0 Type A
  -> 1 x USB 2.0 Type A
```

A used listing containing the exact article number therefore still does not prove the highest known USB capability. Future acquisition evidence should preserve the observed `FS` value whenever it matters.

## Source 1 — Siemens SIMATIC IOT2050 Operating Instructions

Manufacturer operating instructions:

- https://support.industry.siemens.com/cs/attachments/109963259/iot2050_operating_instructions_en_en-US.pdf

Document family: `A5E39456816-AF`  
Checked: 2026-09-14

The exact configuration plan identifies:

- `IOT2050 Advance` / article `6ES7647-0BA00-1YA2`;
- TI SoC AM6548 HS, quad core;
- 2 GB DDR4 RAM;
- 16 GB eMMC;
- battery-backed real-time clock;
- PCIe interface;
- microSD support;
- two Ethernet interfaces;
- serial connectivity;
- USB capability that changes by functional status.

The manual's functional-status table is why `hardware_revision` remains unknown in the device record even though the article number is exact.

### Exact-identity truth boundary

The record does **not** infer:

- FS04 from the article number alone;
- USB 3.0 on every IOT2050 Advanced;
- installed expansion cards;
- eMMC health;
- current Industrial OS state;
- a used unit's security-patch level.

Those are unit-level observations.

## Source 2 — Manufacturer Debian-based example-image workflow

The same Siemens operating instructions document a full local example-image workflow for the IOT2050 family.

The manual describes:

- a Siemens example image containing a Debian-based Linux operating system;
- booting an example image from microSD / USB;
- SSH administration;
- root login;
- UART console login;
- normal Linux commands;
- `apt` package management;
- writing the example image to the Advanced model's internal eMMC.

This is strong manufacturer evidence of general local execution. It does not rely on a vulnerability or hidden service.

### Execution truth boundary

The record scopes these claims to the **documented Siemens example-image workflow**.

It does not silently claim:

- every Industrial OS release ships with the same root-login defaults;
- every package remains available forever;
- arbitrary services survive vendor updates;
- arbitrary services autostart after unexpected power loss;
- the AXM common registry workload has actually run on the device.

No physical IOT2050 was tested by AXM in this activation.

## Source 3 — U-Boot and external-media escape / recovery

The operating instructions also document two useful continuity paths.

### U-Boot console

Through UART, the operator can enter the U-Boot shell and alter boot target / boot order.

This establishes a boot-selection surface. It does **not** establish that a corrupted U-Boot/SPI firmware image can itself be recovered through that same UART path.

### Firmware V1.3.1+ external-media-only boot

For firmware V1.3.1 or later, Siemens documents a USER-button startup behavior that skips eMMC and boots only from external media.

That means a broken or unwanted eMMC operating-system state can be bypassed **when the relevant boot firmware remains functional and the documented firmware-version condition is satisfied**.

This path is represented explicitly instead of being flattened into a global `official_restore: true` claim.

### eMMC re-image

Siemens documents using a booted external example image to write an image to the Advanced model's internal eMMC.

That is treated as destructive to the target system/application image. The record does not claim that this reproduces a licensed factory Industrial OS state or preserves arbitrary user data.

## Source 4 — Current Siemens IOT2050 education/product overview

Manufacturer page:

- https://www.siemens.com/en-gb/content/sce-educational-institutions/iot2000/

Checked: 2026-09-14

Siemens currently presents the IOT2050 as a high-level-language programming platform and lists:

- AM6548 HS quad-core processor;
- 2 GB DDR4 RAM;
- 16 GB eMMC;
- two Gigabit Ethernet ports;
- two USB ports;
- switchable RS232/RS485/RS422 serial interface;
- SD-card slot;
- 24 V DC supply;
- a preinstalled SIMATIC Industrial OS offering.

This source supports the platform's current manufacturer positioning as a programmable industrial gateway.

It is not used to override the exact functional-status differences documented in the operating instructions.

## Source 5 — Manufacturer power figures, not AXM measurements

Later `A5E39456816-AF` IOT2050 operating instructions:

- https://support.industry.siemens.com/cs/attachments/109974073/iot2050_operating_instructions_en_en-US.pdf

Checked: 2026-09-14

The IOT2050 technical data lists:

- direct-current supply in the 12-24 V DC nominal range, with the documented wider input tolerance;
- `12 W` typical basic-device consumption at rated 24 V;
- `24 W` maximum power.

### Power truth boundary

These are **manufacturer technical-data figures**.

They are not:

- AXM wall-power measurements;
- workload-specific measurements;
- measurements of an arbitrary used unit;
- measurements including every expansion card / USB peripheral;
- a reason to write `idle_watts: 12` or `active_watts: 12`.

The device record therefore keeps both idle and active wattage unknown and stores the manufacturer figure separately.

## Source 6 — Current ProductCERT security maintenance evidence

Siemens ProductCERT advisory:

- https://cert-portal.siemens.com/productcert/html/ssa-834709.html

Publication date: 2026-08-11  
Checked: 2026-09-14

`SSA-834709` explicitly names:

> `SIMATIC IoT2050 Advanced (6ES7647-0BA00-1YA2)`

The advisory says that Industrial OS versions below `V4.3.4.1` **with Node-RED installed** are affected by `CVE-2026-58115`, and Siemens recommends updating affected deployments to `V4.3.4.1` or later.

This evidence is recorded as a **maintenance/deployment constraint**, not as an execution technique.

The repo does not infer that:

- every acquired IOT2050 Advanced has Node-RED installed;
- every unit is vulnerable;
- every unit is already patched;
- the vulnerability is needed or appropriate for legitimate local execution.

The legitimate manufacturer-documented root/Linux path already exists independently.

### New operational lesson

A used industrial computer can have strong hardware identity and strong local execution while its deployment fitness still depends on **observed software/security state**.

A market listing that says only `IOT2050 Advanced` is not enough to establish:

```text
functional status
firmware version
Industrial OS version
Node-RED presence
security-patch state
```

Those must remain acquisition or local-observation facts.

## Industrial safety / authority boundary

The IOT2050 is designed to bridge industrial interfaces and production data.

That does not mean a general-purpose Linux workload is automatically authorized or safe to control every attached machine/process.

The census record intentionally separates:

```text
local host execution
!=
authority over attached equipment
!=
safety fitness for process control
```

No claim is made that this device should replace a safety PLC, bypass plant safeguards, or be connected to production equipment without the appropriate owner/operator authority and engineering controls.

## Arbitrage boundary

The IOT2050 Advanced is **not** added to the current low-power registry comparison yet.

It has a plausible technical shape for a local registry/heartbeat role, but comparable evidence is still missing for:

- dated NL/EU used acquisition cost;
- whether a candidate unit includes a suitable 24 V supply;
- exact unit functional status;
- actual Industrial OS / firmware state;
- eMMC wear / remaining life;
- common-workload memory/CPU/storage footprint;
- wall power under the common workload;
- provisioning time;
- service autostart after unexpected power loss;
- repeated hard-power-loss recovery;
- opportunity cost in a real industrial use context.

The manual's `12 W` typical basic-device figure is useful context, but it is not directly comparable to physical registry-workload measurements that the first comparison still requires.

## Explicit unknowns retained

No AXM local test was performed.

Still unknown:

- physical-unit functional status (`FS`);
- actual installed firmware / Industrial OS version;
- Node-RED presence and patch state on an arbitrary unit;
- CPU architecture label in this record beyond the exact AM6548 HS SoC identity;
- usable eMMC space and wear;
- integrated/installed wireless configuration;
- whole-device idle and registry-workload wall power;
- NL/EU used-market cohort;
- power-supply inclusion/cost;
- provisioning time;
- arbitrary-service autostart;
- hard-power-loss restart reliability;
- recovery from corrupted boot firmware;
- remaining hardware life.

These unknowns are intentional.
