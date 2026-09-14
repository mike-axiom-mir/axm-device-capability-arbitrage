# Evidence Packet — Valve Steam Deck LCD 256 GB / SteamOS Execution, Persistence, and Recovery

**Device record:** `devices/valve/steam-deck-lcd-256gb.yaml`  
**Checked:** 2026-09-14  
**Local verification:** No  
**Current evidence state:** `DOCUMENTED`

## Why this device matters

The 256 GB LCD Steam Deck is the first console / handheld-gaming record in the census.

It provides a manufacturer-supported general Linux execution environment rather than an exploit path:

```text
SteamOS 3
  -> KDE Plasma desktop
  -> Flatpak applications on writable storage
  -> optional sudo elevation after explicit password setup
  -> user-accessible BIOS / multi-boot / microSD boot
  -> official SteamOS recovery tooling
```

The new schema pressure is not whether custom code can run. Valve documents that clearly.

The pressure is that **execution authority and persistence across vendor OS updates are different capabilities**.

```text
Flatpak application
  -> Valve says it lives on the writable part of the disk
  -> intended not to be broken by future SteamOS system updates

software installed outside Flatpak
  -> sudo / read-only-image modification can be enabled by the owner
  -> Valve warns that such software may be wiped by a later SteamOS update
```

A future matcher must therefore avoid treating `root` as if it automatically implied durable deployment state.

## Source 1 — Valve LCD Steam Deck technical specifications

Manufacturer source:

- https://www.steamdeck.com/en/tech/deck

Configuration comparison:

- https://www.steamdeck.com/en/deck

Checked: 2026-09-14

Valve's LCD technical page documents:

- a 7 nm AMD APU;
- Zen 2 CPU, 4 cores / 8 threads, 2.4-3.5 GHz;
- 8 RDNA 2 compute units at up to 1.6 GHz;
- manufacturer APU power envelope of 4-15 W;
- 16 GB LPDDR5 memory at 5500 MT/s;
- LCD storage configurations including 256 GB;
- a high-speed microSD slot;
- 7-inch 1280x800 IPS LCD;
- Wi-Fi 5 and Bluetooth 5.0;
- USB-C with DisplayPort 1.4 Alt Mode and USB 3.2 Gen 2;
- 40 Wh battery;
- 45 W USB-C power supply;
- SteamOS 3, described as Arch-based;
- KDE Plasma desktop.

Valve's current Deck comparison identifies the **256 GB LCD** configuration specifically as having a 256 GB NVMe SSD, 7-inch LCD, 7 nm APU, Wi-Fi 5, 40 Wh battery and 45 W power supply.

### Power truth boundary

The following are **not** AXM whole-device power measurements:

- `4-15 W` — Valve's APU power envelope;
- `45 W` — the supplied power-adapter rating.

Neither value is written to `idle_watts` or `active_watts`.

No wall-power, charging-loss, battery-condition or always-on test was performed.

### Configuration truth boundary

This record is for:

> **Steam Deck LCD, 256 GB configuration**

It must not silently transfer configuration-specific fields to:

- 64 GB LCD;
- 512 GB LCD;
- 512 GB OLED;
- 1 TB OLED;
- later or special hardware revisions.

The technical page covers the LCD hardware family while the current Deck comparison identifies the 256 GB configuration. That scope remains explicit in the device record.

## Source 2 — Valve Desktop FAQ: Flatpak, writable state, sudo, and update persistence

Manufacturer support source:

- https://help.steampowered.com/en/faqs/view/671A-4453-E8D2-323C

Checked: 2026-09-14

Valve documents a normal Desktop Mode and explains that Flatpak is used to install and run applications on the writable part of the disk.

Valve explicitly says this arrangement is intended so those applications are not broken by future SteamOS system updates.

Valve also documents the higher-privilege path:

1. the default Deck user ships without a password;
2. the owner can set a password with `passwd`;
3. after that, `sudo` is available where elevation is required;
4. if an owner needs to edit the read-only system image, Valve documents `sudo steamos-readonly disable`.

This is strong manufacturer evidence of privileged local execution.

It is equally important that Valve warns:

- arbitrary commands/scripts can damage the device or data;
- software installed outside Flatpak, for example through `pacman`, may be wiped by the next SteamOS update.

Therefore the record keeps these as different properties:

```text
privilege
!=
update persistence
```

It does **not** claim that a root-installed service survives every SteamOS update.

