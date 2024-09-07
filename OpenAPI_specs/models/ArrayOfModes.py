from pydantic import RootModel
from .Mode import Mode
from typing import List


class ArrayOfModes(RootModel[List[Mode]]):

    class Config:
        from_attributes = True
