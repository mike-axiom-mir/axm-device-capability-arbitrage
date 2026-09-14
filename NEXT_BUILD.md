# Next Build

**Current state:** The foundation is in place and the census now contains fifteen grounded records across fifteen marketed categories. The set spans a consumer camera, router, e-reader, mobile robot, NAS, thin client, media stick, IP camera, smart-home relay, smartphone, office MFP, 3D-printer/manufacturing appliance, handheld gaming PC/console, industrial IoT gateway, and smart TV/display appliance. The required 8-category breadth threshold is exceeded, but Milestone 01 still requires 10 more evidence-backed devices and an evidence-ready arbitrage result. The first registry comparison now has a dated EU acquisition snapshot, an executable common registry workload, evidence-gated comparison records, and local-experiment receipt validation. It still has no ranked winner because the three physical candidates have not produced comparable workload footprint, wall-power, provisioning, hard-power-loss/restart, recovery-burden, and remaining-life evidence.

The census has now exposed several durable boundaries: Roborock S5 showed recovery by persistent device state; DS220+ added recovery data-impact semantics; Wyse 3040 exposed configuration identity; Fire TV AFTKA separated application execution from administrator/root authority; Wyze Cam v2 and SONOFF BASICR2 independently established state-dependent locality; Pixel 3a showed that acquisition variant can gate the execution surface; Canon C3530i showed admission-controlled application execution; Creality K1 showed that manufacturer-documented root host authority must remain separate from physical-actuator suitability and total-useful-cost fit; Steam Deck LCD 256 GB showed that execution privilege must remain separate from persistence across vendor OS updates; Siemens IOT2050 Advanced showed that even an exact manufacturer article number can span functional-status revisions with different hardware capability while acquired software/security state remains a separate deployment fact; and LG OLED55C1PUB now shows that a manufacturer-supported developer execution surface can itself be a renewable vendor-session lease whose expiry removes Developer Mode-installed applications.

## Completed foundation step — Mechanical record checks

Implemented:

- YAML parsing for device and capability-contract records;
- required identity/evidence fields;
- allowed truth-state validation;
- explicit economics state;
- duplicate record/contract ID detection;
- execution-surface structure checks;
- recovery/evidence state checks;
- structured recovery-path checks with evidence-claim references;
- optional structured locality-state checks with evidence-claim references;
- evidence-gated comparison validation;
- configuration-aware market-snapshot validation, including sample-count and descriptive-statistic arithmetic;
- local-experiment receipt validation with authorization, artifact and local-measurement truth gates;
- an executable common registry workload and CI smoke/restart-persistence checks;
- GitHub Actions validation on pushes to `main` and pull requests.

The validator deliberately does **not** reject unknown capability values or enforce a large rigid schema. New hardware classes still need room to challenge v0.1.

`LOCALITY_STATE_MODEL.md` is an evidence-backed optional extension. Wyze Cam v2 and SONOFF BASICR2 independently show that persistent firmware state can change cloud/local behavior. The validator enforces the minimal shape only when `locality.states` is present; it does not force old flat records to migrate.

`MARKET_SNAPSHOT_METHOD.md` keeps acquisition observations separate from permanent device identity. Asking/displayed listing prices, seller class, exact revision/configuration, accessory state and cohort arithmetic remain explicit; a sample median is not treated as transaction-price truth.

`LOCAL_EXPERIMENT_RECEIPT_METHOD.md` now defines the path from a physical candidate test to any local-verification claim. A template or CI workload pass is not physical-device evidence.

## Priority 1 — Run the first actual arbitrage comparison

The hypothesis is not proven by building a database. The three-category candidate set already exists for the current capability contract:

> **low-power local registry / heartbeat node**

Current candidates:

- TP-Link Archer C7 v5 — router / OpenWrt; tiny RAM/flash; strong network role and TFTP recovery;
- Synology DS220+ — NAS / supported containers; much larger storage/compute platform with manufacturer power data but drive and opportunity cost;
- Dell Wyse 3040 — thin client / full Debian; 2 GB RAM, internal eMMC, Gigabit Ethernet, UEFI USB recovery, configurable AC Recovery and a manufacturer sub-4-W claim.

### Acquisition evidence now collected — partial, not ranking-ready

