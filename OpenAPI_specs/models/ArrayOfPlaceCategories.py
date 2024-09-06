from pydantic import BaseModel, Field
from .PlaceCategory import PlaceCategory
from typing import List


class ArrayOfPlaceCategories(BaseModel):
    data: List[PlaceCategory] = Field(..., alias='data')

    class Config:
        from_attributes = True
