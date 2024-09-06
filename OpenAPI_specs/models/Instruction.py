from pydantic import BaseModel, Field
from .InstructionStep import InstructionStep
from typing import List
from typing import Optional


class Instruction(BaseModel):
    summary: Optional[str] = Field(None, alias='summary')
    detailed: Optional[str] = Field(None, alias='detailed')
    steps: Optional[List[InstructionStep]] = Field(None, alias='steps')

    class Config:
        from_attributes = True
