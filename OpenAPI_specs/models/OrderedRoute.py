from pydantic import BaseModel, Field
from typing import Optional, List, Union, ForwardRef, Literal
from datetime import datetime
from enum import Enum


class OrderedRoute(BaseModel):
    name: Optional[str] = Field(None, alias='name')
    naptan_ids: Optional[List[str]] = Field(None, alias='naptanIds')
    service_type: Optional[str] = Field(None, alias='serviceType')
    model_config = {"populate_by_name": True}

OrderedRoute.model_rebuild()
