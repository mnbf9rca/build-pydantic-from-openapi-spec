from pydantic import RootModel
from typing import List
from .Disruption import Disruption


class DisruptionsArray(RootModel[List[Disruption]]):
    class Config:
        from_attributes = True

