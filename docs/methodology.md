# Methodology

## Accounting basis

The engine uses the GHG Protocol corporate inventory structure as its conceptual basis and distinguishes Scope 1, Scope 2, and Scope 3 value-chain emissions.

The implementation is deliberately simplified for portfolio purposes. It demonstrates data architecture and calculation traceability rather than implementing the full methodological requirements of the GHG Protocol or ISO standards.

## Scope 1

Scope 1 examples in the dataset cover direct combustion of fuels in sources controlled by the reporting entity:

- Natural gas
- Diesel

The MVP applies an activity-based calculation:

```text
activity quantity × emission factor
```

## Scope 2

The MVP includes purchased electricity and demonstrates a location-based calculation using a geographic emission factor.

Market-based accounting and contractual instruments such as RECs/EACs are intentionally reserved for a later product iteration because they require additional instrument, matching, and quality metadata.

## Scope 3

The MVP demonstrates two value-chain examples:

- Purchased goods and services using spend-based data
- Business travel using distance-based data

The data model separates Scope 3 category from activity type so additional categories can be introduced without creating a separate engine for each category.

## Emission factors

Emission factors in this repository are **synthetic demonstration data**. They are included to make the calculation engine executable and testable. They must not be used for real corporate inventories.

Each factor includes source, source year, geography, methodology, and version metadata.

## Data quality

The repository uses a simple High / Medium / Low classification to demonstrate how quality metadata can travel through the calculation workflow. This is a portfolio-specific construct, not an official GHG Protocol or ISO scoring scheme.

## Versioning

The calculation result stores the emission-factor version and calculation version. This supports reproducibility when factors or calculation logic change.

## Methodology evolution

GHG accounting methodologies and regulatory requirements evolve. Production systems should therefore treat methodology, factor sources, and calculation logic as versioned configuration rather than immutable assumptions.
