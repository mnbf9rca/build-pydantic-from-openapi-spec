from pydantic import BaseModel, Field
from typing import Optional, List, Union, ForwardRef, Literal
from datetime import datetime
from enum import Enum


class TwentyFourHourClockTime(BaseModel):
    hour: Optional[str] = Field(None, alias='hour')
    minute: Optional[str] = Field(None, alias='minute')
    model_config = {"populate_by_name": True}

TwentyFourHourClockTime.model_rebuild()
