"""
EduInsight AI — AI Service
API bridge to the intelligence pipeline: retrieve cached insights, trigger refresh.
"""

from __future__ import annotations
import structlog
from fastapi import HTTPException
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Any, Dict, List, Optional
from uuid import UUID

logger = structlog.get_logger(__name__)

class AIService:
    @staticmethod
    async def get_student_risk_score(db: AsyncSession, schema: str, student_id: UUID) -> Dict:
        result = await db.execute(text(f"SELECT srs.*, s.full_name FROM {schema}.student_risk_scores srs JOIN {schema}.students s ON srs.student_id=s.id WHERE srs.student_id=:sid ORDER BY srs.computed_at DESC LIMIT 1"),{"sid":str(student_id)})
        row = result.fetchone()
        if not row: return {"student_id":str(student_id),"risk_level":"UNKNOWN","overall_risk_score":None}
        return dict(row._mapping)

    @staticmethod
    async def get_student_insights(db: AsyncSession, schema: str, student_id: UUID, insight_type: Optional[str]=None) -> List[Dict]:
        where = "student_id=:sid AND is_dismissed=FALSE"
        params: Dict[str,Any] = {"sid":str(student_id)}
        if insight_type: where+=" AND insight_type=:type"; params["type"]=insight_type
        result = await db.execute(text(f"SELECT id,insight_type,insight_text,confidence_score,generated_at FROM {schema}.ai_insights WHERE {where} ORDER BY generated_at DESC"),params)
        return [dict(r._mapping) for r in result.fetchall()]

    @staticmethod
    async def trigger_insight_refresh(redis_client, schema: str, student_id: UUID, tenant_id: str) -> Dict:
        rate_key = f"insight_refresh:{tenant_id}:{student_id}"
        if await redis_client.get(rate_key):
            raise HTTPException(429,"Insights can only be refreshed once per hour per student")
        await redis_client.setex(rate_key,3600,"1")
        return {"message":"Insight regeneration queued","student_id":str(student_id)}
