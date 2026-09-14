# Evidence Packet — SONOFF BASICR2 / stock eWeLink vs Tasmota

**Device record:** `devices/sonoff/basicr2.yaml`  
**Checked:** 2026-09-14  
**Local verification:** No  
**Current evidence state:** `COMMUNITY_VERIFIED`

## Why this device matters

The BASICR2 is the first smart-home/microcontroller appliance in the census. It is useful for more than category breadth because it independently reproduces the locality problem first exposed by Wyze Cam v2:

```text
same physical hardware
  + stock eWeLink firmware
      -> local LAN on/off control exists after pairing
      -> account/server-backed provisioning and some internet-dependent functions remain

  + Tasmota replacement firmware
      -> direct local WebUI / console / MQTT control
      -> vendor cloud is not required for normal local runtime
```

This second pressure case is structurally different from the Wyze camera: the device is a tiny ESP8285 relay controller rather than an IP camera, and even the stock firmware already has a meaningful LAN mode. That is useful evidence that `locality.states` is not a one-device special case.

## Source 1 — current SONOFF BASICR2 manual and support index

Current manufacturer sources:

- https://sonoff.tech/en-eu/pages/user-manual
- https://cdn.shopify.com/s/files/1/0742/9963/8001/files/User_Manual_BASICR2_RFR2_V1.5.pdf?v=1758190956

Checked: 2026-09-14

SONOFF's current support index still lists **BASICR2** as a **10A WiFi Basic Smart Switch**. The current BASICR2/RFR2 manual documents for BASICR2:

- input/output: 100–240 V AC, 50/60 Hz;
- maximum load: 10 A;
- Wi-Fi: IEEE 802.11 b/g/n, 2.4 GHz;
- stock setup through the eWeLink app;
- quick pairing and compatible pairing modes;
- a feature list that includes **LAN Control**;
- factory reset by deleting the device from the eWeLink app.

The same manual explicitly warns about electric shock and says to consult a dealer or qualified professional for installation/repair.

### What this proves

- exact product identity and electrical/Wi-Fi class;
- stock eWeLink provisioning path;
- LAN control is a manufacturer-listed capability;
- a stock-state factory reset exists;
- mains-voltage work has an explicit manufacturer safety boundary.

### What this does not prove

- Tasmota compatibility;
- measured self-consumption;
- stock recovery after replacement firmware;
- safe user-serviceability while energized.

## Source 2 — exact BASICR2 Tasmota hardware support

Source:

- https://tasmota.github.io/docs/devices/Sonoff-Basic/

Checked: 2026-09-14

Tasmota's exact Sonoff Basic page has a dedicated **Sonoff Basic R2** section. It documents:

- ESP8285 SoC;
- 1 MB flash integrated in that SoC;
- the board's low-voltage serial programming interface;
- known GPIO mapping for the physical button, relay and status LED;
- Basic R2-specific board-layout differences from earlier/later Basic revisions.

This is enough to establish a real replacement-firmware execution path for the exact product family. It is not evidence that BASICR3/BASICR4 or RF variants are interchangeable.

### Safety boundary

The capability record intentionally does **not** reproduce an energized-mains flashing procedure. The unit contains hazardous mains voltage. Any programming/inspection must be done with mains disconnected and an isolated low-voltage programming setup; mains installation/repair belongs under the manufacturer's qualified-professional warning.

## Source 3 — Tasmota local control surface

Sources:

- https://tasmota.github.io/docs/WebUI/
- https://tasmota.github.io/docs/MQTT/
- https://tasmota.github.io/docs/Getting-Started/

Checked: 2026-09-14

Tasmota documents a WebUI reached directly by the device's IP address. The WebUI provides device control, configuration and a console. Tasmota also documents MQTT configuration where the broker host is a user-selected address/IP; that broker can live on the same LAN.

After flashing, Tasmota's normal initial Wi-Fi configuration can be performed through the device's own local access point.

### What this proves

- local administration/control exists without an eWeLink vendor cloud;
- the relay can participate in a local MQTT automation fabric;
- the persistent replacement-firmware state has materially different locality from stock.

### What this does not prove

- safe public-WAN exposure;
- encrypted MQTT on the normal ESP8285 build;
- enough resource headroom for arbitrary workloads;
- current market value or power use.

## Source 4 — stock eWeLink LAN behavior

Sources:

- https://help.ewelink.cc/hc/en-us/articles/360027586291--eWeLink3-5-10-LAN-feature-updated
- https://ewelink.cc/does-my-ewelink-device-support-lan/

Checked: 2026-09-14

