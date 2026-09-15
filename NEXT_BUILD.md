# Next Build

**Current state:** The foundation is in place and the census now contains nineteen grounded records across nineteen marketed categories. The set spans a consumer camera, router, e-reader, mobile robot, NAS, thin client, media stick, IP camera, smart-home relay, smartphone, office MFP, 3D-printer/manufacturing appliance, handheld gaming PC/console, industrial IoT gateway, smart TV/display appliance, vehicle infotainment/non-safety computer, enterprise IP video phone/desk endpoint, programmable musical instrument/audio processor, and programmable graphing calculator/handheld. The required 8-category breadth threshold is exceeded, but Milestone 01 still requires 6 more evidence-backed devices and an evidence-ready arbitrage result. The first registry comparison now has a dated EU acquisition snapshot, an executable common registry workload, evidence-gated comparison records, and local-experiment receipt validation. It still has no ranked winner because the three physical candidates have not produced comparable workload footprint, wall-power, provisioning, hard-power-loss/restart, recovery-burden, and remaining-life evidence.

The census has now exposed several durable boundaries: Roborock S5 showed recovery by persistent device state; DS220+ added recovery data-impact semantics; Wyse 3040 exposed configuration identity; Fire TV AFTKA separated application execution from administrator/root authority; Wyze Cam v2 and SONOFF BASICR2 independently established state-dependent locality; Pixel 3a showed that acquisition variant can gate the execution surface; Canon C3530i showed admission-controlled application execution; Grandstream GXV3370 independently repeats that admission boundary through administrator-controlled Android app policy and adds Safe Mode as an application-level recovery layer distinct from factory reset/firmware recovery; Creality K1 showed that manufacturer-documented root host authority must remain separate from physical-actuator suitability and total-useful-cost fit; Steam Deck LCD 256 GB showed that execution privilege must remain separate from persistence across vendor OS updates; Siemens IOT2050 Advanced showed that even an exact manufacturer article number can span functional-status revisions with different hardware capability while acquired software/security state remains a separate deployment fact; LG OLED55C1PUB shows that a manufacturer-supported developer execution surface can itself be a renewable vendor-session lease whose expiry removes Developer Mode-installed applications; Polestar 2 MY2026 shows that sandboxed execution inside one vehicle subsystem must not be promoted into authority over the safety-critical parent machine; Critter & Guitari Organelle S2 shows that destructive factory re-imaging of a selected removable root disk can coexist with continuity through physically retaining the prior boot medium; and Texas Instruments TI-Nspire CX II-T now shows that a persisted programming surface can be temporarily inaccessible under a visible operational policy mode without that pre-existing state being deleted.

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
  -> UBports-supported Ubuntu Touch installation path exists

Pixel 3a, Verizon unit
  -> UBports says bootloader cannot be unlocked
  -> replacement-OS path is unavailable
```

A market listing with carrier/origin unknown must not inherit replacement-OS eligibility merely from the model name. Keep the gate explicit or unknown.

### Admission-control rule — independently repeated by Canon C3530i and Grandstream GXV3370

A real application runtime can exist without freely admitted arbitrary applications.

Canon C3530i:

```text
MEAP runtime
  + administrator authority
  + compatible package
  + applicable license/admission state
  -> documented application execution
```

Grandstream GXV3370:

```text
Android application runtime
  + administrator install/uninstall policy
  + compatible application
  -> documented application execution

administrator policy may
  -> allow
  -> require admin password
  -> require admin password for unknown-source install/uninstall conditions
  -> disallow third-party app changes
```

These two platforms independently establish admission as a real capability axis while using different mechanisms. Neither proves arbitrary unsigned package execution, shell, root, bootloader authority or general-purpose host ownership. Preserve the platform-specific controls rather than flattening them into `custom_code: true`.

The GXV3370 also shows that application-level recovery can exist below destructive reset/firmware recovery: Grandstream Safe Mode runs only system applications so an incompatible third-party application can be removed. Safe Mode, factory reset and SD-card firmware recovery target different failure states and must stay distinct.

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

### Parent-system authority rule learned from Polestar 2 MY2026

A documented application surface inside a safety-critical machine must be scoped to the subsystem that actually grants it.

```text
Polestar 2 MY2026
  -> Android Automotive infotainment
  -> car-adapted Google Play app installation
  -> sandboxed third-party application execution

