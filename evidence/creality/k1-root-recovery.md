# Evidence Packet — Creality K1 / Manufacturer-Documented Root SSH and Recovery

**Device record:** `devices/creality/k1.yaml`  
**Checked:** 2026-09-14  
**Local verification:** No  
**Current evidence state:** `DOCUMENTED`

## Why this device matters

The original Creality K1 is the first 3D-printer / manufacturing-appliance record in the census.

It adds a pattern that the earlier records do not isolate cleanly:

```text
stock consumer appliance
  -> user explicitly accepts a root warning
  -> manufacturer exposes root credentials
  -> SSH root access

while the same machine also contains
  -> high-speed motion
  -> a heated fabrication process
```

That means two different questions must remain separate:

> Does the owner have privileged host execution?

and:

> Is an unrelated root-level workload wise to run on this physical appliance?

The first is documented. The second depends on power, memory headroom, restart behavior, opportunity cost, recovery, and physical-safety fit and remains unproven.

## Source 1 — Exact K1 product specification

Manufacturer source:

- https://www.creality.com/products/creality-k1-3d-printer

Checked: 2026-09-14

Creality's exact K1 page documents:

- Creality OS;
- a dual-core 1.2 GHz CPU;
- manufacturer-marketed `8G ROM`;
- printing by USB drive or a data-secure LAN;
- Wi-Fi remote control/monitoring through Creality Print or Creality Cloud;
- CoreXY motion and high-speed printing;
- a ceramic-heated hotend rated up to 300 C;
- a printhead G-sensor used for resonance measurement;
- an 18 W auxiliary chamber fan.

The record preserves `8G ROM` as the manufacturer's storage label. It does not silently translate that into binary MiB, usable free space, or RAM.

The 18 W figure is for one fan. It is not whole-device wall power.

This source does **not** establish:

- CPU architecture;
- RAM size;
- root access;
- arbitrary package compatibility;
- unattended custom-service startup;
- whole-device idle or active power;
- local AXM verification.

## Source 2 — Official K1/K1 Max root account and rollback

Creality official firmware release:

- https://github.com/CrealityOfficial/K1_Series_Klipper/releases/tag/V1.3.2.20

Supporting official Annex:

- https://github.com/CrealityOfficial/K1_Series_Annex

Checked: 2026-09-14

The V1.3.2.20 release is explicitly for K1 and K1 Max. Creality documents a root account/password and the following opt-in path:

```text
Settings
  -> Root Account Information
  -> accept the displayed Warning
  -> obtain root account/password
  -> SSH as root
```

Creality also states that if the warning is not accepted, SSH login to the root account is not permitted.

This is important for the Agency root: privileged access is visible and consent-gated rather than silently enabled.

The same release warns that services such as Moonraker can consume excessive memory and cause system crashes, and says root-related software does not receive Creality technical support even though hardware warranty service may remain.

The release also documents firmware rollback. For K1 it states the earliest rollback version in that release line is `V1.3.1.28`.

The current official K1-Series Annex still lists:

- Fluidd installation/uninstallation;
- Mainsail installation/uninstallation;
- pinout information;
- a root guide;
- the official firmware-recovery-tool.

These sources establish a real manufacturer-documented root execution surface.

They do **not** establish:

- that every future K1 firmware will expose exactly the same root path;
- that every arbitrary binary/package is compatible with the stock userspace;
- that root-added services automatically restart after power loss;
- that root-added state survives rollback;
- AXM local reproduction.

## Source 3 — Manufacturer low-level firmware recovery

Creality official recovery release:

- https://github.com/CrealityOfficial/K1_Series_Annex/releases/tag/V1.0.0

Checked: 2026-09-14

Creality publishes a `firmware-recovery-tool` with English burning instructions for the K1 series.

The documented path requires:

- an external computer;
- a data-capable MicroUSB connection to the printer mainboard;
- physical use of the mainboard `boot` and `reset` buttons;
- detection of an `Ingenic USB BOOT DEVICE`;
- Creality's driver/burning tool;
- loading a `.ingenic` firmware image;
- burning that image to the device.

This is materially stronger recovery evidence than merely having a settings reset.

