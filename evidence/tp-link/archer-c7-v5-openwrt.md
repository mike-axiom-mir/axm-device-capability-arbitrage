# Evidence Packet — TP-Link Archer C7 v5 / OpenWrt

**Device record:** `devices/tp-link/archer-c7-v5.yaml`  
**Evidence state:** `COMMUNITY_VERIFIED`  
**Locally reproduced by AXM:** No  
**Checked:** 2026-09-13

## Why this packet exists

A Wi-Fi router is already closer to a computer in human intuition than a camera, but product-category thinking still tends to reduce it to "network appliance."

The capability-first view is more useful:

```text
QCA9563 CPU
+ 128 MB RAM
+ 16 MB flash
+ 5x Gigabit Ethernet
+ dual-band Wi-Fi
+ USB 2.0
+ U-Boot
+ serial
+ full OpenWrt Linux environment
+ TFTP recovery
```

That makes the device a candidate general-purpose low-power node for workloads that fit its resource envelope.

## Exact hardware support

Primary source:

- https://openwrt.org/toh/hwdata/tp-link/tp-link_archer_c7_v5

The OpenWrt Techdata record for the exact Archer C7 v5 reports:

- target `ath79/generic`;
- package architecture `mips_24kc`;
- U-Boot bootloader;
- Qualcomm Atheros QCA9563 CPU;
- one CPU core at 750 MHz;
- 16 MB flash;
- 128 MB RAM;
- five Gigabit Ethernet ports;
- dual-band Wi-Fi using QCA9563 + QCA9880;
- one USB 2.0 port;
- 3.3 V serial at 115200 8N1;
- current OpenWrt install/upgrade images;
- TP-Link TFTP as the documented recovery method.

## Execution surface

Sources:

- https://openwrt.org/
- https://openwrt.org/docs/guide-user/additional-software/opkg

OpenWrt describes itself as a Linux operating system for embedded devices with a writable filesystem and package management.

For this project the important point is that the router does not merely have a hidden processor. A maintained operating environment exposes that processor to user-controlled software.

This supports:

- Linux userspace execution;
- root administration under the normal OpenWrt model;
- package installation;
- local services;
- persistent configuration;
- network-facing applications constrained by the device's RAM/flash/CPU.

## Recovery evidence

Sources:

- https://openwrt.org/toh/hwdata/tp-link/tp-link_archer_c7_v5
- https://openwrt.org/toh/tp-link/archer_c7

OpenWrt documents TFTP installation/restore for the v5 hardware.

The documented flow uses the bootloader TFTP client and a specifically named recovery image.

This is strategically important to capability arbitrage: a cheap device with a known recovery path can be materially more useful than an equally cheap device with an opaque boot chain.

## Claims supported

`COMMUNITY_VERIFIED`:

- exact Archer C7 v5 hardware is supported by OpenWrt;
- custom Linux userspace execution is available after OpenWrt installation;
- the device has 128 MB RAM and 16 MB flash;
- the device provides five Gigabit Ethernet ports, dual-band Wi-Fi and USB 2.0;
- U-Boot/TFTP recovery is documented for the exact target.

## Claims not yet established here

- real idle/active wattage;
- used-market price in the Netherlands or another target region;
- remaining hardware lifespan for old used units;
- performance of a specific AXM workload;
- reliability of external USB storage over long unattended periods;
- whether every retail-region variant behaves identically beyond the v5 scope documented by OpenWrt.

## Candidate roles

High/medium-value hypotheses to test:

- mesh/network relay;
- heartbeat/watchdog;
- tiny registry/index;
- deterministic worker;
- local API bridge;
- small provenance/logging service;
- sensor-network gateway;
- USB-attached storage/cache with appropriate caution.

The role list is not proof that every workload fits 128 MB RAM.

## Next tests

1. Collect dated used-market price snapshots.
2. Measure real idle and loaded power.
3. Define one tiny registry workload and measure RAM/flash use.
4. Test power-loss recovery and filesystem state.
5. Measure repeated provisioning time from stock → OpenWrt → workload.
6. Compare total useful cost against a cheap thin client, TV box and mini PC.
7. Test whether USB storage improves the role enough to justify its added failure surface.

## Root check

**Truth:** exact v5 scope is preserved; unknown cost/power remain unknown.  
**Agency:** deployment assumes owned/authorized router hardware.  
**Continuity:** firmware/recovery sources and device facts are preserved in-repo.  
**Wisdom before speed:** the record does not call the router "cheap" until market, power and provisioning friction are measured.
