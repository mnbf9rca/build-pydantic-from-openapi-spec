from pydantic import RootModel
from .StopPoint import StopPoint
from typing import List


class ArrayOfStopPoints(RootModel[List[StopPoint]]):

    class Config:
        from_attributes = True
