# Research Case — MF800 / bkovac/modem-thing

**Checked:** 2026-09-22  
**Status:** Grounded external arbitrage case; **not promoted into the 25-device census**  
**Primary upstream:** https://github.com/bkovac/modem-thing  
**Upstream snapshot checked:** 29259d33e30e93672ca529ad273bd90b660f8148 (2026-09-17)  
**Upstream write-up:** https://bkovac.github.io/modem-thing/

## Why this belongs here

This is an unusually clean example of capability arbitrage through an **already-integrated donor platform**.

The project starts from a cheap MF800-class 4G hotspot rather than from a conventional SBC. The source project reports that the selected unit already combines:

~~~text
MSM8916-class compute
+ stock Android
+ ADB access
+ EDL reflashing path
+ 4G modem
+ Wi-Fi
+ Bluetooth
+ battery + charging hardware
+ stock display hardware
+ USB
+ accessible PCB signals
~~~

The creator then turns that substrate into a Linux handheld by adding a physical keyboard, a Sharp memory display, a small adapter PCB, kernel/display-driver work, and a custom enclosure.

The important arbitrage lesson is not "build this exact texting device." It is:

> **Mass-produced consumer hardware can contain a bundle of already-integrated capabilities whose acquisition cost is lower than rebuilding the same substrate from separate hobbyist modules.**

That bundle can include power management, battery charging, radios, antennas, USB, enclosure mechanics, boot/recovery paths and a general-purpose SoC before any new parts are added.

## What the upstream project directly demonstrates

The checked upstream project documents a concrete build around an MF800 hotspot and preserves source code, board files, 3D enclosure models, driver patches, scripts and a long build report.

Grounded findings from that project include:

- the selected MF800 unit is described as MSM8916-based;
- the stock device runs Android;
- ADB is available on the author's unit and can be used to reach EDL/reflash workflow;
- the author explicitly recommends preserving important original partitions before reflashing;
- OpenStick is used as the Linux enablement path;
- the running Android device tree was extracted and used as hardware-discovery evidence;
- the stock display SPI/power signals were mapped and tested before the replacement display was integrated;
- the project uses a Clicks keyboard as a standard USB keyboard once connected to the host;
- a custom adapter PCB provides USB host/device role support, VBUS/VBAT switching, 5 V boost, display power and signal-level conversion;
- named adapter-PCB parts include TUSB320, SN74LVC8T245, MCP1640 and TPS22917 devices;
- the Sharp memory display is connected through SPI;
- the author first validated the display path with small test scripts, then moved to a DRM kernel driver;
- the driver path is based on ardangelo/sharp-drm-driver;
- the author's checked kernel path uses an MSM8916 Linux 6.12.1 configuration;
- project patches add build compatibility, dithering, and a later memory-leak fix;
- the dither implementation exposes Atkinson for video and Floyd-Steinberg for still images;
- the repository preserves STEP enclosure files and helper-PCB design files;
- the final physical build includes a 4G flex antenna and SIM installation.

This is strong enough to treat the build as COMMUNITY_VERIFIED evidence for **this documented project configuration**, not for every product sold under an MF800 label.

## Physical-integration lessons

The project exposes several details that matter when reusing cheap integrated hardware.

### 1. Device tree as a capability map

The creator extracted the running Android device tree and used it to identify SPI pins, power supplies and other hardware relationships.

General lesson:

~~~text
working vendor firmware
  -> inspect/extract hardware description
  -> map candidate interfaces
  -> verify electrically/software-side
  -> only then modify
~~~

A shipping firmware image can therefore be useful evidence even when the goal is to replace that firmware.

### 2. Integration can be worth more than the SoC

The hotspot's value is not merely its processor. The useful donor substrate is the integrated combination of compute, battery, charger/power path, radios, USB and board-level routing.

For arbitrage research, record the **integration bundle** separately from raw CPU/RAM specifications.

### 3. Host/device and power roles are real adaptation costs

The helper PCB exists because repurposing a USB-capable consumer device into a handheld host is not just a connector problem. The project needed role detection/switching, power switching, voltage boost and signal-level conversion.

This is exactly the kind of hidden adaptation cost that can erase a sticker-price advantage if it is ignored.

### 4. High-speed signals punish casual wiring

The project reports a USB enumeration problem that changed when the data-pair wiring was tightened/twisted. That is a useful reminder that a logical interface being present does not make an improvised physical interconnect reliable.

### 5. "Working once" is not maturity

The creator later found a memory leak in the display-driver path and added a fix after hands-on use.

Capability records should therefore keep these separate:

~~~text
proof of execution
!=
stable daily operation
!=
repeatable deployment
~~~

## Current limitations preserved from the source

The source also preserves important negative state instead of presenting the build as finished.

At the checked snapshot:

