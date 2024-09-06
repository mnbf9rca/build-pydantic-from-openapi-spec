from pydantic import BaseModel, Field
from .LiftDisruption import LiftDisruption
from typing import List


class Get200ApplicationJsonResponse(BaseModel):
    data: List[LiftDisruption] = Field(..., alias='data')

    class Config:
        from_attributes = True
