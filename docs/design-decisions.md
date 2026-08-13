# Design Decisions

## Why separate activity data from emission factors?

An enterprise may reuse the same activity type across reporting periods, geographies, and methodologies while emission factors change. Separating the two makes factor updates manageable and keeps calculation logic transparent.

## Why store calculation inputs on the result?

References provide lineage, but references alone are insufficient if source records are later corrected. Storing the values actually used makes historical calculations reproducible and easier to audit.

## Why model Scope 3 categories explicitly?

Scope 3 is a value-chain inventory with distinct categories and calculation approaches. A category field allows the platform to grow without encoding category logic into the core calculation object.

## Why keep the MVP small?

The purpose is to demonstrate a credible product architecture rather than claim full coverage of every GHG accounting methodology. A small deterministic engine is easier to test and review.

## Why no AI in the calculation layer?

The numerical accounting layer should be deterministic and explainable. AI may be useful upstream for document extraction, classification, or data-quality assistance, but the final calculation should remain reproducible and inspectable.

## Why keep market-based Scope 2 for a later version?

Market-based accounting can require contractual-instrument data, matching periods, instrument quality attributes, and retirement or cancellation status. Modeling those explicitly is preferable to treating a REC as a generic emission factor.

## Product evolution

The architecture intentionally leaves room for a future enterprise data-collection workflow:

```text
Data Request
 → Data Owner / Supplier
 → Submission
 → Validation
 → Review
 → Approval
 → Calculation
 → Reporting
```

That workflow is outside the MVP but is an important direction for an enterprise product.
