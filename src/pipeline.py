import csv
from pathlib import Path

from .calculations import calculate
from .emission_factors import find_factor
from .models import Activity, EmissionFactor
from .validation import validate_activity, validate_factor_compatibility


def load_activities(path: str | Path) -> list[Activity]:
    with open(path, newline="", encoding="utf-8") as handle:
        return [
            Activity(
                activity_id=row["activity_id"],
                entity_id=row["entity_id"],
                reporting_year=int(row["reporting_year"]),
                scope=int(row["scope"]),
                category=row["category"],
                activity_type=row["activity_type"],
                quantity=float(row["quantity"]),
                unit=row["unit"],
                source=row["source"],
                data_quality=row["data_quality"],
                is_estimated=row["is_estimated"].lower() == "true",
            )
            for row in csv.DictReader(handle)
        ]


def load_factors(path: str | Path) -> list[EmissionFactor]:
    with open(path, newline="", encoding="utf-8") as handle:
        return [
            EmissionFactor(
                factor_id=row["factor_id"],
                activity_type=row["activity_type"],
                factor_value=float(row["factor_value"]),
                factor_unit=row["factor_unit"],
                geography=row["geography"],
                source=row["source"],
                source_year=int(row["source_year"]),
                version=row["version"],
                methodology=row["methodology"],
            )
            for row in csv.DictReader(handle)
        ]


def run_inventory(activity_path: str | Path, factor_path: str | Path) -> tuple[list, list]:
    activities = load_activities(activity_path)
    factors = load_factors(factor_path)
    calculations = []
    errors = []

    for activity in activities:
        validation_errors = validate_activity(activity)
        if validation_errors:
            errors.extend(validation_errors)
            continue

        factor = find_factor(activity, factors)
        if factor is None:
            from .models import ValidationError
            errors.append(ValidationError(activity.activity_id, "emission_factor", "No compatible emission factor found"))
            continue

        compatibility_errors = validate_factor_compatibility(activity, factor)
        if compatibility_errors:
            errors.extend(compatibility_errors)
            continue

        calculations.append(calculate(activity, factor, f"CALC-{activity.activity_id}"))

    return calculations, errors
