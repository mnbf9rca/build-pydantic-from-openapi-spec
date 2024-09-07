from pydantic import RootModel
from .Place import Place
from typing import List


class ArrayOfPlaces(RootModel[List[Place]]):

    class Config:
        from_attributes = True
