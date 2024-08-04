from pydantic import BaseModel, Field
from typing import Optional, List, Union, ForwardRef, Literal
from datetime import datetime
from enum import Enum

from MatchedStop import MatchedStop

class StopPointSequence(BaseModel):
    line_id: Optional[str] = Field(None, alias='lineId')
    line_name: Optional[str] = Field(None, alias='lineName')
    direction: Optional[str] = Field(None, alias='direction')
    branch_id: Optional[int] = Field(None, alias='branchId')
    next_branch_ids: Optional[List[int]] = Field(None, alias='nextBranchIds')
    prev_branch_ids: Optional[List[int]] = Field(None, alias='prevBranchIds')
    stop_point: Optional[List[MatchedStop]] = Field(None, alias='stopPoint')
    service_type: Optional[Literal['Regular', 'Night']] = Field(None, alias='serviceType')
    model_config = {"populate_by_name": True}

StopPointSequence.model_rebuild()
