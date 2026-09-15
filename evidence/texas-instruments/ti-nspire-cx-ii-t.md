# Evidence Packet — Texas Instruments TI-Nspire CX II-T / Programmable Calculator and Operational-Mode Access Boundary

**Device record:** `devices/texas-instruments/ti-nspire-cx-ii-t.yaml`  
**Exact scope:** Texas Instruments TI-Nspire CX II-T, non-CAS handheld  
**Checked:** 2026-09-15  
**Local verification:** No  
**Current evidence state:** `DOCUMENTED`

## Why this device matters

The TI-Nspire CX II-T adds a genuinely different hardware class to the census: a graphing calculator / programmable educational handheld with manufacturer-supported Python and TI-Basic execution.

Its strongest new model pressure is not merely that a calculator can run code. Texas Instruments documents a visible exam/Press-to-Test operating mode that can temporarily block access to pre-existing documents and programs, then restore access when the mode is exited. Data created during the Press-to-Test session has a different lifecycle and is deleted on exit.

That creates a useful capability-state distinction:

```text
program exists on persistent storage
  !=
program is currently accessible in this operational policy mode
```

It also creates a state-retention distinction:

```text
pre-existing state can be temporarily hidden and later restored
  while
session-created state can be intentionally ephemeral
```

The device record preserves that pressure locally instead of prematurely freezing a universal operational-mode schema after one device.

## Source 1 — Official CX II-T specification and programming surface

Texas Instruments Nederland specification:

- https://education.ti.com/nl/producten/rekenmachines/grafische-rekenmachines/ti-nspire-cx-ii-cx-ii-cas/specifications

Product-family page:

- https://education.ti.com/nl/producten/rekenmachines/grafische-rekenmachines/ti-nspire-cx-ii-cx-ii-cas

Checked: 2026-09-15

The current Dutch pages distinguish the TI-Nspire CX II-T from the TI-Nspire CX II-T CAS and document, for the family:

- 64 MB operating memory;
- 90+ MB storage memory;
- an included rechargeable battery;
- a USB port for computer connection;
- a 320 x 240 color display;
- a dedicated programming environment;
- Python and TI-Basic as programming languages;
- compatibility with TI-Nspire Lab Cradle and selected Vernier USB/temperature sensor systems for data collection.

### Hardware and execution truth boundary

This is sufficient to record real manufacturer-supported on-device programming surfaces.

It does **not** establish:

- CPU or SoC architecture;
- shell access;
- root, kernel or bootloader privilege;
- native-binary execution;
- arbitrary package installation;
- exact free/writable storage on an acquired unit;
- measured wall power;
- unattended boot or service autostart;
- NL/EU acquisition value;
- AXM local reproduction.

The record therefore marks Python and TI-Basic as `DOCUMENTED` execution surfaces while leaving privilege `unknown`.

## Source 2 — Official Python / operating-system dependency

Texas Instruments getting-started guidance:

- https://education.ti.com/en/resources/getting-started-on-ti-technology/ti-nspire-cx-ii

TI states that Python capability on the TI-Nspire CX II is installed and ready when the handheld operating-system version is greater than 5.2. The same page documents writing, storing and running a Python program on the handheld.

### Software-state truth boundary

The exact Dutch CX II-T product page independently establishes that the CX II-T is a Python-capable product. The getting-started page adds an important deployment condition: an acquired handheld's current OS state matters.

Therefore:

```text
exact hardware model supports Python
  !=
unknown acquired software state is automatically Python-ready
```

The record does not guess the OS version on any physical unit.

This source does **not** establish root/native execution, and it does not establish Python availability under every Press-to-Test restriction profile.

## Source 3 — Exact-family exam mode / Press-to-Test access boundary

Texas Instruments Nederland exam-mode guidance:

- https://education.ti.com/nl/ondersteuning/examenstand-nspire

Texas Instruments' current Dutch page explicitly covers the TI-Nspire CX II-T (CAS) family. It describes exam mode as blocking memory access, including access to documents and programs, while the mode is active. The page also documents visible status indicators and multiple explicit methods for exiting exam mode.

Additional TI CX II exam guide:

- https://education.ti.com/en/resources/test-preparation/education-test-prep-guides/ti-nspire-cx-ii

That guide distinguishes two operations:

- **Resetting All Memory**, which restores default settings and permanently removes user-saved data;
- **Press-to-Test**, which temporarily blocks pre-existing data/features and can later be exited.

The guide also states that data created during the Press-to-Test session is permanently deleted when the mode is exited.

### Operational-mode truth boundary

This is enough to preserve a machine-readable pressure case:

