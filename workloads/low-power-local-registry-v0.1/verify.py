#!/usr/bin/env python3
"""Functional check for the common AXM registry workload.

This proves protocol and restart persistence on the CI runner only. It does not
prove behavior on any census device.
"""
from __future__ import annotations

import signal
import socket
import subprocess
import sys
import tempfile
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BINARY = ROOT / "axm-registry"
PORT = 18087


def query(command: str) -> str:
    with socket.create_connection(("127.0.0.1", PORT), timeout=2) as sock:
        sock.sendall((command + "\n").encode("ascii"))
        chunks = []
        while True:
            data = sock.recv(1024)
            if not data:
                break
            chunks.append(data)
            if b"\n" in data:
                break
        return b"".join(chunks).decode("ascii").strip()


def wait_ready(proc: subprocess.Popen[str]) -> None:
    deadline = time.time() + 5
    while time.time() < deadline:
        if proc.poll() is not None:
            raise RuntimeError(f"registry exited early with {proc.returncode}")
        try:
            if query("PING") == "PONG":
                return
        except OSError:
            time.sleep(0.05)
    raise RuntimeError("registry did not become ready")


def start(state: Path) -> subprocess.Popen[str]:
    proc = subprocess.Popen(
        [str(BINARY), str(state), str(PORT)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    wait_ready(proc)
    return proc


def stop(proc: subprocess.Popen[str]) -> None:
    if proc.poll() is None:
        proc.send_signal(signal.SIGTERM)
        try:
            proc.wait(timeout=2)
        except subprocess.TimeoutExpired:
            proc.kill()
            proc.wait(timeout=2)
    if proc.returncode not in (0, -signal.SIGTERM):
        stdout, stderr = proc.communicate()
        raise RuntimeError(
            f"registry exited with {proc.returncode}\nstdout={stdout}\nstderr={stderr}"
        )


def expect(command: str, expected: str) -> None:
    actual = query(command)
    if actual != expected:
        raise AssertionError(f"{command!r}: expected {expected!r}, got {actual!r}")


def main() -> int:
    if not BINARY.exists():
        print(f"missing {BINARY}; compile registry.c first", file=sys.stderr)
        return 2

    with tempfile.TemporaryDirectory(prefix="axm-registry-") as tmp:
        state = Path(tmp) / "registry.tsv"
        proc = start(state)
        try:
            expect("PING", "PONG")
            expect("COUNT", "COUNT 0")
            expect("PUT node01 1", "OK")
            expect("PUT node02 1", "OK")
            expect("GET node01", "VALUE 1")
            expect("COUNT", "COUNT 2")
            expect("PUT node01 2", "OK")
            expect("GET missing", "NOT_FOUND")
        finally:
            stop(proc)

        proc = start(state)
        try:
            expect("GET node01", "VALUE 2")
            expect("GET node02", "VALUE 1")
            expect("COUNT", "COUNT 2")
        finally:
            stop(proc)

        rows = state.read_text(encoding="utf-8").splitlines()
        if sorted(rows) != ["node01\t2", "node02\t1"]:
            raise AssertionError(f"unexpected persisted rows: {rows!r}")

    print("PASS common registry workload protocol + restart persistence")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
