# Evidence Packet — Canon imageRUNNER ADVANCE C3530i / MEAP

**Device record:** `devices/canon/imagerunner-advance-c3530i.yaml`  
**Checked:** 2026-09-14  
**Local verification:** No  
**Current evidence state:** `DOCUMENTED`

## Why this device matters

The imageRUNNER ADVANCE C3530i is the first printer / office-appliance record in the census.

It adds a capability pattern that the earlier devices did not isolate cleanly:

```text
real embedded application runtime
  -> administrator-controlled installation
  -> application/package compatibility requirements
  -> license-aware admission
  -> application execution

does not imply

generic shell / root
arbitrary unsigned JAR execution
general Linux ownership
```

Canon documents MEAP (Multifunctional Embedded Application Platform) on this exact model family as an application framework. That makes the printer materially more than a fixed print engine, while the same documentation also shows why “installable application” must not be inflated into unrestricted compute authority.

## Source 1 — Exact-model hardware specification

Manufacturer source:

- https://www.cla.canon.com/en/p/imagerunner-advance-c3530i

Checked: 2026-09-14

Canon lists the original `imageRUNNER ADVANCE C3530i` as a color laser multifunction device supporting print, copy, scan, send and store.

The product page also lists:

- Canon Dual Custom Processor (Shared);
- 3.0 GB RAM;
- standard 250 GB hard disk;
- 1000Base-T / 100Base-TX / 10Base-T Ethernet;
- IEEE 802.11b/g/n wireless LAN;
- USB host and device interfaces;
- Advanced Box access over SMB or WebDAV.

For power, Canon lists approximately 44.1 W standby and approximately 0.8 W sleep, plus a TEC figure.

These are manufacturer operating-mode figures, not AXM measurements. The page also prints a maximum consumption value with unit text that is not reliable enough to normalize here, so the device record deliberately does not promote it into a watt figure.

This source does **not** establish CPU architecture, arbitrary code execution, exact MEAP application compatibility, hard-power-loss recovery, or the current used-market price.

## Source 2 — MEAP framework on C3530i

Exact-model manual:

- https://oip.manual.canon/USRMA-1814-zz-CS-3500-enUS/contents/devu-apdx-mp.html

Checked: 2026-09-14

Canon describes MEAP as a framework for extending machine functions such as communication, authentication and output.

The same manual states that:

- a dedicated MEAP application is installed on the machine;
- MEAP applications are installed and their status checked through SMS (Service Management Service) in the Remote UI;
- administrator login is required to install a MEAP application;
- SMS uses TLS communication.

This is direct manufacturer evidence for an embedded application execution surface on the C3530i.

It is **not** evidence of:

- root access;
- a shell;
- bootloader control;
- generic Linux userspace;
- arbitrary unsigned application execution.

## Source 3 — MEAP installation and licensing

Exact-model installation manual:

- https://oip.manual.canon/USRMA-1814-zz-CS-3500-enUS/contents/devu-apdx-mp-inst.html

Checked: 2026-09-14

Canon documents the installation flow through Remote UI -> Service Management Service -> Install MEAP Application.

The manual states that:

- MEAP application files use the `.jar` extension;
- the documented license files use the `.lic` extension;
- an installer may choose `Install and Start` or `Only Install`;
- a license may be obtained using a License Access Number and the machine serial number through Canon's licensing system;
- some applications instead receive licensing from the MEAP application provider;
- installation requirements can vary by application;
- up to 19 MEAP applications can be installed;
- MEAP applications can use approximately 4 GB of hard-disk space.

This is important because file extension alone is not authority.

The evidence supports:

```text
Canon-compatible MEAP application
+ administrator access
+ applicable license/admission path
-> documented install/start surface
```

It does **not** support:

```text
any JAR file
-> executable
```

The current record therefore stores the admission controls on the execution surface and leaves `arbitrary_unsigned_jar_execution` unknown.

A later schema may need a general admission-control model, but one device is not enough evidence to freeze that shape.

## Source 4 — Destructive reset path

Exact-model manual:

- https://oip.manual.canon/USRMA-1816-zz-CS-3500-enUV/contents/devu-mcn_mng-hdd_data-initializ.html

Checked: 2026-09-14

Canon documents `Initialize All Data/Settings` for the C3530i family.

The procedure:

- requires administrator privileges;
- returns machine settings to factory defaults;
- overwrites remaining hard-disk data;
- can take 30 minutes or more;
- restarts the machine after completion.

