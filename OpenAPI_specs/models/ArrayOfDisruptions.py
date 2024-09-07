from pydantic import RootModel
from .Disruption import Disruption
from typing import List


class ArrayOfDisruptions(RootModel[List[Disruption]]):

    class Config:
        from_attributes = True
