from pydantic import BaseModel, Field
from typing import Optional, List, Union, ForwardRef, Literal
from datetime import datetime
from enum import Enum


class Mode(BaseModel):
    is_tfl_service: Optional[bool] = Field(None, alias='isTflService')
    is_fare_paying: Optional[bool] = Field(None, alias='isFarePaying')
    is_scheduled_service: Optional[bool] = Field(None, alias='isScheduledService')
    mode_name: Optional[str] = Field(None, alias='modeName')
    model_config = {"populate_by_name": True}

Mode.model_rebuild()
