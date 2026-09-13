# Evidence Packet — Wyze Cam v2 / Thingino

**Device record:** `devices/wyze/cam-v2.yaml`  
**Evidence state:** `COMMUNITY_VERIFIED`  
**Locally reproduced by AXM:** No  
**Checked:** 2026-09-14

## Why this packet exists

Wyze Cam v2 is useful to the census because an inexpensive consumer IP camera contains more than a closed streaming appliance. Current Thingino support turns the same physical camera into a user-controlled embedded Linux camera with local network services and a root administration surface.

It also exposes a schema problem that the first seven records did not make explicit:

```text
same physical hardware
+ stock firmware       -> internet-centred app operation, limited offline recording
+ replacement firmware -> local-first RTSP / ONVIF / Web UI / SSH
```

Locality is therefore not always a permanent property of the device. It can depend on device state just as recovery does.

## Exact hardware identity and variants

Primary Thingino sources:

- https://github.com/themactep/thingino-firmware/blob/master/docs/hardware/supported-hardware.md
- https://github.com/themactep/thingino-firmware/blob/master/configs/cameras/wyze_cam2_t20x_jxf22_rtl8189ftv/wyze_cam2_t20x_jxf22_rtl8189ftv_defconfig
- https://github.com/themactep/thingino-firmware/blob/master/configs/cameras/wyze_cam2_t20x_jxf23_rtl8189ftv/wyze_cam2_t20x_jxf23_rtl8189ftv_defconfig

Thingino currently publishes two Wyze Cam v2 targets:

```text
T20X + JXF22 + RTL8189FTV
T20X + JXF23 + RTL8189FTV
```

The exact defconfigs select the Ingenic T20X / XBurst1 platform.

This matters because `Wyze Cam v2` alone is not enough to choose the correct replacement image. The physical image-sensor variant must remain visible rather than silently inheriting one known configuration.

The record therefore claims only properties supported across both current targets unless a claim is explicitly variant-specific.

## Real replacement-firmware execution

Sources:

- https://github.com/themactep/thingino-firmware/blob/master/docs/hardware/supported-hardware.md
- https://github.com/themactep/thingino-firmware/issues/420
- https://github.com/themactep/thingino-firmware

The supported-hardware list provides current firmware images for both known v2 sensor variants.

Issue #420 is valuable independent evidence because it records an actual Wyze Cam v2 running a `wyze_c2_jxf23` Thingino build and shows commands being run from a `root@webcam` shell. That supports a real root Linux/SSH execution path rather than merely inferring one from the SoC specification.

Thingino itself recommends its stable branch for normal users and warns that the master branch uses experimental U-Boot and is intended for contributors with UART/unbricking skills. This record preserves that distinction instead of treating every branch as equally safe.

## Local camera services

Current Thingino sources:

- https://blog.thingino.com/finding-your-camera-on-the-lan
- https://github.com/themactep/thingino-firmware/blob/master/AGENTS.md

Thingino documents LAN-facing services including:

- a Web UI;
- RTSP streaming;
- ONVIF discovery/service;
- optional MQTT integration;
- SSH/SCP through Dropbear.

The project documentation describes these as local services. The exact-device execution evidence above is what connects the general Thingino runtime to Wyze Cam v2.

The record does not claim that every optional package is enabled in every build or that exposing any of these services to the public internet is appropriate.

## Stock-firmware locality

Wyze sources:

- https://support.wyze.com/hc/en-us/articles/360031483211-Can-I-use-my-Wyze-Cam-v2-Pan-without-Wi-Fi
- https://support.wyze.com/hc/en-us/articles/33883450378523-Which-Wyze-Cams-can-be-used-without-Wi-Fi

Wyze says the stock v2 experience is intended to use an internet connection for live streaming, notifications and settings through the Wyze app.

There is a narrower offline path: after the camera has been configured online with local microSD recording enabled, it can continue recording to the card while offline. During that offline state the normal app live view/settings and cloud alert behavior are unavailable.

So neither of these summaries is accurate:

```text
stock firmware is fully cloud required
stock firmware is fully local
```

The useful statement is capability-scoped: stock firmware retains local recording after provisioning, while several management/live features remain internet-dependent.

