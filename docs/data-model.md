# GHG Accounting Data Engine — Data Model

## 1. Purpose

This document defines the conceptual and logical data model for the GHG Accounting Data Engine.

The model is designed to separate **what was measured** from **how it was converted into emissions**, while preserving enough metadata to reproduce and audit a calculation.

The central design principle is:

```text
Activity Data + Emission Factor + Calculation Method
                         ↓
                   GHG Calculation
                         ↓
                   Audit Trail
```

The model is intentionally normalized so that activity records, emission factors, and calculations can evolve independently.

---

## 2. Design Principles

### Separation of activity data and emission factors

Activity data represents an organization's measured or estimated activity. Emission factors represent the conversion factors used to translate that activity into GHG emissions.

They should not be hard-coded together.

### Immutable calculation inputs

A completed calculation should retain references to the exact activity record and emission-factor version used.

### Explicit methodology

A calculation should identify the method and formula used rather than relying on implicit application behavior.

### Version awareness

Emission factors and calculation logic can change over time. Historical calculations must remain reproducible.

### Extensibility

The model should support additional Scope 3 categories, activity types, units, methodologies, and emission-factor sources without requiring a fundamental redesign.

---

## 3. Entity Relationship Overview

```text
                         ┌─────────────────┐
                         │     Entity      │
                         └────────┬────────┘
                                  │
                                  │ 1:N
                                  ▼
                         ┌─────────────────┐
                         │    Activity     │
                         └────────┬────────┘
                                  │
                                  │ 1:N
                                  ▼
                         ┌─────────────────┐
                         │   Calculation   │
                         └──────┬────┬─────┘
                                │    │
                         N:1    │    │    N:1
                                ▼    ▼
                  ┌──────────────┐  ┌──────────────────┐
                  │    Factor    │  │ Calculation Audit│
                  │    Version   │  │      Event       │
                  └──────────────┘  └──────────────────┘
```

The MVP contains five conceptual entities:

1. Entity
2. Activity
3. Emission Factor
4. Calculation
5. Audit Event

---

# 4. Entity

Represents an organizational reporting entity.

An entity can represent a company, legal entity, business unit, facility, or another reporting boundary used by the application.

### Fields

| Field | Type | Required | Description |
|---|---|---:|---|
| `entity_id` | string | Yes | Unique identifier |
| `entity_name` | string | Yes | Display name |
| `country` | string | No | Country associated with the entity |
| `reporting_year` | integer | Yes | Reporting year |

### Example

```json
{
  "entity_id": "ACME-DE",
  "entity_name": "ACME Germany GmbH",
  "country": "DE",
  "reporting_year": 2025
}
```

---

# 5. Activity

Represents activity data used as an input to a GHG calculation.

Examples include:

- Natural gas consumed in kWh
- Diesel consumed in litres
- Electricity consumed in kWh
- Business travel distance in passenger-km
- Purchased goods represented by monetary spend

### Fields

| Field | Type | Required | Description |
|---|---|---:|---|
| `activity_id` | string | Yes | Unique activity identifier |
| `entity_id` | string | Yes | Reference to reporting entity |
| `reporting_year` | integer | Yes | Reporting year |
| `scope` | integer | Yes | GHG Protocol scope: 1, 2, or 3 |
| `category` | string | Conditional | Scope/category classification |
| `activity_type` | string | Yes | Type of activity represented |
| `quantity` | decimal | Yes | Activity quantity |
| `unit` | string | Yes | Unit of activity data |
| `source` | string | Yes | Source of activity data |
| `data_quality` | string | Yes | Product-level quality classification |
| `is_estimated` | boolean | No | Whether the activity value is estimated |

### Example

```json
{
  "activity_id": "ACT-001",
  "entity_id": "ACME-DE",
  "reporting_year": 2025,
  "scope": 2,
  "category": "Purchased Electricity",
  "activity_type": "electricity",
  "quantity": 100000,
  "unit": "kWh",
  "source": "utility_invoice",
  "data_quality": "high",
  "is_estimated": false
}
```

---

# 6. Emission Factor

Represents a factor used to convert a unit of activity into GHG emissions.

