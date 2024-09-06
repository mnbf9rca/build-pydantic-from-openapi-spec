from pydantic import BaseModel, Field
from .FareTap import FareTap
from typing import List
from typing import Optional


class Fare(BaseModel):
    lowZone: Optional[int] = Field(None, alias='lowZone')
    highZone: Optional[int] = Field(None, alias='highZone')
    cost: Optional[int] = Field(None, alias='cost')
    chargeProfileName: Optional[str] = Field(None, alias='chargeProfileName')
    isHopperFare: Optional[bool] = Field(None, alias='isHopperFare')
    chargeLevel: Optional[str] = Field(None, alias='chargeLevel')
    peak: Optional[int] = Field(None, alias='peak')
    offPeak: Optional[int] = Field(None, alias='offPeak')
    taps: Optional[List[FareTap]] = Field(None, alias='taps')

    class Config:
        from_attributes = True
