# Remote Execution Kind Gate

**Status:** Active additive method + CI gate  
**Checked:** 2026-09-15  
**Scope:** `execution.surfaces[]` entries whose `locus` is `remote_service`

## Why this exists

`EXECUTION_LOCUS_METHOD.md` already prevents a programmable product surface from being mistaken for developer-controlled code running on the physical endpoint.

One remaining ambiguity is materially important for capability arbitrage:

```text
developer code runs somewhere other than the endpoint
```

can mean either:

```text
developer code runs on a local companion computer
```

or:

```text
developer code runs in an internet/cloud service
```

Those are not operationally equivalent.

A companion-host surface may still work with a directly attached or locally controlled machine, while a cloud-hosted surface can add WAN, account, service-continuity, latency, privacy and long-term vendor dependencies. Neither proves code execution on the endpoint itself.

The repository therefore keeps the existing `locus: remote_service` value and adds one narrow classifier when that locus is used.

## Machine-readable extension

When an execution surface declares:

```yaml
locus: remote_service
```

it must now also declare:

```yaml
remote_kind: companion_host
```

Allowed values are:

```text
companion_host
cloud_service
other_remote
unknown
```

Semantics:

- `companion_host` — the developer-controlled logic runs on a separate companion machine, such as the user's PC or another local controller, rather than on the recorded endpoint;
- `cloud_service` — the developer-controlled logic runs in an internet-accessible/cloud service;
- `other_remote` — off-endpoint execution is established, but the execution host does not fit the two named classes;
- `unknown` — off-endpoint execution is established but the kind of remote host is not.

`remote_kind` is invalid on `on_device`, `split`, or `unknown` locus entries. `split` is intentionally not forced into one `remote_kind`: a split surface may later need to preserve more than one off-endpoint component.

This is an additive classifier. It does not change the existing rule that a `remote_service` surface must not promote physical-endpoint `custom_code` to true.

## Pressure case A — Elgato Stream Deck MK.2

The useful discovery is not “Stream Deck is programmable.” The manufacturer documents where that programmability executes.

### Exact product/configuration boundary

Elgato's current EU product page, checked 2026-09-15:

- https://www.elgato.com/eu/en/p/stream-deck

It identifies the current black Classic Keys 15-key product with:

```text
retail SKU: 10GBA9901
keys: 15 customizable LCD keys
interface: USB 2.0
cable: USB-C to USB-C
host software: Stream Deck for Windows/macOS
```

Elgato's HID API, checked 2026-09-15:

- https://docs.elgato.com/streamdeck/hid/stream-deck-classic/

identifies the Stream Deck Classic family and distinguishes:

```text
Stream Deck Mk.2
  protocol model: 20GBA9901
  USB VID: 0x0FD9
  USB PID: 0x0080

Stream Deck Mk.2 (Scissor Keys)
  protocol model: 20GBL9901
  USB VID: 0x0FD9
  USB PID: 0x00A5
```

The same API says the 15-key devices communicate with the host through USB HID for key-event reporting, image upload and device configuration.

The retail SKU and HID protocol model are therefore preserved as different identity namespaces. They must not be silently treated as contradictory identifiers, and the Scissor Keys variant must not be collapsed into the Classic Keys black configuration.

### Where the developer code runs

Elgato's plugin-environment documentation, checked 2026-09-15:

- https://docs.elgato.com/streamdeck/sdk/introduction/plugin-environment/

states that a Stream Deck plugin is hosted entirely on the user's local machine and that hardware communication is managed by the Stream Deck app. It documents the application-layer plugin logic as a host-side Node.js runtime.

For this developer surface the grounded shape is:

```yaml
custom_code: false
locus: remote_service
remote_kind: companion_host
```

within the **physical Stream Deck device record**.

That does not deny programmability. It preserves where the programmable logic executes.

The HID protocol also establishes useful host-controlled I/O on the peripheral. It still does not prove that user plugin code executes on the Stream Deck's internal processor.

### Recovery/continuity boundary

Elgato's firmware-update documentation, checked 2026-09-15:

- https://help.elgato.com/hc/en-us/articles/4412175612429-Elgato-Stream-Deck-Update-Device-Firmware

documents firmware updates through Stream Deck Software and explicitly warns that an interrupted update can leave the device nonfunctional. That is a maintenance/update path, not proof of a low-level recovery image, rescue bootloader or locally reproduced unbrick procedure.

Elgato's profile backup/restore documentation, checked 2026-09-15:

- https://help.elgato.com/hc/en-us/articles/360048424432-Elgato-Stream-Deck-How-to-Back-Up-and-Restore-Profiles

