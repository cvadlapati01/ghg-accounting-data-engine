# Calculation Methodology

## Core formula

For the MVP, emissions are calculated as:

```text
GHG emissions = activity quantity × emission factor
```

The result is stored in kgCO2e and normalized to tCO2e by dividing by 1,000.

## Activity-based example

```text
100,000 kWh × 0.35 kgCO2e/kWh
= 35,000 kgCO2e
= 35 tCO2e
```

## Spend-based example

```text
1,500,000 EUR × 0.20 kgCO2e/EUR
= 300,000 kgCO2e
= 300 tCO2e
```

## Distance-based example

```text
850,000 passenger-km × 0.15 kgCO2e/passenger-km
= 127,500 kgCO2e
= 127.5 tCO2e
```

## Validation before calculation

The engine validates:

1. Scope
2. Reporting year
3. Positive activity quantity
4. Data-quality classification
5. Activity type
6. Unit compatibility
7. Emission-factor availability
8. Emission-factor unit compatibility

Invalid records are excluded from calculation and returned as structured validation errors.

## Determinism

Given the same activity data, compatible emission factor, and calculation version, the numerical result is deterministic.

The timestamp is metadata and does not affect the numerical result.

## Rounding

The engine rounds calculated kgCO2e and tCO2e values to six decimal places. This is an implementation choice for stable machine-readable output, not a statement about reporting precision requirements.

## Calculation lineage

Each result retains:

- Activity ID
- Factor ID
- Factor version
- Calculation method
- Formula
- Activity quantity and unit
- Emission-factor value and unit
- Calculation version
- Calculation timestamp

This provides the basis for reproducibility and audit review.
