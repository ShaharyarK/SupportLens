from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel


class TraceCreate(BaseModel):
    user_message: str
    bot_response: str


class TraceOut(BaseModel):
    id: str
    user_message: str
    bot_response: str
    category: str
    timestamp: datetime
    response_time_ms: int

    class Config:
        from_attributes = True


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    response: str


class CategoryStat(BaseModel):
    category: str
    count: int
    percentage: float


class AnalyticsOut(BaseModel):
    total_traces: int
    category_breakdown: List[CategoryStat]
    average_response_time_ms: float
