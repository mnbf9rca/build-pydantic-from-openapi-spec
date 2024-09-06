from pydantic import BaseModel, Field
from .Crowding import Crowding
from .RouteTypeEnum import RouteTypeEnum
from .StatusEnum import StatusEnum
from typing import Optional


class Identifier(BaseModel):
    id: Optional[str] = Field(None, alias='id')
    name: Optional[str] = Field(None, alias='name')
    uri: Optional[str] = Field(None, alias='uri')
    fullName: Optional[str] = Field(None, alias='fullName')
    type: Optional[str] = Field(None, alias='type')
    crowding: Optional[Crowding] = Field(None, alias='crowding')
    routeType: Optional[RouteTypeEnum] = Field(None, alias='routeType')
    status: Optional[StatusEnum] = Field(None, alias='status')

    class Config:
        from_attributes = True
