from pydantic import BaseModel, Field
from typing import Optional, List, Union, ForwardRef, Literal
from datetime import datetime
from enum import Enum


class LineGroup(BaseModel):
    naptan_id_reference: Optional[str] = Field(None, alias='naptanIdReference')
    station_atco_code: Optional[str] = Field(None, alias='stationAtcoCode')
    line_identifier: Optional[List[str]] = Field(None, alias='lineIdentifier')
    model_config = {"populate_by_name": True}

LineGroup.model_rebuild()