The first validated EU snapshot is:

`market_snapshots/low-power-local-registry-node-eu-2026-09-14.yaml`

Its descriptive cohorts currently show:

```text
Archer C7 v5 exact-revision private asks
  €20–€40, sample median €32

Wyse 3040 private used asks
  €20–€40, sample median €29.50

Wyse 3040 NL dealer-refurbished exact configurations
  €59–€67, sample median €63

DS220+ bare-chassis/no-drive mixed-RAM listings
  €195–€279, sample median €239.50
```

This is meaningful acquisition evidence, but it is deliberately not a price verdict. Asking/displayed prices are not final transaction prices, shipping is not normalized, and required DS220+ storage remains separate.

Do **not** rank the candidates yet. The common workload exists; the missing evidence is now physical candidate execution under that same workload and comparable operational measurement.

Required comparison state before ranking:

- refresh/expand the same-window EU market snapshot when a ranking attempt is made;
- preserve observed configuration and accessory inclusion for listings where model variants matter;
- count shipping, required storage and adapters separately from chassis price;
- run the existing common registry workload on each physical candidate and preserve footprint/results through local experiment receipts;
- measured wall power under comparable workload conditions;
- provisioning friction and repeat-provisioning time;
- recovery quality and data impact;
- hard-power-loss -> reboot -> service restart behavior;
- replacement availability and remaining-life evidence;
- workload fit.

Only then ask whether the non-obvious device is actually cheaper/better.

### Configuration-identity rule learned from Wyse 3040 and reinforced by Wyze Cam v2

A product model can remain exact while still spanning materially different unit configurations.

For Wyse 3040, Dell documents:

```text
same marketed model
  -> 8 GB or 16 GB eMMC
  -> optional WLAN/Bluetooth
```

For Wyze Cam v2, current Thingino support distinguishes:

```text
same marketed model
  -> T20X + JXF22 + RTL8189FTV
  -> T20X + JXF23 + RTL8189FTV
```

Market research, installation and matching must preserve observed unit configuration when it matters. A listing containing only a model name must not inherit the best-known storage/radio/sensor variant silently, and replacement firmware must not be selected from the marketed name alone when hardware variants require separate targets.

A later schema extension may need a more general variant/configuration representation, but do not freeze that shape until more devices pressure it.

### Execution-authority rule learned from Fire TV AFTKA

A documented custom-code path is not automatically an administrator-owned operating system.

For Fire TV Stick 4K Max 1st Gen (`AFTKA`), Amazon documents:

```text
user enables developer options
  -> user authorizes ADB connection
  -> custom APK can be sideloaded and launched
```

That proves a real application execution surface. It does **not** prove:

```text
root
bootloader access
cold-boot custom-app restart
fully offline provisioning/runtime
low-level restore media
```

Future matching must preserve sandbox/application-level capability without silently upgrading it to general Linux/root capability.

The Fire TV therefore does not enter the registry comparison merely because it has 2 GB RAM and networking. A candidate must satisfy the contract, not resemble a computer on paper.

### Locality-state rule — supported by two independent devices

Locality is not always a permanent hardware property.

Wyze Cam v2:

```text
stock Wyze firmware
  -> internet-centred app/live/settings behavior
  -> configured microSD recording can continue offline

Thingino firmware
  -> local RTSP / ONVIF / Web UI / root SSH
  -> vendor cloud is not required for normal local runtime
```

SONOFF BASICR2:

```text
stock eWeLink firmware
  -> same-LAN on/off can survive WAN loss after pairing
  -> stock provisioning and some schedule/scene/share setup remain server/internet dependent

Tasmota firmware
  -> local WebUI / console / LAN MQTT
  -> vendor cloud is not required for normal local runtime
```

These are different hardware and different stock-locality patterns, but both fit the same minimal `locality.states` structure. That is enough to validate the optional structure mechanically.

Do **not** infer from this that replacement firmware is always preferable. State change has cost: modification effort, lost vendor features, physical safety, recovery uncertainty and possible irreversible transitions.

### Market-snapshot rule learned from the first three-candidate comparison

Market evidence must preserve the same configuration discipline as hardware evidence.

```text
asking price
  != transaction price

private used
  != dealer refurbished

bare chassis
  != storage bundle

model name
  != exact configuration
```

