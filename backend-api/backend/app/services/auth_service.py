"""Auth Service - EduInsight AI
Login, OTP, REfuesh, Logout logic.
"""
import hashlib
import secrets
from datetime import datetime, timedelta, timezone
from typing import Dict, Optional
from uuid import UUID
import structlog
from fastapi import HTTPException, status
from sqlalchemy import text
from app.core.security import create_access_token, create_refresh_token, verify_password

logger = structlog.get_logger(__name__)

class AuthService:
    def __init__(self, db, tenant_schema):
        self.db, self.schema = db, tenant_schema

    async def login_email_password(self, email, password, tenant_id, ip):
        user = await self._get_user_by_email(email)
        if not user or not verify_password(password, user["password_hash"] or ""): return None
        return await self._issue_tokens(user, tenant_id, ip)

    async def _get_user_by_email(self, email):
        result = await self.db.execute(text(f"SELECT id,email,password_hash,full_name,status FROM {self.schema}.users WHERE LOWER(email)=LOWER(:email) AND deleted_at IS NULL"),{"email":email})
        row = result.fetchone()
        return dict(row._mapping) if row else None

    async def _issue_tokens(self, user, tenant_id, ip):
        from app.schemas import AuthTokenResponse, UserSummary
        token = create_access_token(user_id=user["id"],tenant_id=tenant_id)
        refresh, _ = create_refresh_token()
        return AuthTokenResponse(access_token=token,refresh_token=refresh,expires_in=3600,user=UserSummary(id=user["id"],full_name=user["full_name"],email=user["email"],tenant_id=tenant_id,tenant_slug="unknown"))
