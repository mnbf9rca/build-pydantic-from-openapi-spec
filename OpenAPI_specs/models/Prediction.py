from pydantic import BaseModel, Field
from typing import Optional, List, Union, ForwardRef, Literal
from datetime import datetime
from enum import Enum

from PredictionTiming import PredictionTiming

class Prediction(BaseModel):
    id: Optional[str] = Field(None, alias='id')
    operation_type: Optional[int] = Field(None, alias='operationType')
    vehicle_id: Optional[str] = Field(None, alias='vehicleId')
    naptan_id: Optional[str] = Field(None, alias='naptanId')
    station_name: Optional[str] = Field(None, alias='stationName')
    line_id: Optional[str] = Field(None, alias='lineId')
    line_name: Optional[str] = Field(None, alias='lineName')
    platform_name: Optional[str] = Field(None, alias='platformName')
    direction: Optional[str] = Field(None, alias='direction')
    bearing: Optional[str] = Field(None, alias='bearing')
    destination_naptan_id: Optional[str] = Field(None, alias='destinationNaptanId')
    destination_name: Optional[str] = Field(None, alias='destinationName')
    timestamp: Optional[datetime] = Field(None, alias='timestamp')
    time_to_station: Optional[int] = Field(None, alias='timeToStation')
    current_location: Optional[str] = Field(None, alias='currentLocation')
    towards: Optional[str] = Field(None, alias='towards')
    expected_arrival: Optional[datetime] = Field(None, alias='expectedArrival')
    time_to_live: Optional[datetime] = Field(None, alias='timeToLive')
    mode_name: Optional[str] = Field(None, alias='modeName')
    timing: Optional[PredictionTiming] = Field(None, alias='timing')
    model_config = {"populate_by_name": True}

Prediction.model_rebuild()