It is also materially higher-friction than a normal firmware rollback because it requires physical mainboard access and external tooling.

The source does **not** establish:

- that configuration survives;
- that uploaded model files survive;
- that root-added applications/services survive;
- that the procedure has been reproduced by AXM;
- that every later K1 board revision is identical.

The record therefore keeps data-impact fields `unknown`.

## New schema pressure — privileged host authority versus actuator suitability

Earlier records already separated:

```text
application execution
!=
root authority
```

The K1 pressures the opposite side:

```text
root authority exists
!=
every use of that authority is a good deployment
```

The host is attached to a machine whose normal job involves heat and motion.

Therefore capability matching should not silently turn:

```text
root SSH + local networking
```

into:

```text
safe general-purpose always-on compute node
```

without counting at least:

- workload memory headroom;
- whole-device power;
- service restart behavior;
- printer opportunity cost;
- recovery burden;
- interaction with normal printing;
- actuator/safety coupling.

This is not a capability restriction based on fear. It is the Wisdom root requiring the actual physical system to remain visible in the cost model.

## Locality truth boundary

Creality documents that K1 can print from a USB drive or a data-secure LAN. Cloud services are therefore not required for basic print execution.

That supports a `cloud_optional` summary for the documented printing path.

It does **not** prove:

- that every rooted service works fully offline;
- that all provisioning can be completed without WAN;
- that firmware updates are fully offline in every supported path;
- that a custom root workload has been tested with internet blocked.

Those remain explicit unknowns.

## Power and economics truth boundary

No AXM power measurement was performed.

The product page documents component behavior, including an 18 W auxiliary fan and a heated hotend, but those values are not whole-device consumption.

No dated NL/EU acquisition cohort was collected.

Current unknowns include:

- used-market price and replacement supply;
- shipping;
- RAM and practical memory headroom;
- idle and workload wall power;
- provisioning/reprovisioning time;
- unattended boot and custom-service restart;
- hard-power-loss recovery;
- remaining mechanical life;
- opportunity cost of dedicating a working fabrication appliance to unrelated compute.

The K1 therefore does **not** enter the current low-power registry comparison merely because root SSH exists.

## Candidate roles

The strongest evidence-backed roles are `local_fabrication_node` and `rooted_fabrication_controller`.

`general_edge_compute` remains low-confidence. A root shell is a strong execution surface, but capability arbitrage is about total useful cost, not about maximizing privilege.

## Next falsifiable tests

1. On an owned/authorized original K1, preserve exact hardware revision, current firmware, storage state, and root-warning state before changing anything.
2. Reproduce the documented opt-in root flow and record the resulting SSH environment in a local experiment receipt.
3. Measure RAM, free persistent storage, and idle CPU/memory footprint before installing any additional service.
4. Run one harmless local service that does not command heaters or motors, then test WAN-disconnected LAN access.
5. Test normal restart and repeated hard-power-loss -> Creality OS -> custom-service restart without starting a print.
6. Measure wall power at stock idle, rooted-service idle, and normal printing with an appropriate meter; do not substitute component ratings.
7. Exercise normal firmware rollback on noncritical owned state and record exactly what configuration/application state survives.
8. Exercise the low-level recovery tool only when recovery is actually required or on deliberately noncritical owned hardware; preserve the exact board/recovery image/tool version and data impact.
9. Collect a dated NL/EU used-market sample only if this class becomes relevant to a real contract.
10. Compare any compute value against the printer's fabrication opportunity cost rather than treating an already-owned printer as a free server.

## Root gate

**Truth:** manufacturer sources establish root SSH, rollback, USB/LAN printing, and a low-level recovery tool, but do not establish RAM, workload power, custom-service restart, current market price, or AXM local reproduction.  
**Agency / non-domination:** root access is explicitly opt-in through a visible warning and applies only to owned/authorized hardware; privileged access does not justify hidden persistence or unsafe actuator control.  
**Continuity:** exact model scope, firmware line, root admission, rollback, low-level recovery steps, unknown data impact, and source URLs live in repository state.  
**Wisdom before speed:** a rooted printer is not called a cheap server until memory, power, restart behavior, recovery, fabrication opportunity cost, and physical-system coupling are counted.
