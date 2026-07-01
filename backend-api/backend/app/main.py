"""EduInsight AI — FastAPI Application Factory"""
import time
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.v1.routes import auth, students, marks, attendance, analytics, notifications, academic

app = FastAPI(
    title="EduInsight AI API",
    version="1.0.0",
    docs_url="/v1/docs",
    redoc_url="/v1/redoc",
    openapi_url="/v1/openapi.json",
)

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

@app.get("/v1/health")
async def health(): return {"status":"healthy","version":"1.0.0"}

app.include_router(auth.router, prefix="/v1")
app.include_router(students.router, prefix="/v1")
app.include_router(marks.router, prefix="/v1")
app.include_router(attendance.router, prefix="/v1")
app.include_router(analytics.router, prefix="/v1")
app.include_router(notifications.router, prefix="/v1")
app.include_router(academic.router, prefix="/v1")