## Manufacturer camera / audio / storage evidence

Source:

- https://www.wyze.com/products/wyze-cam-v2

Wyze documents:

- 1920x1080 video;
- a 1/2.9-inch CMOS-class camera;
- four infrared LEDs;
- built-in speaker and microphone;
- microSD continuous recording.

This proves physical capability. It does not by itself prove which of those components replacement firmware exposes through stable application interfaces.

## Stock recovery / firmware flashing

Source:

- https://support.wyze.com/hc/en-us/articles/360031490871-How-to-flash-your-Wyze-Cam-firmware-manually

Wyze currently documents a v2-specific manual firmware flow:

1. put the desired firmware on a FAT32 microSD card;
2. name the v2 image `demo.bin`;
3. power the camera off;
4. insert the card;
5. hold the setup button while restoring power;
6. let the camera flash and reboot.

This establishes a real stock-firmware reflash path for a camera that can still execute that boot flow.

It does **not** prove that the same path can return an arbitrary Thingino-installed or bootloader-damaged unit to stock. That transition remains explicitly unknown in the machine record.

## Thingino recovery

Sources:

- https://github.com/themactep/thingino-firmware/blob/master/docs/firmware-image-structure.md
- https://thingino.com/installation

Thingino documents full firmware images for initial installation, complete replacement and recovery from serious system failures. Depending on hardware access, documented methods include external/in-circuit programmers, UART/U-Boot, USB Cloner and model-specific SD-card installers.

The existence of those project-wide methods does not mean every method works on every Wyze Cam v2. The record therefore preserves the exact-unit installation method as unresolved and does not claim a local AXM unbrick test.

## New schema pressure — locality by device state

The important discovery from this record is:

```text
locality(device) is not necessarily constant
```

For this camera:

```text
stock_wyze_firmware
  -> internet-centred app lifecycle
  -> offline microSD recording survives after prior configuration

thingino_firmware
  -> local RTSP / ONVIF / Web UI / SSH
  -> vendor cloud is not required for normal local runtime
```

The device record therefore carries structured `locality.states` evidence instead of forcing both states into one misleading boolean.

This is analogous to the earlier recovery lesson from the Roborock S5: persistent software state can change what the same hardware means operationally.

## Claims not established here

- exact RAM capacity;
- exact internal flash capacity;
- CPU clock or core count;
- current NL/EU used-market price;
- measured wall power at idle or under streaming load;
- cold-power-loss reliability;
- safe Thingino-to-stock return path;
- which installation method is least risky for every v2 production variant;
- stable raw-frame APIs beyond Thingino's maintained camera/streaming path;
- long-duration resource headroom for non-camera workloads.

## Candidate roles

Grounded or plausible roles:

- local IP camera;
- local vision sensor;
- offline recorder;
- low-end Linux edge node where camera duties remain primary.

A root shell does not make the camera a sensible general-purpose server automatically. RAM, flash, power, thermal behavior and interference with its camera workload still need evidence.

## Next tests

1. Identify JXF22 vs JXF23 on a physical owned unit before selecting firmware.
2. Preserve the stock firmware and current firmware version before modification.
3. Reproduce Thingino installation with the least invasive supported method for that exact unit.
4. Measure wall power at stock idle, Thingino idle and active RTSP streaming.
5. Test cold power loss -> boot -> Wi-Fi -> RTSP/ONVIF/SSH recovery repeatedly.
6. Test stock manual flash on noncritical stock state and separately research whether a supported Thingino-to-stock procedure exists.
7. Collect a dated NL/EU used-market sample with model/variant ambiguity recorded rather than guessed.

## Root check

**Truth:** exact JXF22/JXF23 variants stay visible; RAM, flash, power, market price and Thingino-to-stock recovery remain unknown.  
**Agency / non-domination:** only owned/authorized cameras should be modified; camera placement and recording require appropriate consent and privacy boundaries.  
**Continuity:** exact sources, state-dependent locality and recovery uncertainty are preserved in the repository.  
**Wisdom before speed:** root access is not treated as proof that this is a good general-purpose node; camera utility, recovery burden and modification risk remain part of the decision.
