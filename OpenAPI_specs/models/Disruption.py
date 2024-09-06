from pydantic import BaseModel, Field
from .CategoryEnum import CategoryEnum
from .RouteSection import RouteSection
from .StopPoint import StopPoint
from typing import List
from typing import Optional


class Disruption(BaseModel):
    category: Optional[CategoryEnum] = Field(None, alias='category')
    type: Optional[str] = Field(None, alias='type')
    categoryDescription: Optional[str] = Field(None, alias='categoryDescription')
    description: Optional[str] = Field(None, alias='description')
    summary: Optional[str] = Field(None, alias='summary')
    additionalInfo: Optional[str] = Field(None, alias='additionalInfo')
    created: Optional[str] = Field(None, alias='created')
    lastUpdate: Optional[str] = Field(None, alias='lastUpdate')
    affectedRoutes: Optional[List[RouteSection]] = Field(None, alias='affectedRoutes')
    affectedStops: Optional[List[StopPoint]] = Field(None, alias='affectedStops')
    closureText: Optional[str] = Field(None, alias='closureText')

    class Config:
        from_attributes = True
