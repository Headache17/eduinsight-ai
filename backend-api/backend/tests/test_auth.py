"""EduInsight AI — Auth Tests"""
import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_login_missing_tenant_header():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/v1/auth/login", json={"email":"test@test.com","password":"test"})
        assert response.status_code == 400

@pytest.mark.asyncio
async def test_login_invalid_credentials():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/v1/auth/login", headers={"X-Tenant-ID":"11111111-1111-1111-1111-111111111111"},json={"email":"bad@test.com","password":"wrong"})
        assert response.status_code == 401
