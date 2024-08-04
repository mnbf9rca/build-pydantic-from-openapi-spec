from pydantic import BaseModel, Field
from typing import Optional, List, Union, ForwardRef, Literal
from datetime import datetime
from enum import Enum


class LineModeGroup(BaseModel):
    mode_name: Optional[str] = Field(None, alias='modeName')
    line_identifier: Optional[List[str]] = Field(None, alias='lineIdentifier')
    model_config = {"populate_by_name": True}

LineModeGroup.model_rebuild()
