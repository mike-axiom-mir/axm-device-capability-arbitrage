# Evidence Packet — LG OLED55C1PUB / Session-Gated webOS Developer Execution

**Device record:** `devices/lg/oled55c1pub.yaml`  
**Exact model:** `OLED55C1PUB`  
**Checked:** 2026-09-14  
**Local verification:** No  
**Current evidence state:** `DOCUMENTED`

## Why this device matters

The LG OLED55C1PUB is a useful capability-arbitrage pressure case because it is a large consumer display with a real manufacturer-supported custom-application path, yet that path is not a permanently owned general-purpose operating system.

The evidence chain is:

```text
exact model OLED55C1PUB
  -> LG documents webOS 6.0
  -> LG webOS developer documentation supports actual-device Developer Mode from webOS TV 3.0+
  -> owner installs Developer Mode app
  -> owner signs in with LG Developer site account
  -> Developer Mode is enabled
  -> development host pairs on the same network
  -> .ipk webOS app can be installed and launched
```

The important continuity boundary is different from the Steam Deck update-persistence case:

```text
custom Developer Mode app exists
  -> Developer Mode session remains valid
  -> app remains available for development/testing

session expires + TV reboots
  OR TV reboots ten times while offline
  -> Developer Mode is disabled
  -> Developer Mode-installed apps are uninstalled
```

This means the execution surface is **vendor-session-gated**. A machine matcher must not read `custom_code: true` and silently assume indefinitely durable unattended deployment.

## Source 1 — Exact LG OLED55C1PUB product page

Manufacturer product page:

- https://www.lg.com/cac/tv-y-barras-de-sonido/lg-oled55c1pub

Checked: 2026-09-14

The page identifies the exact model and documents, among other model-level properties:

- model year 2021;
- webOS 6.0 platform;
- OLED 3840 x 2160 display;
- alpha9 Gen4 AI Processor 4K product label;
- 802.11ac Wi-Fi;
- Bluetooth 5.0;
- one Ethernet input;
- three USB 2.0 ports;
- one RS-232C mini-jack;
- a manufacturer standby/emergency-power claim below 0.5 W.

### Exact-model truth boundary

The record does **not** infer from this page:

- CPU instruction set;
- CPU core count;
- RAM;
- writable internal-storage capacity;
- arbitrary developer-app access to USB, RS-232C, microphone, tuner, HDMI or network APIs;
- active wall power;
- whole-device idle power with webOS/app running;
- suitability as an always-on compute node.

The `<0.5 W` figure remains a manufacturer standby claim only. It is not used as `idle_watts` and is not evidence for the common registry workload.

## Source 2 — LG webOS Developer Mode App

Official developer documentation:

- https://webostv.developer.lge.com/develop/getting-started/developer-mode-app

Checked: 2026-09-14

LG documents a first-party Developer Mode app for testing webOS TV applications on actual televisions.

The current workflow requires:

- a network-connected webOS TV;
- an LG Developer site account;
- installation of the Developer Mode app from LG Apps;
- signing in through that app;
- enabling Developer Mode, which reboots the TV;
- a development PC on the same network with LG tooling;
- pairing/key setup for the TV development target.

The page also documents a **remaining session time** and an EXTEND function.

### Session continuity truth boundary

LG explicitly documents that Developer Mode is disabled:

- after the TV reboots when the remaining session time has run out;
- after the TV reboots ten times while the TV is not connected to a network.

LG further states that after Developer Mode is disabled, the apps installed through Developer Mode are uninstalled.

That is the core new schema/economics lesson:

> **An execution surface can be real, manufacturer-supported, and user-authorized while still being leased by renewable vendor session state.**

The account/network dependency is therefore not treated as a minor setup footnote. It is part of deployment continuity and total useful cost.

The docs do **not** establish:

- root;
- unrestricted shell access;
- kernel authority;
- bootloader access;
- developer-app survival after the Developer Mode session is disabled;
- indefinite fully offline use of the Developer Mode path;
- cold-boot autostart for an arbitrary custom app.

## Source 3 — Building, packaging, installing and launching a webOS app

Official developer documentation:

- https://webostv.developer.lge.com/develop/getting-started/build-your-first-web-app
- https://webostv.developer.lge.com/develop/tools/cli-dev-guide

Checked: 2026-09-14

LG documents the concrete app flow:

```text
web app source
  -> ares-package
  -> .ipk package
  -> ares-install to target TV
  -> ares-launch
  -> application runs on the television
```

The developer guide also states that actual-device testing with the Developer Mode app is available from webOS TV 3.0.

Because the exact OLED55C1PUB product page identifies this television as webOS 6.0, the record treats Developer Mode custom application execution as `DOCUMENTED` for this model.

