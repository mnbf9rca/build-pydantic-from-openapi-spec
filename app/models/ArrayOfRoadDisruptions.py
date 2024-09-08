from pydantic import RootModel
from typing import List
from .RoadDisruption import RoadDisruption


class ArrayOfRoadDisruptions(RootModel[List[RoadDisruption]]):
    class Config:
        from_attributes = True

