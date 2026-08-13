from src.calculations import calculate
from src.models import Activity, EmissionFactor


def test_activity_based_calculation():
    activity = Activity("ACT-TEST", "ACME-DE", 2025, 1, "stationary_combustion", "natural_gas", 1000, "kWh", "test", "high")
    factor = EmissionFactor("EF-TEST", "natural_gas", 0.202, "kgCO2e/kWh", "DE", "test", 2025, "1.0", "activity_based")
    result = calculate(activity, factor, "CALC-TEST")

    assert result.emissions_kgco2e == 202.0
    assert result.emissions_tco2e == 0.202
    assert result.factor_version == "1.0"
