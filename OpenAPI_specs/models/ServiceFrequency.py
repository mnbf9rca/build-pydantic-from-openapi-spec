from pydantic import BaseModel, Field
from typing import Optional, List, Union, ForwardRef, Literal
from datetime import datetime
from enum import Enum


class ServiceFrequency(BaseModel):
    lowest_frequency: Optional[float] = Field(None, alias='lowestFrequency')
    highest_frequency: Optional[float] = Field(None, alias='highestFrequency')
    model_config = {"populate_by_name": True}

ServiceFrequency.model_rebuild()
