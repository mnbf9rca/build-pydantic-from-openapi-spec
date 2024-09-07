from pydantic import RootModel
from .AccidentDetail import AccidentDetail
from typing import List


class AccidentDetailArray(RootModel[List[AccidentDetail]]):

    class Config:
        from_attributes = True
