from pydantic import RootModel
from .PlaceCategory import PlaceCategory
from typing import List


class ArrayOfPlaceCategories(RootModel[List[PlaceCategory]]):

    class Config:
        from_attributes = True
