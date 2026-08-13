from typing import Iterable, List

from .models import Activity, EmissionFactor, ValidationIssue


ALLOWED_SCOPES = {1, 2, 3}
ALLOWED_QUALITY = {"high", "medium", "low"}


# Demonstration registry: activity types and compatible units.
UNIT_REGISTRY = {
    "natural_gas": {"kWh"},
    "diesel": {"L"},
    "electricity": {"kWh"},
    "purchased_goods": {"EUR"},
    "air_travel": {"passenger_km"},
    "rail_travel": {"passenger_km"},
}


def validate_activity(activity: Activity) -> List[ValidationIssue]:
    issues: List[ValidationIssue] = []

    if not activity.activity_id:
        issues.append(ValidationIssue(activity.activity_id, "activity_id", "Activity ID is required."))
    if activity.reporting_year < 2000 or activity.reporting_year > 2100:
        issues.append(ValidationIssue(activity.activity_id, "reporting_year", "Reporting year is outside the supported range."))
    if activity.scope not in ALLOWED_SCOPES:
        issues.append(ValidationIssue(activity.activity_id, "scope", "Scope must be 1, 2, or 3."))
    if activity.quantity <= 0:
        issues.append(ValidationIssue(activity.activity_id, "quantity", "Activity quantity must be greater than zero."))
    if activity.activity_type not in UNIT_REGISTRY:
        issues.append(ValidationIssue(activity.activity_id, "activity_type", f"Unsupported activity type: {activity.activity_type}."))
    elif activity.unit not in UNIT_REGISTRY[activity.activity_type]:
        issues.append(ValidationIssue(activity.activity_id, "unit", f"Unit '{activity.unit}' is not compatible with '{activity.activity_type}'."))
    if activity.data_quality not in ALLOWED_QUALITY:
        issues.append(ValidationIssue(activity.activity_id, "data_quality", "Data quality must be high, medium, or low."))
    if not activity.source:
        issues.append(ValidationIssue(activity.activity_id, "source", "Activity data source is required."))

    return issues


def validate_factor(factor: EmissionFactor) -> List[ValidationIssue]:
    issues: List[ValidationIssue] = []
    if factor.factor_value <= 0:
        issues.append(ValidationIssue(factor.factor_id, "factor_value", "Emission factor must be greater than zero."))
    if not factor.factor_unit:
        issues.append(ValidationIssue(factor.factor_id, "factor_unit", "Emission factor unit is required."))
    if not factor.source:
        issues.append(ValidationIssue(factor.factor_id, "source", "Emission factor source is required."))
    return issues
