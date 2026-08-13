from datetime import datetime, timezone

from .models import Activity, Calculation, EmissionFactor


def calculate(activity: Activity, factor: EmissionFactor, calculation_id: str, calculation_version: str = "1.0") -> Calculation:
    emissions_kgco2e = round(activity.quantity * factor.factor_value, 6)
    return Calculation(
        calculation_id=calculation_id,
        activity_id=activity.activity_id,
        factor_id=factor.factor_id,
        factor_version=factor.version,
        calculation_method=factor.methodology,
        formula="activity_quantity * emission_factor",
        activity_quantity=activity.quantity,
        activity_unit=activity.unit,
        emission_factor=factor.factor_value,
        emission_factor_unit=factor.factor_unit,
        emissions_kgco2e=emissions_kgco2e,
        emissions_tco2e=round(emissions_kgco2e / 1000, 6),
        calculation_version=calculation_version,
        calculated_at=datetime.now(timezone.utc),
    )