The first snapshot therefore uses cohorts and keeps raw observations instead of writing one permanent `price` into each device record. Market medians are descriptive properties of that dated sample only.

### Acquisition-variant rule learned from Pixel 3a

An exact marketed model can still contain an acquisition variant that gates the execution surface itself.

```text
Pixel 3a, bootloader-unlockable unit
  -> UBports Ubuntu Touch installation path exists

Pixel 3a, Verizon unit
  -> UBports says bootloader cannot be unlocked
  -> replacement-OS path is unavailable
```

A market listing with carrier/origin unknown must not inherit replacement-OS eligibility merely from the model name. Keep the gate explicit or unknown.

### Admission-control rule learned from Canon C3530i

A real application runtime can exist without freely admitted arbitrary applications.

```text
MEAP runtime
  + administrator authority
  + compatible package
  + applicable license/admission state
  -> documented application execution
```

This does not prove arbitrary unsigned JAR execution, shell, root or general Linux ownership. Application availability/licensing can be real acquisition friction.

### Privileged-appliance rule learned from Creality K1

A manufacturer-documented root shell is strong execution evidence, but privilege and deployment suitability are different axes.

```text
Creality K1
  -> user accepts visible root warning
  -> manufacturer exposes root credentials
  -> SSH root access

same device
  -> high-speed motion
  -> heated fabrication process
```

Do not silently turn root SSH into a claim that unrelated always-on compute is cheap, low-power, restart-safe or wise. Physical safety, printer opportunity cost, memory headroom, recovery, and interference with normal fabrication remain part of total useful cost.

### Update-persistence rule learned from Steam Deck LCD 256 GB

A manufacturer-supported root/sudo path does not imply that installed state is durable across vendor OS updates.

```text
Flatpak on SteamOS
  -> normal-user application execution
  -> Valve places applications on writable storage
  -> Valve says this avoids breakage from future SteamOS system updates

sudo / non-Flatpak installation
  -> higher privilege exists
  -> Valve warns software installed outside Flatpak may be wiped by a SteamOS update
```

Matching must therefore keep **execution authority** and **update persistence** separate. A less-privileged application path can be operationally stronger for a persistent service if the privileged path is not update-stable.

This is one pressure case. Preserve it in the device record, but do not freeze a universal schema extension until independent hardware or operating-system evidence repeats the pattern.

### Functional-status identity rule learned from Siemens IOT2050 Advanced

An exact manufacturer article/order number can still be too broad to determine every hardware capability.

For Siemens IOT2050 Advanced article `6ES7647-0BA00-1YA2`, the manufacturer documents:

```text
FS01-FS03
  -> 2 x USB 2.0 Type A

FS04
  -> 1 x USB 3.0 Type A
  -> 1 x USB 2.0 Type A
```

Future market observations and local experiment receipts must therefore preserve the physical unit's observed functional status whenever the capability depends on it. Exact article identity is necessary here, but still not always sufficient.

The same record also preserves a current ProductCERT constraint: `SSA-834709` says exact-product Industrial OS deployments below V4.3.4.1 with Node-RED installed are affected by CVE-2026-58115 and should be updated. Do not infer software/security fitness from the product label or use a vulnerability as an execution path when documented local Linux/root execution already exists.

This is one industrial pressure case. Preserve it, but do not freeze a universal FS/security-state schema until independent devices demand it.

### Developer-session lease rule learned from LG OLED55C1PUB

A manufacturer-supported custom-application path can still depend on renewable vendor session state.

```text
LG Developer Mode active
  + valid developer session
  -> package/install/launch custom .ipk app

session expires + TV reboots
  OR TV reboots ten times while offline
  -> Developer Mode is disabled
  -> Developer Mode-installed apps are uninstalled
```

This is not the same as the Steam Deck update-persistence case. On the LG path, the documented developer admission state itself is time/session-gated and can remove developer-installed applications. Matching must therefore keep application authority, vendor-session continuity, runtime locality and indefinite deployment durability separate.

This is one pressure case. Preserve it in the record/evidence packet, but do not freeze a universal execution-lease schema until independent hardware reproduces the pattern.

## Priority 2 — Continue census expansion across genuinely different hardware

