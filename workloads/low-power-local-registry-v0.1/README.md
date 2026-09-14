# Common workload — low-power local registry v0.1

This directory contains the first **shared executable workload** for the repository's cross-category arbitrage comparison.

It exists to remove a major comparison ambiguity: Archer C7 v5, Synology DS220+, and Dell Wyse 3040 should not be compared using three different "small server" stories. They need the same software behavior and the same observation protocol.

## Truth boundary

The workload is implemented and host-CI tested. It has **not** yet been run on any of the three candidate devices.

CI proves only that the C source compiles on the Ubuntu runner, the line protocol works, and state acknowledged by the service survives a normal process restart. CI does **not** prove MIPS/OpenWrt compatibility, DSM/container compatibility, Wyse compatibility, wall power, hard-power-loss integrity, or service autostart on physical hardware.

Those candidate-specific facts remain `not_collected` until they are actually measured.

## Why C99/POSIX

The current comparison spans a resource-constrained MIPS OpenWrt router and x86-64 Linux/container systems. A small C/POSIX implementation keeps runtime dependencies near zero and avoids making Python, Node, Java, or a container engine a hidden requirement of the common workload itself.

This is a comparison fixture, not a production registry.

## Build

```sh
make
```

Equivalent explicit command:

```sh
cc -std=c99 -O2 -Wall -Wextra -Werror registry.c -o axm-registry
```

No prebuilt binaries are committed. Each target must preserve the compiler/toolchain and exact build command used.

## Run

```sh
./axm-registry /var/lib/axm-registry/state.tsv 8087
```

Protocol, one command per TCP connection:

```text
PING
PUT <key> <value>
GET <key>
COUNT
```

Example replies:

```text
PONG
OK
VALUE alive
COUNT 32
```

Keys and values are deliberately single tokens. v0.1 is intentionally tiny and bounded: maximum 64 records, 31-byte keys, and 95-byte values.

## Persistence semantics

For `PUT`, the service writes the complete small registry to a sibling temporary file, flushes it, calls `fsync`, atomically renames it over the state path, then calls `fsync` on the parent directory. `OK` is returned only if that sequence succeeds.

This gives the hard-power-loss trial a precise question: **does the last acknowledged value survive the candidate's real storage/filesystem/power path?** It does not guarantee that every filesystem or storage stack will satisfy the promise under sudden power loss; that is exactly what the physical test must discover.

The implementation rewrites the small state file on each durable `PUT`. That is acceptable for this bounded comparison fixture, but its write amplification and flash-wear implications must be counted when interpreting router/eMMC results.

## Standard comparison profile

The canonical parameters live in `workload.yaml`:

- 32 total records after seeding;
- LAN-only client on another machine;
- one `PING` per second;
- one rotating `GET` per second;
- one durable heartbeat `PUT` every 60 seconds;
- 5-minute warm-up;
- 30-minute measurement window;
- no WAN/vendor-cloud requirement.

The external driver is:

```sh
python3 benchmark_client.py 192.0.2.10
```

Use a shorter duration only for smoke testing. A ranking-quality run should preserve the canonical profile.

## Required evidence from each candidate

Do not replace missing observations with vendor claims. Preserve at least:

1. exact device/revision/configuration and software state;
2. build/install command plus binary/package size;
3. elapsed provisioning time;
4. state-file size after the 32-record seed;
5. best available process memory and CPU/load evidence;
6. wall power before workload and during the measurement window, with meter/method noted;
7. autostart method;
8. last acknowledged heartbeat before the power-loss trial;
9. state observed after reboot;
10. elapsed power-restore -> service-ready time;
11. failures and any manual intervention.

## Hard-power-loss trial

After at least one acknowledged durable `PUT`:

1. record the acknowledged value;
2. remove external power without gracefully stopping the service;
3. restore power;
4. wait for the configured device/service autostart path;
5. query the service from the LAN client;
6. verify whether the last acknowledged value is present;
7. record boot-to-service-ready time and any intervention;
8. target five repetitions before calling the behavior repeatable.

Only perform this on owned/authorized noncritical hardware. The test should not be generalized to safety-critical or hazardous systems.

## CI check

```sh
make test
```

`verify.py` starts the service on the CI host, exercises `PING`, `PUT`, `GET`, and `COUNT`, stops it, restarts it from the same state file, and verifies the acknowledged values are still present.

## What changes in the comparison now

The comparison no longer lacks a common workload **definition or implementation**. It still lacks candidate runs. Until all candidates have comparable results, `decision: no_ranked_winner` remains the truthful state.
