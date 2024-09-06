from pydantic import BaseModel, Field
from .ServiceFrequency import ServiceFrequency
from .TwentyFourHourClockTime import TwentyFourHourClockTime
from .TypeEnum import TypeEnum
from typing import Optional


class Period(BaseModel):
    type: Optional[TypeEnum] = Field(None, alias='type')
    fromTime: Optional[TwentyFourHourClockTime] = Field(None, alias='fromTime')
    toTime: Optional[TwentyFourHourClockTime] = Field(None, alias='toTime')
    frequency: Optional[ServiceFrequency] = Field(None, alias='frequency')

    class Config:
        from_attributes = True