The breadth threshold is exceeded at 15 distinct categories. Do not pad the remaining 10 records with near-duplicates. New records should maximize schema pressure, evidence diversity, or comparison value.

Recommended next categories/patterns:

1. non-safety vehicle/infotainment computer only where the execution boundary is clearly separated from safety-critical systems;
2. an additional network/storage/thin-client candidate only if it materially improves the first comparison's price/power/recovery evidence;
3. a new persistent-state pattern that pressures locality, recovery or execution authority differently again;
4. a second admission-controlled application platform only if it independently tests the Canon lesson;
5. a second privileged physical appliance only if it independently tests the K1 host/actuator distinction;
6. an independent execution/update-persistence case only if it materially tests the Steam Deck lesson rather than repeating Linux root access;
7. a second industrial device only if it independently tests functional-status identity, software-maintenance state, or industrial recovery rather than merely repeating general Linux execution;
8. a second vendor-session-gated developer platform only if it independently tests whether the LG webOS execution-lease pattern generalizes;
9. an oddball appliance whose capability creates a genuinely new schema/evidence pressure rather than repeating root access.

The industrial/commercial-surplus slot is now filled by Siemens SIMATIC IOT2050 Advanced. Its value is not merely that it runs Linux; the exact article number still spans FS-dependent USB capability, and current ProductCERT evidence makes acquired software/security state a separate deployment fact.

The smart-TV/display slot is now represented by LG OLED55C1PUB. Its value is not merely custom app execution; the manufacturer documents developer-session expiry/disable behavior that can remove Developer Mode-installed applications.

Each new record should expose something the existing fifteen do not.

### Recovery-state rule learned from the S5

When a persistent modification changes what recovery paths remain available, record recovery by **device state** rather than treating `factory_reset` as a global property.

Example pattern:

```text
stock state
  -> official factory reset may restore stock firmware

modified state
  -> return-to-stock may be unavailable
  -> same modified state may still be reprovisionable
```

Do not let a valid stock recovery claim imply reversibility after modification.

### Recovery-data rule learned from the DS220+

When two recovery methods have different data/configuration effects, preserve that difference explicitly.

Example pattern:

```text
OS/config recovery
  -> system configuration may be cleared
  -> user data may be preserved

factory erase
  -> system returns to defaults
  -> user data is destroyed
```

Do not let `recovery_path: true` hide whether state, configuration or user data survives.

### Physical-safety rule learned from BASICR2

Software freedom can coexist with hardware hazards.

BASICR2 replacement firmware is an interesting local-control capability, but the device contains hazardous mains voltage. The manufacturer warns about electric shock and recommends qualified-professional installation/repair.

Therefore:

```text
firmware is community-flashable
!=
energized hardware is safe to handle casually
```

Safe installation/inspection effort is real friction and belongs in total useful cost. Research notes should not normalize live-mains experimentation merely because a low-voltage programming interface exists.

### Physical-actuator rule learned from K1

Even manufacturer-sanctioned root access does not erase the physical system attached to the host.

```text
root host authority
!=
actuator-use permission
!=
good always-on infrastructure fit
```

A device record may expose root while still keeping actuator access, whole-device power, unattended service restart, opportunity cost, and safety suitability unknown. Do not hide those unknowns behind the privilege level.

## Priority 3 — Add scoring only after comparison data exists

Do not invent a universal device score yet.

Once the three registry candidates contain comparable cost, power, provisioning and recovery evidence, introduce only the smallest scoring model needed to answer that concrete capability contract. Unknowns must remain visible and must not be converted into neutral-looking numeric values.

## Near-term experiments

### A. Archer C7 v5

- refresh/expand the current exact-v5 EU asking-price cohort before final ranking, preserving shipping and power-supply inclusion separately;
- find credible idle/load power measurements or measure locally later;
- run the existing common tiny registry workload and preserve a local experiment receipt;
- test whether 128 MB RAM + 16 MB flash is genuinely enough;
- test whether USB storage changes the result positively or only adds fragility;
- test hard power loss -> OpenWrt -> registry service restart.

### B. Synology DS220+

