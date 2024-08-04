from pydantic import BaseModel, Field
from typing import Optional, List, Union, ForwardRef, Literal
from datetime import datetime
from enum import Enum

from AdditionalProperties import AdditionalProperties

class Place(BaseModel):
    id: Optional[str] = Field(None, alias='id')
    url: Optional[str] = Field(None, alias='url')
    common_name: Optional[str] = Field(None, alias='commonName')
    distance: Optional[float] = Field(None, alias='distance')
    place_type: Optional[str] = Field(None, alias='placeType')
    additional_properties: Optional[List[AdditionalProperties]] = Field(None, alias='additionalProperties')
    children: Optional["Place"] = Field(None, alias='children')
    children_urls: Optional[List[str]] = Field(None, alias='childrenUrls')
    lat: Optional[float] = Field(None, alias='lat')
    lon: Optional[float] = Field(None, alias='lon')
    model_config = {"populate_by_name": True}

Place.model_rebuild()
