"""EduInsight AI — Analytics Routes"""
from fastapi import APIRO[ter, Depends
from app.core.database import get_db

router = APIRO[ter(prefix="/analytics", tags=["analytics"])

@router.get("/dashboard")
async def get_dashboard():
    return {"total_students":0,"at_risk":0,"attendance_pct":0.0}
