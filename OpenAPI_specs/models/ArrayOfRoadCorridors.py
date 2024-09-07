from pydantic import RootModel
from .RoadCorridor import RoadCorridor
from typing import List


class ArrayOfRoadCorridors(RootModel[List[RoadCorridor]]):

    class Config:
        from_attributes = True
