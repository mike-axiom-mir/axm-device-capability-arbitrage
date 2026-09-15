#!/usr/bin/env python3
"""Validate continuity between machine-readable evidence claims and narrative packets.

The existing packet-sync gate proves that every device has exactly one evidence packet
and that its metadata agrees with the YAML record. This gate closes a different gap:
for every evidence claim, the claim's primary source must still be discoverable in that
device's narrative evidence packet.

This is intentionally a continuity check, not a web verifier. It does not fetch sources,
judge source quality, or promote evidence strength.
"""
from __future__ import annotations

import html
import re
import sys
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit, urlunsplit

import yaml

ROOT = Path(__file__).resolve().parents[1]
DEVICE_REF_RE = re.compile(r"`(devices/[^`\n]+\.yaml)`")
URL_RE = re.compile(r"https?://[^\s<>`\"']+")


class ValidationError(Exception):
    pass


def load_yaml(path: Path) -> dict[str, Any]:
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        raise ValidationError(f"invalid YAML: {exc}") from exc
    if not isinstance(data, dict):
        raise ValidationError("top-level YAML value must be a mapping")
    return data


def require_string(value: Any, context: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValidationError(f"{context} must be a non-empty string")
    return value.strip()


def normalize_url(raw: str) -> str:
    """Normalize a source URL enough to compare document identity conservatively.

    Fragments are removed because a packet may preserve the source document without the
    machine-readable claim's deep-link anchor. Host/scheme case and a non-root trailing
    slash are normalized. Query strings are preserved because they can identify a
    materially different source view.
    """

    value = html.unescape(raw.strip()).rstrip(".,;:")
    parts = urlsplit(value)
    if parts.scheme.lower() not in {"http", "https"} or not parts.netloc:
        return value

    path = parts.path
    if path not in {"", "/"}:
        path = path.rstrip("/")
    return urlunsplit((parts.scheme.lower(), parts.netloc.lower(), path, parts.query, ""))


def packet_device_ref(path: Path, text: str) -> str:
    header = text.split("\n## ", 1)[0]
    refs = list(dict.fromkeys(DEVICE_REF_RE.findall(header)))
    if len(refs) != 1:
        rel = path.relative_to(ROOT)
        raise ValidationError(
            f"{rel} metadata must reference exactly one `devices/...yaml` record; "
            f"found {refs or 'none'}"
        )
    return refs[0]


def index_packets() -> dict[str, tuple[Path, str, set[str]]]:
    packets: dict[str, tuple[Path, str, set[str]]] = {}
    for path in sorted((ROOT / "evidence").glob("**/*.md")):
        text = path.read_text(encoding="utf-8")
        device_ref = packet_device_ref(path, text)
        if device_ref in packets:
            first = packets[device_ref][0].relative_to(ROOT)
            raise ValidationError(
                f"duplicate evidence packets for {device_ref}: {first} and {path.relative_to(ROOT)}"
            )
        urls = {normalize_url(match.group(0)) for match in URL_RE.finditer(text)}
        packets[device_ref] = (path, text, urls)
    return packets


def source_is_preserved(source: str, packet_text: str, packet_urls: set[str]) -> bool:
    normalized = normalize_url(source)
    if normalized.startswith("http://") or normalized.startswith("https://"):
        return normalized in packet_urls

    # Repo-local or other non-URL source identifiers are allowed by the early schema,
    # but they must be preserved literally in the packet so another researcher can
    # discover what the claim referred to.
    return source in packet_text


def validate_device(
    path: Path,
    packets: dict[str, tuple[Path, str, set[str]]],
) -> tuple[int, str]:
    rel = path.relative_to(ROOT).as_posix()
    data = load_yaml(path)
    evidence = data.get("evidence")
    if not isinstance(evidence, dict):
        raise ValidationError("evidence must be a mapping")
    claims = evidence.get("claims")
    if not isinstance(claims, list):
        raise ValidationError("evidence.claims must be a list")

    if rel not in packets:
        raise ValidationError(f"no narrative evidence packet found for {rel}")
    packet_path, packet_text, packet_urls = packets[rel]

    for index, claim in enumerate(claims):
        context = f"evidence.claims[{index}]"
        if not isinstance(claim, dict):
            raise ValidationError(f"{context} must be a mapping")
        claim_id = require_string(claim.get("id"), f"{context}.id")
        source = require_string(claim.get("source"), f"{context}.source")
        if not source_is_preserved(source, packet_text, packet_urls):
            raise ValidationError(
                f"claim {claim_id!r} primary source is missing from "
                f"{packet_path.relative_to(ROOT)}: {source}"
            )

    return len(claims), packet_path.relative_to(ROOT).as_posix()


def main() -> int:
    device_paths = sorted((ROOT / "devices").glob("**/*.yaml"))
    if not device_paths:
        print("FAIL no device YAML records found", file=sys.stderr)
        return 1

    try:
        packets = index_packets()
    except (ValidationError, OSError) as exc:
        print(f"FAIL evidence source continuity index: {exc}", file=sys.stderr)
        return 1

    errors: list[str] = []
    claim_count = 0

    for path in device_paths:
        rel = path.relative_to(ROOT)
        try:
            count, packet_rel = validate_device(path, packets)
            claim_count += count
            print(f"PASS {rel}: {count} primary claim source(s) preserved in {packet_rel}")
        except (ValidationError, OSError) as exc:
            errors.append(f"FAIL {rel}: {exc}")

    print()
    print(
        f"Checked primary-source continuity for {claim_count} evidence claim(s) "
        f"across {len(device_paths)} device record(s)."
    )

    if errors:
        print("\nValidation errors:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(
        "Every machine-readable evidence claim preserves its primary source in the "
        "corresponding narrative evidence packet."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
