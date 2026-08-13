from src.models import Activity
from src.validation import validate_activity


def test_negative_quantity_is_rejected():
    activity = Activity("ACT-INVALID", "ACME-DE", 2025, 2, "purchased_electricity", "electricity", -1, "kWh", "test", "high")
    errors = validate_activity(activity)
    assert any(error.field == "quantity" for error in errors)


def test_incompatible_unit_is_rejected():
    activity = Activity("ACT-INVALID", "ACME-DE", 2025, 3, "business_travel", "business_travel_distance", 100, "miles", "test", "high")
    errors = validate_activity(activity)
    assert any(error.field == "unit" for error in errors)
