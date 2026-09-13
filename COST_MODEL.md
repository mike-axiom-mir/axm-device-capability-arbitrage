# Cost Model — Total Useful Cost

**Status:** v0.1 exploratory model  
**Purpose:** Stop cheap sticker prices from hiding expensive friction.

## 1. Core principle

> **The cheapest device is not necessarily the cheapest capability.**

A device should be compared by the cost of making its verified capabilities useful for the target goal.

## 2. Base model

```text
TOTAL USEFUL COST =
    acquisition
  + required accessories
  + storage / expansion
  + provisioning labor
  + expected electricity
  + maintenance burden
  + expected failure cost
  + recovery burden
  + replacement burden
```

This is intentionally broader than purchase price.

## 3. Monetary components

### Acquisition

```yaml
acquisition:
  device_price_eur: unknown
  shipping_eur: unknown
  taxes_fees_eur: unknown
```

### Accessories

Examples:

- power supply;
- USB cable;
- serial adapter;
- FTDI adapter;
- storage card;
- SATA/USB adapter;
- antenna;
- battery;
- enclosure;
- cooling;
- proprietary cable.

Only count accessories required for the target role or provisioning path.

### Electricity

Use measured power when possible.

```text
annual_kwh = average_watts × hours_per_year / 1000
annual_energy_cost = annual_kwh × electricity_price_per_kwh
```

For intermittent devices, estimate duty cycle explicitly instead of pretending they are always on.

## 4. Friction components

Money alone misses the biggest differences between repurposed devices.

Track at least:

```yaml
friction:
  research_minutes: unknown
  provisioning_minutes: unknown
  repeat_provisioning_minutes: unknown
  special_skill_required: unknown
  soldering_required: unknown
  destructive_disassembly_required: unknown
  documentation_quality: unknown
```

Research time and repeat provisioning time are separate. A painful first investigation can still lead to an excellent reusable recipe.

## 5. Risk components

Suggested qualitative fields:

```yaml
risk:
  brick_probability: unknown
  recovery_difficulty: unknown
  hardware_revision_uncertainty: unknown
  firmware_dependency: unknown
  vendor_cloud_dependency: unknown
  supply_volatility: unknown
```

Do not invent numeric probabilities without data. Early versions may use explicit ordinal ratings with the evidence attached.

## 6. Replacement burden

A device that is cheap only because one rare listing exists is not equivalent to a device with broad replacement supply.

Track:

- number of market observations;
- regional availability;
- common e-waste presence;
- hardware-revision consistency;
- replacement lead time;
- whether required accessories are still available.

## 7. Cost snapshots

Price data is a dated observation.

Recommended structure:

```yaml
market_snapshot:
  region: NL
  checked_at: "2026-09-13"
  currency: EUR
  condition: used_working
  sample_count: 0
  low: unknown
  median: unknown
  high: unknown
  notes: not_collected
```

Never make a permanent device property called simply `price: 15`.

## 8. Comparison modes

Different goals need different rankings.

### Cheapest acquisition
Useful for experiments where failure is acceptable.

### Cheapest one-year ownership
Adds electricity, expected replacement and basic maintenance.

### Cheapest three-year ownership
Useful for always-on infrastructure.

### Lowest deployment friction
May favor a more expensive device with a clean open runtime.

### Lowest recovery risk
May favor hardware with dual firmware, removable boot media or strong rescue tooling.

### Highest capability per euro
Useful only after the relevant capability weights are defined by the goal.

There should be no universal "best hardware" score independent of a capability contract.

## 9. Capability-weighted value

A future matcher may calculate:

```text
MATCHED_CAPABILITY_VALUE =
  sum(goal_weight_i × verified_match_i × evidence_confidence_i)
```

Then compare:

```text
VALUE_PER_EURO = MATCHED_CAPABILITY_VALUE / TOTAL_USEFUL_COST
```

This remains experimental. Do not let a numerical score hide weak evidence.

## 10. Composition cost

For multi-device solutions:

```text
composition_cost =
    sum(device_total_useful_cost)
  + interconnect_cost
  + coordination_overhead
  + extra_power
  + composition_recovery_burden
```

A three-router composition is not automatically cheaper than one mini PC just because three sticker prices are lower.

## 11. Labor policy

The project should preserve raw time separately from monetized time.

Why:

- hobby/research time may be intentionally free;
- commercial deployment time is not free;
- machine provisioning time can become near-zero after automation;
- first-time reverse engineering should not permanently poison the cost of a reproducible recipe.

Record:

```yaml
labor:
  one_time_research_minutes: unknown
  first_device_minutes: unknown
  repeat_device_minutes: unknown
  automation_level: manual|partial|automated|unknown
```

Then a consumer of the data can apply its own hourly-rate model.

## 12. Stop condition

A candidate should lose its "cheap" status when hidden cost materially defeats the advantage for the target goal.

Examples:

- rare proprietary adapter costs more than the device;
- recovery requires destructive hardware work;
- power cost dominates acquisition savings;
- repeat setup remains fragile/manual;
- replacement units vary unpredictably by hardware revision.

## 13. Foundational cost rule

> **Count the price of turning the object into a reliable capability, not just the price of acquiring the object.**