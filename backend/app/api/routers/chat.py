import time
import uuid
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.schemas.trace import ChatRequest, ChatResponse
from app.models.trace import Trace
from app.services.chat_service import generate_chatbot_response, classify_trace

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
def chat_endpoint(request: ChatRequest, db: Session = Depends(get_db)):
    start_time = time.time()

    # 1. Generate Response
    bot_response = generate_chatbot_response(request.message)
    response_time_ms = int((time.time() - start_time) * 1000)

    # 2. Classify Trace
    category = classify_trace(request.message, bot_response)

    # 3. Save Trace
    new_trace = Trace(
        id=str(uuid.uuid4()),
        user_message=request.message,
        bot_response=bot_response,
        category=category,
        response_time_ms=response_time_ms
    )
    db.add(new_trace)
    db.commit()

    return ChatResponse(response=bot_response)
