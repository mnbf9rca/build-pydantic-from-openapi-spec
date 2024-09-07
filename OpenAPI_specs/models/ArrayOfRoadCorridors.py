from pydantic import RootModel
from typing import List
from typing import RoadCorridor


class ArrayOfRoadCorridors(RootModel[List[RoadCorridor]]):

    class Config:
        from_attributes = True
