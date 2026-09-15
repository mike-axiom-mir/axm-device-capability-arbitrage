# Execution Locus Method — v0.1

**Status:** Evidence-backed research method, intentionally not yet a frozen schema extension.  
**Checked:** 2026-09-15  
**Purpose:** Prevent a developer extension surface from being silently promoted into on-device custom-code execution when the developer-controlled code actually runs somewhere else.

---

## 1. Why this distinction exists

A product can expose a real programming/developer surface without executing the developer's code on the physical device itself.

That creates a separate question from privilege, application admission, locality, or update persistence:

> **Where does the developer-controlled code actually execute?**

The repository already distinguishes application execution from root authority, and local runtime from vendor-cloud dependence. This method adds a narrower truth boundary for platforms where the human-facing device is an endpoint into a remotely executed extension system.

A useful first vocabulary for research is:

```text
on_device
remote_service
split
unknown
```

These labels are research descriptors only for now. Do not bulk-migrate existing device records and do not make them mandatory after one pressure case.

---

## 2. Core rule

A documented extension, plugin, skill, action, automation, or integration surface does **not** prove on-device custom-code execution by itself.

Before a capability contract treats a device as a custom-code host, identify the execution locus of the developer-controlled logic.

```text
user can create an extension
  !=
developer code runs on the endpoint device

cloud service receives endpoint requests
  -> developer-controlled behavior is real
  -> endpoint may still be programmable in a product sense
  -> on-device arbitrary/custom execution remains unproven
```

Do not solve this ambiguity by setting `custom_code: true` on the physical endpoint unless exact evidence proves that some developer-controlled code actually executes there.

Likewise, do not set `custom_code: false` for the entire physical machine merely because one supported extension model is remote. A remote extension architecture does not prove that no other local execution surface exists.

The safe state is often:

```text
supported developer extension: documented
extension execution locus: remote_service
on-device custom-code execution: unknown / not established by this evidence
```

---

## 3. First pressure case — Amazon Echo Dot (5th Generation), C2N6L4

This device is **not being added to the census in this activation**. The point of the case is to pressure the research model without forcing a misleading device record.

### Exact hardware identity

Amazon's safety/compliance page identifies:

```text
Device Name: Echo Dot (5th Generation)
Model: C2N6L4
Connectivity: dual-band 2.4/5 GHz Wi-Fi, 802.11a/b/g/n/ac, Bluetooth/BLE
Power adapter output: 12 VDC, 1.25 A, 15 W
```

Primary source, checked 2026-09-15:

- https://digprjsurvey.amazon.com/csad/help/node/TR7RlV0WehGNoLYxKM

Truth boundary:

- the 15 W figure is an **adapter output rating**, not a measured device idle/load value;
- it must not be copied into `idle_watts` or `active_watts`;
- CPU, RAM, persistent-storage size, privilege, bootloader access and arbitrary local execution are not established by this source.

### Provisioning and cloud boundary

Amazon's exact-generation setup page says setup requires an Amazon account and an internet connection/Wi-Fi, and uses the Alexa app. It also states that when the blue indicator is active, Alexa is listening and processing the request in Amazon's secure cloud.

Primary source, checked 2026-09-15:

- https://digprjsurvey.amazon.com/csad/help/node/TdLI5SX5VhnxC6x6Ct

This supports a documented account/internet dependency for normal setup and cloud processing for Alexa requests. It does **not** prove that every hardware function is unavailable offline, so a future device record should not flatten the whole endpoint into `offline_operation: false` without a broader exact-model locality study.

### Developer extension architecture

Amazon's Alexa Skills Kit documentation is explicit that a custom skill's developer-controlled service is cloud-based. Amazon documents two supported hosting patterns:

- AWS Lambda; or
- an HTTPS web service endpoint.

Alexa sends requests to that service; the service code performs the developer logic and sends a response back.

Primary sources, checked 2026-09-15:

- https://developer.amazon.com/en-US/docs/alexa/custom-skills/host-a-custom-skill-as-an-aws-lambda-function.html
- https://developer.amazon.com/en-US/docs/alexa/custom-skills/understanding-custom-skills.html
- https://developer.amazon.com/en-US/docs/alexa/build/build-your-skill-overview.html

Therefore the supported custom-skill path establishes:

```text
Echo / Alexa endpoint
  -> captures/mediates user interaction
  -> Alexa service invokes developer endpoint
  -> developer-controlled skill logic executes in Lambda or HTTPS service
  -> response returns through Alexa
```

It does **not** establish:

```text
custom skill code executes on C2N6L4 itself
shell / SSH / ADB on C2N6L4
root or administrator host authority
local package installation
boot persistence for user code
WAN-independent custom-skill operation
```

This is the key model pressure:

> **A programmable user experience can be real while the developer's program does not run on the endpoint hardware.**

