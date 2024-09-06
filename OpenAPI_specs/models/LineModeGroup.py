from pydantic import BaseModel, Field
from typing import List
from typing import Optional


class LineModeGroup(BaseModel):
    modeName: Optional[str] = Field(None, alias='modeName')
    lineIdentifier: Optional[List[str]] = Field(None, alias='lineIdentifier')

    class Config:
        from_attributes = True