Emission factors are treated as independently managed data because the same activity type may have different factors depending on geography, source, year, methodology, or other attributes.

### Fields

| Field | Type | Required | Description |
|---|---|---:|---|
| `factor_id` | string | Yes | Stable identifier for the factor record |
| `activity_type` | string | Yes | Compatible activity type |
| `factor_value` | decimal | Yes | Numerical emission factor |
| `factor_unit` | string | Yes | Factor unit, e.g. kgCO2e/kWh |
| `geography` | string | No | Geographic applicability |
| `source` | string | Yes | Published or maintained source |
| `source_year` | integer | Yes | Year associated with source/factor |
| `version` | string | Yes | Factor version |
| `methodology` | string | No | Methodology or accounting basis |

### Example

```json
{
  "factor_id": "EF-001",
  "activity_type": "electricity",
  "factor_value": 0.35,
  "factor_unit": "kgCO2e/kWh",
  "geography": "DE",
  "source": "Example Dataset",
  "source_year": 2025,
  "version": "1.0",
  "methodology": "location-based"
}
```

> The factors included in this portfolio project are demonstration data and should not be interpreted as authoritative emission factors for real corporate reporting.

---

# 7. Calculation

Represents a completed transformation of activity data into an emissions result.

A calculation stores both the result and the references required to reproduce it.

### Fields

| Field | Type | Required | Description |
|---|---|---:|---|
| `calculation_id` | string | Yes | Unique calculation identifier |
| `activity_id` | string | Yes | Activity input used |
| `factor_id` | string | Yes | Emission factor used |
| `factor_version` | string | Yes | Exact factor version used |
| `calculation_method` | string | Yes | Calculation method |
| `formula` | string | Yes | Human-readable formula |
| `activity_quantity` | decimal | Yes | Quantity used in calculation |
| `activity_unit` | string | Yes | Unit used |
| `emission_factor` | decimal | Yes | Factor value used |
| `emission_factor_unit` | string | Yes | Factor unit |
| `emissions_kgco2e` | decimal | Yes | Result in kgCO2e |
| `emissions_tco2e` | decimal | Yes | Result in tCO2e |
| `calculation_version` | string | Yes | Version of calculation logic |
| `calculated_at` | datetime | Yes | Calculation timestamp |

### Example

```json
{
  "calculation_id": "CALC-001",
  "activity_id": "ACT-001",
  "factor_id": "EF-001",
  "factor_version": "1.0",
  "calculation_method": "activity_based",
  "formula": "activity_quantity * emission_factor",
  "activity_quantity": 100000,
  "activity_unit": "kWh",
  "emission_factor": 0.35,
  "emission_factor_unit": "kgCO2e/kWh",
  "emissions_kgco2e": 35000,
  "emissions_tco2e": 35,
  "calculation_version": "1.0",
  "calculated_at": "2026-08-13T00:00:00Z"
}
```

### Why store the input values again?

The calculation record stores the values actually used, in addition to references to the source records.

This provides a stronger audit trail if source data is later corrected or emission-factor records are updated.

The reference tells us **where the input came from**.

The stored calculation input tells us **what value was actually used**.

---

# 8. Audit Event

Represents an event associated with a calculation's lifecycle.

The MVP uses a lightweight event model rather than implementing a full enterprise audit-log system.

### Fields

| Field | Type | Required | Description |
|---|---|---:|---|
| `audit_event_id` | string | Yes | Unique event identifier |
| `calculation_id` | string | Yes | Calculation associated with event |
| `event_type` | string | Yes | Event type |
| `timestamp` | datetime | Yes | Event timestamp |
| `description` | string | Yes | Human-readable event description |

### Example

```json
{
  "audit_event_id": "AUDIT-001",
  "calculation_id": "CALC-001",
  "event_type": "calculation_created",
  "timestamp": "2026-08-13T00:00:00Z",
  "description": "Calculation created using emission factor EF-001 version 1.0"
}
```

Possible event types include:

```text
activity_created
activity_updated
validation_failed
factor_matched
calculation_created
calculation_recalculated
```

---

# 9. Relationships

