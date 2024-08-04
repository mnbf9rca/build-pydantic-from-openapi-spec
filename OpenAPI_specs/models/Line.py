from pydantic import BaseModel, Field
from typing import Optional, List, Union, ForwardRef, Literal
from datetime import datetime
from enum import Enum

from MatchedRoute import MatchedRoute
from Crowding import Crowding
from LineServiceTypeInfo import LineServiceTypeInfo
from Disruption import Disruption
from LineStatus import LineStatus

class Line(BaseModel):
    id: Optional[str] = Field(None, alias='id')
    name: Optional[str] = Field(None, alias='name')
    mode_name: Optional[str] = Field(None, alias='modeName')
    disruptions: Optional[List[Disruption]] = Field(None, alias='disruptions')
    created: Optional[datetime] = Field(None, alias='created')
    modified: Optional[datetime] = Field(None, alias='modified')
    line_statuses: Optional[List[LineStatus]] = Field(None, alias='lineStatuses')
    route_sections: Optional[List[MatchedRoute]] = Field(None, alias='routeSections')
    service_types: Optional[List[LineServiceTypeInfo]] = Field(None, alias='serviceTypes')
    crowding: Optional[Crowding] = Field(None, alias='crowding')
    model_config = {"populate_by_name": True}

Line.model_rebuild()
