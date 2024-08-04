from pydantic import BaseModel, Field
from typing import Optional, List, Union, ForwardRef, Literal
from datetime import datetime
from enum import Enum


class MatchedRoute(BaseModel):
    route_code: Optional[str] = Field(None, alias='routeCode')
    name: Optional[str] = Field(None, alias='name')
    direction: Optional[str] = Field(None, alias='direction')
    origination_name: Optional[str] = Field(None, alias='originationName')
    destination_name: Optional[str] = Field(None, alias='destinationName')
    originator: Optional[str] = Field(None, alias='originator')
    destination: Optional[str] = Field(None, alias='destination')
    service_type: Optional[str] = Field(None, alias='serviceType')
    valid_to: Optional[datetime] = Field(None, alias='validTo')
    valid_from: Optional[datetime] = Field(None, alias='validFrom')
    model_config = {"populate_by_name": True}

MatchedRoute.model_rebuild()