This is a two-source manufacturer inference with explicit scope. It is not local verification.

### Application-authority truth boundary

The installed application surface is represented as sandboxed application execution.

The repo does not turn:

```text
same-network pairing
+ SSH-key setup used by developer tooling
+ .ipk install/launch
```

into:

```text
root shell
unrestricted Linux host
bootloader control
persistent service manager ownership
```

Transport used by the developer toolchain is not automatically general operating-system authority.

## Source 4 — LG factory reset / Reset to Initial Settings

Official LG support:

- https://www.lg.com/us/support/help-library/how-do-i-factory-reset-my-lg-tv-if-it-keeps-freezing-or-showing-errors-CT10000030-20155311398606
- https://www.lg.com/us/support/help-library/lg-tv-how-to-reset-my-lg-smart-tv--1441914092672

Checked: 2026-09-14

LG documents Reset to Initial Settings for 2021 webOS 6.0 televisions and states that a full reset removes installed apps and personal/account settings.

The device record models this as a destructive settings/data/application reset path.

It is **not** promoted into evidence of:

- firmware-image reflash;
- bootloader recovery;
- rescue partition;
- recovery from failed mainboard/storage hardware;
- preservation of custom Developer Mode application state.

No reset was performed by AXM.

## Locality and account dependency

The evidence supports one strong provisioning fact:

```text
Developer Mode provisioning/session management
  -> LG Developer account required
  -> network connection required
```

It does **not** support a blanket statement that every custom app requires the vendor cloud for its own normal logic.

A webOS application could be local in its own design while the **developer execution lease** still depends on account/session maintenance. Those are different questions and remain separate in the record.

This is why the record keeps overall runtime locality `unknown` while marking Developer Mode provisioning/account dependency explicitly.

## Power boundary

The manufacturer page says standby/emergency consumption is below 0.5 W.

That figure must not be reused as:

- active app power;
- panel-on idle power;
- a common-workload measurement;
- proof of low total useful cost.

A 55-inch OLED display has a primary role and physical opportunity cost far beyond a tiny registry node even if a low standby mode exists.

No AXM wall-power measurement was made.

## Recovery and continuity summary

Known:

- ordinary webOS factory reset exists for the model generation;
- the reset removes installed apps/settings;
- Developer Mode can be re-established through a documented owner-visible workflow while the service remains available;
- Developer Mode apps can be automatically removed when the developer session is disabled.

Unknown:

- low-level firmware restore media;
- rescue partition behavior;
- bootloader recovery;
- storage-failure recovery;
- whether a chosen custom app can automatically resume after cold boot;
- how a future LG service/account change would affect this 2021 model's Developer Mode path;
- local reproduction of any recovery path.

## Economics / arbitrage boundary

No used-market cohort was collected in this activation.

Any later acquisition sample should preserve at least:

- exact model / region suffix;
- screen condition and burn-in/dead-pixel disclosures;
- stand and Magic Remote inclusion;
- firmware/webOS state if disclosed;
- transport/collection cost for a large fragile 55-inch panel.

A television already present in a room may have near-zero incremental purchase cost for a display workload while still having high opportunity cost for unrelated infrastructure. The repo must not treat an already-owned appliance as economically free.

## Local verification status

None.

This packet does not claim:

- a physical OLED55C1PUB was available to AXM;
- Developer Mode was enabled locally;
- an `.ipk` was installed or launched locally;
- session expiry/removal was reproduced;
- factory reset was tested;
- active/idle power was measured;
- any market price was observed.

## New schema pressure

The strongest new distinction is:

```text
application execution exists
!=
execution is indefinitely durable

vendor developer account/session
  -> can be a capability gate
  -> can be a continuity dependency
  -> can create recurring maintenance friction
```

This is not the same as the Steam Deck case where a privileged system modification may be wiped by an OS update. Here, the vendor-supported **developer admission state itself** has a documented lease/expiry mechanism that can remove installed developer applications.

One device is enough to preserve the lesson in evidence. It is not enough to freeze a universal schema extension until another independent platform shows the same pattern.

## Root check

**Truth:** webOS 6.0, Developer Mode app install/launch, session expiry behavior and factory reset are all scoped to official LG evidence; no root, permanent persistence, workload power, market price or local test is invented.  
**Agency / non-domination:** Developer Mode is explicitly owner-enabled and account-authenticated; nothing here suggests bypassing another person's TV, account, or consent.  
**Continuity:** session expiry and automatic developer-app removal are preserved as first-class deployment risks rather than hidden behind `custom_code: true`.  
**Wisdom before speed:** a 55-inch OLED can be a useful programmable display, but its primary utility, panel wear, physical size, power and renewable developer-session burden must be counted before calling it cheap compute.
