from pydantic import BaseModel, Field
from typing import Optional, List, Union, ForwardRef, Literal
from datetime import datetime
from enum import Enum

from RouteSectionNaptanEntrySequence import RouteSectionNaptanEntrySequence

class RouteSection(BaseModel):
    id: Optional[str] = Field(None, alias='id')
    line_id: Optional[str] = Field(None, alias='lineId')
    route_code: Optional[str] = Field(None, alias='routeCode')
    name: Optional[str] = Field(None, alias='name')
    line_string: Optional[str] = Field(None, alias='lineString')
    direction: Optional[str] = Field(None, alias='direction')
    origination_name: Optional[str] = Field(None, alias='originationName')
    destination_name: Optional[str] = Field(None, alias='destinationName')
    valid_to: Optional[datetime] = Field(None, alias='validTo')
    valid_from: Optional[datetime] = Field(None, alias='validFrom')
    route_section_naptan_entry_sequence: Optional[List[RouteSectionNaptanEntrySequence]] = Field(None, alias='routeSectionNaptanEntrySequence')
    model_config = {"populate_by_name": True}

RouteSection.model_rebuild()
