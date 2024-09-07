from pydantic import RootModel
from typing import List
from typing import Mode


class ArrayOfModes(RootModel[List[Mode]]):

    class Config:
        from_attributes = True
