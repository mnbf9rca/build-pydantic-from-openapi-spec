from pydantic import BaseModel, Field
from pydantic import BaseModel, Field
from typing import Optional


class Casualty(BaseModel):
    age: Optional[int] = Field(None, alias='age')
    class_field: Optional[str] = Field(None, alias='class')
    severity: Optional[str] = Field(None, alias='severity')
    mode: Optional[str] = Field(None, alias='mode')
    ageBand: Optional[str] = Field(None, alias='ageBand')

    class Config:
        from_attributes = True
