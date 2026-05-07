from sqlalchemy import Column, Integer, String, DateTime
from .database import Base
import datetime

class ToolUsageLog(Base):
    __tablename__ = "tool_usage_logs"

    id = Column(Integer, primary_key=True, index=True)
    tool_name = Column(String(50), index=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    action = Column(String(100), nullable=True)
