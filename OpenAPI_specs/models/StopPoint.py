from pydantic import BaseModel, Field
from typing import Optional, List, Union, ForwardRef, Literal
from datetime import datetime
from enum import Enum

from LineGroup import LineGroup
from AdditionalProperties import AdditionalProperties
from Identifier import Identifier
from LineModeGroup import LineModeGroup
from Place import Place

class StopPoint(BaseModel):
    naptan_id: Optional[str] = Field(None, alias='naptanId')
    platform_name: Optional[str] = Field(None, alias='platformName')
    indicator: Optional[str] = Field(None, alias='indicator')
    stop_letter: Optional[str] = Field(None, alias='stopLetter')
    modes: Optional[List[str]] = Field(None, alias='modes')
    ics_code: Optional[str] = Field(None, alias='icsCode')
    sms_code: Optional[str] = Field(None, alias='smsCode')
    stop_type: Optional[str] = Field(None, alias='stopType')
    station_naptan: Optional[str] = Field(None, alias='stationNaptan')
    accessibility_summary: Optional[str] = Field(None, alias='accessibilitySummary')
    hub_naptan_code: Optional[str] = Field(None, alias='hubNaptanCode')
    lines: Optional[List[Identifier]] = Field(None, alias='lines')
    line_group: Optional[List[LineGroup]] = Field(None, alias='lineGroup')
    line_mode_groups: Optional[List[LineModeGroup]] = Field(None, alias='lineModeGroups')
    full_name: Optional[str] = Field(None, alias='fullName')
    naptan_mode: Optional[str] = Field(None, alias='naptanMode')
    status: Optional[bool] = Field(None, alias='status')
    id: Optional[str] = Field(None, alias='id')
    url: Optional[str] = Field(None, alias='url')
    common_name: Optional[str] = Field(None, alias='commonName')
    distance: Optional[float] = Field(None, alias='distance')
    place_type: Optional[str] = Field(None, alias='placeType')
    additional_properties: Optional[List[AdditionalProperties]] = Field(None, alias='additionalProperties')
    children: Optional[List[Place]] = Field(None, alias='children')
    children_urls: Optional[List[str]] = Field(None, alias='childrenUrls')
    lat: Optional[float] = Field(None, alias='lat')
    lon: Optional[float] = Field(None, alias='lon')
    model_config = {"populate_by_name": True}

StopPoint.model_rebuild()
