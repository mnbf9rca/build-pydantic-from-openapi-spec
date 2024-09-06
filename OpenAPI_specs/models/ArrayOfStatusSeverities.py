from pydantic import BaseModel, Field
from .StatusSeverity import StatusSeverity
from typing import List


class ArrayOfStatusSeverities(BaseModel):
    data: List[StatusSeverity] = Field(..., alias='data')

    class Config:
        from_attributes = True
