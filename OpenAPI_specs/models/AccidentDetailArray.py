from pydantic import BaseModel, Field
from .AccidentDetail import AccidentDetail
from typing import List


class AccidentDetailArray(BaseModel):
    data: List[AccidentDetail] = Field(..., alias='data')

    class Config:
        from_attributes = True