### Recovery boundary

Amazon documents two visible reset paths for Echo Dot generations including the 5th Generation:

- Action button for 20 seconds: reset while keeping smart-home connections, then enter setup mode;
- Volume Down + Microphone Off for 20 seconds: factory reset, erase personal information plus device/smart-home connections, then enter setup mode.

Amazon also states that deregistration erases device settings.

Primary source, checked 2026-09-15:

- https://digprjsurvey.amazon.com/csad/help/node/GK84VTU42NKF2E8E

This is useful recovery evidence, but it does not establish low-level firmware restore media, bootloader recovery, preservation of every cloud-side skill/account object, or AXM local reproduction.

---

## 4. Tweakers NL/EU discovery context

Tweakers Pricewatch is useful here as a Netherlands-facing product/variant and retail-context cross-check.

Checked 2026-09-15:

- https://tweakers.net/pricewatch/2303014/amazon-echo-dot-5e-generatie-blauw.html
- https://tweakers.net/speakers/amazon/echo-dot-5e-generatie_p1664480/vergelijken/

Observed scope:

```text
surface: Tweakers Pricewatch
use: variant/specification/retail-context discovery
family shown: Echo Dot (5e generatie)
visible variants: blue / white / black
visible specification context: Alexa, Wi-Fi a/b/g/n/ac, mains power, adapter included
```

Do **not** convert the currently displayed retailer offers on those aggregate Pricewatch pages into a used-market acquisition cohort or transaction-price claim. The existing market-snapshot vocabulary represents individual observations; Pricewatch remains supporting context until a dedicated aggregate/history representation exists.

No exact Echo Dot 5th Generation Vraag & Aanbod observation was collected in this activation. Do not substitute a different Echo generation/model merely to create a used-price sample.

---

## 5. Research checklist for extension-capable endpoints

When a device advertises skills, plugins, actions, integrations, webhooks, apps, macros, or automations, ask these separately:

1. **Endpoint identity** — exact model/revision and current software state.
2. **Extension authoring** — can a third party create behavior at all?
3. **Execution locus** — endpoint, remote service, split, or unknown?
4. **Admission** — who approves/enables the extension?
5. **Privilege** — what authority does the extension have on the endpoint, if any?
6. **Transport dependency** — does the extension require WAN/vendor infrastructure?
7. **Persistence** — what survives reboot, update, account/session expiry, or vendor-side removal?
8. **Recovery** — how are endpoint state and remote extension state independently restored or removed?
9. **Economics** — account, hosting, subscription, network and maintenance cost belong in total useful cost when the developer logic is remote.
10. **Local verification** — only a physical/authorized experiment receipt can promote endpoint-local behavior to local verification.

---

## 6. Capability-contract consequence

A future matcher should not satisfy an on-device execution requirement from a remote extension alone.

Example:

```text
contract requires:
  local custom-code execution
  WAN-independent runtime

platform proves only:
  custom skill backed by Lambda / HTTPS service

result:
  extension capability = real
  local host requirement = not proven
```

For a different contract such as `voice endpoint for a remotely hosted workflow`, the same device may be a legitimate candidate. Capability arbitrage depends on the goal, not on whether the extension sounds like an "app."

---

## 7. Why the Echo Dot is not counted yet

The current census counting rule asks for a meaningful execution-surface finding. The C2N6L4 research clearly exposes a meaningful **developer extension** surface, but the existing v0.1 device shape can easily be read as though `execution.surfaces` describes code executing on the recorded physical machine.

Counting this device immediately by calling Alexa Skills `custom_code: true` would therefore create a false local-host implication.

For now:

```text
exact hardware identity: documented
supported remote extension system: documented
remote developer-code locus: documented
on-device custom-code execution: not established
recovery paths: documented
local verification: none
market cohort: not collected
census status: intentionally not counted yet
```

A second independent hardware/platform case with the same execution-locus problem would justify testing the smallest reusable additive schema shape. Until then, preserve the pressure without freezing the schema.

---

## 8. Root gate

**Truth** — do not turn a remote skill/plugin/backend into on-device custom execution; do not turn a power-adapter rating into measured consumption; unknown endpoint privilege remains unknown.  
**Agency / non-domination** — extension/account enrollment remains explicit and user-visible; do not seek hidden persistence or unauthorized access to endpoints.  
**Continuity** — preserve exact model, source URLs, checked dates, execution locus, cloud dependency and recovery boundaries in repo state rather than hidden chat context.  
**Wisdom before speed** — a remote extension can be useful, but cloud/account/hosting/network dependency and recovery burden are part of total useful cost; do not count a device simply to increase census volume.

---

## 9. One-line rule

> **A developer can control behavior through a device without their code executing on that device; record the execution locus before calling the endpoint a custom-code host.**
