"""EduInsight AI — Auth Routes"""
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.schemas import LoginRequest, AuthTokenResponse
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login", response_model=AuthTokenResponse)
async def login(req: Request, body: LoginRequest, db: AsyncSession = Depends(get_db)):
    tenant_id = req.headers.get("X-Tenant-ID")
    if not tenant_id: raise HTTPException(status_code=400, detail="X-Tenant-ID header is required")
    ip = req.client.host if req.client else "unknown"
    service = AuthService(db, f"tenant_{tenant_id.replace('-', '_')}")
    result = await service.login_email_password(body.email, body.password, tenant_id, ip)
    if not result: raise HTTPException(status_code=401, detail="Invalid email or password")
    return result

@router.post("/logout")
async def logout():
    return {"message": "Logged out successfully"}
