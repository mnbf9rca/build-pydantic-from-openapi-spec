from pydantic import BaseModel, Field
from typing import Optional, List, Union, ForwardRef, Literal
from datetime import datetime
from enum import Enum

from StopPoint import StopPoint

class ArrayOfStopPoint(BaseModel):
    StopPoints: List[StopPoint] = Field(None)
    content_expires: Optional[datetime] = Field(None)
    shared_expires: Optional[datetime] = Field(None)
    model_config = {"populate_by_name": True}

ArrayOfStopPoint.model_rebuild()
