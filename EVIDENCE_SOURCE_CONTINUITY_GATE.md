# Evidence Source Continuity Gate

**Status:** Mechanical Truth + Continuity guard for the early v0.1 evidence model.

## Purpose

`tools/validate_evidence_packets.py` already proves that every device record has exactly one narrative evidence packet and that the packet agrees with the YAML record on checked date, overall evidence state, and local-verification status.

That is necessary, but it leaves a source-chain gap: a machine-readable `evidence.claims[].source` can be changed, removed, or replaced while the narrative packet still points at an older source. Both files can remain structurally valid while no longer describing the same evidence trail.

This gate closes that gap.

## Invariant

For every device under `devices/**/*.yaml`:

1. locate the corresponding `evidence/**/*.md` packet through its metadata device reference;
2. read every machine-readable `evidence.claims[].source` value;
3. require that the primary source is still discoverable in that device's narrative packet.

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
- additional/supporting sources are complete;
- local verification occurred;
- any evidence state should be promoted.

Those questions remain owned by the claim-scope, structured-evidence-strength, packet-sync, local-verification, and human research methods already present in the repository.

The validator deliberately performs no network fetch. CI therefore remains reproducible even if an external site is temporarily unavailable.

## Why primary sources first

The current machine-readable record contract requires one primary `source` for every evidence claim. `additional_sources` is optional and is already checked structurally by `tools/validate_evidence_claim_scope.py`.

This gate therefore starts with the smallest stable continuity invariant: the required primary source may not silently disappear from the durable narrative packet.

A later extension may also require all `additional_sources` to be mirrored when enough evidence shows that doing so improves continuity without making packets brittle or duplicative.

## Failure examples

The gate fails if:

```text
YAML claim source
  -> https://vendor.example/manual-v2

narrative evidence packet
  -> only preserves https://vendor.example/manual-v1
```

It also fails if a machine-readable claim is added with a source that never appears in the corresponding narrative packet.

It does not fail merely because the packet uses a URL fragment and the YAML stores the same source document without that fragment, or vice versa.

## Run locally

```bash
python tools/validate_evidence_source_continuity.py
```

The GitHub validation workflow runs this immediately after evidence-packet synchronization so one-to-one packet identity is established before source continuity is checked.

## Root compatibility

### Truth

Machine-readable evidence cannot silently point somewhere different from the narrative evidence trail.

### Agency / non-domination

The gate adds no hidden control and performs no external action. It only validates repository-owned evidence references.

### Continuity

A future human or machine can follow the primary source from either representation without depending on chat history or a temporary operator.

### Wisdom before speed

The guard checks the smallest durable invariant and intentionally avoids live-network availability tests or universal source-quality scoring that would create brittle or overreaching CI.
