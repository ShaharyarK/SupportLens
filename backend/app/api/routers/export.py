from fastapi import APIRouter, Depends
from fastapi.responses import PlainTextResponse
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.models.trace import Trace, TraceCategory

router = APIRouter()


@router.get("/export", response_class=PlainTextResponse)
def export_traces_csv(db: Session = Depends(get_db)):
    traces = db.query(Trace).order_by(Trace.timestamp.desc()).all()
    csv_content = "id,timestamp,category,response_time_ms,user_message,bot_response\n"
    for t in traces:
        user_msg = t.user_message.replace('"', '""').replace('\n', ' ')
        bot_msg = t.bot_response.replace('"', '""').replace('\n', ' ')
        cat_name = t.category.value if isinstance(
            t.category, TraceCategory) else str(t.category)
        csv_content += f'"{t.id}","{t.timestamp}","{cat_name}",{t.response_time_ms},"{user_msg}","{bot_msg}"\n'
    return csv_content
