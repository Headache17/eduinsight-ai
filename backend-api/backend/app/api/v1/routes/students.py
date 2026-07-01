"""EduInsight AI — Student Routes"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db

router = APIRouter(prefix="/students", tags=["students"])

@router.get("/")
async def list_students(page: int = 1, page_size: int = 25, db: AsyncSession = Depends(get_db)):
    return {"data":[],"pagination":{"page":page,"total":0}}

@router.get("/{student_id}")
async def get_student(student_id: str, db: AsyncSession = Depends(get_db)):
    return {"id":student_id}
