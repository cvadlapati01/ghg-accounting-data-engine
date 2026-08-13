from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass(frozen=True)
class Activity:
    activity_id: str
    entity_id: str
    reporting_year: int
    scope: int
    category: str
    activity_type: str
    quantity: float
    unit: str
    source: str
    data_quality: str
    is_estimated: bool = False


@dataclass(frozen=True)
class EmissionFactor:
    factor_id: str
    activity_type: str
    factor_value: float
    factor_unit: str
    geography: str
    source: str
    source_year: int
    version: str
    methodology: str


@dataclass(frozen=True)
class Calculation:
    calculation_id: str
    activity_id: str
    factor_id: str
    factor_version: str
    calculation_method: str
    formula: str
    activity_quantity: float
    activity_unit: str
    emission_factor: float
    emission_factor_unit: str
    emissions_kgco2e: float
    emissions_tco2e: float
    calculation_version: str
    calculated_at: datetime


@dataclass(frozen=True)
class AuditEvent:
    audit_event_id: str
    calculation_id: str
    event_type: str
    timestamp: datetime
    description: str


@dataclass(frozen=True)
class ValidationError:
    activity_id: str
    field: str
    message: str
    value: Optional[str] = None
