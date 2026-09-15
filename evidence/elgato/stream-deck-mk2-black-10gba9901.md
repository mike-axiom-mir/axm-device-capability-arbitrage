# Evidence Packet — Elgato Stream Deck MK.2 Black / Companion-host programmability

**Device record:** `devices/elgato/stream-deck-mk2-black-10gba9901.yaml`  
**Exact scope:** Elgato Stream Deck MK.2 - Black, retail SKU 10GBA9901; documented Mk.2 HID identity 20GBA9901 / VID 0x0FD9 / PID 0x0080  
**Checked:** 2026-09-15  
**Local verification:** No  
**Current evidence state:** `DOCUMENTED`

## Why this device matters

This device adds a hardware class that looks programmable from the user's perspective while forcing a more precise capability boundary underneath:

```text
custom behavior exists
  -> plugins can implement arbitrary host-side logic
  -> keys report input
  -> host can upload images/configuration to the peripheral

but

developer plugin code is documented on the companion computer
  -> not proven on the Stream Deck endpoint
```

That makes the Stream Deck MK.2 useful capability-arbitrage evidence even though it is not an autonomous compute node. The machine is a programmable **host-attached control/display endpoint**, and its required companion host is part of the real system cost and continuity story.

## Source 1 — Exact retail SKU and black MK.2 product identity

Elgato regional MSRP table:

- https://www.elgato.com/pl/pl/s/elgato-product-msrps-by-region

Elgato current Stream Deck product page:

- https://www.elgato.com/eu/en/p/stream-deck

Checked: 2026-09-15

The manufacturer MSRP table explicitly maps:

```text
10GBA9901 -> Stream Deck MK.2 - Black
10GBA9911 -> Stream Deck MK.2 - White
```

The current 15-key Stream Deck product page for SKU `10GBA9901` documents:

```text
15 customizable LCD keys
USB 2.0
USB-C to USB-C cable
Windows/macOS companion software path
```

### Identity truth boundary

This is sufficient to scope the retail configuration to the black 15-key MK.2 SKU.

It does **not** establish the endpoint SoC, CPU architecture, RAM, writable storage, firmware layout, shell/root authority, or wall/USB power use.

## Source 2 — Exact USB HID identity and host-controlled I/O

Elgato Stream Deck HID API, Classic family:

- https://docs.elgato.com/streamdeck/hid/stream-deck-classic/

Checked: 2026-09-15

Elgato documents the 15-key Classic family as USB 2.0 input devices that communicate with the host through USB HID for:

- key-event reporting;
- image upload;
- device configuration.

The device table distinguishes:

```text
Stream Deck Mk.2
  HID model: 20GBA9901
  VID: 0x0FD9
  PID: 0x0080

Stream Deck Mk.2 (Scissor Keys)
  HID model: 20GBL9901
  VID: 0x0FD9
  PID: 0x00A5
```

### Identity-namespace boundary

The manufacturer uses different identifiers for different purposes:

```text
retail SKU:        10GBA9901
HID protocol model: 20GBA9901
USB identity:       0x0FD9 / 0x0080
```

Those identifiers are preserved side by side rather than treated as a contradiction or silently collapsed into one field.

The Scissor Keys variant is explicitly outside this record because its documented HID model/PID differs.

## Source 3 — Where the developer-controlled plugin code runs

Elgato Stream Deck SDK plugin environment:

- https://docs.elgato.com/streamdeck/sdk/introduction/plugin-environment/

Checked: 2026-09-15

Elgato states that a Stream Deck plugin is hosted entirely on the user's local machine and that hardware communication is managed by the Stream Deck app.

For the physical Stream Deck device record, the grounded execution shape is therefore:

```yaml
custom_code: false
locus: remote_service
remote_kind: companion_host
```

That wording does **not** deny programmability. It preserves where the developer logic actually executes.

The hardware still has a useful bidirectional surface:

```text
key press -> host event
host -> key/display image upload
host -> device configuration
```

But those host-control capabilities do not prove that arbitrary developer code executes on the endpoint processor.

