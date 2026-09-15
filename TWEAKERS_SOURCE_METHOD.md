# Tweakers Source Method — v0.2

**Status:** Supporting research method.  
**Purpose:** Use the Dutch Tweakers ecosystem as a strong local discovery, specification-cross-check and market-observation source without promoting community anecdotes into verified hardware truth.

## 1. Why Tweakers matters here

Tweakers combines several surfaces that are unusually useful for device-capability arbitrage in the Netherlands:

- **Pricewatch** — product identity, variants, specifications, price history/current retail context and linked user reviews;
- **Vraag & Aanbod** — dated Dutch used-market offers, often with seller class, condition, location and configuration details;
- **community / forum discussions** — device-specific modifications, hidden interfaces, firmware tricks, power/thermal observations, failure modes, recovery notes and practical ownership experience.

Those surfaces solve different research problems and must not be flattened into one evidence class.

## 2. Evidence roles

### Pricewatch

Use for:

- discovering exact product variants;
- checking whether a marketed model has multiple storage/RAM/bundle versions;
- retail/current-or-historical price context;
- specification cross-checking;
- finding user reviews that may expose practical limitations worth researching elsewhere.

Pricewatch specifications are useful secondary/reference evidence. For decisive capability claims such as custom-code execution, privilege, recovery, firmware support or hardware-revision constraints, prefer manufacturer documentation, upstream firmware/project documentation, working source code, or reproducible local evidence.

Pricewatch is **not** the same thing as one seller listing. The current v0.1 market-snapshot observation shape represents individual acquisition observations, so do not squeeze an aggregate Pricewatch product/history page into `retailer_offer` or `direct_listing`. Preserve Pricewatch as supporting retail/variant context until the repository gains a dedicated representation for that surface.

### Vraag & Aanbod

Use as a preferred Dutch acquisition-evidence source when relevant.

Preserve each observation as a dated listing observation, including where visible:

```text
exact model / revision
configuration
asking price
seller class
condition
included accessories
location / market region
listed date
checked date
source URL
```

Treat displayed prices as asking prices unless the page explicitly establishes another bounded price type.

Do not merge private used, dealer refurbished, bare chassis, bundled storage, or materially different configurations into one cohort merely to enlarge the sample.

### Community / forum threads

Use aggressively for **discovery**:

- alternative firmware;
- UART/JTAG/USB/service interfaces;
- boot/recovery behavior;
- hardware revisions;
- low-power observations;
- thermal behavior;
- hidden settings;
- device teardown details;
- known brick/failure patterns;
- weird repurposing ideas;
- practical tricks that point to an execution surface.

But a forum post is not automatically device truth.

A useful community report should normally be promoted only after one or more of the following corroborates it:

1. manufacturer documentation;
2. upstream firmware/project documentation;
3. source code or release artifacts that implement the claim;
4. multiple independent exact-model reports with compatible details;
5. locally reproduced evidence captured through this repository's receipt method.

Community/forum, review and editorial pages may be cited as leads or bounded secondary context. They must not be encoded as raw acquisition-price observations merely because they mention a price.

## 3. Preserve two provenance dimensions

Do not overload one field with two meanings.

### A. Capture mode: `source_scope`

For `market_snapshots/`, `source_scope` already has a mechanical meaning: **how the observation was captured**.

Current validated values are:

```text
direct_listing
search_result_snapshot
direct_retailer_offer
```

A direct Tweakers Vraag & Aanbod page therefore uses:

```yaml
source_scope: direct_listing
```

Do **not** replace that value with `tweakers_vraag_en_aanbod_listing`. Doing so would mix capture mode with evidence surface and would violate the current market-snapshot validator.

### B. Evidence surface: Tweakers provenance

Separately preserve which Tweakers surface supplied the evidence.

Useful surface labels are:

```text
tweakers_pricewatch_product
tweakers_pricewatch_price_history
tweakers_vraag_en_aanbod_listing
tweakers_user_review
tweakers_forum_thread
tweakers_news_or_editorial
```

Where a record shape can carry additive metadata without changing existing semantics, `source_surface` is the preferred field name.

Example:

