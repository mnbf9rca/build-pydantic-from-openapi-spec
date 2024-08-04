from pydantic import BaseModel, Field
from typing import Optional, List, Union, ForwardRef, Literal
from datetime import datetime
from enum import Enum

from TimetableRoute import TimetableRoute

class Timetable(BaseModel):
    departure_stop_id: Optional[str] = Field(None, alias='departureStopId')
    routes: Optional[List[TimetableRoute]] = Field(None, alias='routes')
    model_config = {"populate_by_name": True}

Timetable.model_rebuild()
