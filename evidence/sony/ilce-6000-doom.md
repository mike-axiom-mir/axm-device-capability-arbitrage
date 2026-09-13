# Evidence Packet — Sony ILCE-6000 / DoomCam

**Device record:** `devices/sony/ilce-6000.yaml`  
**Evidence state:** `COMMUNITY_VERIFIED`  
**Locally reproduced by AXM:** No  
**Checked:** 2026-09-13

## Why this packet exists

The interesting claim is not "a camera can display Doom."

The useful claim is:

> **A consumer camera marketed for photography exposes a custom software execution surface strong enough to run a native-code application, consume physical camera controls, render custom output, access removable storage, and support debugging paths.**

This is the kind of cross-category evidence this repository is meant to capture.

## Primary working implementation

Source:

- https://github.com/EfelerGibi/A6000-DOOM

The project states that Doom runs on a Sony α6000 as a PlayMemories Camera App.

The implementation documents:

- custom APK installation through Sony-PMCA-RE;
- Doom rendering at its native 320×200 and being presented on the camera panel;
- physical camera controls mapped to Doom actions;
- game data loaded from the removable memory card;
- Android native-code build tooling;
- live debugging through adb when OpenMemories: Tweak is active;
- an Android 2.3.7 compatibility target;
- performance timing showing the display path, rather than game logic, as the approximate frame-rate ceiling in the tested build.

### Strongest claims supported by this source

`COMMUNITY_VERIFIED`:

- a custom PlayMemories APK executes on a tested Sony α6000;
- the app can run native Doom code;
- the app can draw custom frames to the camera display;
- several camera-body controls can be read and mapped by the app;
- the app can read game assets from removable storage;
- adb-based debugging can be used with the documented Tweak workflow.

### Claims this source does not establish

Keep these unknown unless separately evidenced:

- exact SoC;
- exact RAM capacity;
- root privilege during normal custom-app execution;
- unattended auto-start;
- long-term 24/7 reliability;
- safe recovery from every failed modification;
- identical compatibility across every PlayMemories camera.

The author explicitly says the project was tested only on the α6000 and that other PlayMemories cameras may require screen/control changes.

## Execution-platform evidence

Source:

- https://github.com/ma1co/Sony-PMCA-RE

Sony-PMCA-RE documents that cameras supporting PlayMemories Camera Apps can install custom Android applications.

It also documents OpenMemories: Tweak as a path for starting telnet and adb servers to execute code on the system.

The project describes additional updater/service modes that can execute commands on supported cameras, but those deeper paths should be scoped per exact model before being promoted into the ILCE-6000 device record.

Sony-PMCA-RE also warns that the tooling is experimental reverse engineering and may harm hardware. That warning belongs in recovery/risk state rather than being omitted because execution works.

## Manufacturer interface evidence

Source:

- https://www.sony.com/electronics/support/e-mount-body-ilce-6000-series/ilce-6000/specifications

Sony's specification page documents, among other interfaces:

- Wi-Fi;
- NFC;
- Multi/Micro USB;
- mass-storage / MTP / PC-remote modes;
- downloadable camera apps.

This supports interface presence. It does **not** by itself prove arbitrary custom-code access to each interface.

## Performance observation

The DoomCam project reports roughly 26 fps in its optimized build and describes the frame pacing as display-bound rather than CPU-bound.

That is useful evidence that the device has more compute headroom than a simple visual inspection of the product category might suggest.

Do not turn this into a general benchmark. The result is specific to the DoomCam implementation and its tested rendering path.

## Recovery / failure evidence

Current state: insufficient.

Known public notes include:

- Sony-PMCA-RE warns modifications may harm hardware;
- DoomCam reports occasional camera reboots during development, particularly with Wi-Fi enabled.

Missing before deployment recommendation:

- tested factory recovery process;
- exact firmware-version scope;
- brick modes;
- whether a failed APK/app install can always be recovered without specialist tools;
- long-term thermal/power behavior.

## AXM interpretation

The value of this example is structural:

```text
marketed object: camera
        ↓
actual machine properties:
  application runtime
  + native execution
  + storage access
  + physical controls
  + display output
  + Wi-Fi / USB interfaces
        ↓
potential machine roles beyond photography
```

The display is useful evidence for humans, but it is not the fundamental discovery.

The fundamental discovery is the execution surface.

## Next research actions

1. Identify exact SoC/architecture from reliable model-specific evidence.
2. Identify RAM and internal storage from reliable model-specific evidence.
3. Verify exact privilege level of the APK, adb and telnet paths.
4. Map which camera APIs are reachable from custom apps: sensor, microphone, Wi-Fi sockets, USB, storage.
5. Document recovery paths and firmware-version constraints.
6. Collect a dated used-market price snapshot.
7. Compare the ILCE-6000 against conventional embedded nodes for specific capability contracts.
8. Expand the Sony PlayMemories family only through explicit per-model evidence or authoritative supported-model lists.

## Root check

**Truth:** claims are restricted to what the sources establish.  
**Agency:** research concerns user-owned/authorized hardware only.  
**Continuity:** source URLs and claim boundaries are preserved in-repo.  
**Wisdom before speed:** no recommendation is made before recovery, cost and long-term fit are investigated.
