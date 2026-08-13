from typing import Iterable, Optional

from .models import EmissionFactor


def match_factor(
    activity_type: str,
    unit: str,
    geography: str,
    factors: Iterable[EmissionFactor],
) -> Optional[EmissionFactor]:
    """Return the best available compatible factor using geography first, then GLOBAL."""
    compatible = [
        factor
        for factor in factors
        if factor.activity_type == activity_type
        and factor.factor_unit.endswith(f"/{unit}")
    ]

    exact = [factor for factor in compatible if factor.geography == geography]
    if exact:
        return exact[0]

    global_factors = [factor for factor in compatible if factor.geography == "GLOBAL"]
    return global_factors[0] if global_factors else None
