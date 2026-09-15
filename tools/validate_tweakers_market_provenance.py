#!/usr/bin/env python3
"""Validate Tweakers provenance inside market snapshots.

The generic market-snapshot schema uses ``source_scope`` for capture mode
(``direct_listing``, ``search_result_snapshot``, ``direct_retailer_offer``).
Tweakers has a separate provenance dimension: Pricewatch, Vraag & Aanbod,
community/forum, review, or editorial. This gate keeps those meanings separate
and prevents community or aggregate Pricewatch pages from being silently
represented as direct acquisition-price observations.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

import yaml

ROOT = Path(__file__).resolve().parents[1]

TWEAKERS_VA_MARKETPLACE = "Tweakers_Vraag_En_Aanbod"
TWEAKERS_VA_SOURCE_SURFACE = "tweakers_vraag_en_aanbod_listing"
TWEAKERS_VA_PRICE_TYPES = {"asking", "displayed_sold_listing_price"}


class ValidationError(Exception):
    pass


def load_yaml(path: Path) -> dict[str, Any]:
    try:
        raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        raise ValidationError(f"invalid YAML: {exc}") from exc
    if not isinstance(raw, dict):
        raise ValidationError("top-level YAML value must be a mapping")
    return raw


def require_string(value: Any, context: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValidationError(f"{context} must be a non-empty string")
    return value


def is_tweakers_host(hostname: str | None) -> bool:
    if hostname is None:
        return False
    host = hostname.lower().rstrip(".")
    return host == "tweakers.net" or host.endswith(".tweakers.net")


def iter_observations(data: dict[str, Any]):
    candidates = data.get("candidates")
    if not isinstance(candidates, list):
        raise ValidationError("candidates must be a list")

    for candidate_index, candidate in enumerate(candidates):
        if not isinstance(candidate, dict):
            raise ValidationError(f"candidates[{candidate_index}] must be a mapping")
        cohorts = candidate.get("cohorts")
        if not isinstance(cohorts, list):
            raise ValidationError(f"candidates[{candidate_index}].cohorts must be a list")

        for cohort_index, cohort in enumerate(cohorts):
            if not isinstance(cohort, dict):
                raise ValidationError(
                    f"candidates[{candidate_index}].cohorts[{cohort_index}] must be a mapping"
                )
            observations = cohort.get("observations")
            if not isinstance(observations, list):
                raise ValidationError(
                    f"candidates[{candidate_index}].cohorts[{cohort_index}].observations "
                    "must be a list"
                )

            for observation_index, observation in enumerate(observations):
                if not isinstance(observation, dict):
                    raise ValidationError(
                        f"candidates[{candidate_index}].cohorts[{cohort_index}]."
                        f"observations[{observation_index}] must be a mapping"
                    )
                context = (
                    f"candidates[{candidate_index}].cohorts[{cohort_index}]."
                    f"observations[{observation_index}]"
                )
                yield context, observation


def validate_tweakers_observation(context: str, observation: dict[str, Any]) -> bool:
    source = require_string(observation.get("source"), f"{context}.source")
    parsed = urlparse(source)
    if not is_tweakers_host(parsed.hostname):
        return False

    host = (parsed.hostname or "").lower().rstrip(".")
    path = parsed.path.lower()

    if host == "gathering.tweakers.net":
        raise ValidationError(
            f"{context}: Tweakers community/forum pages are research leads, "
            "not raw acquisition-price observations"
        )

    if path.startswith("/aanbod/"):
        marketplace = require_string(
            observation.get("marketplace"), f"{context}.marketplace"
        )
        if marketplace != TWEAKERS_VA_MARKETPLACE:
            raise ValidationError(
                f"{context}: Tweakers /aanbod/ observations must use "
                f"marketplace={TWEAKERS_VA_MARKETPLACE!r}"
            )

        source_scope = require_string(
            observation.get("source_scope"), f"{context}.source_scope"
        )
        if source_scope != "direct_listing":
            raise ValidationError(
                f"{context}: Tweakers /aanbod/ observations are direct listings; "
                "source_scope must remain the generic capture mode 'direct_listing'"
            )

        listed_at = require_string(observation.get("listed_at"), f"{context}.listed_at")
        if listed_at == "unknown":
            raise ValidationError(
                f"{context}: Tweakers Vraag & Aanbod observation must preserve "
                "the visible listing date"
            )

        require_string(observation.get("seller_class"), f"{context}.seller_class")
        require_string(observation.get("model_identity"), f"{context}.model_identity")
        configuration = observation.get("configuration")
        if not isinstance(configuration, dict) or not configuration:
            raise ValidationError(
                f"{context}.configuration must be a non-empty mapping"
            )

        price_type = require_string(
            observation.get("price_type"), f"{context}.price_type"
        )
        if price_type not in TWEAKERS_VA_PRICE_TYPES:
            allowed = ", ".join(sorted(TWEAKERS_VA_PRICE_TYPES))
            raise ValidationError(
                f"{context}: Tweakers Vraag & Aanbod price_type {price_type!r} "
                f"must be one of: {allowed}"
            )

        source_surface = observation.get("source_surface")
        if source_surface is not None:
            surface = require_string(source_surface, f"{context}.source_surface")
            if surface != TWEAKERS_VA_SOURCE_SURFACE:
                raise ValidationError(
                    f"{context}: Tweakers /aanbod/ source_surface must be "
                    f"{TWEAKERS_VA_SOURCE_SURFACE!r}"
                )

        return True

    if path.startswith("/pricewatch/"):
        raise ValidationError(
            f"{context}: Tweakers Pricewatch is retail/variant/price-history context, "
            "not a raw acquisition listing under the current market-snapshot "
            "observation vocabulary; preserve it as supporting evidence until a "
            "dedicated Pricewatch representation exists"
        )

    if path.startswith(("/nieuws/", "/reviews/", "/review/", "/productreview/")):
        raise ValidationError(
            f"{context}: Tweakers editorial/review pages may support discovery or "
            "context, but must not be encoded as raw acquisition-price observations"
        )

    raise ValidationError(
        f"{context}: unclassified Tweakers source path {parsed.path!r}; "
        "classify the evidence surface explicitly instead of guessing"
    )


def main() -> int:
    snapshot_paths = sorted((ROOT / "market_snapshots").glob("**/*.yaml"))
    if not snapshot_paths:
        print("FAIL no market snapshot YAML records found", file=sys.stderr)
        return 1

    errors: list[str] = []
    tweakers_observation_count = 0

    for path in snapshot_paths:
        rel = path.relative_to(ROOT)
        try:
            data = load_yaml(path)
            for context, observation in iter_observations(data):
                if validate_tweakers_observation(context, observation):
                    tweakers_observation_count += 1
            print(f"PASS {rel}")
        except (ValidationError, OSError) as exc:
            errors.append(f"FAIL {rel}: {exc}")

    print()
    print(
        "Validated Tweakers market provenance for "
        f"{tweakers_observation_count} observation(s) across "
        f"{len(snapshot_paths)} market snapshot(s)."
    )

    if errors:
        print("\nValidation errors:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print("All Tweakers market provenance checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
