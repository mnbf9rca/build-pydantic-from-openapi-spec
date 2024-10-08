from pydantic import BaseModel, Field
from pydantic import BaseModel, Field
from typing import Optional


class ActiveServiceType(BaseModel):
    mode: Optional[str] = Field(None, alias='mode')
    serviceType: Optional[str] = Field(None, alias='serviceType')

    class Config:
        from_attributes = True
