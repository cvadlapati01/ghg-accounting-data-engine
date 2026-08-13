from pathlib import Path

from src.pipeline import run_inventory


ROOT = Path(__file__).resolve().parents[1]


def test_pipeline_processes_valid_records_and_flags_invalid_ones():
    calculations, errors = run_inventory(ROOT / "data/activity_data.csv", ROOT / "data/emission_factors.csv")

    assert len(calculations) == 10
    assert len(errors) == 2
    assert sum(c.emissions_tco2e for c in calculations) > 0
