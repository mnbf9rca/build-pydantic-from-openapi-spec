from pydantic import BaseModel, Field
from typing import Optional, List, Union, ForwardRef, Literal
from datetime import datetime
from enum import Enum


class ValidityPeriod(BaseModel):
    from_date: Optional[datetime] = Field(None, alias='fromDate')
    to_date: Optional[datetime] = Field(None, alias='toDate')
    is_now: Optional[bool] = Field(None, alias='isNow')
    model_config = {"populate_by_name": True}

ValidityPeriod.model_rebuild()
