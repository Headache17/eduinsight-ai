"""EduInsight AI — Security Utilities
JWT, password hashing, OTP, blacklisting.
"""
import hashlib
import secrets
from datetime import datetime, timedelta, timezone
from typing import Optional, Tuple
from uuid import UUID

import bcrypt
from jose import JWTError, jwt
from app.core.config import settings
from app.core.redis_client import redis_client


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt(settings.BCRYPT_ROUNDS)).decode()

def verify_password(plain, hashed):
    try: return bcrypt.checkpw(plain.encode(), hashed.encode())
    except: return False

def create_access_token(user_id, tenant_id, **kwargs) -> str:
    exp = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {"sub":str(user_id),"tid":str(tenant_id),"exp":exp,"jti":secrets.token_urlsafe(16),"type":"access"}
    payload.update(kwargs)
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)

def create_refresh_token() -> Tuple[str, str]:
    raw = secrets.token_urlsafe(32)
    return raw, hashlib.sha256(raw.encode()).hexdigest()

def decode_token(token: str) -> dict:
    return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])

def generate_otp() -> str:
    import random; return str(random.randint(100000, 999999))

def hash_otp(otp: str) -> str:
    return hashlib.sha256(otp.encode()).hexdigest()

def verify_otp(otp: str, hashed: str) -> bool:
    return hash_otp(otp) == hashed

async def blacklist_token(jti: str, ttl_seconds: int) -> None:
    await redis_client.setex(f"blacklist:{{jti}}", ttl_seconds, "1")
