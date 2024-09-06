from pydantic import BaseModel, Field
from .StopPoint import StopPoint
from typing import List


class ArrayOfStopPoints(BaseModel):
    data: List[StopPoint] = Field(..., alias='data')

    class Config:
        from_attributes = True
