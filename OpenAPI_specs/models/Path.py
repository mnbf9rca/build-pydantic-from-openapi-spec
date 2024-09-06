from pydantic import BaseModel, Field
from .Identifier import Identifier
from .JpElevation import JpElevation
from typing import List
from typing import Optional


class Path(BaseModel):
    lineString: Optional[str] = Field(None, alias='lineString')
    stopPoints: Optional[List[Identifier]] = Field(None, alias='stopPoints')
    elevation: Optional[List[JpElevation]] = Field(None, alias='elevation')

    class Config:
        from_attributes = True