```text
normal mode
  -> pre-existing documents/programs accessible

Press-to-Test / exam mode
  -> access to pre-existing documents/programs blocked
  -> restriction state visibly indicated

exit Press-to-Test
  -> prior stored state/features become available again
  -> data created during the Press-to-Test session is deleted
```

This is **not** treated as firmware recovery, and the evidence does not prove that every possible selectable restriction disables exactly the same feature set. The record therefore does not claim that Python or TI-Basic is disabled under every Press-to-Test configuration.

## Source 4 — Destructive Reset All Memory

The same TI CX II exam guide documents Resetting All Memory as returning settings to factory defaults and permanently removing user-saved data.

### Reset truth boundary

The structured recovery path records:

```text
system configuration -> erased/reset to defaults
user data -> erased
application state -> unknown
```

Application state remains unknown because the cited page does not establish the exact disposition of every built-in or downloadable application, and the operation is not presented as an operating-system reinstall.

No AXM destructive reset was performed.

## Source 5 — Official OS reinstall over USB

Texas Instruments België knowledge-base article:

- https://education.ti.com/nl-be/klantenservice/kennisbank/hardware/80000

The article explicitly covers TI-Nspire CX/CAS and TI-Nspire CX II-T/CX II-T CAS units that report that the operating system is not found. It documents downloading the correct official OS, installing TI connectivity software on a computer, connecting the handheld by USB, and transferring/installing the OS onto the calculator.

### OS-recovery truth boundary

This proves an official OS-reinstallation path for the exact product family.

It does **not** establish whether that operation preserves or erases:

- user documents;
- settings;
- custom Python/TI-Basic programs;
- application state.

Those structured data-impact fields therefore remain `unknown` rather than being inferred from a different recovery procedure.

It also does not prove recovery from failed USB hardware, mainboard, battery or storage hardware.

## Power boundary

The manufacturer specifies an included rechargeable battery, but this activation collected no exact battery-capacity or device-consumption measurement suitable for capability-arbitrage scoring.

Do not substitute:

- battery presence;
- USB connectivity;
- charger/adapter specifications from a different source;

for measured idle or workload power.

Idle watts, active watts, charging behavior, battery health and always-on suitability remain unknown.

## Locality boundary

On-device Python and TI-Basic execution are real, but this activation did not perform a full locality study covering:

- initial provisioning;
- OS/update acquisition;
- all language/runtime dependencies;
- external sensor workflows;
- every normal calculator operation.

The record therefore does not promote `offline_operation` or vendor-cloud dependence from the mere existence of local code execution.

## Economics boundary

No dated NL/EU acquisition cohort was collected in this activation.

The record keeps:

- used price unknown;
- new price unknown;
- setup time unknown;
- replacement availability unknown;
- `market_data_state: not_collected`.

A visible current retail listing would still be one asking/displayed price, not a reusable market distribution.

## Local verification status

No AXM local verification was performed.

AXM did **not**:

- inspect a physical TI-Nspire CX II-T hardware revision;
- inspect its installed OS version;
- create or run a Python program;
- create or run a TI-Basic program;
- enter or exit Press-to-Test/exam mode;
- verify what exact restriction profile affects Python/TI-Basic;
- reset all memory;
- reinstall the OS;
- inspect battery health;
- measure wall/charging power;
- collect market prices.

The strongest evidence state remains `DOCUMENTED`.

## Census lesson

The TI-Nspire CX II-T adds a capability-state boundary that the first eighteen devices had not made explicit:

```text
execution surface is installed/persisted
  !=
execution surface is currently accessible under every operational policy mode
```

And the mode can have asymmetric continuity semantics:

```text
pre-existing programs/documents
  -> temporarily inaccessible
  -> accessible again after exit

session-created Press-to-Test data
  -> intentionally ephemeral
  -> deleted on exit
```

That is different from persistent replacement firmware, vendor-session lease expiry, OS-update persistence, or destructive factory restore. One documented calculator is enough to preserve the pressure locally, not enough to define a universal operational-mode schema.

## Root check

**Truth:** exact product-family documentation supports Python/TI-Basic, memory/USB/display facts, exam-mode access suppression, destructive memory reset and official OS reinstall; CPU architecture, privilege, acquired OS state, locality, power, prices and local reproduction remain unknown where unproven.  
**Agency / non-domination:** Press-to-Test/exam mode and recovery actions are visible owner/administrator procedures; no exploit, covert restriction, or hidden persistence is introduced.  
**Continuity:** the distinction between temporarily hidden pre-existing state, ephemeral session state, destructive memory reset and OS reinstall lives in the repo instead of hidden chat context.  
**Wisdom before speed:** a programmable calculator is not treated as an infrastructure node merely because it runs Python; networking, unattended behavior, power, battery wear, privilege and workload fit remain unverified.
