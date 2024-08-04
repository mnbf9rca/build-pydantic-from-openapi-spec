from pydantic import BaseModel, Field
from typing import Optional, List, Union, ForwardRef, Literal
from datetime import datetime
from enum import Enum

from ServiceFrequency import ServiceFrequency
from TwentyFourHourClockTime import TwentyFourHourClockTime

class Period(BaseModel):
    type: Optional[Literal['Normal', 'FrequencyHours', 'FrequencyMinutes', 'Unknown']] = Field(None, alias='type')
    from_time: Optional[TwentyFourHourClockTime] = Field(None, alias='fromTime')
    to_time: Optional[TwentyFourHourClockTime] = Field(None, alias='toTime')
    frequency: Optional[ServiceFrequency] = Field(None, alias='frequency')
    model_config = {"populate_by_name": True}

Period.model_rebuild()
