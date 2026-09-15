# Tweakers Source Method — v0.1

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

Pricewatch specifications are useful secondary/reference evidence. For decisive capability claims such as custom code execution, privilege, recovery, firmware support or hardware revision constraints, prefer manufacturer documentation, upstream firmware/project documentation, working source code, or reproducible local evidence.

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

## 3. Source-scope labels

When Tweakers contributes evidence, preserve the scope rather than only the domain name.

Suggested values:

```text
tweakers_pricewatch_product
tweakers_pricewatch_price_history
tweakers_vraag_en_aanbod_listing
tweakers_user_review
tweakers_forum_thread
tweakers_news_or_editorial
```

The label describes the evidence surface, not its truth strength.

Example:

```yaml
source:
  url: https://tweakers.net/...
  source_scope: tweakers_vraag_en_aanbod_listing
  checked_at: "2026-09-15"
  proves:
    - "this exact observed listing asked EUR X at check time"
  does_not_prove:
    - "final transaction price"
    - "permanent market value"
```

## 4. Market-snapshot integration

Tweakers Vraag & Aanbod is especially valuable for the current NL/EU arbitrage comparison because it can provide a consistent local market surface across networking, PCs/thin clients, servers, storage and many other device classes.

It should complement, not replace, other public marketplaces.

The comparison method should prefer multiple independent sources where practical so one marketplace's audience or seller mix does not become invisible sampling bias.

Pricewatch can provide useful retail and historical context beside used-market observations, but retail product pages and used listings remain separate cohorts.

## 5. Example already relevant to the repo

The Synology DS220+ Pricewatch pages expose an important configuration distinction directly: the same DS220+ family appears as a bare chassis and in multiple drive bundles/capacities. Tweakers also exposes Vraag & Aanbod entries for the product.

That is exactly the kind of evidence this repository needs to preserve rather than collapsing everything to `DS220+ = one price`.

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

**Truth** — preserve source type, scope, date, exact model/configuration and uncertainty; community reports remain secondary until corroborated.  
**Agency / non-domination** — observe public information only; do not bypass account/access controls, pressure sellers, or modify devices not owned/authorized by the operator.  
**Continuity** — record exact URLs, checked dates and claim scope in repository evidence rather than relying on remembered forum knowledge.  
**Wisdom before speed** — use Tweakers to widen discovery and sharpen Dutch market evidence, but do not let rich community information shortcut recovery, safety, power or reproducibility requirements.

## 8. One-line rule

> **Use Tweakers broadly for discovery and Dutch market reality; promote only the exact claims that stronger evidence can actually carry.**

## Initial public surfaces checked

- https://tweakers.net/
- https://tweakers.net/laptops-en-systemen/aanbod/
- https://tweakers.net/servers/aanbod/
- https://tweakers.net/opslag/aanbod/
- https://tweakers.net/netwerkaccessoires/aanbod/
- Example DS220+ bare-chassis Pricewatch page: https://tweakers.net/pricewatch/1551242/synology-diskstation-ds220%2B-zonder-harde-schijven.html
