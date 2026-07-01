"""Student Service - EduInsight AI"""
import uuid
from typing import Any, Dict, List, Optional, Tuple
from uuid import UUID
import structlog
from fastapi import HTTPException, status
from sqlalchemy import text

logger = structlog.get_logger(__name__)

class StudentService:
    @staticmethod
    async def create_student(db, schema, data, created_by):
        student_id = uuid.uuid4()
        await db.execute(text(f"INSERT INTO {schema}.students (id,first_name,last_name,date_of_birth,gender,status,created_by) VALUES (:id,:first_name,:last_name,:dob,:gender,'ACTIVE',:by)"),{"id":str(student_id),"first_name":data["first_name"],"last_name":data["last_name"],"dob":data["date_of_birth"],"gender":data["gender"],"by":str(created_by)})
        return {"id":str(student_id),**data}

    @staticmethod
    async def list_students(db, schema, scope_context, user_role, page=1, page_size=25):
        result = await db.execute(text(f"SELECT id,full_name,student_code FROM {schema}.students WHERE deleted_at IS NULL LIMIT":{page_size}"),{"page_size":page_size})
        return [dict(r._mapping) for r in result.fetchall()], 0
