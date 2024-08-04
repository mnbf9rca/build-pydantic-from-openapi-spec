from pydantic import BaseModel, Field
from typing import Optional, List, Union, ForwardRef, Literal
from datetime import datetime
from enum import Enum


class Interval(BaseModel):
    stop_id: Optional[str] = Field(None, alias='stopId')
    time_to_arrival: Optional[float] = Field(None, alias='timeToArrival')
    model_config = {"populate_by_name": True}

Interval.model_rebuild()
