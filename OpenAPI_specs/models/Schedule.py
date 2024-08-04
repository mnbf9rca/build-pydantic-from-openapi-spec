from pydantic import BaseModel, Field
from typing import Optional, List, Union, ForwardRef, Literal
from datetime import datetime
from enum import Enum

from KnownJourney import KnownJourney
from Period import Period

class Schedule(BaseModel):
    name: Optional[str] = Field(None, alias='name')
    known_journeys: Optional[List[KnownJourney]] = Field(None, alias='knownJourneys')
    first_journey: Optional[KnownJourney] = Field(None, alias='firstJourney')
    last_journey: Optional[KnownJourney] = Field(None, alias='lastJourney')
    periods: Optional[List[Period]] = Field(None, alias='periods')
    model_config = {"populate_by_name": True}

Schedule.model_rebuild()
