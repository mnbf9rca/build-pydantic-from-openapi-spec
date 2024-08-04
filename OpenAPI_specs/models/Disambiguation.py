from pydantic import BaseModel, Field
from typing import Optional, List, Union, ForwardRef, Literal
from datetime import datetime
from enum import Enum

from DisambiguationOption import DisambiguationOption

class Disambiguation(BaseModel):
    disambiguation_options: Optional[List[DisambiguationOption]] = Field(None, alias='disambiguationOptions')
    model_config = {"populate_by_name": True}

Disambiguation.model_rebuild()
