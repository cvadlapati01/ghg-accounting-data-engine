# GHG Accounting Data Engine — Product Overview

## 1. Product Vision

The GHG Accounting Data Engine is a transparent, auditable calculation framework for converting enterprise activity data into structured greenhouse gas (GHG) emissions data.

The engine is designed to demonstrate how complex GHG accounting requirements can be translated into a scalable data product with:

- Structured activity-data ingestion
- Emission-factor matching
- Scope 1–3 classification
- GHG emissions calculation
- Data-quality validation
- Calculation traceability
- Versioned methodology and emission factors
- Audit-ready calculation records

The project focuses on the **data and calculation layer** of an enterprise GHG accounting platform rather than attempting to reproduce a complete commercial carbon-accounting product.

## 2. Problem Statement

Enterprise GHG accounting requires organizations to collect activity data from multiple sources and convert that information into comparable emissions values.

In practice, input data can be incomplete, inconsistent, provided in different units, sourced from different systems, associated with different levels of data quality, or linked to emission factors that change over time.

A reliable accounting product therefore needs to do more than perform a multiplication. It needs to establish a traceable relationship between:

```text
Activity Data
      ↓
Validation
      ↓
Normalization
      ↓
Emission Factor
      ↓
Calculation
      ↓
GHG Result
      ↓
Audit Trail
```

## 3. Target Users

### Sustainability / Carbon Accounting Teams

Users responsible for preparing organizational GHG inventories and sustainability disclosures.

Key needs:

- Import activity data
- Review calculation inputs
- Understand emissions results
- Identify data-quality issues
- Trace results back to source data
- Reproduce calculations

### Sustainability Data Managers

Users responsible for collecting, validating, and maintaining environmental data across an organization.

Key needs:

- Standardize incoming data
- Identify missing or invalid information
- Manage data-quality metadata
- Track data sources
- Maintain consistent reporting structures

### Auditors / Assurance Teams

Users who need to understand how reported emissions were calculated.

Key needs:

- Calculation traceability
- Emission-factor provenance
- Version history
- Source documentation
- Reproducibility

### Product / Engineering Teams

Teams responsible for building and maintaining enterprise carbon-accounting software.

Key needs:

- Clear data models
- Deterministic calculation logic
- Validation rules
- Extensible Scope 1–3 architecture
- Testable calculation components

## 4. Product Goals

### Goal 1 — Convert Activity Data into GHG Results

Provide a consistent calculation framework for converting activity data and emission factors into GHG emissions.

Example:

```text
100,000 kWh × 0.35 kgCO2e/kWh = 35,000 kgCO2e = 35 tCO2e
```

### Goal 2 — Make Calculations Traceable

Every emissions result should be traceable to:

- The original activity record
- The emission factor used
- The emission-factor source
- The calculation formula
- The calculation version
- The reporting period

The user should be able to answer:

> Where did this emissions number come from?

without manually reconstructing the calculation.

### Goal 3 — Make Data Quality Explicit

The engine should identify data-quality issues before they propagate into emissions results.

Examples include missing activity quantity, unsupported unit, missing emission factor, invalid reporting period, incomplete source information, or estimated activity data.

### Goal 4 — Support Scope 1–3

The data model should support all three GHG Protocol scopes while keeping the initial implementation intentionally limited.

The architecture should allow additional Scope 3 categories and calculation methods to be added without redesigning the core data model.

### Goal 5 — Enable Reproducibility

The same inputs, emission-factor version, and calculation version should produce the same result.

A historical calculation should remain reproducible even if an emission factor is subsequently updated.

## 5. Product Scope

### MVP

The initial version supports:

#### Scope 1

- Stationary combustion
- Mobile combustion

#### Scope 2

- Purchased electricity

#### Scope 3

- Purchased goods and services
- Business travel

### Calculation Methods

The MVP supports simplified examples of:

- Activity-based calculation
- Spend-based calculation
- Distance-based calculation

### Data Management

The MVP includes:

- Activity-data ingestion
- Emission-factor lookup
- Unit validation
- Scope/category classification
- Calculation
- Data-quality metadata
- Calculation traceability

## 6. Non-Goals

This project does **not** attempt to:

- Implement the complete GHG Protocol methodology
- Provide an assurance opinion
- Replace a commercial carbon-accounting platform
- Provide legally binding regulatory compliance
- Maintain an authoritative global emission-factor database
- Automatically determine organizational boundaries
- Implement every Scope 3 category in the first release
- Provide a complete CSRD/ESRS reporting solution

The project is intended as a **technical and product demonstration**, not a compliance certification tool.

## 7. Core Product Workflow

```text
1. Activity Data
       ↓
2. Validation
       ↓
3. Normalization
       ↓
4. Scope / Category Classification
       ↓
5. Emission Factor Matching
       ↓
6. GHG Calculation
       ↓
7. Data Quality Assessment
       ↓
8. Calculation Record
       ↓
9. Audit Trail
```

Each stage should be independently testable.

## 8. Core Entities

The initial data model consists of five core entities.

### Entity

Represents an organizational reporting entity.

```text
entity_id
entity_name
country
reporting_year
```

### Activity

Represents a source of GHG activity data.

```text
activity_id
entity_id
reporting_year
scope
category
activity_type
quantity
unit
source
data_quality
```

### Emission Factor

Represents the factor used to convert activity data into GHG emissions.

```text
factor_id
activity_type
factor_value
factor_unit
geography
source
source_year
version
```

### Calculation

Represents the resulting emissions calculation.

