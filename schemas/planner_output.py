from typing import Literal
from pydantic import BaseModel


class PlannerOutput(BaseModel):
    action: Literal["tool", "clarify", "respond"]
    message: str