Canon explicitly tells administrators to back up important data before the operation, including MEAP application license files and data stored by MEAP applications.

That gives the record a real recovery/state-reset path with destructive data semantics:

```text
operating stock firmware
  -> Initialize All Data/Settings
  -> factory-default settings
  -> configuration/user/application state erased
```

It does **not** establish an official firmware reinstall, boot-media restore, recovery from corrupt firmware, or recovery from failed HDD/hardware.

## New schema pressure — admission-controlled execution

Earlier census devices already separated application execution from root authority.

The C3530i pressures a different boundary:

```text
runtime exists
!=
runtime is freely admitted
```

MEAP application execution is real, but the manufacturer-supported route is shaped by:

- administrator authority;
- MEAP-compatible packaging;
- license state;
- application-specific conditions;
- platform storage/application limits.

That matters for capability arbitrage because a cheap surplus office machine may contain useful compute and I/O while still having high acquisition friction if the required application or license cannot be obtained.

The useful question is therefore not merely:

> Can applications run?

It is also:

> Can an authorized owner reproducibly obtain, install, start, recover and replace the particular application needed for the target capability contract?

This record preserves that distinction without treating licensing as automatically bad or automatically available.

## Locality truth boundary

The C3530i exposes local-network surfaces such as Remote UI and Advanced Box SMB/WebDAV.

That does not establish that every MEAP application works fully locally.

Some MEAP installation flows use Canon's license-management service, while some applications may receive a provider-supplied license. Runtime network dependencies are application-specific.

Therefore the record keeps full offline operation and vendor-cloud requirements `unknown` rather than flattening one local management surface into `fully_local`.

## Power and economics truth boundary

No AXM power measurement was performed.

The manufacturer standby/sleep figures are useful evidence about the stock machine's documented operating modes, but they are not directly comparable to the repository's common registry workload protocol.

No dated NL/EU used-price cohort was collected.

Current unknowns include:

- current acquisition price and replacement supply;
- shipping/transport cost for a ~97 kg office machine;
- exact application/license acquisition cost;
- provisioning time;
- workload-specific wall power;
- hard-power-loss -> boot -> MEAP application restart behavior;
- firmware-level restore path;
- remaining HDD/mechanical life.

The machine should therefore not enter the low-power registry comparison merely because MEAP exists.

## Candidate roles

The strongest evidence-backed role is `document_workflow_edge`: the device combines scanner/printer functions, local networking, storage and a manufacturer-supported embedded application framework.

`document_ingestion_gateway` is plausible but still needs application-specific MEAP API evidence.

`general_edge_compute` remains low-confidence because MEAP admission, generic runtime authority, application availability, power and restart behavior are not yet comparable with conventional compute devices.

## Next falsifiable tests

1. Find one legitimately distributable MEAP application that still supports the original C3530i and preserve its exact compatibility/license terms.
2. Determine whether a used/retired C3530i can obtain the required license without depending on a previous owner's account or hidden service state.
3. On an owned/authorized unit, record firmware/controller version, installed MEAP applications and license state before modification.
4. Install/start one noncritical MEAP application through SMS and preserve a local experiment receipt.
5. Test whether that application continues to run with WAN unavailable where the application itself is designed for local operation.
6. Test normal restart and hard-power-loss -> boot -> application state repeatedly; do not infer autostart from `Install and Start`.
7. Measure stock standby, sleep and application-active wall power with a suitable meter rather than reusing manufacturer figures as local measurements.
8. Collect a dated NL/EU acquisition sample that includes transport, consumables/mechanical condition and any license/application dependency.
9. Exercise `Initialize All Data/Settings` only on noncritical owned/authorized state and preserve exactly what is destroyed and what must be restored.
10. Research an official firmware recovery/reinstall route separately; do not promote the destructive settings/data reset into firmware recovery.

## Root gate

**Truth:** the exact-model manuals prove a real MEAP application platform but do not prove shell/root, arbitrary JAR execution, local verification, current price, workload power or firmware recovery.  
**Agency / non-domination:** installation is administrator-controlled and applies only to owned/authorized equipment; the record preserves those admission boundaries rather than suggesting bypass.  
**Continuity:** exact model identity, installation/licensing conditions, destructive reset semantics and source URLs live in repository state.  
**Wisdom before speed:** a surplus MFP is not called a compute bargain until application availability, licensing, transport, power, recovery and remaining mechanical life are counted.
