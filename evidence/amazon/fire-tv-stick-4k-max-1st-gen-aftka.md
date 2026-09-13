# Evidence Packet — Amazon Fire TV Stick 4K Max, 1st Gen (AFTKA)

**Device record:** `devices/amazon/fire-tv-stick-4k-max-1st-gen-aftka.yaml`  
**Checked:** 2026-09-14  
**Local verification:** No  
**Current evidence state:** DOCUMENTED

## Why this device matters

This is the first media/TV/signage-class device in the census. It pressures a different boundary from the existing router, NAS and thin-client records: a consumer media stick exposes a manufacturer-supported application runtime and ADB sideload path, but that does **not** imply root, unrestricted Linux administration, unattended service startup, offline provisioning, or deep recovery.

The record therefore preserves the useful capability while refusing to promote `ADB available` into `general root computer`.

## Source 1 — Amazon exact-model device specification

Source:

- https://developer.amazon.com/docs/device-specs/device-specifications-fire-tv-streaming-media-player.html

Source class: manufacturer technical documentation  
Checked: 2026-09-14

Amazon's exact section for **Fire TV Stick 4K Max - 1st Gen (2021)** identifies:

- build model `AFTKA`;
- release year 2021;
- Android API level 28 / Android 9;
- Fire OS 7;
- MediaTek MT8696 + MT7921LS;
- quad-core 1.8 GHz CPU;
- 32-bit application ABI;
- IMG GE9215 GPU at 750 MHz;
- 2 GB DDR4 RAM;
- Wi-Fi 6 / 802.11 a/b/g/n/ac/ax with 2x2 MIMO on 2.4/5 GHz;
- Bluetooth 5.0;
- 10/100 Ethernet through an external dongle;
- 8 GB storage;
- OpenGL ES support and hardware media decode capability.

Amazon also lists `amazon.nl` among the marketplaces for this exact model.

### What this proves

- exact build identity (`AFTKA`);
- exact-model CPU/SoC, RAM, storage and wireless specifications;
- Android-derived Fire OS 7 application environment;
- HDMI/media-oriented output capability inherent to the streaming-stick platform.

### What this does not prove

- root or administrator privilege;
- unrestricted native Linux execution;
- unattended boot of a custom application;
- wall-power draw;
- fully offline operation;
- present-day used-market price.

## Source 2 — Amazon ADB application installation and launch

Source:

- https://developer.amazon.com/docs/fire-tv/installing-and-running-your-app.html

Source class: manufacturer developer documentation  
Checked: 2026-09-14

Amazon documents installing an APK outside the Appstore with:

```text
adb install <path-to-apk-file>
```

and launching a sideloaded application either from the Fire TV UI or through an Android activity-manager command over ADB.

### What this proves

- Fire TV exposes a supported path for user-supplied Android APK installation;
- sideloaded applications can be launched on-device;
- a custom application runtime exists independently of Appstore publication.

### What this does not prove

- root access;
- arbitrary kernel/bootloader access;
- a persistent background service surviving all Fire OS lifecycle policies;
- automatic launch after hard power loss;
- that every Android API is exposed identically to generic Android hardware.

The machine-readable record therefore describes an `android_apk` execution surface rather than a generic `linux_root` surface.

## Source 3 — Amazon ADB connection and user authorization

Source:

- https://developer.amazon.com/docs/fire-tv/connecting-adb-to-device.html

Source class: manufacturer developer documentation  
Checked: 2026-09-14

Amazon documents enabling ADB Debugging and Apps from Unknown Sources, then connecting a development computer to Fire TV over the local network. Both devices must be on the same network for network ADB. The first connection requires visible authorization on the Fire TV device.

### What this proves

- a local-network developer-control path exists;
- ADB access is opt-in through device settings;
- first connection requires user-visible authorization;
- network ADB can install/manage Android apps and issue Android shell/activity commands.

### What this does not prove

- root privilege;
- hidden or zero-consent persistence;
- remote access from outside the local network;
- reliable unattended reconnect after every reboot.

The explicit authorization step is compatible with the AXM agency root and should remain visible rather than being treated as friction to bypass.

## Source 4 — Official Fire TV setup requirements

Source:

- https://www.amazon.com/gp/help/customer/display.html?nodeId=G7HTKNXBW4GPXSH6

Amazon currently serves this help content through its Fire TV support system.

Source class: manufacturer support documentation  
Checked: 2026-09-14

Amazon's generic Fire TV setup sequence requires:

1. connect the Fire TV to the display/power;
2. select a language and connect to Wi-Fi;
3. sign in to or create an Amazon account;
4. complete on-screen setup.

### What this proves

- normal stock provisioning has network and Amazon-account dependence.

### What this does not prove

- that a previously provisioned sideloaded application cannot execute during an internet outage;
- that every custom application itself requires Amazon cloud services;
- that the stock launcher remains fully useful offline.

The record therefore marks vendor-cloud provisioning as required while leaving full offline operation `unknown`.

## Source 5 — Official factory reset

Source:

- https://www.amazon.com/gp/help/customer/display.html?nodeId=GBVZEZKT6A6LH4UP

Amazon currently serves this help content through its Fire TV support system.

Source class: manufacturer support documentation  
Checked: 2026-09-14

Amazon documents factory reset from settings or through a remote-button combination. It explicitly states that factory reset removes account information and downloaded content, after which remote-pairing/setup instructions appear again.

### Recovery interpretation

```text
configured Fire OS state
  -> official factory reset
  -> fresh setup state
  -> account information and downloaded content removed
```

### What this proves

- an official user-accessible reset path exists for the normal configured state;
- the reset is destructive to account/downloaded state;
- the device returns to a setup flow after reset.

### What this does not prove

- recovery from corrupted boot firmware;
- availability of an official flash image;
- USB/bootloader recovery;
- recovery after unsupported low-level modification;
- preservation of arbitrary local application data.

## Power truth boundary

No credible exact-model wall-power measurement was collected in this activation. `idle_watts` and `active_watts` therefore remain `unknown`, and `measured` remains `false`.

Do not substitute a USB adapter rating, a neighboring Fire TV model, or a marketplace claim for measured consumption.

## Economics truth boundary

No dated NL/EU used-market sample was collected. The exact specification establishes that this model was sold through `amazon.nl`, but historical retail availability is not a current used-price measurement.

Economics remains `not_collected`.

## Schema pressure learned from this device

The useful lesson is:

```text
developer execution surface != administrator ownership of the operating system
```

The Fire TV Stick can run user-supplied APKs through a documented, consent-visible ADB path. That is real machine capability. But the current evidence does not establish root, bootloader control, fully local provisioning, unattended app restart, or low-level recovery.

A future matcher must be able to value a sandboxed/application-level runtime without silently upgrading it to a general-purpose root computer.

## Root gate

**Truth:** execution is scoped to documented APK/ADB capability; privilege, power, unattended startup and offline behavior remain bounded or unknown.  
**Agency / non-domination:** ADB requires enabling developer settings and first-connection authorization on the device; no bypass path is claimed.  
**Continuity:** exact build model, source URLs, reset semantics and open unknowns are preserved here.  
**Wisdom before speed:** the device is not promoted into the low-power registry comparison merely because it has 2 GB RAM and Wi-Fi; boot, service restart, cloud dependence and power still matter.
