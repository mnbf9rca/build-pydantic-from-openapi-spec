from pydantic import RootModel
from .Line import Line
from typing import List


class ArrayOfLines(RootModel[List[Line]]):

    class Config:
        from_attributes = True