documents host-side profile backup and restoration. Imported backups overwrite existing profiles, and profile backups do not themselves contain copies of plugins.

That is useful configuration continuity on the companion host. It must not be promoted into physical-device firmware recovery.

No AXM physical Stream Deck was inspected in this activation. No firmware update, profile restore, USB capture, power measurement or local plugin deployment was performed.

## Netherlands/EU discovery evidence — Tweakers

Tweakers was used deliberately as a Dutch market/variant discovery layer, not as proof of execution architecture.

### Pricewatch variant context

Exact URL, checked 2026-09-15:

- https://tweakers.net/pricewatch/1723656/elgato-stream-deck-mk2-classic-keys-zwart.html

Observed scope:

```text
product: Elgato Stream Deck MK.2
variant: Classic Keys, Zwart
category presentation: macro keyboard with 15 keys
displayed retail context: from EUR 134.40
retailer count shown: 14 shops
```

The corresponding Tweakers family comparison, checked 2026-09-15:

- https://tweakers.net/toetsenborden/elgato/stream-deck-mk2_p1291392/vergelijken/

separates:

```text
Classic Keys, Zwart
Scissor Keys, Zwart
Classic Keys, Wit
```

Evidence scope: variant/specification and dated retail-discovery context only. This is not a transaction-price sample and is not promoted into permanent device economics.

### Vraag & Aanbod observation

Exact URL:

- https://tweakers.net/aanbod/4203478/elgato-stream-deck-mk2-classic-keys-zwart.html

Listing observation preserved from the page:

```text
listed_at: 2026-08-26 17:21
model/configuration: Elgato Stream Deck MK.2, Classic Keys, Zwart
asking_price_eur: 80
shipping: excluded
condition: Nieuwstaat
warranty: no
included per description: box and cables
seller account: LOWLVND
seller location: 4902 VJ Oosterhout, Netherlands
seller_class: unknown
seller_class_basis: the listing exposes an account name, history, rating and location but does not explicitly classify the seller as private, business or dealer
evidence_scope: one dated asking-price observation; not a transaction price, not a market distribution, and not proof of HID model/SKU identity unless those identifiers are explicitly present in the listing
```

No seller-class inference is made from account age, karma, listing count, wording or location.

No Tweakers community anecdote is promoted into device truth in this method.

## Pressure case B — Alexa custom skills

Amazon's current custom-skill documentation, checked 2026-09-15:

- https://developer.amazon.com/en-US/docs/alexa/custom-skills/host-a-custom-skill-as-an-aws-lambda-function.html
- https://www.developer.amazon.com/en-US/docs/alexa/custom-skills/host-a-custom-skill-as-a-web-service.html
- https://www.developer.amazon.com/en-US/docs/alexa/custom-skills/understanding-custom-skills.html

documents developer-controlled custom-skill logic in AWS Lambda or an HTTPS web service. The web-service path must be internet-accessible.

For that surface the grounded classifier is:

```yaml
custom_code: false
locus: remote_service
remote_kind: cloud_service
```

inside a physical Alexa endpoint record.

The contrast with Stream Deck is the reason for the new field:

```text
same high-level locus: off-endpoint
different operational dependency:
  Stream Deck plugin -> companion_host
  Alexa custom skill -> cloud_service
```

## Mechanical gate

`tools/validate_remote_execution_kind.py` enforces:

- every `locus: remote_service` surface has `remote_kind`;
- the value is one of the bounded four tokens;
- `remote_kind` cannot appear on a non-`remote_service` locus.

`tools/test_remote_execution_kind.py` covers companion-host, cloud-service, bounded-other and uncertainty-preserving cases plus missing/invalid/misplaced classification failures.

The existing execution-locus gate remains responsible for `custom_code`, `source_claim_ids`, truth-state and linked-evidence-strength rules. This gate does not duplicate those semantics.

## What this gate does not prove

Passing this check does not establish:

- that the remote code can actually perform a target workload;
- that a companion-host path works offline;
- that a cloud service is available indefinitely;
- endpoint root, shell or arbitrary package execution;
- endpoint power use;
- endpoint recovery;
- exact market value;
- local AXM reproduction.

Those remain separate evidence questions.

## Root check

- **Truth:** “programmable” no longer hides whether developer logic is on the endpoint, a companion computer, or a cloud service.
- **Agency / non-domination:** local companion execution and externally hosted service dependence remain visible to the user instead of being collapsed.
- **Continuity:** the dependency type survives in machine-readable state and can later affect matching without reconstructing chat context.
- **Wisdom before speed:** a seemingly useful programmable peripheral or assistant is not ranked as an autonomous node until its real execution dependency is counted.
