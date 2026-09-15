# Evidence Packet — Google Nest Mini (2nd gen) H2C / On-device Local Home SDK Runtime

**Device record:** `devices/google/nest-mini-2nd-gen-h2c.yaml`  
**Exact scope:** Google Nest Mini (2nd generation), model H2C  
**Checked:** 2026-09-15  
**Local verification:** No  
**Current evidence state:** `DOCUMENTED`

## Why this device matters

The Nest Mini H2C adds a genuinely different hardware class to the census: a smart speaker / voice-assistant endpoint whose manufacturer documents a real developer-controlled JavaScript/TypeScript runtime executing on the physical device.

The useful boundary is narrower than “a smart speaker can run code.”

Google's Local Home architecture shows that all of these facts can be true at the same time:

```text
developer-controlled code executes on the Nest Mini
  -> on-device execution locus is real

and

the runtime is a Google-hosted sandbox
  -> not shell/root/native host ownership

and

the app is loaded on demand and may be terminated under memory pressure
  -> not an always-running custom service

and

the integration still depends on Cloud-to-cloud / account-linked state
  -> local execution does not imply WAN-independent end-to-end operation
```

This independently validates the repository's per-surface execution-locus distinction while adding a new lifecycle/admission pressure case.

## Source 1 — Exact model identity and manufacturer hardware specification

Google Store device information:

- https://support.google.com/store/answer/6160585?hl=en-GB

Google Nest/Home specifications:

- https://support.google.com/googlehome/answer/7072284?hl=en-AU

Checked: 2026-09-15

The first page explicitly identifies:

```text
Product: Google Nest Mini (2nd gen)
Model: H2C
Manufacturer: Google LLC
Rated input: AC 100-240 V
Rated power-consumption specification: 15 W
Wi-Fi: 802.11b/g/n/ac, 2.4/5 GHz
Speaker: 40 mm driver
Microphones: three far-field microphones
Port: DC power jack
```

The broader current Nest Mini specification additionally documents:

- Bluetooth 5.0 and Google Cast;
- a quad-core 64-bit ARM CPU at 1.4 GHz;
- a high-performance ML hardware engine;
- capacitive touch controls;
- ultrasound sensing;
- a 15 W power adapter.

### Hardware truth boundary

The sources are sufficient to preserve exact model identity and those manufacturer-listed hardware properties.

They do **not** establish:

- the SoC model;
- RAM amount;
- writable persistent-storage capacity;
- shell, root or administrator access;
- bootloader access;
- hidden/internal service interfaces;
- arbitrary package installation;
- developer access to microphones or ultrasound sensing;
- measured generic idle or active wall power.

The record therefore keeps those fields unknown where the evidence does not carry them.

The Korea-specific regulatory page has a region-specific release-date field. That date is not promoted into a universal global release date for H2C.

## Source 2 — Local Home SDK on-device execution

Google Local Home SDK documentation:

- https://developers.home.google.com/local-home/overview

Checked: 2026-09-15

Google documents that the Local Home SDK lets developers write a local fulfillment application in TypeScript or JavaScript. The page explicitly says supported Google Home or Google Nest devices load and run that app **on-device**.

Its supported-device table lists:

```text
Nest Mini | Speaker | Chrome
```

Google also documents that:

- production local fulfillment runs in a secure JavaScript sandbox on the user's Home/Nest device;
- the Chrome runtime is Chrome M80 or later with ES2018 support;
- the local app can communicate with smart-home devices over the LAN using HTTP, TCP or UDP through the SDK;
- the local app is loaded on demand;
- it may be terminated under memory pressure;
- the platform restarts it when new intents arrive and resources permit;
- it is unloaded after idle/account/device-association conditions described by Google;
- Cloud-to-cloud fulfillment remains the fallback when local fulfillment fails;
- local discovery/fulfillment is linked to the Cloud-to-cloud integration's SYNC/account state.

### Execution truth boundary

This is sufficient to record:

```text
surface: Google Local Home SDK
developer code: TypeScript / JavaScript
locus: on_device
runtime: Chrome sandbox
state: DOCUMENTED
```

