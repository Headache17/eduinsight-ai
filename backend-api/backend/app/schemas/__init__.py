"""Pydantic Schemas - EduInsight AI"""
from datetime import date, datetime
from typing import Any, Dict, List, Optional
from uuid import UUID
from pydantic import BaseModel, ConfigDict, EmailStr, Field

class APIModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

class UserSummary(APIModel):
    id: UUID
    full_name: str
    email: str
    roles: List[str] = []
    permissions: List[str] = []
    tenant_id: UUID
    tenant_slug: str
    force_password_reset: bool = False
    mfa_required: bool = False

class AuthTokenResponse(APIModel):
    access_token: str
    refresh_token: str
    token_type: str = "Bearer"
    expires_in: int
    user: UserSummary

class MFAChallengeResponse(APIModel):
    mfa_required: bool = True
    mfa_token: str
    expires_in: int

class DeviceInfo(APIModel):
    browser: Optional[str] = None
    os: Optional[str] = None

class StudentResponse(APIModel):
    id: UUID
    student_code: str
    full_name: str
    status: str