- sleep is the largest unresolved issue;
- convenient power-button behavior is unfinished;
- battery percentage logic is not fully implemented at the kernel/user boundary described;
- charging through the keyboard passthrough is reported to require the device to be booted;
- the creator explicitly says the software side is still being ironed out through use;
- physical finish/reliability still has temporary elements such as glue/tape and enclosure cleanup;
- the project should not be read as evidence that every MF800 unit is electrically identical;
- the project is not evidence of current NL/EU market price or long-term supply at the author's approximately-$20 acquisition level;
- real idle/active power, battery runtime, suspend reliability, unattended boot and long-term modem behavior are not established here;
- the project does not establish an AXM workload result.

These unknowns matter because this repository studies **total useful cost**, not novelty alone.

## Why this is not a census record yet

The current census requires an exact model identity and disciplined scope.

The public project uses the model label MF800, but the checked material does not establish:

- a manufacturer identity;
- a stable hardware-revision identifier;
- whether all marketplace MF800 listings use the same board/SoC/debug paths;
- a dated multi-listing market cohort;
- exact unit-to-unit compatibility boundaries.

Promoting "MF800" directly into the 25-device census would risk turning one well-documented unit/project into an unsupported product-family claim.

This case therefore remains a **research reference** until a purchasable unit can be identified tightly enough for the normal device-record contract.

## New discovery heuristic — integrated-substrate arbitrage

When scanning surplus/cheap hardware, ask two questions instead of one.

First:

> What execution surface can we reach?

Second:

> What expensive integration work has mass production already done for us?

Useful pre-integrated capabilities may include:

- battery and charger;
- regulators and power sequencing;
- cellular/Wi-Fi/Bluetooth radios;
- antennas;
- SIM/eSIM path;
- USB PHY/connector;
- display and backlight;
- buttons;
- microphones/speakers;
- sensors;
- enclosure;
- thermal solution;
- boot/recovery hardware;
- factory-tested board assembly.

A cheap donor becomes especially interesting when several of those are useful to the target goal and the execution/recovery path is evidenced.

## Scouting checklist derived from this case

For future hotspot/modem/router/phone-class donor hardware, collect:

1. exact board/model/revision photographs or identifiers;
2. SoC and architecture;
3. RAM and persistent storage;
4. stock OS and debug surfaces such as ADB/UART;
5. recovery path such as EDL, bootloader, removable media or vendor flashing;
6. whether original partitions/images can be backed up;
7. mainline/community Linux support;
8. USB host/device capability;
9. exposed SPI/I2C/UART/GPIO or test pads;
10. battery/charger/power-management reuse potential;
11. radio availability under replacement software;
12. hardware-variant consistency across listings;
13. required adapter PCB/components;
14. destructive mechanical changes;
15. measured power and suspend behavior;
16. repeated provisioning time;
17. dated regional market supply;
18. whether a useful role can be achieved without destroying more original value than the arbitrage saves.

## Cost-model consequence

This case suggests tracking an **integration dividend** as a descriptive concept:

~~~text
integration dividend
  = useful hardware integration already included in donor
    that would otherwise need separate parts/design/assembly
~~~

Do **not** turn this into fake savings by subtracting imaginary retail BOM prices.

Instead preserve:

- which integrated capabilities are actually useful;
- which extra parts are still required;
- adaptation/provisioning labor;
- destructive work;
- recovery burden;
- repeatability;
- supply/variant uncertainty.

The donor is only an arbitrage win when the useful integrated bundle still wins after those costs are counted.

## Provenance and license boundary

No upstream code, PCB design, STEP model, photo or article text is vendored by this research note.

Upstream license map at the checked snapshot:

- patches/: GPL-2.0-or-later;
- docs/: CC BY 4.0;
- enclosure/ and helper-pcb/: CERN-OHL-P-2.0;
- remaining upstream scripts/code: MIT.

If AXM later imports or adapts upstream artifacts, preserve the applicable upstream license and attribution at the file/artifact boundary rather than assuming this repository's root license applies to third-party material.

## Sources

Primary:

- https://github.com/bkovac/modem-thing
- https://github.com/bkovac/modem-thing/tree/29259d33e30e93672ca529ad273bd90b660f8148
- https://bkovac.github.io/modem-thing/

Referenced upstream projects from the build:

- https://github.com/OpenStick/OpenStick
- https://github.com/ardangelo/sharp-drm-driver

Secondary discovery/coverage:

- https://blog.adafruit.com/2026/09/15/converting-a-20-4g-wireless-hotspot-into-a-texting-device/
- https://hackaday.com/2026/09/19/a-hotspot-becomes-a-handheld/

## Root check

**Truth:** one creator's documented MF800 project is not generalized into every MF800 listing; current price, power and unit consistency remain unknown.  
**Agency:** the technique is framed for owned/authorized donor hardware and visible modification.  
**Continuity:** upstream commit, sources, license boundary, negative findings and derived heuristics are preserved.  
**Wisdom before speed:** the approximately-$20 donor price is treated as a lead, not as proof that the finished capability is cheap after adapter hardware, labor, recovery and reliability are counted.
