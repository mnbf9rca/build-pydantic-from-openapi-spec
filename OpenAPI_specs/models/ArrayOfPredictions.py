from pydantic import BaseModel, Field
from .Prediction import Prediction
from typing import List


class ArrayOfPredictions(BaseModel):
    data: List[Prediction] = Field(..., alias='data')

    class Config:
        from_attributes = True
