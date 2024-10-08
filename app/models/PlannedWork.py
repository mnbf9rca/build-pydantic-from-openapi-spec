from pydantic import BaseModel, Field
from pydantic import BaseModel, Field
from typing import Optional


class PlannedWork(BaseModel):
    id: Optional[str] = Field(None, alias='id')
    description: Optional[str] = Field(None, alias='description')
    createdDateTime: Optional[str] = Field(None, alias='createdDateTime')
    lastUpdateDateTime: Optional[str] = Field(None, alias='lastUpdateDateTime')

    class Config:
        from_attributes = True
