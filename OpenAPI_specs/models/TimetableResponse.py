from pydantic import BaseModel, Field
from typing import Optional, List, Union, ForwardRef, Literal
from datetime import datetime
from enum import Enum

from MatchedStop import MatchedStop
from Timetable import Timetable
from Disambiguation import Disambiguation

class TimetableResponse(BaseModel):
    line_id: Optional[str] = Field(None, alias='lineId')
    line_name: Optional[str] = Field(None, alias='lineName')
    direction: Optional[str] = Field(None, alias='direction')
    pdf_url: Optional[str] = Field(None, alias='pdfUrl')
    stations: Optional[List[MatchedStop]] = Field(None, alias='stations')
    stops: Optional[List[MatchedStop]] = Field(None, alias='stops')
    timetable: Optional[Timetable] = Field(None, alias='timetable')
    disambiguation: Optional[Disambiguation] = Field(None, alias='disambiguation')
    status_error_message: Optional[str] = Field(None, alias='statusErrorMessage')
    content_expires: Optional[datetime] = Field(None)
    shared_expires: Optional[datetime] = Field(None)
    model_config = {"populate_by_name": True}

TimetableResponse.model_rebuild()
