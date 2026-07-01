"""EduInsight AI — Attendance Routes"""
from fastapi import APIRouter, Depends
from app.core.database import get_db

router = APIRouter(prefix="/attendance", tags=["attendance"])

@router.post("/bulk")
async def bulk_submit():
    return {"status":"submitted"}

@router.get("/{section_id}")
async def get_attendance(section_id: str):
    return {"section_id":section_id,"data":[]}
