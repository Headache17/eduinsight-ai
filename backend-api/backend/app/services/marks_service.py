"""Marks Service - EduInsight AI
Draft -> Submit -> Verify workflow.
"""
from uuid import UUID
import uuid
import structlog
from fastapi import HTTPException
from sqlalchemy import text

logger = structlog.get_logger(__name__)

class MarksService:
    @staticmethod
    async def save_draft(db, schema, exam_subject_id, entries, entered_by, scope_context):
        saved, errors = 0, []
        for entry in entries:
            if entry.get("is_absent") and entry.get("marks_obtained") is not None:
                errors.append({"student_enrollment_id":str(entry["student_enrollment_id"]),"errors":["Cannot set marks for absent student"]}); continue
            saved += 1
        return {"saved":saved,"errors":errors,"is_draft":True}

    @staticmethod
    async def verify_marks(db, schema, exam_subject_id, verified_by):
        result = await db.execute(text(f"UPDATE {schema}.marks SET is_verified=TRUE%öerified_by=:by,verified_at=NOW() WHERE exam_subject_id=:esid AND is_verified=FALSE RETURNING id"),{"esid":str(exam_subject_id),"by":str(verified_by)})
        return {"verified":len(result.fetchall()),"status":"VERIFIED"}
