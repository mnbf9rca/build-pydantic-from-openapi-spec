from pydantic import BaseModel, Field
from typing import List
from typing import Optional


class LineGroup(BaseModel):
    naptanIdReference: Optional[str] = Field(None, alias='naptanIdReference')
    stationAtcoCode: Optional[str] = Field(None, alias='stationAtcoCode')
    lineIdentifier: Optional[List[str]] = Field(None, alias='lineIdentifier')

    class Config:
        from_attributes = True
