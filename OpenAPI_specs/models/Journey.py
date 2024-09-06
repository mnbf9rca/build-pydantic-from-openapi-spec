from pydantic import BaseModel, Field
from .JourneyFare import JourneyFare
from .Leg import Leg
from typing import List
from typing import Optional


class Journey(BaseModel):
    startDateTime: Optional[str] = Field(None, alias='startDateTime')
    duration: Optional[int] = Field(None, alias='duration')
    arrivalDateTime: Optional[str] = Field(None, alias='arrivalDateTime')
    legs: Optional[List[Leg]] = Field(None, alias='legs')
    fare: Optional[JourneyFare] = Field(None, alias='fare')

    class Config:
        from_attributes = True
