from pydantic import RootModel
from .RoadDisruption import RoadDisruption
from typing import List


class ArrayOfRoadDisruptions(RootModel[List[RoadDisruption]]):

    class Config:
        from_attributes = True
