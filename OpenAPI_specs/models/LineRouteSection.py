from pydantic import BaseModel, Field
from typing import Optional, List, Union, ForwardRef, Literal
from datetime import datetime
from enum import Enum


class LineRouteSection(BaseModel):
    route_id: Optional[int] = Field(None, alias='routeId')
    direction: Optional[str] = Field(None, alias='direction')
    destination: Optional[str] = Field(None, alias='destination')
    from_station: Optional[str] = Field(None, alias='fromStation')
    to_station: Optional[str] = Field(None, alias='toStation')
    service_type: Optional[str] = Field(None, alias='serviceType')
    vehicle_destination_text: Optional[str] = Field(None, alias='vehicleDestinationText')
    model_config = {"populate_by_name": True}

LineRouteSection.model_rebuild()
