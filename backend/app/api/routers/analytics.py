from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.api.dependencies import get_db
from app.schemas.trace import AnalyticsOut, CategoryStat
from app.models.trace import Trace, TraceCategory

router = APIRouter()


@router.get("/analytics", response_model=AnalyticsOut)
def get_analytics(db: Session = Depends(get_db)):
    total = db.query(Trace).count()
    if total == 0:
        return AnalyticsOut(total_traces=0, category_breakdown=[], average_response_time_ms=0.0)

    avg_time = db.query(func.avg(Trace.response_time_ms)).scalar() or 0.0

    breakdown = []
    category_counts = db.query(Trace.category, func.count(
        Trace.id)).group_by(Trace.category).all()

    for cat, count in category_counts:
        cat_name = cat.value if isinstance(cat, TraceCategory) else str(cat)
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
