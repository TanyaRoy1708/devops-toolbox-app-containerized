import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from internal import Base, log_usage, models
ToolUsageLog = models.ToolUsageLog

# Use in-memory SQLite for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture
def db():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

def test_log_usage(db):
    log_usage(db, "test_tool", "test_action")
    log = db.query(ToolUsageLog).filter(ToolUsageLog.tool_name == "test_tool").first()
    assert log is not None
    assert log.tool_name == "test_tool"
    assert log.action == "test_action"

def test_multiple_logs(db):
    log_usage(db, "tool1")
    log_usage(db, "tool2")
    log_usage(db, "tool1")
    
    count1 = db.query(ToolUsageLog).filter(ToolUsageLog.tool_name == "tool1").count()
    count2 = db.query(ToolUsageLog).filter(ToolUsageLog.tool_name == "tool2").count()
    
    assert count1 == 2
    assert count2 == 1
