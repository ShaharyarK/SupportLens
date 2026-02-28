from enum import Enum
from datetime import datetime
from sqlalchemy import Column, String, Integer, DateTime, Enum as SQLEnum
from app.core.database import Base


class TraceCategory(str, Enum):
    BILLING = "Billing"
    REFUND = "Refund"
    ACCOUNT_ACCESS = "Account Access"
    CANCELLATION = "Cancellation"
    GENERAL_INQUIRY = "General Inquiry"


class Trace(Base):
    __tablename__ = "traces"

    id = Column(String, primary_key=True, index=True)
    user_message = Column(String, nullable=False)
    bot_response = Column(String, nullable=False)
    category = Column(SQLEnum(TraceCategory), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    response_time_ms = Column(Integer, nullable=False)
