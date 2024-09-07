from pydantic import RootModel
from typing import List
from typing import StatusSeverity


class ArrayOfStatusSeverities(RootModel[List[StatusSeverity]]):

    class Config:
        from_attributes = True
