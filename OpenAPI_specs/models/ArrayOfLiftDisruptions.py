from pydantic import BaseModel, Field
from .LiftDisruption import LiftDisruption
from typing import List


class ArrayOfLiftDisruptions(BaseModel):
    data: List[LiftDisruption] = Field(..., alias='data')

    class Config:
        from_attributes = True
