"""EduInsight AI — Marks Routes"""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db

router = APIRouter(prefix="/marks", tags=["marks"])

@router.post("/draft")
async def save_draft(db: AsyncSession = Depends(get_db)):
    return {"status":"draft_saved"}

@router.post("/submit")
async def submit_marks(db: AsyncSession = Depends(get_db)):
    return {"status":"submitted"}

@router.post("/verify")
async def verify_marks(db: AsyncSession = Depends(get_db)):
    return {"status":"verified"}
