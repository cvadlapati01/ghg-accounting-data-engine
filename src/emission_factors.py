from .models import Activity, EmissionFactor


def find_factor(activity: Activity, factors: list[EmissionFactor]) -> EmissionFactor | None:
    matches = [
        factor for factor in factors
        if factor.activity_type == activity.activity_type
        and factor.geography == _geography_for_activity(activity)
        and factor.factor_unit == f"kgCO2e/{activity.unit}"
    ]
    return matches[0] if matches else None


def _geography_for_activity(activity: Activity) -> str:
    # Geography is supplied through the entity in a production system.
    # The MVP dataset uses entity prefixes to keep the demo dependency-free.
    return "US" if activity.entity_id.endswith("US") else "DE"
