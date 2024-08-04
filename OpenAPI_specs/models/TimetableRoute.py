from pydantic import BaseModel, Field
from typing import Optional, List, Union, ForwardRef, Literal
from datetime import datetime
from enum import Enum

from StationInterval import StationInterval
from Schedule import Schedule

class TimetableRoute(BaseModel):
    station_intervals: Optional[List[StationInterval]] = Field(None, alias='stationIntervals')
    schedules: Optional[List[Schedule]] = Field(None, alias='schedules')
    model_config = {"populate_by_name": True}

TimetableRoute.model_rebuild()
