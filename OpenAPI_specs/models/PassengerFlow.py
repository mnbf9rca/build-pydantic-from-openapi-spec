from pydantic import BaseModel, Field
from typing import Optional, List, Union, ForwardRef, Literal
from datetime import datetime
from enum import Enum


class PassengerFlow(BaseModel):
    time_slice: Optional[str] = Field(None, alias='timeSlice')
    value: Optional[int] = Field(None, alias='value')
    model_config = {"populate_by_name": True}

PassengerFlow.model_rebuild()
