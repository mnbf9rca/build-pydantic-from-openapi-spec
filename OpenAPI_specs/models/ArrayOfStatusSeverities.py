from pydantic import RootModel
from .StatusSeverity import StatusSeverity
from typing import List


class ArrayOfStatusSeverities(RootModel[List[StatusSeverity]]):

    class Config:
        from_attributes = True