It does **not** establish:

```text
root
administrator host access
shell
arbitrary native binaries
bootloader access
persistent always-running service semantics
microphone access from the Local Home app
full WAN-independent Google Assistant operation
```

The machine record therefore uses `custom_code: true`, `locus: on_device`, `privilege: sandboxed`, and preserves the documented demand-loaded lifecycle separately.

## Source 3 — Exact-model EU networked-standby measurement

Google EU ecodesign test summary:

- https://support.google.com/product-documentation/answer/9851803?hl=en

Checked: 2026-09-15

Google's current EU test summary identifies:

```text
Product: Nest Mini (2nd gen)
Model: H2C
Product type: networked equipment, non-HiNA
External power-supply models: G1029 / G1030
Supply output: 14.0 V DC, 1.1 A, 15.4 W
```

For the documented networked-standby condition, Google reports:

```text
Input: 230 V AC, 50 Hz
Test method: EN 50564:2011
Microphone switch: mute

Wi-Fi 2.4 GHz: 1.6 W
Wi-Fi 5 GHz:   1.6 W
Bluetooth:     1.6 W
```

### Power truth boundary

This is useful exact-model power evidence, but the measurement scope must survive intact.

The record preserves the 1.6 W value as a **manufacturer standardized networked-standby result under the stated condition**.

It is **not** relabeled as:

- AXM local measurement;
- generic idle power;
- active audio power;
- Local Home workload power;
- maximum active power.

Likewise, the 15 W / 15.4 W supply rating is not substituted for device self-consumption.

## Source 4 — Official factory reset

Google factory-reset support:

- https://support.google.com/googlehome/answer/7073477?hl=en

Checked: 2026-09-15

Google documents the Nest Mini (2nd gen) reset sequence:

1. switch the microphone off;
2. press and hold the center where the lights are;
3. after about five seconds the reset begins;
4. continue holding for about ten more seconds until confirmation.

The support page states that factory reset returns the speaker/display to factory settings, clears data from the device, and cannot be undone.

### Recovery truth boundary

This establishes a visible user-level factory-reset path and destructive local-data impact.

It does **not** establish:

- downloadable firmware restoration media;
- bootloader recovery;
- recovery from low-level flash corruption;
- restoration of Google Home / Home Graph / developer-cloud account state;
- local reproduction by AXM.

The structured recovery path therefore leaves `application_state` unknown and does not promote `official_restore` beyond the documented factory reset.

## Tweakers NL discovery and market context

Tweakers was deliberately checked for Dutch variant and acquisition context.

### Pricewatch product/variant context

Tweakers Pricewatch:

- https://tweakers.net/pricewatch/1475630/google-nest-mini-wit.html

Checked: 2026-09-15

The page identifies the Google Nest Mini product surface and visible variants including white, white 2-pack and black. It also exposes current retail context and links to the second-hand supply surface.

Evidence scope:

```text
source_surface: tweakers_pricewatch_product
use: variant/specification/retail-context discovery
exact H2C model code visible in the captured product text: no
```

Pricewatch is not converted into a single seller observation or exact-H2C transaction price.

### Vraag & Aanbod leads

The following direct listings were checked as dated NL market leads:

| Listed | URL | Asking price | Visible configuration / condition | Seller account | Seller-class boundary |
|---|---|---:|---|---|---|
| 2026-08-09 16:37 | https://tweakers.net/aanbod/4192160/google-nest-mini-wit-2e-gen.html | €50 | White 2nd gen; `Nieuwstaat`; box + charger stated; Arnhem | Bongoarnhem | Tweakers account listing; private/business status not independently established |
| 2026-08-11 14:17 | https://tweakers.net/aanbod/4154442/google-nest-mini-wit-gen-2.html | €45 each; €120 for 3 stated | White gen 2; three units described as unused/unopened; Zwolle | hzinstaller | Tweakers account listing; private/business status not independently established |
| 2026-08-29 16:15 | https://tweakers.net/aanbod/4205544/google-nest-mini-wit-gen-2.html | €40 | White gen 2; `Goede staat`; Maastricht | Bld- | Tweakers account listing; private/business status not independently established |
| 2026-08-30 20:05 | https://tweakers.net/aanbod/4206446/google-nest-mini-wit.html | €37.50 each | Two `V2` units; adapter + wall mount stated; `Nieuwstaat`; Nieuwpoort | SpoekGTi | Tweakers account listing; private/business status not independently established |

