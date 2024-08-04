from pydantic import BaseModel, Field
from typing import Optional, List, Union, ForwardRef, Literal
from datetime import datetime
from enum import Enum

from Crowding import Crowding

class Identifier(BaseModel):
    id: Optional[str] = Field(None, alias='id')
    name: Optional[str] = Field(None, alias='name')
    uri: Optional[str] = Field(None, alias='uri')
    full_name: Optional[str] = Field(None, alias='fullName')
    type: Optional[str] = Field(None, alias='type')
    crowding: Optional[Crowding] = Field(None, alias='crowding')
    route_type: Optional[Literal['Unknown', 'All', 'Cycle Superhighways', 'Quietways', 'Cycleways', 'Mini-Hollands', 'Central London Grid', 'Streetspace Route']] = Field(None, alias='routeType')
    status: Optional[Literal['Unknown', 'All', 'Open', 'In Progress', 'Planned', 'Planned - Subject to feasibility and consultation.', 'Not Open']] = Field(None, alias='status')
    model_config = {"populate_by_name": True}

Identifier.model_rebuild()
