from pydantic import RootModel
from typing import LiftDisruption
from typing import List


class ArrayOfLiftDisruptions(RootModel[List[LiftDisruption]]):

    class Config:
        from_attributes = True
