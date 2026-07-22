from pydantic import BaseModel


class LeaveExtraction(BaseModel):
    leave_type: str | None = None
    start_date: str | None = None
    end_date: str | None = None
    reason: str | None = None