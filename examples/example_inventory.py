from pathlib import Path

from src.audit_trail import create_calculation_event
from src.pipeline import run_inventory

ROOT = Path(__file__).resolve().parents[1]
calculations, errors = run_inventory(ROOT / "data/activity_data.csv", ROOT / "data/emission_factors.csv")

print("GHG ACCOUNTING DATA ENGINE")
print("=" * 28)
print(f"Calculations created: {len(calculations)}")
print(f"Validation errors:    {len(errors)}")
print()

for calculation in calculations:
    event = create_calculation_event(calculation)
    print(
        f"{calculation.calculation_id}: "
        f"{calculation.emissions_tco2e:.3f} tCO2e "
        f"[{calculation.calculation_method}] "
        f"factor={calculation.factor_id} v{calculation.factor_version}"
    )

print("\nValidation errors")
for error in errors:
    print(f"- {error.activity_id}: {error.field} — {error.message}")
