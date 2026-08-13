# GHG Accounting Data Engine

A transparent, auditable calculation framework for converting enterprise activity data into structured greenhouse gas (GHG) emissions data.

## What this project demonstrates

- Structured activity-data ingestion
- Emission-factor matching
- Scope 1–3 classification
- GHG emissions calculation
- Data-quality validation
- Calculation traceability
- Versioned emission factors and calculation logic

The project focuses on the **data and calculation layer** of an enterprise GHG accounting platform rather than attempting to reproduce a complete commercial carbon-accounting product.

## Core workflow

```text
Activity Data
      ↓
Validation
      ↓
Normalization
      ↓
Scope / Category Classification
      ↓
Emission Factor Matching
      ↓
GHG Calculation
      ↓
Data Quality Assessment
      ↓
Calculation Record
      ↓
Audit Trail
```

## MVP coverage

| Scope | Initial examples |
|---|---|
| Scope 1 | Stationary and mobile combustion |
| Scope 2 | Purchased electricity |
| Scope 3 | Purchased goods/services and business travel |

The architecture is intentionally extensible so additional Scope 3 categories and calculation methods can be added without redesigning the core model.

## Why auditability matters

A calculated emissions result should not be a black box. Each result should be traceable to its source activity data, emission factor, source, formula, and calculation version.

```text
Calculation Result
       ↓
Calculation Record
       ↓
Activity Data
       ↓
Emission Factor
       ↓
Emission Factor Source
       ↓
Calculation Version
```

## Project documentation

- [Product Overview](docs/product-overview.md)
- Data Model *(coming next)*
- Methodology *(coming next)*
- Calculation Methodology *(coming next)*
- Design Decisions *(coming next)*

## Disclaimer

This is an educational and portfolio implementation demonstrating product and technical concepts for GHG accounting. It does not constitute professional GHG verification, assurance, legal advice, or a complete implementation of the GHG Protocol, ISO standards, or regulatory reporting requirements.
