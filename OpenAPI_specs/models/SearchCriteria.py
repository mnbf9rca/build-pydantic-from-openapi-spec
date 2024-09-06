from pydantic import BaseModel, Field
from .DateTimeTypeEnum import DateTimeTypeEnum
from .TimeAdjustments import TimeAdjustments
from typing import Optional


class SearchCriteria(BaseModel):
    dateTime: Optional[str] = Field(None, alias='dateTime')
    dateTimeType: Optional[DateTimeTypeEnum] = Field(None, alias='dateTimeType')
    timeAdjustments: Optional[TimeAdjustments] = Field(None, alias='timeAdjustments')

    class Config:
        from_attributes = True
