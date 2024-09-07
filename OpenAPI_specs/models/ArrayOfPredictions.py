from pydantic import RootModel
from .Prediction import Prediction
from typing import List


class ArrayOfPredictions(RootModel[List[Prediction]]):

    class Config:
        from_attributes = True
