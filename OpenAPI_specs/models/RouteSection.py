from pydantic import BaseModel, Field
from .RouteSectionNaptanEntrySequence import RouteSectionNaptanEntrySequence
from typing import List
from typing import Optional


class RouteSection(BaseModel):
    id: Optional[str] = Field(None, alias='id')
    lineId: Optional[str] = Field(None, alias='lineId')
    routeCode: Optional[str] = Field(None, alias='routeCode')
    name: Optional[str] = Field(None, alias='name')
    lineString: Optional[str] = Field(None, alias='lineString')
    direction: Optional[str] = Field(None, alias='direction')
    originationName: Optional[str] = Field(None, alias='originationName')
    destinationName: Optional[str] = Field(None, alias='destinationName')
    validTo: Optional[str] = Field(None, alias='validTo')
    validFrom: Optional[str] = Field(None, alias='validFrom')
    routeSectionNaptanEntrySequence: Optional[List[RouteSectionNaptanEntrySequence]] = Field(None, alias='routeSectionNaptanEntrySequence')

    class Config:
        from_attributes = True
