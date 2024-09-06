from pydantic import BaseModel, Field
from .Bay import Bay
from typing import List
from typing import Optional


class CarParkOccupancy(BaseModel):
    id: Optional[str] = Field(None, alias='id')
    bays: Optional[List[Bay]] = Field(None, alias='bays')
    name: Optional[str] = Field(None, alias='name')
    carParkDetailsUrl: Optional[str] = Field(None, alias='carParkDetailsUrl')

    class Config:
        from_attributes = True
