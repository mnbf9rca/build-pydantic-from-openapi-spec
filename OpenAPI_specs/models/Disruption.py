from pydantic import BaseModel, Field
from typing import Optional, List, Union, ForwardRef, Literal
from datetime import datetime
from enum import Enum

from StopPoint import StopPoint
from RouteSection import RouteSection

class Disruption(BaseModel):
    category: Optional[Literal['Undefined', 'RealTime', 'PlannedWork', 'Information', 'Event', 'Crowding', 'StatusAlert']] = Field(None, alias='category')
    type: Optional[str] = Field(None, alias='type')
    category_description: Optional[str] = Field(None, alias='categoryDescription')
    description: Optional[str] = Field(None, alias='description')
    summary: Optional[str] = Field(None, alias='summary')
    additional_info: Optional[str] = Field(None, alias='additionalInfo')
    created: Optional[datetime] = Field(None, alias='created')
    last_update: Optional[datetime] = Field(None, alias='lastUpdate')
    affected_routes: Optional[List[RouteSection]] = Field(None, alias='affectedRoutes')
    affected_stops: Optional[List[StopPoint]] = Field(None, alias='affectedStops')
    closure_text: Optional[str] = Field(None, alias='closureText')
    model_config = {"populate_by_name": True}

Disruption.model_rebuild()
