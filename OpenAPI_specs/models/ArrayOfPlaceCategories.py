from pydantic import RootModel
from typing import List
from typing import PlaceCategory


class ArrayOfPlaceCategories(RootModel[List[PlaceCategory]]):

    class Config:
        from_attributes = True
