"""EduInsight AI — Analytics Routes"""
from __future__ import annotations
from typing import Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query, Request
from app.core.database import get_db

router = APIRouter(prefix="/analytics", tags=["analytics"])

@router.get("/overview")
async def get_overview(db=Depends(get_db)):
    return {"total_students":0,"at_risk":0,"attendance_pct":0.0}

@router.get("/students/at-risk")
async def get_at_risk(db=Depends(get_db)):
    return {"total_at_risk":0,"critical":0,"high":0,"students":[]}
