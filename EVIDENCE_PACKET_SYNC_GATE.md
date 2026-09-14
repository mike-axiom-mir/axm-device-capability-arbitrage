# Evidence Packet Synchronization Gate

**Status:** Active validation rule.  
**Purpose:** Keep human-readable evidence packets and machine-readable device evidence state synchronized one-to-one.

## Why this exists

The repository intentionally stores both:

- `devices/**/*.yaml` for machine-readable capability and evidence state; and
- `evidence/**/*.md` for the narrative source packet, claim boundaries, unknowns, recovery context, and root check.

Before this gate, CI could validate each side independently while still allowing silent drift:

- a device's `evidence.last_checked` could change without its evidence packet;
- a packet could say `DOCUMENTED` while the YAML said `COMMUNITY_VERIFIED`;
- a packet could still say no local verification after the YAML was promoted;
- a new device could land without a durable narrative evidence packet;
- two packets could accidentally point at the same device.

That is both a Truth and Continuity problem: people and machines could read different repository states.

## Required invariant

For every device under `devices/**/*.yaml`:

1. exactly one Markdown evidence packet exists beneath `evidence/`;
2. that packet's front metadata references the exact device-record path;
3. `Checked` is canonical `YYYY-MM-DD` and equals `evidence.last_checked`;
4. the packet truth state equals `evidence.overall_state`;
5. the packet local-verification Yes/No value equals `evidence.locally_verified`;
6. no evidence packet may reference a missing device or duplicate another packet's target.

Existing historical labels are accepted, including:

- `Device record` and `Record`;
- `Evidence state`, `Current evidence state`, and `Current overall state`;
- `Local verification`, `Local hardware test`, and `Locally reproduced by AXM`.

The semantic values are the invariant; cosmetic label age is not.

## What this does not prove

This gate does **not**:

- fetch or trust external URLs;
- decide whether a source is factually correct;
- decide whether `proves` wording faithfully represents a source;
- promote or demote evidence state;
- create local verification;
- substitute product documentation for physical measurement;
- impose an automatic evidence-expiry policy.

Those responsibilities remain with source review, the claim-scope and evidence-strength gates, and preserved local experiment receipts.

## Validation order

```text
base record structure
  -> claim scope
  -> evidence packet synchronization
  -> evidence strength
  -> census / market / comparison / experiment gates
```

The packet-sync gate sits after basic claim structure because it compares already-parseable repository state, and before evidence-strength validation because human and machine summaries should agree before downstream semantics are evaluated.

## Failure examples

```text
packet Checked: 2026-09-13
YAML evidence.last_checked: 2026-09-14
=> FAIL

packet Current evidence state: DOCUMENTED
YAML evidence.overall_state: COMMUNITY_VERIFIED
=> FAIL

device YAML exists
no evidence packet points to it
=> FAIL

two evidence packets -> same device path
=> FAIL
```

## Why one packet per device

The one-to-one rule does not mean one source per device. A packet can and often does preserve many independent manufacturer, upstream, community, and recovery sources.

The rule means there is one durable narrative evidence boundary for the current machine-readable device record. That keeps a future reader from having to guess which of several packets describes the canonical current evidence state.

If a device later needs large specialized evidence studies, those can exist as supporting research artifacts, while the canonical evidence packet remains the single synchronization target.

## Root gate

**Truth:** human-readable and machine-readable evidence summaries cannot silently disagree about checked date, truth state, or local verification.  
**Agency / non-domination:** the gate only reports inconsistency; it never auto-promotes, rewrites, or hides uncertainty.  
**Continuity:** every device keeps exactly one durable narrative evidence packet linked to its machine-readable record.  
**Wisdom before speed:** consistency is required before adding more volume; the gate does not invent source credibility or hardware verification merely to make records pass.
