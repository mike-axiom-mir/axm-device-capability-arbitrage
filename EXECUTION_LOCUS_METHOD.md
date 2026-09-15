# Execution Locus Method — v0.2

**Status:** Evidence-backed additive v0.1 schema extension; optional, mechanically gated when present.  
**Checked:** 2026-09-15  
**Purpose:** Prevent a developer extension surface from being silently promoted into on-device custom-code execution when the developer-controlled code actually runs somewhere else.

---

## 1. Why this distinction exists

A product can expose a real programming/developer surface without executing the developer's code on the physical device itself.

That creates a separate question from privilege, application admission, locality, or update persistence:

> **Where does the developer-controlled code actually execute?**

The repository already distinguishes application execution from root authority, and local runtime from vendor-cloud dependence. Execution locus is narrower: it describes where the developer-controlled logic for one execution surface actually runs.

Two independent platform families now pressure the same distinction:

- Amazon Alexa custom skills: developer logic is hosted in AWS Lambda or an HTTPS service rather than being established as code running on the Echo endpoint;
- Google Home / Nest smart-home integrations: Cloud-to-cloud fulfillment runs in a developer cloud, while Local Home SDK can run a developer JavaScript/TypeScript fulfillment app on supported Google Home or Nest devices, including Nest Mini.

That independent repetition is enough to test the smallest reusable additive machine field without forcing older records to migrate.

---

## 2. Optional machine-readable field

Execution locus belongs to an individual execution surface, not to the device globally:

```yaml
execution:
  surfaces:
    - type: local_home_sdk
      environment: chrome_sandbox
      custom_code: true
      locus: on_device
      privilege: sandboxed
      state: DOCUMENTED
```

Allowed values:

```text
on_device
remote_service
split
unknown
```

Semantics:

- `on_device` — the evidence establishes that developer-controlled code for this surface executes on the recorded physical device;
- `remote_service` — the developer-controlled logic for this surface executes somewhere else; the endpoint may mediate input/output but this surface does not establish endpoint custom-code execution;
- `split` — the documented surface contains both endpoint-local and remote developer-controlled execution as one coupled path;
- `unknown` — the developer extension exists, but the evidence does not establish where its developer-controlled logic executes.

`locus` is optional. Existing records remain valid without it. Do not bulk-migrate records merely to fill the field.

### `custom_code` relation

Within a physical-device record, `custom_code` continues to mean developer/user-controlled code executing on that recorded device.

Therefore, when `locus` is present:

```text
locus: on_device     -> custom_code must be true
locus: split         -> custom_code must be true
locus: remote_service -> custom_code must not be true
locus: unknown       -> custom_code must not be true
```

This is intentionally conservative. A remote webhook is real programmable behavior, but it must not satisfy a capability contract that requires local code execution on the endpoint.

The mechanical gate is `tools/validate_execution_locus.py`; its regression test is `tools/test_execution_locus.py`.

---

## 3. Core truth rule

A documented extension, plugin, skill, action, automation, integration, or webhook does **not** prove on-device custom-code execution by itself.

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

Do not solve this ambiguity by setting `custom_code: true` unless exact evidence proves that some developer-controlled code actually executes on the recorded physical device.

Likewise, proving one remote extension path does **not** prove that the whole physical machine lacks every possible local execution surface. Keep unresearched surfaces unknown.

---

## 4. First pressure case — Amazon Echo Dot (5th Generation), C2N6L4

This device is **not counted in the census** from this research alone. The point of the case is to preserve the difference between a programmable user experience and endpoint-local execution.

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

- the 15 W figure is an adapter/output rating, not a measured idle/load value;
- it must not be copied into `idle_watts` or `active_watts`;
- CPU, RAM, persistent-storage size, privilege, bootloader access and arbitrary local execution are not established by this source.

### Provisioning and cloud boundary

Amazon's exact-generation setup page says setup requires an Amazon account and an internet connection/Wi-Fi, and uses the Alexa app. It also says Alexa requests are processed in Amazon's cloud.

Primary source, checked 2026-09-15:

- https://digprjsurvey.amazon.com/csad/help/node/TdLI5SX5VhnxC6x6Ct

This supports account/internet dependency for normal setup and cloud processing for Alexa requests. It does **not** prove that every hardware function is unavailable offline.

### Developer extension architecture

Amazon's Alexa Skills Kit documentation says a custom skill's developer-controlled service is hosted through either:

- AWS Lambda; or
- an HTTPS web service endpoint.

Primary sources, checked 2026-09-15:

- https://developer.amazon.com/en-US/docs/alexa/custom-skills/host-a-custom-skill-as-an-aws-lambda-function.html
- https://developer.amazon.com/en-US/docs/alexa/custom-skills/understanding-custom-skills.html
- https://developer.amazon.com/en-US/docs/alexa/build/build-your-skill-overview.html

