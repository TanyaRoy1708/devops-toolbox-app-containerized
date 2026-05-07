from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ToolUsageLogBase(BaseModel):
    tool_name: str
    action: Optional[str] = None

class ToolUsageLogCreate(ToolUsageLogBase):
    pass

class ToolUsageLog(ToolUsageLogBase):
    id: int
    timestamp: datetime

    class Config:
        from_attributes = True
