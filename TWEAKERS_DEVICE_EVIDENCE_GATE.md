# Tweakers Device-Evidence Gate — v0.1

**Status:** Narrow evidence-strength guard.  
**Companion:** `TWEAKERS_SOURCE_METHOD.md` and `tools/validate_tweakers_device_evidence.py`.  
**Purpose:** Keep high-value Dutch discovery and community research from silently becoming stronger device truth than the evidence supports.

## 1. Why this gate exists

Tweakers is unusually useful for this repository because one ecosystem exposes several different evidence surfaces:

- **Pricewatch** — product/variant/specification cross-checks and current or historical retail context;
- **Vraag & Aanbod** — dated Dutch used-market observations;
- **Gathering of Tweakers / user community** — modification tricks, failure modes, hidden interfaces, thermal/power observations and device-specific research leads.

Those surfaces do not have the same evidentiary meaning.

A forum post can be an excellent lead and still be weaker than manufacturer documentation, upstream firmware/project documentation, working source code, or a preserved local reproduction. A Vraag & Aanbod listing can be excellent acquisition evidence and still prove nothing about root access, firmware recovery, power consumption, or arbitrary execution. Pricewatch can sharpen variant identity and specification cross-checks without becoming a substitute for an exact-model technical source.

The gate therefore protects **role**, not domain reputation.

## 2. Mechanical rules

### A. Tweakers community/forum as primary source

If the primary source of a positive device evidence claim is a Tweakers community surface, the claim must include explicit stronger corroboration:

```yaml
- id: community_report_with_corroboration
  state: COMMUNITY_VERIFIED
  source: https://gathering.tweakers.net/forum/list_messages/...
  proves:
    - exact bounded claim
  tweakers_corroboration:
    - claim_id: exact_model_upstream_project
      kind: upstream_project_documentation
```

Allowed corroboration kinds are deliberately bounded:

```text
manufacturer_documentation
upstream_project_documentation
working_source_code
local_reproduction
```

The referenced claim must:

- exist in the same device record;
- itself be positive evidence;
- use a non-Tweakers primary source;
- not self-reference the community claim.

This does not magically prove the claim. It proves that the record preserved the stronger evidence relationship instead of allowing a forum anecdote to carry the claim alone.

### B. Tweakers community as additional evidence

A non-Tweakers primary source may include a Tweakers forum/user report in `additional_sources` without extra corroboration metadata.

That keeps the community observation visibly secondary to the already stronger primary evidence.

### C. Non-promoting community leads

Community research leads may be preserved without corroboration when their truth state is non-promoting:

```text
UNRESEARCHED
DEPRECATED
CONTRADICTED
```

That is useful for continuity: a future researcher can see the lead without the machine-readable record pretending it is settled device truth.

### D. Pricewatch inside device evidence

A Pricewatch page may be a positive primary source only at `DOCUMENTED` strength and only when the record declares one of these bounded scopes:

```text
variant_crosscheck
specification_crosscheck
retail_context
historical_retail_context
```

Example:

```yaml
- id: pricewatch_variant_crosscheck
  state: DOCUMENTED
  source: https://tweakers.net/pricewatch/.../product.html
  tweakers_evidence_scope: variant_crosscheck
  proves:
    - Tweakers distinguishes the observed marketed variant from another listed variant
```

This gate does **not** authorize Pricewatch to prove custom execution, privilege, recovery, or local/offline behavior. Those claims still need the source quality appropriate to the claim.

### E. Vraag & Aanbod inside device evidence

A positive device evidence claim may not use a Tweakers `/aanbod/` page as its primary source.

Vraag & Aanbod belongs in the dated acquisition evidence flow under `market_snapshots/`, where listing date, seller class, configuration, accessories, price type, shipping scope and cohort arithmetic are preserved. `tools/validate_tweakers_market_provenance.py` protects that path.

A non-promoting research note may still preserve a listing URL when it is useful as a lead.

## 3. What the gate detects

The validator classifies Tweakers URLs conservatively:

