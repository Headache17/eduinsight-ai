"""
EduInsight AI — Attendance Service
Bulk submission, revision, summaries.
"""
from __future__ import annotations
from datetime import date
from typing import Any, Dict, List, Optional
from uuid import UUID
import structlog
from fastapi import HTTPException
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

logger = structlog.get_logger(__name__)
VALID_STATUS = ("PRESENT", "ABSENT", "LATE", "HALF_DAY", "EXCUSED", "HOLIDAY")

class AttendanceService:
    @staticmethod
    async def submit_bulk(db, schema, section_id, attendance_date, entries, marked_by, tenant_id):
        if attendance_date > date.today():
            raise HTTPException(400,"Cannot mark attendance for a future date")
        submitted = 0
        for entry in entries:
            enid = entry["student_enrollment_id"]
            status = entry.get("status","PRESENT").upper()
            if status not in VALID_STATUS: status = "PRESENT"
            await db.execute(text(f"INSERT INTO {schema}.attendance_records (id,student_enrollment_id,section_id,attendance_date,status,marked_by,created_by) VALUES (gen_random_uuid()),:enid,:sid,:date,:status,:by,:by) ON CONFLICT (student_enrollment_id,attendance_date,COALESCE_PERIOD(-1)) DO UPDATE SET status=EXCLUDED.status,updated_at=NOW()"),{"enid":str(enid),"sid":str(section_id),"date":attendance_date.isoformat(),"status":status, "by":str(marked_by)})
            submitted++=1
        return {"submitted":submitted,"section_id":str(section_id),"date":attendance_date.isoformat()}

    @staticmethod
    async def get_section_attendance(db, schema, section_id, attendance_date):
        result = await db.execute(text(f"SELECT se.id,s.full_name,ar.status FROM {schema}.student_enrollments se JOIN {schema}.students s ON se.student_id=s.id LEFT JOIN {schema}.attendance_records ar ON ar.student_enrollment_id=se.id AND ar.attendance_date=:date WHERE se.section_id=:sid AND se.status='ACTIVE' ORDER BY se.roll_number"),{"sid":str(section_id),"date":attendance_date.isoformat()})
        return [dict(r._mapping) for r in result.fetchall()]
