# Evidence Source Continuity Gate

**Status:** Mechanical Truth + Continuity guard for the early v0.1 evidence model.

## Purpose

`tools/validate_evidence_packets.py` already proves that every device record has exactly one narrative evidence packet and that the packet agrees with the YAML record on checked date, overall evidence state, and local-verification status.

That is necessary, but it leaves a source-chain gap: a machine-readable `evidence.claims[].source` or `evidence.claims[].additional_sources[]` entry can be changed, removed, or replaced while the narrative packet still points at an older evidence trail. Both files can remain structurally valid while no longer preserving the same declared provenance.

This gate closes that gap.

## Invariant

For every device under `devices/**/*.yaml`:

1. locate the corresponding `evidence/**/*.md` packet through its metadata device reference;
2. read every machine-readable claim's required primary `source` plus every optional `additional_sources[]` entry;
3. require that **every declared source** is still discoverable in that device's narrative packet.

For HTTP(S) sources, comparison is conservative:

- scheme and host case are normalized;
- a non-root trailing slash is ignored;
- URL fragments are ignored because a packet may preserve the source document without preserving one deep-link anchor;
- query strings are preserved because they can identify a materially different source view.

For non-URL source identifiers, the value must be preserved literally in the packet.

## What this gate does not prove

Passing this validator does **not** prove that:

- a URL is currently reachable;
- a source is authoritative, trustworthy, or current;
- the narrative interpretation of the source is correct;
- a source proves every machine-readable claim attached to it;
- undeclared additional/supporting sources are complete;
- local verification occurred;
- any evidence state should be promoted.

Those questions remain owned by the claim-scope, structured-evidence-strength, packet-sync, local-verification, and human research methods already present in the repository.

The validator deliberately performs no network fetch. CI therefore remains reproducible even if an external site is temporarily unavailable.

## Why all declared sources are now protected

The first version of this gate protected the required primary `source` only. That was the smallest safe continuity invariant.

The census now has machine-readable claims that intentionally preserve more than one source. For example, the TI-Nspire CX II-T record uses `additional_sources` to keep a product-family page alongside the primary specification and to keep a second manufacturer exam guide alongside the primary regional exam-mode page.

Once a supporting source is explicitly declared in the machine-readable claim, silently losing it from the narrative packet is still provenance loss. The gate therefore now protects the whole declared source set rather than only its first entry.

This does **not** require researchers to invent a supporting source where none is justified. `additional_sources` remains optional; the validator only preserves evidence references that the record actually declares.

## Failure examples

The gate fails if:

```text
YAML claim primary source
  -> https://vendor.example/manual-v2

narrative evidence packet
  -> only preserves https://vendor.example/manual-v1
```

It also fails when the primary source is preserved but a declared supporting source silently disappears:

```text
YAML claim
  source: https://vendor.example/specification
  additional_sources:
    - https://vendor.example/recovery-guide

narrative evidence packet
  -> specification is present
  -> recovery guide is absent
```

It does not fail merely because the packet uses a URL fragment and the YAML stores the same source document without that fragment, or vice versa.

## Run locally

```bash
python tools/validate_evidence_source_continuity.py
```

The GitHub validation workflow runs this immediately after evidence-packet synchronization so one-to-one packet identity is established before source continuity is checked.

## Root compatibility

### Truth

Machine-readable evidence cannot silently point somewhere different from the narrative evidence trail, including supporting sources that may carry a separate part of the claim boundary.

### Agency / non-domination

The gate adds no hidden control and performs no external action. It only validates repository-owned evidence references.

### Continuity

A future human or machine can follow every declared claim source from either representation without depending on chat history or a temporary operator.

### Wisdom before speed

The guard protects declared provenance without adding live-network availability tests, source-ranking heuristics, or a requirement to collect unnecessary supporting sources. It strengthens reproducibility without pretending to solve source quality mechanically.
