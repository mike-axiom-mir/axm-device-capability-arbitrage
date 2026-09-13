# Evidence Packet — Kobo Clara HD (N249)

**Record:** `devices/kobo/clara-hd-n249.yaml`  
**Checked:** 2026-09-13  
**Local hardware test:** No  
**Current overall state:** `COMMUNITY_VERIFIED`

## Why this device matters

The Clara HD is useful to the capability-arbitrage research because it is marketed as an e-reader, yet public tooling demonstrates that Kobo devices can host custom native applications and launch local commands/scripts.

The important finding is not that the screen can show a custom application. The important finding is that the device exposes a usable local execution surface that is richer than the marketed reading workflow implies.

At the same time, an e-reader introduces constraints that a router does not: aggressive suspend behavior, slow/partial display refresh characteristics, battery-first design and uncertain unattended service behavior. Those differences are useful pressure on the schema.

## Evidence 1 — Exact device identity

Rakuten Kobo's support page identifies the **Kobo Clara HD** as model **N249** and shows the external power button and USB port.

Source:

- https://help.kobo.com/hc/en-us/articles/360019127253-Kobo-Clara-HD

This proves the model identity used by the census record. It does not prove any third-party execution capability.

## Evidence 2 — Official display/storage facts

Kobo's 2018 launch announcement states that Clara HD has:

- a 6-inch HD Carta E Ink touchscreen;
- 300 ppi display density;
- ComfortLight PRO;
- 8 GB marketed storage.

Source:

- https://www.kobo.com/news/rakuten-kobo-launches-kobo-clara-hd-its-newest-entry-level-feature-rich-ereader

This is useful product-level evidence but is not evidence of CPU architecture, RAM, privilege or arbitrary code execution.

## Evidence 3 — Clara HD-specific custom native application execution

KOReader is a substantial third-party native application for e-readers.

The KOReader source tree contains an explicit **Kobo Clara HD** device definition (`KoboNova`). A May 2026 issue additionally documents a real **Kobo Clara HD running firmware 4.38.23171** where newer KOReader nightlies regressed and the user returned to a known working build.

Sources:

- https://github.com/koreader/koreader/blob/master/frontend/device/kobo/device.lua
- https://github.com/koreader/koreader/issues/15444

What this establishes:

- Clara HD is a real KOReader target, not merely a generic Kobo assumption;
- third-party native application execution on the exact product is community-demonstrated;
- application rollback can restore a known-working third-party build after a software regression.

What this does **not** establish:

- root privilege;
- bootloader control;
- unattended startup of arbitrary services;
- compatibility with every firmware revision;
- always-on networking suitability.

## Evidence 4 — Script / process execution layer

NickelMenu describes itself as a way to launch custom scripts, change settings and run actions on Kobo eReaders. It is installed by copying `KoboRoot.tgz` to the reader's `.kobo` directory.

Its command-action documentation contains `cmd_spawn` / `cmd_output` examples that execute local commands and can start a telnet daemon.

Sources:

- https://github.com/pgaskin/NickelMenu
- https://github.com/pgaskin/NickelMenu/blob/master/res/doc

Important constraint at check date:

> NickelMenu's README says firmware **5.x is not supported yet**.

Therefore the census must not simplify this into "all Clara HD firmware supports NickelMenu." The execution path is version-sensitive.

## Evidence 5 — Recovery

Kobo documents a manual factory-reset procedure covering the Clara HD. The documentation states that the reset removes locally added books, settings and account state and returns the eReader to its original settings.

Source:

- https://help.kobo.com/hc/en-us/articles/360017605314-Manual-reset-your-Kobo-Clara-Colour-Kobo-Clara-BW-Kobo-Clara-HD-Kobo-Nia-Kobo-Elipsa-Kobo-Clara-2E-Kobo-Elipsa-2E

NickelMenu also documents its own uninstall path and a failsafe trigger.

That makes recovery materially better than a modification path with no documented exit, but the current evidence still does **not** prove low-level firmware or bootloader recovery.

## Current unknowns deliberately preserved

The record does not currently claim:

- exact SoC;
- exact RAM;
- exact CPU clock;
- exact custom-code privilege level;
- measured idle/active power;
- unattended auto-start;
- long-running network-service stability;
- bootloader access;
- used-market price;
- hardware-level recovery beyond documented factory reset.

These are research tasks, not blanks to fill from neighboring models or forum memory.

## Preliminary role implications

The evidence supports research into roles such as:

- local/offline script host;
- low-refresh human/machine status display;
- offline data courier;
- local interactive control surface.

The evidence does **not** yet justify calling it a good always-on registry or mesh node. E-reader sleep/network behavior and real power measurements need to be part of that decision.

## Truth boundary

`COMMUNITY_VERIFIED` here means there is exact-model community evidence of real third-party application execution. It does not mean AXM has physically tested a Clara HD.

Promotion to `LOCALLY_VERIFIED` requires a controlled local test with device/firmware identity, installation steps, observed execution, failure notes and recovery receipt preserved in the repo.