The FAQ also documents adding desktop applications to Steam as non-Steam applications for launch from the Deck interface.

## Source 3 — Valve FAQ: BIOS, multi-boot, microSD boot, and repair supply

Manufacturer FAQ:

- https://www.steamdeck.com/en/faq

Checked: 2026-09-14

Valve states that:

- users have access to the BIOS menu;
- multi-boot is supported;
- an operating system can boot from microSD;
- replacement parts and repair guides are available through Valve's iFixit collaboration.

For the census, the first three items are direct execution/recovery evidence.

The repair-parts statement is useful supply evidence, but it is **not** converted into a claim about current NL used-unit replacement availability or remaining hardware life. Those remain unknown until market/reliability evidence is collected.

## Source 4 — SteamOS recovery and previous-OS rollback

Manufacturer support source:

- https://help.steampowered.com/en/faqs/view/1B71-EDF2-EB6D-2BB3

Checked: 2026-09-14

Valve documents multiple recovery choices, including:

- factory reset;
- rollback to a previous known-good OS;
- erasing local user data;
- reinstall/re-image/repair paths.

Valve describes the previous-OS rollback as retaining user data.

The record therefore models this as a separate recovery path instead of flattening all recovery into `factory_reset: true`.

It does **not** infer that every application, service, privileged modification, package or configuration survives rollback.

## Source 5 — Official SteamOS recovery image, repair, and destructive re-image

Manufacturer support source:

- https://help.steampowered.com/en/faqs/view/65B4-2AA3-5F37-4227

Checked: 2026-09-14

Valve publishes an official SteamOS recovery image and documents preparing an 8 GB or larger USB drive.

Its recovery environment includes:

### Re-image Device

Valve describes this as a complete factory reset that erases:

- user information;
- installed games;
- applications;
- operating systems;

and replaces them with stock SteamOS.

The record therefore marks user/application/configuration state destructive for this path.

### Repair SteamOS

Valve says this reinstalls SteamOS while **attempting** to preserve games and personal content.

Because the source uses that qualified wording, the device record does not upgrade it into a guarantee that all custom application/configuration state is preserved.

### Recovery tools

Valve also documents access to tools that can modify the boot partition.

No AXM recovery path was locally reproduced.

## New schema pressure — privilege is not persistence

Earlier records established distinctions such as:

```text
application execution
!=
root authority

root authority
!=
physical-actuator suitability
```

The Steam Deck adds:

```text
root authority
!=
update-stable deployment
```

The same physical device has at least two manufacturer-documented execution patterns:

```text
Flatpak on writable storage
  -> lower privilege
  -> explicit manufacturer statement about surviving normal SteamOS system updates

sudo / non-Flatpak system modification
  -> higher privilege
  -> manufacturer warning that installed state may be removed by an update
```

This matters for capability arbitrage because a registry, relay, service or agent may value **persistence and recoverability** more than maximum privilege.

One device is enough to preserve the lesson but not enough to freeze a universal new schema. The record therefore carries an additive `update_persistence` note on each execution surface while the core schema remains v0.1.

## Locality truth boundary

The Steam Deck is a general Linux computer with local applications, local storage and local boot paths.

That does not make every part of the Steam commercial ecosystem fully offline.

This record does not claim:

- all initial provisioning works without internet;
- all games run without online licensing;
- package acquisition is offline;
- every Flatpak has no network dependency;
- every Steam account feature is local.

The summary remains `local_after_provisioning` / partial offline rather than `fully_local`.

## Arbitrage boundary

The device is **not** added to the current low-power registry comparison.

It has far more general compute than the router candidate, but the comparison still lacks:

- measured whole-device wall power under the common workload;
- battery and charging behavior for always-on use;
- service autostart after unexpected power loss;
- repeated hard-power-loss recovery;
- provisioning time;
- used-market cohort;
- battery/SSD remaining-life evidence;
- opportunity cost of consuming a useful handheld gaming PC.

Capability abundance alone is not arbitrage.

## Explicit unknowns retained

No AXM local test was performed.

Still unknown:

- exact unit hardware revision;
- whole-device idle and workload power;
- used NL/EU acquisition cohort;
- battery health;
- SSD wear/health;
- provisioning time;
- arbitrary-service autostart;
- hard-power-loss restart reliability;
- survival of arbitrary privileged modifications across SteamOS updates;
- application-state survival across rollback/repair;
- remaining hardware life.

These unknowns are intentional.