The supported custom-skill path therefore establishes:

```text
Echo / Alexa endpoint
  -> captures or mediates interaction
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

For this surface, the grounded execution-locus descriptor is `remote_service`.

### Recovery boundary

Amazon documents two visible reset paths for Echo Dot generations including the 5th Generation:

- Action button for 20 seconds: reset while keeping smart-home connections, then enter setup mode;
- Volume Down + Microphone Off for 20 seconds: factory reset, erase personal information plus device/smart-home connections, then enter setup mode.

Primary source, checked 2026-09-15:

- https://digprjsurvey.amazon.com/csad/help/node/GK84VTU42NKF2E8E

This does not establish low-level firmware restore media, bootloader recovery, preservation of every cloud-side object, or AXM local reproduction.

---

## 5. Second pressure case — Google Nest Mini (2nd generation), H2C

This second independent vendor/platform case justifies making `execution.surfaces[].locus` an optional additive field that is mechanically validated when present.

It does **not** by itself justify bulk migration of older records or a universal claim that every Google/Nest extension executes locally.

### Exact hardware identity and power boundary

Google's device-information page identifies the Google Nest Mini (2nd gen) as model `H2C`. Google also documents the Nest Mini's 802.11b/g/n/ac Wi-Fi, Bluetooth 5.0, 40 mm driver, three far-field microphones, quad-core 64-bit ARM CPU at 1.4 GHz, and a 15 W power adapter.

Primary sources, checked 2026-09-15:

- https://support.google.com/store/answer/6160585?hl=en-GB
- https://support.google.com/googlehome/answer/7072284?hl=en-AU

Truth boundary:

- the 15 W value is a rated consumption / adapter specification, not a locally measured idle or active result;
- the generic device specification does not establish root, shell, bootloader access, arbitrary native package installation, unattended custom service persistence, or writable storage capacity available to developer code.

### Remote developer execution — Cloud-to-cloud

Google's Cloud-to-cloud smart-home model requires a developer-provided cloud fulfillment/webhook for smart-home intents. Google's documentation describes Assistant sending intents to the developer's fulfillment and the developer cloud acting on the target device.

Primary sources, checked 2026-09-15:

- https://developers.home.google.com/cloud-to-cloud/primer/intents
- https://developers.home.google.com/codelabs/smarthome-local

For that path:

```text
Google Assistant / Home surface
  -> Google cloud
  -> developer cloud fulfillment/webhook
  -> target smart-home device or hub
```

The developer-controlled fulfillment code is therefore `remote_service` with respect to the Nest Mini endpoint.

### On-device developer execution — Local Home SDK

Google's Local Home SDK documentation independently establishes a different path. It says developers can write a local fulfillment app in TypeScript or JavaScript containing smart-home business logic, and that supported Google Home or Google Nest devices can load and run that app **on-device**. The supported-device table explicitly includes `Nest Mini` with a Chrome execution environment.

Google also documents that the local app communicates with local smart devices over LAN protocols and that cloud fulfillment remains a fallback if the local path fails.

Primary source, checked 2026-09-15:

- https://developers.home.google.com/local-home/overview

Supporting codelab, checked 2026-09-15:

- https://developers.home.google.com/codelabs/smarthome-local

This establishes a real on-device developer-code surface for the supported Nest Mini platform:

```text
Local Home SDK app
  -> JavaScript / TypeScript developer logic
  -> loaded into supported Nest Mini runtime
  -> executes in Chrome sandbox on the device
  -> communicates to local smart devices over LAN