For each observation:

```text
capture mode: direct_listing
source surface: tweakers_vraag_en_aanbod_listing
price type: asking
market: Netherlands
exact H2C model code visible in listing text: no
```

Therefore these observations remain **generation-level acquisition leads**. They are not promoted into `economics.used_price_eur` for the exact H2C record and are not described as completed transaction prices.

No Tweakers user review or forum anecdote is used to promote a positive execution, recovery, power, or compatibility claim. The positive device claims rest on Google documentation.

## Locality and lifecycle boundary

Local Home is genuinely local at one execution step: Google documents the Nest Mini running the local fulfillment code and communicating directly with local smart-home devices over LAN protocols.

But the documented architecture also depends on prior Cloud-to-cloud integration state and retains cloud fulfillment as fallback.

Therefore:

```text
local code execution exists
  !=
whole integration is fully offline

local LAN device control exists
  !=
provisioning is vendor-cloud independent

on-device developer code exists
  !=
developer owns the host OS
```

The top-level locality state remains `unknown` rather than flattening one local path into a global device locality claim.

## Economics boundary

No exact-H2C acquisition cohort was established.

The Dutch listings above are useful because they show active second-hand supply for explicitly named second-generation Nest Mini units, but the captured listing text does not expose model code H2C.

The machine record therefore keeps:

- exact-model used-price low/median/high: unknown;
- transaction price: unknown;
- setup time: unknown;
- replacement availability: unknown;
- `market_data_state: not_collected`.

A later exact-model snapshot can use those listings only if physical/model-code identity becomes recoverable without guessing.

## Local verification status

No AXM local verification was performed.

AXM did **not**:

- inspect a physical H2C unit;
- deploy a Local Home application;
- inspect the production Chrome runtime locally;
- verify cloud fallback behavior;
- test WAN-disconnected end-to-end operation;
- measure RAM or writable storage;
- test cold-power-loss behavior;
- perform the factory reset;
- measure wall power;
- verify that any Tweakers-listed unit is H2C;
- buy or transact on any listing.

The strongest evidence state remains `DOCUMENTED`.

## Census lesson

Nest Mini H2C adds a hardware class and a distinct execution-quality lesson:

```text
on-device custom code
  !=
arbitrary host ownership

on-device custom code
  !=
always-running service

on-device custom code
  !=
WAN-independent system

standardized low networked-standby power
  !=
workload power
```

The Local Home runtime is useful precisely because the evidence is narrow: it is real code on the endpoint, but it remains sandboxed, admitted by Google's integration system and lifecycle-managed by the platform.

This is a stronger capability-arbitrage signal than either extreme story:

```text
"it is only a speaker, so it cannot compute"
```

or

```text
"it runs JavaScript, so it is a tiny general-purpose server"
```

Both would outrun the evidence.

## Root check

**Truth:** exact H2C identity, manufacturer hardware facts, Local Home on-device execution, standardized networked-standby power and factory reset are documented; RAM/storage, arbitrary host authority, WAN-independent operation, workload power, exact-H2C market value and local reproduction remain unknown where unproven.  
**Agency / non-domination:** the documented developer path uses explicit Google developer/account admission and the recovery path is a visible physical owner action; no exploit, hidden persistence or seller contact is involved.  
**Continuity:** execution locus, lifecycle limits, standardized power conditions, exact source URLs, dated Tweakers leads, configuration scope and recovery impact are preserved in repository evidence instead of chat memory.  
**Wisdom before speed:** a 1.6 W standardized standby result and a JavaScript runtime do not make the device a cheap general-purpose server; cloud coupling, admission, persistence, workload fit, recovery and opportunity cost remain part of the comparison.
