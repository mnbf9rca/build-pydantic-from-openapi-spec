from pydantic import BaseModel, Field
from .Mode import Mode
from typing import List


class ArrayOfModes(BaseModel):
    data: List[Mode] = Field(..., alias='data')

    class Config:
        from_attributes = True
