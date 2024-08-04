from pydantic import BaseModel, Field
from typing import Optional, List, Union, ForwardRef, Literal
from datetime import datetime
from enum import Enum


class KnownJourney(BaseModel):
    hour: Optional[str] = Field(None, alias='hour')
    minute: Optional[str] = Field(None, alias='minute')
    interval_id: Optional[int] = Field(None, alias='intervalId')
    model_config = {"populate_by_name": True}

KnownJourney.model_rebuild()