### Capability-arbitrage consequence

A future matcher must count the companion computer and Stream Deck software as dependencies for the official plugin path. The endpoint should not satisfy a contract that requires autonomous on-device custom execution merely because the overall product experience is programmable.

## Source 4 — Firmware-update maintenance and brick-risk boundary

Elgato firmware-update documentation:

- https://help.elgato.com/hc/en-us/articles/4412175612429-Elgato-Stream-Deck-Update-Device-Firmware

Checked: 2026-09-15

Elgato documents firmware updates through Stream Deck software and warns that if a firmware update does not complete correctly, the Stream Deck device may stop functioning. The instructions say not to disconnect the device or shut down the computer while the update is in progress.

This establishes:

```text
official firmware-update path: yes
documented update failure / nonfunctional-device risk: yes
```

It does **not** establish:

```text
official low-level unbrick image
rescue bootloader
arbitrary firmware flashing
USB restore from arbitrary corruption
AXM local recovery reproduction
```

The record therefore keeps physical firmware recovery unknown while preserving the documented brick risk.

## Source 5 — Host-side profile backup/restore is not device firmware recovery

Elgato profile backup/restore documentation:

- https://help.elgato.com/hc/en-us/articles/360048424432-Elgato-Stream-Deck-How-to-Back-Up-and-Restore-Profiles

Checked: 2026-09-15

Elgato documents creating and importing backups of Stream Deck profiles in the companion software. This is useful continuity for the human's configuration state.

The documentation also treats missing plugins separately: profile backup is not the same thing as bundling/restoring the plugin software itself.

Therefore:

```text
host profile backup/restore
  !=
physical-device firmware recovery

host profile continuity
  !=
endpoint execution continuity without the companion host
```

## Netherlands/EU evidence — Tweakers

Tweakers was deliberately used as a Dutch discovery/market layer. None of the Tweakers material below is promoted into endpoint execution or recovery truth.

### Pricewatch — exact named retail variant

Tweakers Pricewatch:

- https://tweakers.net/pricewatch/1723656/elgato-stream-deck-mk2-classic-keys-zwart.html

Tweakers family comparison:

- https://tweakers.net/toetsenborden/elgato/stream-deck-mk2_p1291392/vergelijken/

Checked: 2026-09-15

The exact Pricewatch page identifies:

```text
Elgato Stream Deck MK.2
variant: Classic Keys, Zwart
category presentation: macro keyboard
keys: 15
connection: wired USB 2.0 Type-C
```

The captured exact-product page showed current retail offers beginning at **EUR 134.40**. The family comparison separately exposes three variants:

```text
Classic Keys, Zwart
Scissor Keys, Zwart
Classic Keys, Wit
```

Evidence scope:

```text
source_surface: Tweakers Pricewatch
use: variant/specification cross-check + dated retail context
price_type: current displayed retailer offer
not: completed transaction price
not: permanent device economics
```

The displayed shop count/lowest price is dynamic market data and must be rechecked at any later ranking attempt.

### Vraag & Aanbod — one dated exact-named asking-price observation

Direct listing:

- https://tweakers.net/aanbod/4203478/elgato-stream-deck-mk2-classic-keys-zwart.html

Listing date/time shown by Tweakers:

```text
2026-08-26 17:21
```

Captured observation:

```text
model/configuration: Elgato Stream Deck MK.2, Classic Keys, Zwart
asking_price_eur: 80
shipping: excluded
condition: Nieuwstaat
warranty: no
description: Stream Deck MK.2 including box and cables
seller account: LOWLVND
seller location: 4902 VJ Oosterhout, Netherlands
seller_class: unknown
seller_class_basis: the listing exposes account name/history/rating/location but does not explicitly classify the seller as private, business or dealer
evidence_scope: one asking-price observation, not a transaction and not a market distribution
```

The listing does not expose retail SKU `10GBA9901` or HID model/PID in the captured text. Therefore its exact-name match is useful acquisition evidence, but it is not used as proof of those lower-level identifiers.

