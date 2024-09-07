from pydantic import RootModel
from typing import Any
from typing import List


class ArrayOfStrings(RootModel[List[Any]]):

    class Config:
        from_attributes = True
