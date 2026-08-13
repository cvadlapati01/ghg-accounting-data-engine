from datetime import datetime, timezone

from .models import AuditEvent, Calculation


def create_calculation_event(calculation: Calculation) -> AuditEvent:
    return AuditEvent(
        audit_event_id=f"AUDIT-{calculation.calculation_id}",
        calculation_id=calculation.calculation_id,
        event_type="calculation_created",
        timestamp=datetime.now(timezone.utc),
        description=(
            f"Calculation created using emission factor {calculation.factor_id} "
            f"version {calculation.factor_version}"
        ),
    )