```text
gathering.tweakers.net/...  -> community
/aanbod/...                 -> market listing
/pricewatch/...             -> Pricewatch
/reviews/...                -> community
/productreview/...          -> community
```

An optional claim-level `source_surface` can also declare the evidence surface. Known community, Pricewatch and Vraag & Aanbod labels must not contradict the primary URL class.

The validator does not fetch URLs. Network availability must never decide whether committed evidence is structurally valid.

## 4. Public research grounding checked 2026-09-15

This guard is based on the way the live Tweakers surfaces actually separate evidence today, not on an invented taxonomy.

### Pricewatch example — Philips Hue Bridge 2.1

Exact URL:

- https://tweakers.net/pricewatch/1507414/philips-hue-bridge-21.html

Checked: `2026-09-15`

Observed scope:

- marketed product: `Philips Hue Bridge 2.1`;
- specification cross-checks include Zigbee/HomeKit, one 100 Mbps Ethernet port, up to 50 linked products, and `0.1 W` standby as listed by Tweakers;
- current retail offers and a refurbished offer are shown on the same Pricewatch product surface;
- a user review is embedded on the page, which is a **community claim**, not equivalent to the Pricewatch specification table.

The gate therefore lets Pricewatch support bounded spec/variant/retail context while refusing to turn that page into stronger execution or recovery truth.

### Vraag & Aanbod example — Philips Hue Bridge 2.0

Exact URL:

- https://tweakers.net/aanbod/4214620/philips-hue-bridge-20.html

Visible listing date: `2026-09-11 13:27`  
Checked: `2026-09-15`  
Market: Netherlands / Pijnacker  
Marketed model label: `Philips Hue Bridge 2.0`  
Condition: `Goede staat`  
Configuration/accessories: bridge + power supply; Ethernet cable is not stated as included  
Displayed asking price: `EUR 25`  
Shipping: excluded  
Seller class: private-user marketplace surface; no business seller was identified on the listing page  
Evidence scope: one dated asking-price observation only

This does **not** establish a stable market value, BSB002 identity for that physical unit, transaction price, power use, firmware state, or device capability.

### Community lead example

Tweakers community discussions contain practical claims about Hue local control, account/provisioning behavior and migration/failure cases. These are valuable research triggers, but the current Philips Hue developer documentation independently documents the local bridge API and physical link-button authorization. The official source should carry the positive device truth; the community thread remains supporting context or a lead for unresolved provisioning/offline questions.

Relevant manufacturer source:

- https://developers.meethue.com/develop/get-started-2/
- https://developers.meethue.com/support/

This is exactly the boundary this gate is meant to preserve.

## 5. Explicit non-goals

This gate does **not**:

- decide that every non-Tweakers URL is strong evidence;
- decide whether a claimed manufacturer/upstream/source-code source is interpreted correctly;
- fetch or archive external pages;
- promote forum evidence to `COMMUNITY_VERIFIED` merely because another URL exists;
- infer exact hardware revision from a marketed product label;
- turn an asking price into transaction-price truth;
- verify power, thermal, compatibility, recovery, or local execution;
- replace the existing evidence claim-scope, source-continuity, strength, market, or local-verification gates.

Human/machine review still has to judge whether the corroborating claim actually covers the same exact model, revision, firmware and bounded proposition.

## 6. Root gate

**Truth** — community anecdotes remain leads/secondary evidence unless stronger corroboration is explicit; marketplace pages do not prove capability.  
**Agency / non-domination** — public research does not authorize access, modification, persistence, or bypass on hardware the operator does not own/control.  
**Continuity** — the record preserves which source carried the claim and which stronger claim corroborated it, rather than relying on remembered context.  
**Wisdom before speed** — rich forum knowledge accelerates discovery without becoming a shortcut around exact-model, recovery, power, safety, or reproducibility work.

## 7. One-line rule

> **Use Tweakers broadly to discover reality; make the machine record remember exactly which parts are market evidence, bounded reference evidence, community leads, and independently corroborated device truth.**
