from pydantic import BaseModel, Field
from .ActiveServiceType import ActiveServiceType
from typing import List


class ArrayOfActiveServiceTypes(BaseModel):
    data: List[ActiveServiceType] = Field(..., alias='data')

    class Config:
        from_attributes = True
