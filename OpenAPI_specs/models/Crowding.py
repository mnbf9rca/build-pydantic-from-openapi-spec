from pydantic import BaseModel, Field
from typing import Optional, List, Union, ForwardRef, Literal
from datetime import datetime
from enum import Enum

from PassengerFlow import PassengerFlow
from TrainLoading import TrainLoading

class Crowding(BaseModel):
    passenger_flows: Optional[List[PassengerFlow]] = Field(None, alias='passengerFlows')
    train_loadings: Optional[List[TrainLoading]] = Field(None, alias='trainLoadings')
    model_config = {"populate_by_name": True}

Crowding.model_rebuild()