does not prove
  -> braking / steering / propulsion control
  -> safety-system authority
  -> CAN access
  -> arbitrary vehicle-property read/write
```

Android documents car-specific review, driver-distraction restrictions and permission-bounded car APIs. The Polestar evidence does not grant ordinary third-party Play apps whole-vehicle authority. Matching must therefore keep **subsystem execution** and **parent-system authority** separate.

This is one vehicle pressure case. Preserve the local `safety_boundary` evidence in the record, but do not freeze a universal parent-system schema until independent hardware reproduces the need.

## Priority 2 — Continue census expansion across genuinely different hardware

The breadth threshold is exceeded at 19 distinct categories. Do not pad the remaining 6 records with near-duplicates. New records should maximize schema pressure, evidence diversity, or comparison value.

Recommended next categories/patterns:

1. an additional network/storage/thin-client candidate only if it materially improves the first comparison's price/power/recovery evidence;
2. a new persistent-state pattern that pressures locality, recovery or execution authority differently again;
3. a third admission-controlled application platform only if it adds a materially different signing, licensing, lease, credential or distribution boundary beyond the Canon/GXV3370 cases;
4. a second privileged physical appliance only if it independently tests the K1 host/actuator distinction;
5. an independent execution/update-persistence case only if it materially tests the Steam Deck lesson rather than repeating Linux root access;
6. a second industrial device only if it independently tests functional-status identity, software-maintenance state, or industrial recovery rather than merely repeating general Linux execution;
7. a second vendor-session-gated developer platform only if it independently tests whether the LG webOS execution-lease pattern generalizes;
8. a second safety-critical-parent / non-safety-subsystem case only if it independently tests the Polestar nested-authority lesson without requiring unsafe experimentation;
9. an oddball appliance whose capability creates a genuinely new schema/evidence pressure rather than repeating root access.

The industrial/commercial-surplus slot is now filled by Siemens SIMATIC IOT2050 Advanced. Its value is not merely that it runs Linux; the exact article number still spans FS-dependent USB capability, and current ProductCERT evidence makes acquired software/security state a separate deployment fact.

The smart-TV/display slot is now represented by LG OLED55C1PUB. Its value is not merely custom app execution; the manufacturer documents developer-session expiry/disable behavior that can remove Developer Mode-installed applications.

The vehicle-infotainment/non-safety slot is now represented by Polestar 2 MY2026. Its value is not merely Android Automotive app execution; the record explicitly prevents sandboxed infotainment authority from leaking into claims about braking, steering, propulsion, CAN or other safety-critical vehicle controls.

The enterprise IP video-phone / desk-endpoint slot is now represented by Grandstream GXV3370. Its value is not merely Android execution; the manufacturer exposes a policy-controlled third-party application surface and separately documents Safe Mode, factory reset and SD-card Recovery Mode. It independently pressures admission control and layered recovery without requiring exploit-based access.

The programmable musical-instrument/audio-processor slot is now represented by Critter & Guitari Organelle S2. Its value is not merely Linux execution: the manufacturer documents user-authored patches, console/compile workflows and a removable microSD root disk whose official factory restore wipes the selected card while explicitly permitting a new card so the old OS can be retained.

The programmable graphing-calculator slot is now represented by Texas Instruments TI-Nspire CX II-T. Its value is not merely Python/TI-Basic execution: its visible Press-to-Test/exam state can temporarily suppress access to persisted programs/documents and later restore that access, while state created during the restricted session is intentionally deleted on exit. That pressures operational-mode accessibility rather than repeating a firmware-state, update-persistence or developer-session case.

Each new record should expose something the existing nineteen do not.

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

### Removable-root-media recovery rule learned from Organelle S2

A restore can be destructive to its selected target while continuity remains possible by preserving the previous removable boot medium.

```text
re-image current microSD
  -> target OS + patch state is erased

image a separate new microSD
  -> factory boot medium is created
  -> old OS/root disk can remain physically retained
```

Do not flatten these into either `recovery is destructive` or `recovery preserves state`. The correct answer depends on **which medium is targeted** and whether the prior medium remains retained outside the restore operation. Preserve that distinction locally until independent hardware shows the smallest reusable schema.

### Operational-mode accessibility rule learned from TI-Nspire CX II-T

Installed or persisted custom code is not necessarily usable in every current operational policy state.

```text
normal calculator state
  -> stored programs/documents accessible

