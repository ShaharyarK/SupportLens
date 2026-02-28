from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.database import engine, Base
from app.api.routers import chat, traces, analytics, export

# Create all DB tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.PROJECT_NAME)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat.router, prefix="/api", tags=["Chat"])
app.include_router(traces.router, prefix="/api", tags=["Traces"])
app.include_router(analytics.router, prefix="/api", tags=["Analytics"])
app.include_router(export.router, prefix="/api", tags=["Export"])