- refresh/expand the current bare-chassis/no-drive EU cohort rather than recollecting from zero;
- price a minimal supported storage configuration so required drive cost is visible;
- verify a currently compatible Container Manager release on owned hardware;
- run the existing common tiny registry workload and measure RAM/CPU/storage footprint;
- measure wall power with drives active, idle and hibernated and compare with Synology's manufacturer figures;
- test power loss -> Power Recovery -> DSM -> container restart behavior;
- test Mode 2 recovery on noncritical data and preserve which application/container state must be rebuilt.

### C. Dell Wyse 3040

- refresh/expand the current private-used EU cohort, preserving 8/16-GB eMMC and power-adapter inclusion; keep dealer-refurbished offers as a separate cohort;
- record whether each listing identifies optional WLAN/Bluetooth rather than assuming it;
- on owned hardware, record BIOS version and actual eMMC capacity before install;
- install Debian from preserved media and time the complete provisioning flow including the EFI/GRUB workaround;
- run the same common registry workload used on Archer/DS220+;
- measure wall power at boot, idle and registry-active state rather than substituting Dell's sub-4-W product claim;
- test AC loss -> AC Recovery -> Debian -> service restart repeatedly;
- test USB reinstall and record exactly which system/user/application state must be recreated;
- inspect eMMC health because soldered used flash is a real replacement/reliability cost.

### D. Sony ILCE-6000

- identify exact SoC/architecture from model-specific evidence;
- identify RAM from reliable evidence;
- map PlayMemories API access to sensor, network, storage and audio;
- document recovery/version constraints;
- collect used-price snapshot;
- decide which non-camera roles are actually rational rather than merely possible.

### E. Roborock S5

- collect an NL/EU used-price sample;
- collect credible idle-on-dock / charging / cleaning power data or measure locally;
- verify exact production/recovery firmware before any local modification test;
- enumerate actual S5 Valetudo capabilities rather than inheriting every generic integration feature;
- treat permanent loss of stock state as setup/recovery cost rather than hiding it;
- only add stock-vs-Valetudo `locality.states` if direct stock-locality evidence is collected rather than inferred.

### F. Fire TV Stick 4K Max 1st Gen / AFTKA

- if an owned unit becomes available, preserve its exact build model and Fire OS version before testing;
- locally verify ADB authorization, APK sideload and removal without assuming root;
- test whether a deliberately local APK works with WAN disconnected after stock provisioning;
- test cold power loss -> Fire OS -> application/service lifecycle rather than assuming auto-start;
- measure wall power at boot, idle, local-app active and media-active states;
- verify factory reset on noncritical state and document exactly what application data survives, if anything;
- collect a dated NL/EU used-market sample only after exact-generation identity can be distinguished from 2nd Gen listings.

### G. Wyze Cam v2

- identify JXF22 vs JXF23 on a physical owned unit before selecting replacement firmware;
- preserve stock firmware/version before modification;
- reproduce Thingino installation using the least invasive supported method for that exact unit;
- measure wall power in stock idle, Thingino idle and active RTSP states;
- test cold power loss -> Thingino -> Wi-Fi -> RTSP/ONVIF/SSH repeatedly;
- test the official stock `demo.bin` flash on noncritical stock state separately from researching a Thingino-to-stock transition;
- collect a dated NL/EU used-market sample with sensor-variant ambiguity recorded rather than guessed;
- do not treat root SSH as proof that the camera is a rational general-purpose registry node until RAM/flash headroom and opportunity cost are known.

### H. SONOFF BASICR2

- only inspect/modify an owned or explicitly authorized unit with mains disconnected;
- follow the manufacturer warning that installation/repair should be handled by a qualified professional;
- identify the exact BASICR2 board/revision before firmware work;
- record stock firmware/app state and test stock LAN on/off with WAN deliberately unavailable after normal pairing;
- determine whether a trustworthy stock-firmware preservation/restore path exists before replacement; do not assume stock factory reset restores overwritten firmware;
- reproduce Tasmota only through an isolated low-voltage programming setup and preserve firmware/tool hashes;
- test local WebUI and local MQTT with outbound internet blocked;
- test repeated hard power loss -> Tasmota -> Wi-Fi -> local control and preserve relay power-on-state behavior;
- measure device self-consumption only using an appropriate safe mains measurement method, not an exposed energized PCB;
- collect a dated NL/EU price sample only if actuator-node comparison becomes useful.

