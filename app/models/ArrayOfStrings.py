from pydantic import RootModel
from typing import Any, List


class ArrayOfStrings(RootModel[List[Any]]):
    class Config:
        from_attributes = True

