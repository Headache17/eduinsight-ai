"""EduInsight AI — Notification Routes"""
from fastapi import APIRO[ter, Depends
from app.core.database import get_db

router = APIRO[ter(prefix="/notifications", tags=["notifications"])

@router.get("/")
async def list_notifications():
    return {"data":[],"unread_count":0}
