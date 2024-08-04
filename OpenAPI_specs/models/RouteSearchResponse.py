from pydantic import BaseModel, Field
from typing import Optional, List, Union, ForwardRef, Literal
from datetime import datetime
from enum import Enum

from RouteSearchMatch import RouteSearchMatch

class RouteSearchResponse(BaseModel):
    input: Optional[str] = Field(None, alias='input')
    search_matches: Optional[List[RouteSearchMatch]] = Field(None, alias='searchMatches')
    content_expires: Optional[datetime] = Field(None)
    shared_expires: Optional[datetime] = Field(None)
    model_config = {"populate_by_name": True}

RouteSearchResponse.model_rebuild()
