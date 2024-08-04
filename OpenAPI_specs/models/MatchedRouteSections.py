from pydantic import BaseModel, Field
from typing import Optional, List, Union, ForwardRef, Literal
from datetime import datetime
from enum import Enum


class MatchedRouteSections(BaseModel):
    id: Optional[int] = Field(None, alias='id')
    model_config = {"populate_by_name": True}

MatchedRouteSections.model_rebuild()
