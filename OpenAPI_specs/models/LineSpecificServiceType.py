from pydantic import BaseModel, Field
from .LineServiceTypeInfo import LineServiceTypeInfo
from typing import Optional


class LineSpecificServiceType(BaseModel):
    serviceType: Optional[LineServiceTypeInfo] = Field(None, alias='serviceType')
    stopServesServiceType: Optional[bool] = Field(None, alias='stopServesServiceType')

    class Config:
        from_attributes = True
