from pydantic import BaseModel, Field
from .Disruption import Disruption
from typing import List


class ArrayOfDisruptions(BaseModel):
    data: List[Disruption] = Field(..., alias='data')

    class Config:
        from_attributes = True
