from pydantic import BaseModel, Field
from typing import Optional, List, Union, ForwardRef, Literal
from datetime import datetime
from enum import Enum

from Identifier import Identifier

class MatchedStop(BaseModel):
    route_id: Optional[int] = Field(None, alias='routeId')
    parent_id: Optional[str] = Field(None, alias='parentId')
    station_id: Optional[str] = Field(None, alias='stationId')
    ics_id: Optional[str] = Field(None, alias='icsId')
    top_most_parent_id: Optional[str] = Field(None, alias='topMostParentId')
    direction: Optional[str] = Field(None, alias='direction')
    towards: Optional[str] = Field(None, alias='towards')
    modes: Optional[List[str]] = Field(None, alias='modes')
    stop_type: Optional[str] = Field(None, alias='stopType')
    stop_letter: Optional[str] = Field(None, alias='stopLetter')
    zone: Optional[str] = Field(None, alias='zone')
    accessibility_summary: Optional[str] = Field(None, alias='accessibilitySummary')
    has_disruption: Optional[bool] = Field(None, alias='hasDisruption')
    lines: Optional[List[Identifier]] = Field(None, alias='lines')
    status: Optional[bool] = Field(None, alias='status')
    id: Optional[str] = Field(None, alias='id')
    url: Optional[str] = Field(None, alias='url')
    name: Optional[str] = Field(None, alias='name')
    lat: Optional[float] = Field(None, alias='lat')
    lon: Optional[float] = Field(None, alias='lon')
    model_config = {"populate_by_name": True}

MatchedStop.model_rebuild()
