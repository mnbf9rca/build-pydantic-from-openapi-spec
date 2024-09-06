from pydantic import BaseModel, Field
from typing import List
from typing import Optional


class PlaceCategory(BaseModel):
    category: Optional[str] = Field(None, alias='category')
    availableKeys: Optional[List[str]] = Field(None, alias='availableKeys')

    class Config:
        from_attributes = True
