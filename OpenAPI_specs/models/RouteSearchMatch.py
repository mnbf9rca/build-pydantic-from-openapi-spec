from pydantic import BaseModel, Field
from typing import Optional, List, Union, ForwardRef, Literal
from datetime import datetime
from enum import Enum

from MatchedStop import MatchedStop
from MatchedRouteSections import MatchedRouteSections
from LineRouteSection import LineRouteSection

class RouteSearchMatch(BaseModel):
    line_id: Optional[str] = Field(None, alias='lineId')
    mode: Optional[str] = Field(None, alias='mode')
    line_name: Optional[str] = Field(None, alias='lineName')
    line_route_section: Optional[List[LineRouteSection]] = Field(None, alias='lineRouteSection')
    matched_route_sections: Optional[List[MatchedRouteSections]] = Field(None, alias='matchedRouteSections')
    matched_stops: Optional[List[MatchedStop]] = Field(None, alias='matchedStops')
    id: Optional[str] = Field(None, alias='id')
    url: Optional[str] = Field(None, alias='url')
    name: Optional[str] = Field(None, alias='name')
    lat: Optional[float] = Field(None, alias='lat')
    lon: Optional[float] = Field(None, alias='lon')
    model_config = {"populate_by_name": True}

RouteSearchMatch.model_rebuild()
