from fastapi.responses import PlainTextResponse
import time
import uuid
from typing import List, Optional
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import func
from pydantic import BaseModel
from datetime import datetime

import models
import database
from llm import generate_chatbot_response, classify_trace

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="SupportLens API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    response: str


class TraceOut(BaseModel):
    id: str
    user_message: str
    bot_response: str
    category: str
    timestamp: datetime
    response_time_ms: int

    class Config:
        from_attributes = True


class TraceCreate(BaseModel):
    user_message: str
    bot_response: str


class CategoryStat(BaseModel):
    category: str
    count: int
    percentage: float


class AnalyticsOut(BaseModel):
    total_traces: int
    category_breakdown: List[CategoryStat]
    average_response_time_ms: float


@app.post("/api/chat", response_model=ChatResponse)
def chat_endpoint(request: ChatRequest, db: Session = Depends(database.get_db)):
    start_time = time.time()

    # 1. Generate Response
    bot_response = generate_chatbot_response(request.message)
    response_time_ms = int((time.time() - start_time) * 1000)

    # 2. Classify Trace
    category = classify_trace(request.message, bot_response)

    # 3. Save Trace
    new_trace = models.Trace(
        id=str(uuid.uuid4()),
        user_message=request.message,
        bot_response=bot_response,
        category=category,
        response_time_ms=response_time_ms
    )
    db.add(new_trace)
    db.commit()

    return ChatResponse(response=bot_response)


@app.post("/api/traces", response_model=TraceOut)
def record_trace(trace: TraceCreate, db: Session = Depends(database.get_db)):
    """
    Endpoint explicitly requested in requirements if the chatbot logic is separate.
    Receives a trace, classifies it, saves it, and returns it.
    """
    start_time = time.time()

    category = classify_trace(trace.user_message, trace.bot_response)
    response_time_ms = int((time.time() - start_time) * 1000)

    new_trace = models.Trace(
        id=str(uuid.uuid4()),
        user_message=trace.user_message,
        bot_response=trace.bot_response,
        category=category,
        response_time_ms=response_time_ms
    )
    db.add(new_trace)
    db.commit()
    db.refresh(new_trace)

    return new_trace


@app.get("/api/traces", response_model=List[TraceOut])
def get_traces(category: Optional[str] = None, db: Session = Depends(database.get_db)):
    query = db.query(models.Trace)
    if category:
        query = query.filter(models.Trace.category == category)
    return query.order_by(models.Trace.timestamp.desc()).all()


@app.get("/api/analytics", response_model=AnalyticsOut)
def get_analytics(db: Session = Depends(database.get_db)):
    total = db.query(models.Trace).count()
    if total == 0:
        return AnalyticsOut(total_traces=0, category_breakdown=[], average_response_time_ms=0.0)

    avg_time = db.query(
        func.avg(models.Trace.response_time_ms)).scalar() or 0.0

    breakdown = []
    category_counts = db.query(models.Trace.category, func.count(
        models.Trace.id)).group_by(models.Trace.category).all()
    for cat, count in category_counts:
        # Convert Enum to str if needed
        cat_name = cat.value if isinstance(
            cat, models.TraceCategory) else str(cat)
        breakdown.append(CategoryStat(
            category=cat_name,
            count=count,
            percentage=round((count / total) * 100, 2)
        ))

    return AnalyticsOut(
        total_traces=total,
        category_breakdown=breakdown,
        average_response_time_ms=round(avg_time, 2)
    )


@app.get("/api/export", response_class=PlainTextResponse)
def export_traces_csv(db: Session = Depends(database.get_db)):
    traces = db.query(models.Trace).order_by(
        models.Trace.timestamp.desc()).all()
    csv_content = "id,timestamp,category,response_time_ms,user_message,bot_response\n"
    for t in traces:
        # Replace newlines and commas to keep CSV safe
        user_msg = t.user_message.replace('"', '""').replace('\n', ' ')
        bot_msg = t.bot_response.replace('"', '""').replace('\n', ' ')
        cat_name = t.category.value if isinstance(
            t.category, models.TraceCategory) else str(t.category)
        csv_content += f'"{t.id}","{t.timestamp}","{cat_name}",{t.response_time_ms},"{user_msg}","{bot_msg}"\n'
    return csv_content