```

It does **not** establish:

```text
root or administrator host authority
arbitrary native binaries
persistent always-running service semantics
microphone access from the Local Home app
bootloader access
full WAN-independent Google Assistant operation
locally measured power
```

Google explicitly documents lifecycle limits: the local fulfillment app is loaded on demand and may be terminated because the device is memory constrained; the platform restarts it when new intents arrive and resources permit. Execution authority and service persistence must therefore remain separate.

### Why this is a stronger second case

The same supported product family exposes both:

```text
Cloud-to-cloud fulfillment -> remote_service
Local Home SDK fulfillment -> on_device
```

And the production architecture can use the cloud path as fallback when the local path fails.

Therefore execution locus is not safely modeled as one device-wide property. It belongs to the execution surface or integration path.

---

## 6. Tweakers NL/EU discovery and market boundary

Tweakers remains useful here for Dutch variant and market discovery, but its evidence role stays bounded.

### Exact-generation used-market lead

Vraag & Aanbod listing checked 2026-09-15:

- https://tweakers.net/aanbod/4192160/google-nest-mini-wit-2e-gen.html

Observed listing facts:

```text
surface: Tweakers Vraag & Aanbod
listing date: 2026-08-09 16:37
seller class: private community seller
location: Arnhem, Netherlands
advertised product: Google Nest Mini white, 2nd generation
condition: Nieuwstaat
asking price: EUR 50
shipping: excluded
included by description: box and charger
exact H2C model code shown in listing: no
```

This is a useful dated generation-level market observation, but it is **not** promoted into exact-model economics because the listing text does not expose model code `H2C`. Asking price is also not transaction-price truth.

Tweakers product-family context:

- https://tweakers.net/serie/11168/nest/

That surface is useful for variant/retail discovery, not as a substitute for one seller observation or a completed transaction.

Tweakers community anecdotes may still provide failure-mode or hidden-interface leads, but none are used here to establish positive execution-locus truth. The positive locus claims rest on Google developer documentation.

---

## 7. Recovery boundary for the second case

Google's factory-reset support page documents the Nest Mini (2nd gen) reset sequence: microphone off, press the center for five seconds to begin reset, then continue for about ten more seconds until confirmation.

Primary source, checked 2026-09-15:

- https://support.google.com/googlehome/answer/7073477

This is an official user-level reset path. It does **not** establish low-level firmware restoration, bootloader recovery, developer-project/account recovery, or preservation of cloud-side integration state. A future census record must keep those separate.

---

## 8. Research checklist for extension-capable endpoints

When a device advertises skills, plugins, actions, integrations, webhooks, apps, macros, or automations, ask separately:

1. **Endpoint identity** — exact model/revision and current software state.
2. **Extension authoring** — can a third party create behavior at all?
3. **Execution locus** — endpoint, remote service, split, or unknown?
4. **Admission** — who approves/enables the extension?
5. **Privilege** — what authority does the extension have on the endpoint, if any?
6. **Transport dependency** — does the extension require WAN/vendor infrastructure?
7. **Persistence** — what survives reboot, update, account/session expiry, memory pressure, or vendor-side removal?
8. **Recovery** — how are endpoint state and remote extension state independently restored or removed?
9. **Economics** — account, hosting, subscription, network and maintenance cost belong in total useful cost when developer logic is remote.
10. **Local verification** — only a physical/authorized experiment receipt can promote endpoint-local behavior to local verification.

---

## 9. Capability-contract consequence

A matcher must not satisfy an on-device execution requirement from a remote extension alone.

Example:

```text
contract requires:
  local custom-code execution
  WAN-independent runtime

platform proves only:
  remote webhook / cloud fulfillment

result:
  programmable extension = real
  local host requirement = not proven
```

A different contract such as `voice endpoint for a remotely hosted workflow` may legitimately accept the same remote surface.

For a supported Nest Mini Local Home SDK surface, on-device JavaScript execution is documented, but that still does not prove WAN-independent end-to-end operation, always-on service persistence, root authority, arbitrary native code, or sufficient resource headroom for an unrelated workload.

Capability arbitrage depends on the exact goal, not on whether the extension sounds like an "app."

---

## 10. Migration rule

The two independent cases justify an additive field, not a migration campaign.

Use `locus` when:

- a new or edited record has evidence that materially depends on where developer code runs;
- an existing execution surface would otherwise be easy to misread as endpoint-local;
- a capability comparison depends on local-vs-remote execution.

Do not add it when evidence is weak merely to make records look complete.

Older records without `locus` remain valid. When an older record is touched for relevant evidence, annotate only the surface actually supported by the evidence.

The Amazon Fire TV AFTKA APK surface is an example of a safe first annotation: Amazon documents the sideloaded APK being installed and launched on the Fire TV itself, so `locus: on_device` is grounded for that APK surface without upgrading privilege beyond the existing application-user boundary.

---

## 11. Root gate

**Truth** — do not turn a remote skill/webhook/backend into endpoint-local execution; do not turn adapter/rated power into measured consumption; per-surface locus must follow evidence.  
**Agency / non-domination** — account linking, developer enrollment and device authorization remain visible; do not seek hidden persistence or unauthorized endpoint access.  
**Continuity** — preserve exact model, source URLs, checked dates, per-surface execution locus, cloud dependency and recovery boundaries in repo state rather than chat memory.  
**Wisdom before speed** — local execution can still have lifecycle, memory, cloud-fallback, account, maintenance and recovery costs; do not treat `on_device` as synonymous with unrestricted or infrastructure-suitable.

---

## 12. One-line rule

> **Record where each developer-controlled execution surface actually runs; a programmable endpoint is not automatically the computer executing the program.**
