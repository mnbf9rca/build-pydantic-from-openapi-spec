from pydantic import BaseModel, Field
from typing import Any
from typing import List


class ArrayOfStrings(BaseModel):
    data: List[Any] = Field(..., alias='data')

    class Config:
        from_attributes = True
