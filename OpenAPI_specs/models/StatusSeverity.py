from pydantic import BaseModel, Field
from typing import Optional, List, Union, ForwardRef, Literal
from datetime import datetime
from enum import Enum


class StatusSeverity(BaseModel):
    mode_name: Optional[str] = Field(None, alias='modeName')
    severity_level: Optional[int] = Field(None, alias='severityLevel')
    description: Optional[str] = Field(None, alias='description')
    model_config = {"populate_by_name": True}

StatusSeverity.model_rebuild()