### I. Google Pixel 3a / sargo

- preserve carrier/origin and confirm the bootloader is actually unlockable before buying or testing a unit for Ubuntu Touch;
- record exact Android/factory-image state before replacement-OS installation;
- reproduce the UBports installation on owned/authorized hardware and preserve a local experiment receipt;
- test WAN-disconnected local service operation after provisioning;
- characterize charging/battery behavior, wall power and battery-health dependence before considering an always-on role;
- test cold boot -> Ubuntu Touch -> chosen local service restart;
- collect market observations with unlockability/carrier status attached rather than pooling unknown-origin units.

### J. Canon imageRUNNER ADVANCE C3530i

- find one legitimately distributable MEAP application still compatible with the original C3530i and preserve exact license terms;
- determine whether a used unit can obtain the required license without hidden previous-owner account state;
- on owned/authorized hardware, record firmware/controller version and existing MEAP/license state before modification;
- install/start one noncritical MEAP application and preserve a local experiment receipt;
- test application runtime with WAN unavailable where the application itself is designed for local use;
- test normal restart and hard-power-loss -> boot -> MEAP application state;
- measure whole-device wall power rather than reusing manufacturer standby/sleep claims;
- research firmware-level restore separately from destructive `Initialize All Data/Settings`.

### K. Creality K1

- on an owned/authorized original K1, preserve exact hardware revision, firmware, storage state and root-warning state before modification;
- reproduce the documented opt-in root flow and preserve a local experiment receipt;
- measure RAM/free storage and stock idle footprint before adding services;
- run only a harmless local service that does not command heaters or motors, then test WAN-disconnected LAN access;
- test normal restart and repeated hard-power-loss -> Creality OS -> harmless custom-service restart without starting a print;
- measure wall power at stock idle, service-active idle and normal printing with an appropriate meter;
- test normal firmware rollback on noncritical state and record exactly what configuration/root-added state survives;
- use the low-level mainboard recovery tool only on noncritical owned hardware or when recovery is actually required, preserving board/image/tool identity and data impact;
- collect a dated NL/EU used-market sample only if a real contract makes the K1 a plausible candidate;
- count fabrication opportunity cost instead of treating an already-owned printer as a free server.

### L. Valve Steam Deck LCD 256 GB

- on an owned/authorized 256 GB LCD unit, preserve hardware revision, SteamOS version, battery health and SSD state before testing;
- reproduce the manufacturer-supported Flatpak path and preserve an experiment receipt;
- separately test one harmless sudo-level service only if needed, without assuming privileged state survives a SteamOS update;
- verify what survives a normal SteamOS update for Flatpak application state versus any explicitly chosen non-Flatpak service state;
- test normal restart and hard-power-loss -> SteamOS -> chosen local service lifecycle;
- measure whole-device wall power at idle, charging idle and common-workload active state rather than reusing the 4-15 W APU envelope or 45 W charger rating;
- test previous-OS rollback, Repair SteamOS and full re-image only on noncritical state, preserving exact data/application impact;
- collect a dated NL/EU used-market cohort with battery condition and storage configuration attached where listings disclose them;
- do not add it to the low-power registry comparison until power, autostart, acquisition cost, battery/charging behavior and opportunity cost are comparable.

### M. Siemens SIMATIC IOT2050 Advanced / 6ES7647-0BA00-1YA2

- on an owned/authorized unit, record the exact manufacturer functional status (`FS`) before assuming USB capability;
- record firmware, Industrial OS/image state, Node-RED presence and current security-patch state before network deployment;
- if an affected Industrial OS + Node-RED state is present, follow Siemens ProductCERT remediation and update to V4.3.4.1 or later before treating the unit as deployment-ready;
- preserve eMMC health/free-space evidence and power-supply identity;
- reproduce the manufacturer-documented external-image boot, root SSH/UART and apt path and preserve a local experiment receipt;
- run the common registry workload only after the unit state is recorded, then measure CPU/RAM/storage footprint and whole-device DC/wall power rather than substituting the manual's 12 W typical-basic-device figure;
- test normal restart and repeated hard-power-loss -> Linux -> chosen service lifecycle;
- test the firmware-V1.3.1+ USER-button external-media escape on noncritical state and keep it distinct from recovery from bootloader/SPI corruption;
- if re-imaging eMMC, treat the target system/application state as destructive and preserve exact image/hash/source;
- collect a dated NL/EU used-market cohort with article number, FS, power-supply inclusion and observed software state attached where listings disclose them;
- do not connect experiment workloads to production or safety-critical equipment merely because industrial interfaces are present.

