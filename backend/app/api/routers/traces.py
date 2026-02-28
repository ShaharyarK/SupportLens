import time
import uuid
from typing import List, Optional
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.schemas.trace import TraceCreate, TraceOut
from app.models.trace import Trace
from app.services.chat_service import classify_trace

router = APIRouter()


@router.post("/traces", response_model=TraceOut)
def record_trace(trace: TraceCreate, db: Session = Depends(get_db)):
    start_time = time.time()

    category = classify_trace(trace.user_message, trace.bot_response)
    response_time_ms = int((time.time() - start_time) * 1000)

    new_trace = Trace(
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


@router.get("/traces", response_model=List[TraceOut])
def get_traces(category: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(Trace)
    if category:
        query = query.filter(Trace.category == category)
    return query.order_by(Trace.timestamp.desc()).all()