No contact, purchase or transaction was performed.

### Tweakers community thread — secondary failure-mode lead only

Tweakers community thread:

- https://gathering.tweakers.net/forum/list_messages/2179934

Original post date: 2023-03-20  
Resolution post date: 2023-03-21  
Checked: 2026-09-15

A user reported a Stream Deck becoming unusable through the companion software after a Windows/software change, and later reported the issue was caused by a Citrix Workspace software conflict.

Evidence scope is intentionally narrow:

```text
source_surface: Tweakers community/forum
model/revision: not established in the thread excerpt
value: secondary lead that companion-host software conflicts can matter operationally
promotion_to_verified_device_truth: no
```

This anecdote is **not** used to assert a MK.2 defect, compatibility rule, recovery method, or general failure rate. The stronger architectural fact—that the plugin and hardware communication path depend on companion-host software—rests on Elgato's own SDK documentation.

## Power boundary

No credible endpoint consumption measurement was collected in this activation.

The manufacturer documents USB connectivity, but this packet does not convert a USB standard, cable, port rating, or host capability into device watts.

Therefore:

- idle watts: unknown;
- active watts: unknown;
- local measurement: none;
- always-on suitability: unknown.

## Locality boundary

The official plugin runtime is local to the companion computer, and physical hardware communication is local through the Stream Deck app/USB path.

That does not establish that:

- Stream Deck software installation/provisioning is fully offline;
- Marketplace/plugin acquisition is cloud-independent;
- every plugin works without WAN access;
- endpoint behavior is independent of the companion process;
- the device is useful as an autonomous node when the host is absent.

The top-level locality state therefore remains `unknown`.

## Economics boundary

The Pricewatch data is useful live retail context and the Vraag & Aanbod record is one dated asking-price observation. Neither is enough for a stable exact-unit used-price distribution.

The machine record therefore keeps:

- used low/median/high: unknown;
- new permanent price: unknown;
- transaction price: unknown;
- replacement availability: unknown;
- `market_data_state: not_collected`.

More importantly, a capability-arbitrage calculation for the official plugin path must not price only the Stream Deck. A compatible companion computer, Stream Deck software state, USB attachment and host maintenance/recovery are dependencies of the programmable system.

## Local verification status

No AXM local verification was performed.

AXM did **not**:

- inspect a physical 10GBA9901 unit;
- confirm its physical USB VID/PID locally;
- capture HID traffic;
- install or execute a Stream Deck plugin;
- test companion-host failure/restart behavior;
- update firmware;
- corrupt or recover firmware;
- create/restore a profile backup;
- measure USB or wall power;
- verify offline behavior;
- contact or purchase the Tweakers listing.

The strongest evidence state remains `DOCUMENTED`.

## Census lesson

This device adds a distinct class and a useful model pressure:

```text
programmable product behavior
  !=
endpoint custom-code execution

local companion-host plugin
  !=
autonomous local appliance

profile backup
  !=
endpoint firmware recovery

cheap peripheral asking price
  !=
cheap standalone capability
```

The required companion host is not an incidental accessory when the target capability depends on it. It is part of the composition that must be counted in total useful cost, power, failure/restart behavior and recovery.

## Root check

**Truth:** exact retail SKU, HID identity, USB host-control surface, companion-host plugin locus, firmware-update risk and host-profile backup behavior are documented; endpoint compute resources, endpoint developer execution, low-level recovery, power and offline autonomy remain unknown where unproven.  
**Agency / non-domination:** the researched paths are manufacturer-supported host software/HID/developer interfaces on owned or authorized hardware; no exploit, hidden persistence, seller contact or unauthorized access is involved.  
**Continuity:** retail SKU, HID model/VID/PID, source URLs, check dates, variant exclusions, Tweakers seller-class boundary, community-evidence scope and recovery limits are preserved in repo evidence rather than chat memory.  
**Wisdom before speed:** a programmable EUR 80 asking-price peripheral is not called an autonomous cheap computer; companion-host cost, software dependency, power, restart behavior and recovery remain part of capability value.