Press-to-Test / exam state
  -> access to pre-existing programs/documents blocked
  -> restriction visibly indicated

exit restricted state
  -> prior state becomes accessible again
  -> restricted-session-created data is deleted
```

Do not turn `custom_code: true` into an unconditional claim that the code is currently available in every device mode. Keep this separate from persistent firmware state, update persistence, vendor-session lease state and recovery. One device is enough to preserve a local `operational_modes` pressure structure, not enough to freeze a universal schema.

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

### Parent-system safety rule learned from Polestar 2

A subsystem can be programmable without making the whole parent machine programmable to the same authority level.

```text
infotainment app executes
!=
vehicle-control permission
```

Research on vehicles or other safety-critical parent systems must remain on documented non-safety surfaces unless exact evidence establishes otherwise, and even then deployment must remain owned/authorized and safety-bounded. Do not turn generic platform APIs into exact-model actuator claims.

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

### O. Polestar 2 model year 2026

- if an owned/authorized exact-MY2026 vehicle is available, record market/trim, installed software version and account state before any application test;
- use only the manufacturer-supported Google Play application surface; do not seek safety-critical controls or bypass vehicle security boundaries for this census goal;
- install and run one harmless car-adapted application, preserving a local experiment receipt if a suitable app can be legitimately distributed/installed;
- record which permissions and car-data APIs are actually exposed to that app rather than inheriting generic Android Automotive capabilities;
- test normal app restart and centre-display restart on noncritical app state, keeping display restart distinct from firmware recovery;
- if testing factory reset at all, do so only on a deliberately prepared noncritical vehicle profile/state and preserve exact profile/key/app-settings impact;
- do not infer subsystem power from traction-battery capacity or charging specifications; only measure infotainment energy if a safe, meaningful method exists;
- do not collect a used-vehicle price merely to call the embedded computer cheap: whole-vehicle acquisition, depreciation, insurance, maintenance and opportunity cost dominate unless the car is already owned for another purpose;
- keep braking, steering, propulsion, safety systems, CAN and arbitrary vehicle-property control outside the experiment unless a future independent research question, explicit authority and appropriate safety process justify studying them.

### P. Grandstream GXV3370

- on an owned/authorized exact unit, record hardware revision, firmware/system/recovery versions, administrator-policy state and installed third-party applications before changing anything;
- use the documented application surface rather than seeking an exploit path; install one harmless compatible test application only when administrator policy/authorization permits it;
- preserve which `Permission to Install/Uninstall Apps` mode is active and whether unknown-source or Developer Mode controls are needed for the chosen test path;
- test a deliberately local application with WAN unavailable after provisioning without turning local Web-GUI/firmware support into a blanket claim that all telephony/application functions are cloud-independent;
- test normal reboot -> chosen application lifecycle and keep application persistence separate from mere successful installation;
- enter Safe Mode on noncritical app state and verify third-party isolation/removal behavior before considering destructive recovery;
- test factory reset only on prepared noncritical state and record configuration/user/application/SD-card effects separately;
- test SD-card Recovery Mode only on owned noncritical hardware or when recovery is genuinely required, preserving firmware image identity/hash and exact data/configuration impact;
- measure whole-device wall/PoE power under a defined profile rather than converting the 12 VDC 1.5 A adapter or PoE class into consumption;
- collect a dated NL/EU used-market cohort with power supply/stand/accessory state and administrator usability preserved where listings disclose it;
- do not add GXV3370 to the low-power registry comparison merely because it has 2 GB RAM and Gigabit Ethernet; admission policy, privilege, application persistence, power, market cost and workload fit must be comparable first.

### Q. Critter & Guitari Organelle S2

- on an owned/authorized exact S2, record OS version, microSD identity/capacity, free space and installed patch state before changing anything;
- reproduce one harmless user-authored Pure Data patch and preserve a local experiment receipt;
- open the manufacturer-supported terminal and compile one noncritical patch-local source artifact without promoting console access to root unless the local evidence proves it;
- test basic locally stored patch operation with WAN unavailable while preserving the distinction between local performance and internet-dependent patch/update acquisition;
- test normal restart and external power loss -> boot -> selected patch/service lifecycle rather than assuming arbitrary custom autostart;
- measure whole-device wall power under a defined audio/patch profile instead of converting the 9 VDC / 1.0 A supply requirement into consumption;
- on noncritical media, reproduce the official factory-image process and record exact target-card data loss;
- separately test the documented new-card recovery strategy while physically retaining the prior card, preserving image/hash/card identity and whether the old root disk remains bootable;
- collect a dated NL/EU used-market cohort only if a real capability contract makes the instrument a plausible candidate;
- count musical-instrument opportunity cost instead of treating an already-owned programmable instrument as a free Linux node.

### R. Texas Instruments TI-Nspire CX II-T

- on an owned/authorized exact non-CAS CX II-T, record OS version, free storage and existing document/program state before testing;
- reproduce one harmless Python program and one TI-Basic program and preserve a local experiment receipt without treating either runtime as shell/root authority;
- verify the acquired OS state satisfies the manufacturer-documented Python requirement rather than assuming current capability from model identity alone;
- enter the documented Press-to-Test/exam mode on deliberately noncritical test documents/programs and record which selected restrictions actually affect Python, TI-Basic and document access;
- exit the mode through a documented method and verify pre-existing state becomes accessible again while separately recording the deletion of intentionally created Press-to-Test session data;
- test Reset All Memory only on a prepared noncritical device image/state and preserve exact user/configuration/application impact;
- test official OS reinstall only when justified on owned noncritical hardware, preserving OS version/source/hash where possible and recording unknown data impact rather than assuming preservation;
- measure charging/idle/use power only with a defined safe method; do not infer consumption from battery presence or USB connection;
- collect a dated NL/EU used-market cohort only if a capability contract makes the calculator relevant, preserving OS state and accessories where listings disclose them;
- do not add it to the low-power registry comparison merely because Python exists: networking, unattended restart, service persistence, power, battery wear, privilege and workload fit are unproven.

## Stop conditions

Do not expand the census blindly if:

- records keep requiring exceptions the schema cannot represent;
- evidence quality is too weak to compare devices;
- cost data cannot be time/region scoped;
- a scoring system starts hiding unknowns;
- product category begins acting as an implicit capability claim;
- recovery claims stop identifying which device state they apply to;
- recovery claims hide configuration/data destruction behind a single positive boolean;
- removable-root-media recovery is flattened so destructive impact on the selected target is confused with whether an older boot medium can be retained separately;
- a persisted execution surface is treated as currently accessible without checking a documented operational policy mode that can temporarily suppress it;
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
- subsystem execution inside a safety-critical parent machine is silently promoted to authority over the parent system or its safety-critical actuators;
- generic platform vehicle APIs are treated as exact-model permissions without device-specific evidence;
- a known security-maintenance condition is ignored because the hardware model is otherwise well documented;
- listing asking prices are silently promoted to transaction prices or permanent device values;
- private-used, dealer-refurbished, bare-chassis and bundled-storage prices are merged merely to increase sample size;
- CI or template workload execution is described as physical-device verification.

When one of those occurs, repair the model before adding volume.

## Root gate

**Truth:** no fake verification, silent best-variant/functional-status inheritance, privilege inflation, locality flattening, admission inflation, update-persistence inflation, developer-session durability inflation, parent-system authority inflation, operational-mode accessibility inflation, recovery-target/retained-media conflation, security-state guessing, electrical-rating-as-power-measurement substitution, or asking-price-as-transaction-price substitution.  
**Agency / non-domination:** owned/authorized hardware only; consent-visible developer/root/exam-mode access stays consent-visible; cameras add privacy/recording consent; physical actuators, industrial process connections and vehicle/safety boundaries remain visibly user/operator-controlled.  
**Continuity:** evidence, variant/functional-status caveats, execution/admission/update-persistence/session-lease/parent-system/operational-mode boundaries, software/security state, locality states, recovery target/retained-media distinctions, market observations, experiment receipts and safety constraints live in repo state.  
**Wisdom before speed:** compare common evidence before ranking hardware; root/replacement-firmware gains, removable-media recovery flexibility, renewable developer access, temporary policy-mode restrictions and cheap listings must be weighed against installation, recovery, update/session/mode durability, opportunity cost, electricity, battery wear, physical/industrial/vehicle safety and interference with the device's primary useful role.
