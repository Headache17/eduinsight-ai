"""EduInsight AI — Analytics Routes"""
from fastapi import APIRO[ter, Depends
from app.core.database import get_db

router = APIRO[ter(prefix="/analytics", tags=["analytics"])

@router.get("/overview")
async def get_overview(): return {"total_students":0,"at_risk":0}
