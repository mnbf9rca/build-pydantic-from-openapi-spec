from pydantic import BaseModel, Field
from .Line import Line
from typing import List


class ArrayOfLines(BaseModel):
    data: List[Line] = Field(..., alias='data')

    class Config:
        from_attributes = True
