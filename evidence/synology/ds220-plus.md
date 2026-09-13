# Evidence Packet — Synology DiskStation DS220+

**Device record:** `devices/synology/ds220-plus.yaml`  
**Checked:** 2026-09-13  
**Local verification:** No  
**Current evidence state:** DOCUMENTED

## Why this device matters

The DS220+ is the first NAS/storage appliance in the census and the first record where a manufacturer-supported container runtime is the primary execution surface rather than a firmware replacement, community launcher, or rooting path.

That makes it useful schema pressure in several directions:

- custom code can run inside supported containers without replacing the NAS firmware;
- persistent state is a native product strength rather than an add-on;
- power data exists from the manufacturer under a named test condition;
- the product is discontinued while DSM updates remain supported, separating hardware lifecycle from software support;
- recovery has different **data impact** depending on the reset path.

The most important new recovery lesson is:

```text
recovery path exists
  !=
recovery path preserves the same state/data
```

That distinction is different from the Roborock S5's stock-vs-modified reversibility issue and should be retained rather than flattened into `recovery: true`.

## Source 1 — Exact model hardware, lifecycle and power

Primary model source:

- https://www.synology.com/nl-nl/store/Refurbished%20DS220%2B

Lifecycle source:

- https://www.synology.com/en-us/products/status?status=all

Checked: 2026-09-13

Synology's current DS220+ product material documents:

- Intel Celeron J4025 CPU;
- two CPU cores / two threads;
- 2 GB DDR4 memory, expandable to 6 GB;
- two 3.5-inch/2.5-inch SATA drive bays;
- hot-swap support;
- two 1GbE Ethernet ports;
- two USB 3-class ports;
- Wake on LAN/WAN;
- scheduled power on/off;
- Power Recovery;
- 60 W external power adapter;
- 14.69 W access power consumption;
- 4.41 W HDD-hibernation consumption.

Synology states that the power figures were measured with the NAS fully loaded with specified Western Digital 1 TB drives. They are therefore useful manufacturer measurements, but they are **not** AXM local measurements and must not be treated as a universal container-workload power profile.

Synology's current product-support table marks the DS220+ as:

- product availability: discontinued;
- DSM Update: Full;
- technical support: Limited.

### What this proves

- exact-model CPU/RAM/network/storage-bay configuration;
- supported power-management features;
- manufacturer power measurements under a named configuration;
- discontinued hardware lifecycle with continuing DSM update support at check date.

### What this does not prove

- current NL used-market price;
- drive cost;
- real power under the proposed AXM registry workload;
- remaining life of a used unit;
- local container stability.

## Source 2 — Exact-model Container Manager compatibility

Source:

- https://kb.synology.com/en-af/DSM/tutorial/Why_is_Container_Manager_1630_not_available_on_my_Synology_NAS

Last updated by Synology: 2026-05-06  
Checked: 2026-09-13

Synology's compatibility notice for Container Manager 24.0.2-1630 explicitly lists **DS220+** among the models excluded from that specific update. The same notice directs affected models to install **24.0.2-1606 or another compatible version**.

This is unusually useful evidence because it establishes two things at once:

1. DS220+ has a supported Container Manager path;
2. newest package version compatibility is not guaranteed forever.

The record therefore does not claim "latest Container Manager" as a stable property.

### What this proves

- an exact-model manufacturer-supported Container Manager release path exists;
- package compatibility is version-sensitive.

### What this does not prove

- compatibility with every container image;
- indefinite support for future Container Manager releases;
- performance of a particular container workload.

## Source 3 — What Container Manager actually exposes

Source:

- https://www.synology.com/nl-nl/dsm/feature/docker

Checked: 2026-09-13

Synology describes Container Manager as a runtime where users can:

- browse container images;
- download images;
- run containers;
- monitor CPU, RAM and network use;
- create multi-container projects;
- manage projects with Compose files.

### Capability interpretation

For the census this supports a `container` execution surface. It means user-selected code can execute in an explicitly supported application environment without replacing DSM firmware.

The record uses `sandboxed` privilege because container execution is not equivalent to host-root control.

### What this does not prove

- host root privilege;
- arbitrary kernel access;
- every Docker/Compose feature;
- every image architecture/runtime combination.

## Source 4 — CPU instruction-set evidence

