from pydantic import BaseModel, Field
from .Place import Place
from typing import List


class ArrayOfPlaces(BaseModel):
    data: List[Place] = Field(..., alias='data')

    class Config:
        from_attributes = True
