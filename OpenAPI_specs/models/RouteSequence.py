from pydantic import BaseModel, Field
from typing import Optional, List, Union, ForwardRef, Literal
from datetime import datetime
from enum import Enum

from MatchedStop import MatchedStop
from OrderedRoute import OrderedRoute
from StopPointSequence import StopPointSequence

class RouteSequence(BaseModel):
    line_id: Optional[str] = Field(None, alias='lineId')
    line_name: Optional[str] = Field(None, alias='lineName')
    direction: Optional[str] = Field(None, alias='direction')
    is_outbound_only: Optional[bool] = Field(None, alias='isOutboundOnly')
    mode: Optional[str] = Field(None, alias='mode')
    line_strings: Optional[List[str]] = Field(None, alias='lineStrings')
    stations: Optional[List[MatchedStop]] = Field(None, alias='stations')
    stop_point_sequences: Optional[List[StopPointSequence]] = Field(None, alias='stopPointSequences')
    ordered_line_routes: Optional[List[OrderedRoute]] = Field(None, alias='orderedLineRoutes')
    content_expires: Optional[datetime] = Field(None)
    shared_expires: Optional[datetime] = Field(None)
    model_config = {"populate_by_name": True}

RouteSequence.model_rebuild()
