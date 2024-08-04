from pydantic import BaseModel, Field
from typing import Optional, List, Union, ForwardRef, Literal
from datetime import datetime
from enum import Enum


class DisambiguationOption(BaseModel):
    description: Optional[str] = Field(None, alias='description')
    uri: Optional[str] = Field(None, alias='uri')
    model_config = {"populate_by_name": True}

DisambiguationOption.model_rebuild()
