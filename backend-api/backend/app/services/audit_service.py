"""Audit Service - EduInsight AI"""
import structlog
from sqlalchemy import text
from app.core.database import async_session_factory

logger = structlog.get_logger(__name__)

class AuditService:
    @staticmethod
    async def log_request(tenant_schema, action, http_status, **kwargs):
        if not tenant_schema: return
        try:
            async with async_session_factory() as session:
                await session.execute(text(f"SET search_path TO {tenant_schema}, public"))
                await session.commit()
        except Exception as e:
            logger.error("audit_write_failed", error=str(e))
