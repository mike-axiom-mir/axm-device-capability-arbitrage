#!/usr/bin/env python3
"""Drive the deterministic low-power registry comparison profile from another host."""
from __future__ import annotations

import argparse
import json
import socket
import time


def query(host: str, port: int, command: str) -> str:
    with socket.create_connection((host, port), timeout=3) as sock:
        sock.sendall((command + "\n").encode("ascii"))
        data = bytearray()
        while b"\n" not in data:
            chunk = sock.recv(1024)
            if not chunk:
                break
            data.extend(chunk)
        return data.decode("ascii").strip()


def expect(host: str, port: int, command: str, prefix: str) -> str:
    result = query(host, port, command)
    if not result.startswith(prefix):
        raise RuntimeError(f"{command!r}: expected prefix {prefix!r}, got {result!r}")
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("host")
    parser.add_argument("--port", type=int, default=8087)
    parser.add_argument("--duration", type=int, default=1800)
    parser.add_argument("--tick", type=float, default=1.0)
    parser.add_argument("--write-interval", type=int, default=60)
    args = parser.parse_args()

    if args.duration < 1 or args.tick <= 0 or args.write_interval < 1:
        parser.error("duration, tick, and write-interval must be positive")

    for i in range(31):
        expect(args.host, args.port, f"PUT node{i:02d} seeded", "OK")
    expect(args.host, args.port, "PUT heartbeat 0", "OK")
    if expect(args.host, args.port, "COUNT", "COUNT ") != "COUNT 32":
        raise RuntimeError("seed count is not 32")

    start = time.monotonic()
    deadline = start + args.duration
    next_tick = start
    tick_no = 0
    writes = 0
    pings = 0
    reads = 0
    next_write_at = start + args.write_interval

    while True:
        now = time.monotonic()
        if now >= deadline:
            break
        if now < next_tick:
            time.sleep(min(next_tick - now, 0.1))
            continue

        expect(args.host, args.port, "PING", "PONG")
        pings += 1
        node = tick_no % 31
        expect(args.host, args.port, f"GET node{node:02d}", "VALUE ")
        reads += 1

        elapsed_whole = int(now - start)
        if now >= next_write_at:
            expect(args.host, args.port, f"PUT heartbeat {elapsed_whole}", "OK")
            writes += 1
            while next_write_at <= now:
                next_write_at += args.write_interval

        tick_no += 1
        next_tick = start + tick_no * args.tick

    final_heartbeat = expect(args.host, args.port, "GET heartbeat", "VALUE ")
    print(json.dumps({
        "workload_id": "low-power-local-registry-v0.1",
        "duration_seconds_requested": args.duration,
        "ticks": tick_no,
        "pings": pings,
        "reads": reads,
        "durable_writes": writes,
        "final_heartbeat": final_heartbeat.removeprefix("VALUE "),
        "count": expect(args.host, args.port, "COUNT", "COUNT "),
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
