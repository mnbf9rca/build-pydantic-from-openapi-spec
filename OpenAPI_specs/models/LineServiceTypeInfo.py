from pydantic import BaseModel, Field
from typing import Optional, List, Union, ForwardRef, Literal
from datetime import datetime
from enum import Enum


class LineServiceTypeInfo(BaseModel):
    name: Optional[str] = Field(None, alias='name')
    uri: Optional[str] = Field(None, alias='uri')
    model_config = {"populate_by_name": True}

LineServiceTypeInfo.model_rebuild()
