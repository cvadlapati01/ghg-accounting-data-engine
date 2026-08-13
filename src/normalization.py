from .models import Activity


UNIT_CONVERSIONS = {
    ("MWh", "kWh"): 1000.0,
}


def normalize_activity(activity: Activity) -> Activity:
    """Normalize supported activity units without changing the source record."""
    target_unit = "kWh" if activity.activity_type in {"electricity", "natural_gas"} else activity.unit
    conversion = UNIT_CONVERSIONS.get((activity.unit, target_unit), 1.0)

    if conversion == 1.0 and activity.unit != target_unit:
        raise ValueError(f"No conversion available from {activity.unit} to {target_unit}.")

    return Activity(
        activity_id=activity.activity_id,
        entity_id=activity.entity_id,
        reporting_year=activity.reporting_year,
        scope=activity.scope,
        category=activity.category,
        activity_type=activity.activity_type,
        quantity=activity.quantity * conversion,
        unit=target_unit,
        source=activity.source,
        data_quality=activity.data_quality,
        is_estimated=activity.is_estimated,
    )