```yaml
marketplace: Tweakers_Vraag_En_Aanbod
listed_at: "2026-08-18"
checked_at: "2026-09-14"
price_eur: 195
price_type: asking
seller_class: private
model_identity: "Synology DS220+"
configuration:
  installed_ram_gb: 6
  drives: none
  power_supply: included
source: https://tweakers.net/aanbod/4197732/...
source_scope: direct_listing
source_surface: tweakers_vraag_en_aanbod_listing
```

Existing observations do not need a bulk rewrite merely to add `source_surface`. For current market snapshots, the exact URL plus marketplace name must still make the Tweakers surface recoverable. `tools/validate_tweakers_market_provenance.py` checks that boundary mechanically.

The surface label describes provenance, not truth strength.

## 4. Market-snapshot integration

Tweakers Vraag & Aanbod is especially valuable for the current NL/EU arbitrage comparison because it can provide a consistent local market surface across networking, PCs/thin clients, servers, storage and many other device classes.

It should complement, not replace, other public marketplaces.

The comparison method should prefer multiple independent sources where practical so one marketplace's audience or seller mix does not become invisible sampling bias.

Pricewatch can provide useful retail and historical context beside used-market observations, but retail product pages, aggregate/history views and individual used listings remain separate evidence shapes.

### Mechanical gate

`tools/validate_tweakers_market_provenance.py` adds a narrow provenance gate on top of the generic market validator:

- Tweakers `/aanbod/` observations must remain identifiable as `Tweakers_Vraag_En_Aanbod`;
- they must use `source_scope: direct_listing`;
- their visible listing date, seller class, model identity and configuration must remain explicit;
- their current price type must be an asking price or a displayed sold-listing price, not a fabricated transaction price;
- optional `source_surface`, when present, must agree with the URL;
- Pricewatch pages are rejected as raw v0.1 acquisition observations because the current observation vocabulary cannot faithfully represent the aggregate/history surface;
- Tweakers forum/community/review/editorial pages are rejected as raw acquisition-price observations.

The gate validates provenance shape only. It does not fetch the source, prove seller claims, establish a transaction price, or promote community evidence.

## 5. Example already relevant to the repo

The current low-power-registry snapshot already contains a direct Tweakers Vraag & Aanbod observation for a DS220+ bare chassis with an explicit RAM configuration, no drives, seller class, listing date, checked date and exact source URL.

That is the intended pattern: preserve the exact offered configuration and the observation scope instead of collapsing everything to `DS220+ = one price`.

Pricewatch also exposes an important configuration distinction around the DS220+ family: bare chassis and drive bundles/capacities are separate products/offers. Use that to discover and cross-check configuration, not to erase cohort boundaries.

## 6. Community tricks as research triggers

A useful rule for this project:

> **A community trick is a lead, not a promotion.**

If a Tweakers user reports that an old router, camera, NAS, TV, calculator, printer or other device can run custom code, the next research step is to identify the execution surface and find stronger evidence for it.

Good flow:

```text
Tweakers thread / review
  -> surprising capability lead
  -> exact model/revision identification
  -> upstream/manufacturer/source-code corroboration
  -> device record + bounded claim
  -> local reproduction later when hardware is available
```

Bad flow:

```text
forum anecdote
  -> LOCALLY_VERIFIED / REPRODUCIBLE claim
```

## 7. Root gate

**Truth** — preserve source type, capture mode, evidence surface, date, exact model/configuration and uncertainty; community reports remain secondary until corroborated.  
**Agency / non-domination** — observe public information only; do not bypass account/access controls, pressure sellers, or modify devices not owned/authorized by the operator.  
**Continuity** — record exact URLs, listed/checked dates and claim scope in repository evidence rather than relying on remembered forum knowledge.  
**Wisdom before speed** — use Tweakers to widen discovery and sharpen Dutch market evidence, but do not let rich community information shortcut recovery, safety, power or reproducibility requirements.

## 8. One-line rule

> **Use Tweakers broadly for discovery and Dutch market reality; preserve capture mode separately from source surface, and promote only the exact claims stronger evidence can actually carry.**

## Initial public surfaces checked

- https://tweakers.net/
- https://tweakers.net/laptops-en-systemen/aanbod/
- https://tweakers.net/servers/aanbod/
- https://tweakers.net/opslag/aanbod/
- https://tweakers.net/netwerkaccessoires/aanbod/
- Example DS220+ bare-chassis Pricewatch page: https://tweakers.net/pricewatch/1551242/synology-diskstation-ds220%2B-zonder-harde-schijven.html
