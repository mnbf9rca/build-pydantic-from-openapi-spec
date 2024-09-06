from pydantic import BaseModel, Field
from .RoadDisruption import RoadDisruption
from typing import List


class ArrayOfRoadDisruptions(BaseModel):
    data: List[RoadDisruption] = Field(..., alias='data')

    class Config:
        from_attributes = True
