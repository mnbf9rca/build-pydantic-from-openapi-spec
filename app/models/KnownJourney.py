from pydantic import BaseModel, Field
from pydantic import BaseModel, Field
from typing import Optional


class KnownJourney(BaseModel):
    hour: Optional[str] = Field(None, alias='hour')
    minute: Optional[str] = Field(None, alias='minute')
    intervalId: Optional[int] = Field(None, alias='intervalId')

    class Config:
        from_attributes = True
