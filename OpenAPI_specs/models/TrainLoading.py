from pydantic import BaseModel, Field
from typing import Optional, List, Union, ForwardRef, Literal
from datetime import datetime
from enum import Enum


class TrainLoading(BaseModel):
    line: Optional[str] = Field(None, alias='line')
    line_direction: Optional[str] = Field(None, alias='lineDirection')
    platform_direction: Optional[str] = Field(None, alias='platformDirection')
    direction: Optional[str] = Field(None, alias='direction')
    naptan_to: Optional[str] = Field(None, alias='naptanTo')
    time_slice: Optional[str] = Field(None, alias='timeSlice')
    value: Optional[int] = Field(None, alias='value')
    model_config = {"populate_by_name": True}

TrainLoading.model_rebuild()