## Entity → Activity

One entity can have many activity records.

```text
Entity 1 ─────── N Activity
```

An activity belongs to one reporting entity in the MVP.

---

## Activity → Calculation

One activity can produce multiple calculations over time.

```text
Activity 1 ─────── N Calculation
```

This supports recalculation when methodology or calculation logic changes while preserving historical calculation records.

---

## Emission Factor → Calculation

One emission factor version can be used by many calculations.

```text
Emission Factor 1 ─────── N Calculation
```

A calculation references the exact factor version used.

---

## Calculation → Audit Event

One calculation can have multiple audit events.

```text
Calculation 1 ─────── N Audit Event
```

---

# 10. Scope and Category Representation

The model separates `scope` from `category`.

### Scope 1

Examples:

```text
scope = 1
category = stationary_combustion
```

```text
scope = 1
category = mobile_combustion
```

### Scope 2

Examples:

```text
scope = 2
category = purchased_electricity
```

The model can later distinguish location-based and market-based accounting through calculation-method metadata and/or contractual-instrument data.

### Scope 3

Examples:

```text
scope = 3
category = purchased_goods_and_services
```

```text
scope = 3
category = business_travel
```

The architecture is intended to support expansion to additional Scope 3 categories without creating separate calculation engines for each category.

---

# 11. Unit Handling

Units are treated as explicit data rather than embedded in activity-type names.

Example:

```text
activity_type = electricity
unit = kWh
```

rather than:

```text
activity_type = electricity_kwh
```

This allows the validation layer to determine whether a given emission factor is compatible with the activity data.

The MVP will support a deliberately small set of units and extend the unit registry as additional calculation methods are implemented.

---

# 12. Calculation Lineage

A completed result should be navigable through the following lineage:

```text
                 ┌───────────────┐
                 │ Entity        │
                 └───────┬───────┘
                         │
                         ▼
                 ┌───────────────┐
                 │ Activity      │
                 │ ACT-001       │
                 └───────┬───────┘
                         │
                         ▼
                 ┌───────────────┐
                 │ Calculation   │
                 │ CALC-001      │
                 └───────┬───────┘
                         │
                ┌────────┴────────┐
                ▼                 ▼
        ┌──────────────┐  ┌───────────────┐
        │ EF-001 v1.0  │  │ Audit Events  │
        └──────────────┘  └───────────────┘
```

The lineage should make it possible to answer:

1. Which entity generated the activity?
2. What activity data was used?
3. Which emission factor was selected?
4. Which factor version was used?
5. Which methodology was applied?
6. What formula was used?
7. What emissions resulted?
8. When was the calculation performed?
9. What audit events occurred?

---

# 13. Future Extensions

The model intentionally leaves room for additional enterprise capabilities.

### Organizational boundaries

A future version could introduce:

```text
Organization
Reporting Boundary
Facility
Consolidation Rule
```

### Evidence management

Activity records could reference supporting evidence such as:

```text
invoice
utility_bill
travel_report
supplier_submission
ERP_export
```

### Data collection workflow

A future enterprise layer could introduce:

```text
Data Request
 → Supplier / Data Owner
 → Submission
 → Validation
 → Review
 → Approval
 → Calculation
```

### Scope 2 contractual instruments

A future model could add explicit entities for:

```text
Energy Contract
REC / EAC
Instrument Quantity
Matching Period
Retirement Status
```

These are intentionally outside the MVP calculation model.

---

# 14. Key Design Decision

The most important architectural decision in this project is to treat **activity data, emission factors, calculations, and audit events as separate concerns**.

This enables the engine to evolve from a simple calculation script into a more realistic enterprise data product without changing the fundamental calculation model.

```text
                    Enterprise Data
                          │
                          ▼
                   Activity Records
                          │
                          ▼
                    Validation Layer
                          │
                          ▼
                 Factor Matching Layer
                          │
                          ▼
                   Calculation Engine
                          │
              ┌───────────┴───────────┐
              ▼                       ▼
       Emissions Results         Audit Trail
```

The design prioritizes **traceability, reproducibility, and extensibility** over premature complexity.
