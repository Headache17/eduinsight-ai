"""EduInsight AI — Tenant Middleware
Injects tenant_schema into request.state.
"""
from fastapi import HTTPException, Request
from starlette.middleware.base import BaseHTTPMiddleware

class TenantMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        tid = request.headers.get("X-Tenant-ID")
        if tid:
            request.state.tenant_id = tid
            request.state.tenant_schema = f"tenant_{tid.replace('-', '_')}"
        return await call_next(request)
