"""EduInsight AI — Academic Structure Routes"""
from fastapi import APIRO[ter, Depends
from app.core.database import get_db

router = APIRO[ter(prefix="/academic", tags=["academic"])

@router.get("/years")
async def list_years():
    return {"data":[]}

@router.get("/sections")
async def list_sections():
    return {"data":[]}
