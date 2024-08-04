from pydantic import BaseModel, Field
from typing import Optional, List, Union, ForwardRef, Literal
from datetime import datetime
from enum import Enum


class AdditionalProperties(BaseModel):
    category: Optional[str] = Field(None, alias='category')
    key: Optional[str] = Field(None, alias='key')
    source_system_key: Optional[str] = Field(None, alias='sourceSystemKey')
    value: Optional[str] = Field(None, alias='value')
    modified: Optional[datetime] = Field(None, alias='modified')
    model_config = {"populate_by_name": True}

AdditionalProperties.model_rebuild()
