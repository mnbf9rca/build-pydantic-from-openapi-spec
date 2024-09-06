from pydantic import BaseModel, Field
from .StreetSegment import StreetSegment
from typing import List
from typing import Optional


class Street(BaseModel):
    name: Optional[str] = Field(None, alias='name')
    closure: Optional[str] = Field(None, alias='closure')
    directions: Optional[str] = Field(None, alias='directions')
    segments: Optional[List[StreetSegment]] = Field(None, alias='segments')
    sourceSystemId: Optional[int] = Field(None, alias='sourceSystemId')
    sourceSystemKey: Optional[str] = Field(None, alias='sourceSystemKey')

    class Config:
        from_attributes = True
