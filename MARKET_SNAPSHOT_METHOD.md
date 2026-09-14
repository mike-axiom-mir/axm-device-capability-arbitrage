# Market Snapshot Method — v0.1

**Status:** Early evidence method.  
**Purpose:** Preserve dated acquisition evidence without turning marketplace listings into permanent prices or fake transaction data.

## 1. Why this exists

Capability arbitrage cannot be tested with sticker-price folklore.

A useful comparison needs acquisition evidence collected in a common time/region window, but marketplace data is noisy:

- asking price is not transaction price;
- listings disappear;
- shipping varies;
- sellers bundle power supplies, storage or upgrades differently;
- one marketed model can span materially different hardware configurations;
- retailer-refurbished stock is not the same cohort as private used hardware.

This method keeps those differences visible.

## 2. Raw observation first

Every market observation should preserve at least:

```yaml
marketplace: example
country: NL
listed_at: "2026-09-14"
checked_at: "2026-09-14"
price_eur: 25
price_type: asking
seller_class: private
model_identity: exact_model_or_revision
configuration: {}
source: https://example.invalid/listing
source_scope: direct_listing
```

Unknown configuration stays `unknown`.

Do not silently assign the best-known storage, RAM, radio, sensor or accessory variant to a listing that does not identify it.

## 3. Cohorts before medians

Only summarize observations inside an explicit cohort.

Examples:

```text
private used exact revision
dealer refurbished 8 GB
bare chassis, no drives
bundle with storage
```

Do not mix these merely to make the sample larger.

A cohort may report descriptive:

- sample count;
- low;
- median;
- high.

Those are properties of the collected sample, not a permanent market-price claim.

## 4. Asking price is not sold price

Allowed price types in v0.1:

```text
asking
displayed_sold_listing_price
retailer_offer
```

`displayed_sold_listing_price` means only that the marketplace page is marked sold while displaying that amount.

It does **not** prove the negotiated/final transaction price.

## 5. Shipping and accessories

The first comparison snapshot excludes shipping from cohort statistics unless a future snapshot explicitly states otherwise.

Required accessories remain separate evidence:

- power supply;
- storage;
- cables;
- adapters;
- mounting hardware;
- proprietary media.

An inexpensive chassis without the hardware required by the capability contract is not equivalent to a ready-to-run unit.

## 6. Same-window discipline

When a comparison uses market evidence, candidates should be sampled from the same broad date/region window.

The window must be recorded explicitly.

A later ranking refresh should not compare:

```text
one candidate's 2024 bargain listing
vs
another candidate's current 2026 retailer price
```

without preserving that mismatch.

## 7. Search-result evidence

A direct listing is preferable.

A marketplace search-result page may be used when it visibly preserves:

- exact model/revision identity;
- displayed price;
- listing date or enough date context;
- marketplace/source URL.

Such observations must use `source_scope: search_result_snapshot` so a search index snippet is not silently upgraded to direct-listing evidence.

## 8. Configuration identity

Variant-sensitive records must preserve listing configuration.

Examples already present in this repository:

```text
Dell Wyse 3040
  -> 8 GB or 16 GB eMMC

Synology DS220+
  -> bare chassis vs drives included
  -> RAM upgrades

TP-Link Archer C7
  -> exact hardware revision matters
```

If a listing does not identify the needed variant, the configuration value remains unknown.

## 9. What a market snapshot can prove

A snapshot can support statements such as:

```text
"In this collected cohort, observed asking prices ranged from X to Y."
```

It cannot by itself prove:

```text
"the device is worth X"
"the device always costs X"
"X is the final transaction price"
"this device wins total useful cost"
```

The first low-power-registry comparison still needs common workload, wall-power, provisioning, restart/recovery and replacement-life evidence before ranking.

## 10. Mechanical validation

`tools/validate_market_snapshots.py` checks:

- referenced device and contract IDs exist;
- snapshot/cohort/observation IDs are unique;
- country/currency/date/source fields are present;
- price values are non-negative numbers;
- declared `sample_count` matches observations;
- declared low/median/high exactly match the observation prices;
- asking/retailer/sold-display price types use the bounded v0.1 vocabulary.

Validation checks structure and arithmetic.

It does **not** prove that a seller is truthful, a listing is still available, or a displayed asking price became a transaction.

## 11. Root gate

**Truth:** asking prices stay asking prices; mixed configurations stay visible; sample statistics are not market truth.  
**Agency / non-domination:** research observes public offers and does not require seller contact, scraping around access controls, or purchase pressure.  
**Continuity:** raw observations, source URLs, dates, configuration notes and arithmetic live in repository state.  
**Wisdom before speed:** acquisition evidence is one part of total useful cost; ranking still waits for power, workload, recovery and friction evidence.

## 12. One-line rule

> **Preserve what was actually offered, when and in what configuration; never turn a small listing sample into a permanent price story.**