```text
calculation_id
activity_id
factor_id
formula
emissions_kgco2e
emissions_tco2e
calculation_version
calculated_at
```

### Audit Event

Represents an event that contributes to calculation traceability.

```text
audit_event_id
calculation_id
event_type
timestamp
description
```

## 9. Calculation Principle

The core calculation is:

```text
GHG Emissions = Activity Data × Emission Factor
```

The engine should normalize results into kgCO2e and tCO2e.

For example:

```text
Activity:
100,000 kWh

Emission Factor:
0.35 kgCO2e/kWh

Calculation:
100,000 × 0.35

Result:
35,000 kgCO2e

Normalized Result:
35 tCO2e
```

The calculation record should retain the original units and values used.

## 10. Data Quality

The MVP uses a simplified product-level data-quality classification:

| Level | Description |
|---|---|
| High | Primary, complete, and well-documented activity data |
| Medium | Secondary or partially estimated data |
| Low | Highly estimated, incomplete, or weakly documented data |

This classification is a **product design construct for this project** and is not intended to replace any specific GHG Protocol or ISO data-quality methodology.

Data quality should be stored as metadata rather than modifying the calculated emissions value.

## 11. Auditability & Traceability

Every calculation should maintain a lineage chain:

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

Example:

```text
Calculation ID: CALC-001

Activity: ACT-001

Emission Factor: EF-001

Formula: activity × emission_factor

Activity Quantity: 100,000 kWh

Emission Factor: 0.35 kgCO2e/kWh

Result: 35,000 kgCO2e

Calculation Version: 1.0

Data Quality: High
```

This design enables historical calculations to be reviewed and reproduced.

## 12. Product Requirements

### Functional Requirements

The engine must:

- Accept structured activity data
- Validate required fields
- Validate units
- Validate Scope classification
- Match compatible emission factors
- Calculate GHG emissions
- Normalize emissions into kgCO2e and tCO2e
- Assign calculation identifiers
- Store calculation metadata
- Store emission-factor provenance
- Produce validation errors
- Preserve calculation traceability

### Non-Functional Requirements

The engine should be:

- Deterministic
- Testable
- Modular
- Extensible
- Transparent
- Reproducible
- Version-aware

## 13. Example User Story

> As a sustainability data manager, I want to upload activity data and receive a calculated GHG result with its underlying emission factor and source so that I can review and trace the result before using it in reporting.

### Acceptance Criteria

- Activity data contains all required fields
- The unit is compatible with the selected activity type
- A valid emission factor is available
- The calculation is performed deterministically
- The result is returned in kgCO2e and tCO2e
- The emission-factor source is retained
- A unique calculation ID is generated
- Data-quality metadata is retained
- Validation errors are clearly reported

## 14. Product Metrics

### Calculation Accuracy

Percentage of test calculations producing the expected result.

### Validation Coverage

Percentage of invalid input scenarios correctly identified by the validation layer.

### Traceability Coverage

Percentage of calculation results with complete activity-data reference, emission-factor reference, source, and calculation version.

### Processing Success Rate

Percentage of valid activity records successfully processed.

## 15. Roadmap

### v0.1 — Core Calculation Engine

- Activity data
- Emission factors
- Scope classification
- Basic calculations
- Validation

### v0.2 — Auditability

- Calculation IDs
- Factor versions
- Source tracking
- Calculation lineage
- Data-quality metadata

### v0.3 — Scope 3 Expansion

- Additional Scope 3 categories
- Spend-based calculation
- Activity-based calculation
- Category-specific validation

### v0.4 — Scope 2 Expansion

- Location-based method
- Market-based method
- Renewable Energy Certificate metadata
- Contractual instrument tracking

### v0.5 — Enterprise Data Layer

- Multiple entities
- Reporting periods
- Consolidation
- CSV ingestion
- API ingestion
- Error management

### v1.0 — Reporting Layer

- Scope 1–3 inventory
- Consolidated emissions
- Reporting exports
- Calculation lineage views
- Data-quality reporting

## 16. Design Principles

### 1. Traceability over black-box automation

Automation should not come at the expense of understanding how a result was produced.

### 2. Data quality is part of the calculation workflow

Data-quality issues should be identified before they affect downstream reporting.

### 3. Methodology should be explicit

Calculation methods, assumptions, and emission-factor sources should be documented rather than hidden inside application logic.

### 4. Version everything that affects a result

Emission factors, methodologies, and calculation logic should be versioned to support reproducibility.

### 5. Separate data from calculation logic

Activity data and emission factors should be stored independently from the calculation engine.

### 6. Design for extension

The initial implementation is intentionally small, but the data model should support additional GHG categories and calculation methods.

## 17. Methodological Disclaimer

This project is an educational and portfolio implementation demonstrating product and technical concepts for GHG accounting.

It does not constitute professional GHG verification, assurance, legal advice, or a complete implementation of the GHG Protocol, ISO standards, or regulatory reporting requirements.

Methodologies, emission factors, regulatory requirements, and accounting standards may evolve. The project therefore treats methodology and emission-factor versions as explicit metadata rather than assuming that a calculation framework is permanently fixed.

## 18. Success Criteria

The project will be considered successful when a user can:

1. Submit valid activity data.
2. Validate the input.
3. Match an appropriate emission factor.
4. Calculate GHG emissions.
5. Receive a normalized tCO2e result.
6. Understand the calculation formula.
7. Identify the emission-factor source.
8. Review data-quality metadata.
9. Reproduce the calculation.
10. Trace the final result back to the original activity data.

The final product should demonstrate that a GHG accounting engine can be both **automated and explainable**.