Source:

- https://www.intel.com/content/www/us/en/products/sku/197307/intel-celeron-processor-j4025-4m-cache-up-to-2-90-ghz/specifications.html

Checked: 2026-09-13

Intel documents the J4025 as:

- 2 cores / 2 threads;
- 2.0 GHz base frequency;
- up to 2.9 GHz burst;
- Intel 64 supported;
- 64-bit instruction set.

This supports the record's `intel_64` architecture description without deriving architecture from the DS220+ marketing category.

## Source 5 — Recovery / DSM reinstallation

Source:

- https://kb.synology.com/DSM/tutorial/How_to_reset_my_Synology_NAS_7

Last updated by Synology: 2026-02-13  
Checked: 2026-09-13

Synology's current reset guide distinguishes at least two physical-reset modes:

- **Mode 1** resets administrator login credentials and network settings;
- **Mode 2** clears system configuration and requires DSM reinstallation.

The guide explicitly states that the reset process does not affect stored data, while strongly recommending backup first.

Separately, Synology's DSM reset-to-default documentation includes an **Erase all data** factory-reset path that deletes user data and returns the system to defaults.

### Recovery interpretation

These are not interchangeable:

| Recovery path | System configuration | Stored user data | Meaning |
|---|---|---|---|
| Mode 1 | Partially reset | Preserved | Credential/network recovery |
| Mode 2 + DSM reinstall | Cleared/reinstalled | Documented as preserved | OS/config recovery |
| Erase-all-data factory reset | Reset | Erased | Destructive return to defaults |

A single boolean such as `factory_reset: true` would erase important operational meaning.

### Schema consequence

Future recovery modeling should preserve at least:

- recovery target/state;
- whether system configuration survives;
- whether user data survives;
- whether application/container state survives or must be recreated.

The last item remains unknown for DS220+ Mode 2 in this record and should not be guessed.

## Fit against the existing low-power registry contract

The DS220+ is an interesting candidate for `low-power-local-registry-node` because current evidence gives it:

- custom container execution;
- 2 GB RAM;
- persistent SATA storage once drives are installed;
- dual Gigabit Ethernet;
- documented recovery;
- manufacturer-measured power below 15 W in the cited access test;
- power recovery / wake / scheduling features.

However the repo should **not** mark it as a contract winner yet because the following remain ungrounded:

- used purchase price in the target region;
- required drive cost;
- exact container autostart behavior after a hard power loss;
- fully offline first-time provisioning/update path;
- actual power and RAM usage of the intended registry workload;
- replacement availability and remaining hardware life.

The product may prove to be a good node, but NAS storage value can also make it unnecessarily expensive for a tiny registry compared with a router or thin client.

## Current unknowns deliberately preserved

- exact motherboard/hardware subrevision;
- host-shell/root execution path in the supported product model;
- container autostart semantics across all failure modes;
- fully offline initial provisioning;
- AXM local power measurements;
- NL/EU used-price distribution;
- drive cost and storage configuration;
- remaining life of used units;
- application/container-state survival through Mode 2 recovery;
- low-level bootloader/serial recovery.

## Next falsifiable tests

1. Collect at least 5–10 dated NL/EU used DS220+ listings and keep bare-chassis price separate from included drives.
2. Price two minimal storage configurations and record whether drive cost destroys the apparent compute bargain.
3. On owned hardware, install a compatible Container Manager release and preserve the package/DSM versions.
4. Run a tiny registry container and measure RAM, CPU and disk footprint.
5. Measure wall power with drives active, idle and hibernated; compare with Synology's published figures.
6. Test hard power loss → Power Recovery → DSM → container restart behavior.
7. Test Mode 2 recovery on noncritical storage and record which application/container state must be rebuilt.
8. Compare total useful cost against Archer C7 v5 and at least one thin client using the same capability contract.

## Root gate

**Truth:** container compatibility and hardware/power claims are manufacturer-documented; local verification remains false.  
**Agency / non-domination:** only owned/authorized NAS hardware and storage should be modified or reset.  
**Continuity:** the execution, lifecycle, power and recovery evidence now lives in repository state rather than temporary chat.  
**Wisdom before speed:** the NAS is not called a bargain until drive cost, market price, power, restart behavior and opportunity cost are counted.
