from pydantic import BaseModel, Field
from typing import Optional, List, Union, ForwardRef, Literal
from datetime import datetime
from enum import Enum


class PredictionTiming(BaseModel):
    countdown_server_adjustment: Optional[str] = Field(None, alias='countdownServerAdjustment')
    source: Optional[datetime] = Field(None, alias='source')
    insert: Optional[datetime] = Field(None, alias='insert')
    read: Optional[datetime] = Field(None, alias='read')
    sent: Optional[datetime] = Field(None, alias='sent')
    received: Optional[datetime] = Field(None, alias='received')
    model_config = {"populate_by_name": True}

PredictionTiming.model_rebuild()
