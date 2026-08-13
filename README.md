# GHG Accounting Data Engine

A transparent, auditable calculation framework for converting enterprise activity data into structured greenhouse gas (GHG) emissions data.

> **Portfolio project:** demonstrates how GHG accounting requirements can be translated into a modular data product with validation, calculation logic, provenance, and auditability.

## What this project demonstrates

- Structured activity-data ingestion
- Emission-factor matching
- Scope 1–3 classification
- GHG emissions calculation
- Data-quality validation
- Calculation traceability
- Versioned emission factors and calculation logic
- Testable, deterministic calculation components

The project focuses on the **data and calculation layer** of an enterprise GHG accounting platform rather than attempting to reproduce a complete commercial carbon-accounting product.

## Architecture

```text
Activity Data
      ↓
Validation
      ↓
Normalization / Unit Checks
      ↓
Scope & Category Classification
      ↓
Emission Factor Matching
      ↓
GHG Calculation
      ↓
Calculation Record
      ↓
Audit Trail
```

## MVP coverage

| Scope | Initial examples | Method |
|---|---|---|
| Scope 1 | Natural gas, diesel | Activity-based |
| Scope 2 | Purchased electricity | Location-based |
| Scope 3 | Purchased goods/services | Spend-based |
| Scope 3 | Business travel | Distance-based |

The architecture is intentionally extensible so additional Scope 3 categories and calculation methods can be added without redesigning the core model.

## Quick start

Requires Python 3.10+.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest -q
python examples/example_inventory.py
```

On Windows PowerShell, activate the environment with:

```powershell
.venv\Scripts\Activate.ps1
```

## Example result

The core calculation is:

```text
activity quantity × emission factor = kgCO2e
kgCO2e ÷ 1,000 = tCO2e
```

For example:

```text
100,000 kWh × 0.35 kgCO2e/kWh
= 35,000 kgCO2e
= 35 tCO2e
```

## Why auditability matters

A calculated emissions result should not be a black box. Each result is traceable to its source activity data, emission factor, source metadata, formula, and calculation version.

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
- [Data Model](docs/data-model.md)
- [Methodology](docs/methodology.md)
- [Calculation Methodology](docs/calculation-methodology.md)
- [Design Decisions](docs/design-decisions.md)

## Repository structure

```text
ghg-accounting-data-engine/
├── data/                 # Demonstration activity data and factors
├── docs/                 # Product and methodology documentation
├── examples/             # Runnable example
├── src/                  # Calculation engine
└── tests/                # Automated tests
```

## Important methodological note

The emission factors in this repository are **synthetic demonstration data**. They exist to make the engine executable and testable and must not be used for real corporate reporting.

The project uses the GHG Protocol corporate inventory structure as a conceptual basis, but it is intentionally not a complete implementation of the GHG Protocol, ISO standards, or regulatory reporting requirements.

## Roadmap

- [x] Product specification
- [x] Core data model
- [x] Activity and emission-factor datasets
- [x] Validation layer
- [x] Calculation engine
- [x] Calculation traceability model
- [x] Automated tests
- [ ] Scope 2 market-based accounting and contractual instruments
- [ ] Enterprise data-collection workflow
- [ ] Multi-entity consolidation
- [ ] API layer

## Disclaimer

This is an educational and portfolio implementation demonstrating product and technical concepts for GHG accounting. It does not constitute professional GHG verification, assurance, legal advice, or a complete implementation of the GHG Protocol, ISO standards, or regulatory reporting requirements.