### N. LG OLED55C1PUB

- on an owned/authorized exact model, preserve region suffix, firmware/webOS version, account state and installed-app state before enabling Developer Mode;
- reproduce the official Developer Mode workflow, install/launch one harmless `.ipk` test application, and preserve a local experiment receipt;
- record the visible remaining session time and renewal behavior without presenting the developer lease as permanent capability;
- test a deliberately local application with WAN unavailable while Developer Mode is still valid, keeping app runtime locality separate from session-renewal dependency;
- test normal restart and cold-power-loss -> webOS -> chosen app/service lifecycle rather than assuming autostart;
- measure whole-device wall power in standby, panel-on idle and custom-app-active states rather than reusing LG's `<0.5 W` standby claim;
- if intentionally testing session expiry/disable behavior, use only noncritical developer-app state and record whether the documented uninstall behavior occurs; do not risk unrelated owner data merely to reproduce a known vendor condition;
- test Reset to Initial Settings only on noncritical owned state and preserve exact account/app/data impact; do not call it firmware recovery;
- collect a dated NL/EU used-market cohort only if a real display/signage contract needs it, preserving burn-in/dead-pixel condition, stand/remote inclusion, exact region and transport/collection cost;
- do not add the TV to the low-power registry comparison until active power, RAM/storage headroom, autostart, developer-session durability and display opportunity cost are comparable.

## Stop conditions

Do not expand the census blindly if:

- records keep requiring exceptions the schema cannot represent;
- evidence quality is too weak to compare devices;
- cost data cannot be time/region scoped;
- a scoring system starts hiding unknowns;
- product category begins acting as an implicit capability claim;
- recovery claims stop identifying which device state they apply to;
- recovery claims hide configuration/data destruction behind a single positive boolean;
- a model-family record silently assigns optional or higher-spec unit variants to every physical device;
- an exact manufacturer article/order number silently assigns a higher functional-status capability to every physical unit;
- an application/developer execution surface is silently promoted to root or unrestricted operating-system authority;
- an acquisition variant that gates execution is silently merged into the model-level capability claim;
- an admission-controlled application platform is treated as freely admitting arbitrary applications;
- a single locality label hides materially different persistent-state cloud behavior;
- replacement-firmware capability is treated as free while recovery, lost vendor features or physical hazard are ignored;
- privileged host access is silently promoted to safe actuator control or cheap general-purpose infrastructure;
- execution privilege is silently promoted to update-stable deployment state;
- a time/session/account-gated developer surface is treated as indefinitely durable merely because custom applications can be installed successfully;
- a known security-maintenance condition is ignored because the hardware model is otherwise well documented;
- listing asking prices are silently promoted to transaction prices or permanent device values;
- private-used, dealer-refurbished, bare-chassis and bundled-storage prices are merged merely to increase sample size;
- CI or template workload execution is described as physical-device verification.

When one of those occurs, repair the model before adding volume.

## Root gate

**Truth:** no fake verification, silent best-variant/functional-status inheritance, privilege inflation, locality flattening, admission inflation, update-persistence inflation, developer-session durability inflation, security-state guessing, electrical-rating-as-power-measurement substitution, or asking-price-as-transaction-price substitution.  
**Agency / non-domination:** owned/authorized hardware only; consent-visible developer/root access stays consent-visible; cameras add privacy/recording consent; physical actuators and industrial process connections remain visibly user/operator-controlled.  
**Continuity:** evidence, variant/functional-status caveats, execution/admission/update-persistence/session-lease boundaries, software/security state, locality states, recovery, market observations, experiment receipts and safety constraints live in repo state.  
**Wisdom before speed:** compare common evidence before ranking hardware; root/replacement-firmware gains, renewable developer access and cheap listings must be weighed against installation, recovery, update/session durability, opportunity cost, electricity, physical/industrial safety and interference with the device's primary useful role.