from pydantic import BaseModel, Field
from typing import Optional, List, Union, ForwardRef, Literal
from datetime import datetime
from enum import Enum

from Interval import Interval

class StationInterval(BaseModel):
    id: Optional[str] = Field(None, alias='id')
    intervals: Optional[List[Interval]] = Field(None, alias='intervals')
    model_config = {"populate_by_name": True}

StationInterval.model_rebuild()
