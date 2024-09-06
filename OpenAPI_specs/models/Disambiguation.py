from pydantic import BaseModel, Field
from .DisambiguationOption import DisambiguationOption
from typing import List
from typing import Optional


class Disambiguation(BaseModel):
    disambiguationOptions: Optional[List[DisambiguationOption]] = Field(None, alias='disambiguationOptions')

    class Config:
        from_attributes = True
