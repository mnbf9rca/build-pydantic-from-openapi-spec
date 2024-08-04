from pydantic import BaseModel, Field
from typing import Optional, List, Union, ForwardRef, Literal
from datetime import datetime
from enum import Enum

from ValidityPeriod import ValidityPeriod
from Disruption import Disruption

class LineStatus(BaseModel):
    id: Optional[int] = Field(None, alias='id')
    line_id: Optional[str] = Field(None, alias='lineId')
    status_severity: Optional[int] = Field(None, alias='statusSeverity')
    status_severity_description: Optional[str] = Field(None, alias='statusSeverityDescription')
    reason: Optional[str] = Field(None, alias='reason')
    created: Optional[datetime] = Field(None, alias='created')
    modified: Optional[datetime] = Field(None, alias='modified')
    validity_periods: Optional[List[ValidityPeriod]] = Field(None, alias='validityPeriods')
    disruption: Optional[Disruption] = Field(None, alias='disruption')
    model_config = {"populate_by_name": True}

LineStatus.model_rebuild()
