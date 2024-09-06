from pydantic import BaseModel, Field
from .RoadCorridor import RoadCorridor
from typing import List


class ArrayOfRoadCorridors(BaseModel):
    data: List[RoadCorridor] = Field(..., alias='data')

    class Config:
        from_attributes = True
