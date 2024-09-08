from pydantic import RootModel
from typing import List
from .StatusSeverity import StatusSeverity


class ArrayOfStatusSeverities(RootModel[List[StatusSeverity]]):
    class Config:
        from_attributes = True

