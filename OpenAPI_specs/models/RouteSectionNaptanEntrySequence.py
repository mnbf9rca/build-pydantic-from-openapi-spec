from pydantic import BaseModel, Field
from typing import Optional, List, Union, ForwardRef, Literal
from datetime import datetime
from enum import Enum

from StopPoint import StopPoint

class RouteSectionNaptanEntrySequence(BaseModel):
    ordinal: Optional[int] = Field(None, alias='ordinal')
    stop_point: Optional[StopPoint] = Field(None, alias='stopPoint')
    model_config = {"populate_by_name": True}

RouteSectionNaptanEntrySequence.model_rebuild()
