from .models import Activity, EmissionFactor, ValidationError

SUPPORTED_UNITS = {
    "natural_gas": {"kWh"},
    "diesel": {"L"},
    "electricity": {"kWh"},
    "purchased_goods_spend": {"EUR", "USD"},
    "business_travel_distance": {"passenger_km"},
}

VALID_DATA_QUALITY = {"high", "medium", "low"}


def validate_activity(activity: Activity) -> list[ValidationError]:
    errors: list[ValidationError] = []

    if activity.scope not in {1, 2, 3}:
        errors.append(ValidationError(activity.activity_id, "scope", "Scope must be 1, 2, or 3", str(activity.scope)))

    if activity.reporting_year < 1900 or activity.reporting_year > 2100:
        errors.append(ValidationError(activity.activity_id, "reporting_year", "Reporting year is outside the supported range", str(activity.reporting_year)))

    if activity.quantity <= 0:
        errors.append(ValidationError(activity.activity_id, "quantity", "Activity quantity must be greater than zero", str(activity.quantity)))

    if activity.data_quality not in VALID_DATA_QUALITY:
        errors.append(ValidationError(activity.activity_id, "data_quality", "Data quality must be high, medium, or low", activity.data_quality))

    allowed_units = SUPPORTED_UNITS.get(activity.activity_type)
    if allowed_units is None:
        errors.append(ValidationError(activity.activity_id, "activity_type", "Unsupported activity type", activity.activity_type))
    elif activity.unit not in allowed_units:
        errors.append(ValidationError(activity.activity_id, "unit", f"Unit is not supported for {activity.activity_type}", activity.unit))

    if activity.scope == 2 and activity.category != "purchased_electricity":
        errors.append(ValidationError(activity.activity_id, "category", "MVP Scope 2 category must be purchased_electricity", activity.category))

    return errors


def validate_factor_compatibility(activity: Activity, factor: EmissionFactor) -> list[ValidationError]:
    errors: list[ValidationError] = []
    if activity.activity_type != factor.activity_type:
        errors.append(ValidationError(activity.activity_id, "emission_factor", "Emission factor activity type does not match activity data", factor.factor_id))
    expected_factor_unit = f"kgCO2e/{activity.unit}"
    if factor.factor_unit != expected_factor_unit:
        errors.append(ValidationError(activity.activity_id, "emission_factor", f"Emission factor unit must be {expected_factor_unit}", factor.factor_unit))
    return errors