eWeLink documents LAN mode for supported switch/socket classes. When the phone and device are on the same Wi-Fi network, supported devices can remain controllable locally even if public internet connectivity is lost. eWeLink also states that LAN is preferred over WAN for supported devices.

The same documentation preserves an important boundary: schedules, scenes, sharing and some other setup operations still require internet access.

The exact BASICR2 manufacturer manual independently lists **LAN Control**, connecting this generic eWeLink behavior to the product rather than assuming every eWeLink device supports it.

### Locality interpretation

The stock state should therefore **not** be simplified to either extreme:

```text
stock BASICR2 is fully cloud required   # false/too strong
stock BASICR2 is fully local            # also too strong
```

The supported statement is capability-scoped:

```text
stock paired state:
  local LAN on/off control can survive WAN loss
  while some account/setup/automation functions still depend on internet/server services
```

## Source 5 — stock pairing/server path

Sources:

- https://help.ewelink.cc/hc/en-us/articles/360052454912-Crack-the-codes-of-pairing-failure
- https://help.ewelink.cc/hc/en-us/articles/7224516410393-Permissions-Requested-by-eWeLink

Checked: 2026-09-14

eWeLink's pairing troubleshooting explicitly discusses registering/connecting the device through eWeLink servers, and its permissions documentation describes device registration in the eWeLink app and servers.

This is why the stock locality entry records a cloud/server provisioning dependency while separately preserving post-pairing LAN control.

## Recovery interpretation

The manufacturer stock reset is clear:

```text
stock eWeLink firmware
  -> delete device in eWeLink
  -> documented factory settings / pairing state
```

But the gathered evidence does **not** establish this transition:

```text
Tasmota firmware
  -> stock eWeLink firmware
```

Tasmota proves that the firmware can be replaced; it does not provide, in the sources gathered for this record, an official BASICR2 stock image or a tested generic return-to-stock receipt.

That path remains `unknown`. The repo must not silently turn `stock factory reset exists` into `replacement firmware is reversible`.

## Second locality-state pressure case

Wyze Cam v2 was the first case:

```text
stock camera firmware -> cloud-centred with narrow offline recording
Thingino              -> local RTSP / ONVIF / WebUI / SSH
```

BASICR2 independently produces:

```text
stock eWeLink         -> partial LAN locality after cloud-backed provisioning
Tasmota               -> local WebUI / console / LAN MQTT without vendor cloud runtime
```

The common structure is now strong enough to mechanically validate the optional `locality.states` extension when a device record uses it:

- unique state-entry IDs;
- explicit persistent `device_state`;
- a bounded locality classification;
- evidence truth state;
- evidence-claim references that resolve within the same record.

This does **not** mean every existing device should be rewritten into multiple locality states. Flat locality remains valid where the evidence does not need state-dependent modeling.

## Economics and power truth boundary

No dated NL/EU used-price sample was collected. No AXM self-consumption measurement was performed.

The 100–240 V / 10 A values in the manual are electrical/load ratings, **not** evidence that the device consumes 10 A and not a substitute for idle/active watts.

Economics remains `not_collected`; power remains unknown/unmeasured.

## Candidate roles

Evidence supports:

- local Wi-Fi relay;
- local MQTT actuator under Tasmota;
- tiny smart-home edge controller.

The record does not promote BASICR2 into a general registry/server node simply because firmware ownership exists. One megabyte of flash, unknown RAM, mains coupling and the value of the relay's original function all count against that leap.

## Next falsifiable tests

1. On an owned/authorized unit, identify the exact BASICR2 board while fully disconnected from mains.
2. Record stock firmware/app version and verify stock LAN on/off control with WAN deliberately unavailable after normal pairing.
3. Before replacement, determine whether a trustworthy unit-specific stock-firmware preservation/restore path exists; if not, count that as modification cost.
4. Reproduce Tasmota installation only with the unit isolated from mains and preserve tool/firmware hashes.
5. Verify local WebUI and LAN-MQTT relay control with outbound internet blocked.
6. Test repeated cold power loss -> Tasmota boot -> Wi-Fi -> local control, including relay power-on-state behavior.
7. Measure self-consumption only with an appropriate safe mains measurement method; do not probe an exposed energized board.
8. Collect a dated NL/EU price sample if the device is later compared against other actuator nodes.

## Root gate

**Truth:** stock LAN capability, server-backed provisioning, Tasmota execution and unresolved return-to-stock are kept separate.  
**Agency / non-domination:** owned/authorized hardware only; no bypass of account/device ownership is part of this research.  
**Continuity:** the exact sources, firmware states, recovery unknown and safety boundary are preserved in repository state.  
**Wisdom before speed:** mains hazard and uncertain stock recovery are treated as real costs; replacement firmware capability does not erase them.
