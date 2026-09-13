# Safety and Recovery

**Status:** v0.1  
**Purpose:** Keep capability discovery broad without confusing execution ability with wise deployment.

## 1. Capability is not permission

Finding an execution surface does not authorize using it.

Research and deployment should assume:

- the operator owns the hardware or has explicit authority to modify it;
- shared hardware requires appropriate consent;
- network access to a device is not permission to control it;
- capability discovery must not create hidden persistence or hidden control over others.

## 2. Recovery is a first-class capability

A device that can run useful code but cannot be recovered safely is materially different from one with a robust restore path.

Every serious candidate should investigate:

- factory reset;
- official restore image;
- signed recovery path;
- rescue partition;
- dual-bank firmware;
- removable storage boot;
- USB recovery;
- UART/serial recovery;
- bootloader access;
- configuration export;
- reproducible reprovisioning.

`execution_verified` and `recovery_verified` are separate facts.

## 3. Modification classes

### Class 0 — No modification
Use documented built-in functionality only.

### Class 1 — Reversible user-space extension
Install an app, package, script or plugin through an existing mechanism.

### Class 2 — Reversible service/recovery execution
Use a service, updater or recovery path that executes custom code without permanently replacing the main firmware.

### Class 3 — Firmware replacement
Flash an alternate firmware or system image.

### Class 4 — Hardware-assisted recovery/modification
Requires UART, boot pins, external programmer, soldering, test points or disassembly.

### Class 5 — Destructive / high-risk modification
Irreversible fuse changes, destructive extraction, unknown mains-side work, safety-system modification or similarly high-risk operations.

The class describes intervention depth, not moral value. The evidence and recovery quality determine whether it is appropriate.

## 4. Safety-sensitive categories

Extra caution is required around:

- mains-voltage smart plugs and appliances;
- vehicles;
- medical equipment;
- alarms and physical security systems;
- drones and mobile robots;
- machinery capable of causing injury;
- batteries and charging systems;
- devices controlling heat, pressure, locks or high current.

Research may document a compute surface without recommending deployment on safety-critical control paths.

## 5. Vehicle boundary

Infotainment, navigation and fleet terminals may contain useful general-purpose compute.

Keep those conceptually separate from:

- braking;
- steering;
- airbags;
- drivetrain safety;
- battery-management safety;
- other safety-critical vehicle controllers.

A shared enclosure or network does not make these systems equivalent.

## 6. Mains-voltage boundary

A low-cost smart plug may contain an attractive microcontroller, but opening or modifying mains hardware adds an electrical hazard unrelated to its compute value.

Records should state whether useful access is possible without exposing the operator to mains-voltage internals.

## 7. Original-function preservation

Where practical prefer paths that:

- retain the original firmware image;
- allow factory restoration;
- avoid destructive enclosure changes;
- preserve the device's original useful function;
- isolate experiments from safety-critical behavior.

Preserving original function is not an absolute rule, but irreversible loss belongs in total useful cost and recovery scoring.

## 8. Brick-risk recording

Suggested states:

```text
unknown
low_documented_recovery
moderate_recovery_requires_tools
high_recovery_uncertain
irreversible_known_risk
```

Do not convert vague community warnings into fake percentages.

## 9. Provisioning receipts

For modifications that change persistent state, preserve:

- original firmware/version;
- backup/checksum where lawful and practical;
- exact tool versions;
- commands/steps;
- changed partitions/files;
- reboot behavior;
- recovery steps;
- recovery test result.

## 10. Network exposure

A repurposed device should not become an accidental weak point.

Record:

- default credentials;
- whether remote administration is enabled;
- exposed services;
- whether the device receives security updates;
- whether it can be isolated to a local segment;
- whether an execution path depends on intentionally insecure services such as open telnet.

A useful compute node can still be a bad network citizen.

## 11. Root gate

### Truth
Do not call a path safe or reversible without evidence.

### Agency / non-domination
Use only owned/authorized devices and preserve visible control.

### Continuity
Preserve restore/provisioning knowledge outside temporary chat state.

### Wisdom before speed
A cheap hack that creates a fragile, dangerous or unrecoverable dependency can fail the goal even when it technically works.

## 12. Foundational safety rule

> **Execution tells us what a device can do. Recovery, ownership, isolation and context tell us whether using that capability is wise.**