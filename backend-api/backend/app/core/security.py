"""EduInsight AI — Security Utilities
JWT, password hashing, OTP, blacklisting.
"""
import hashlib
import secrets
from datetime import datetime, timedelta, timezone
from typing import Tuple
import bcrypt
from jose import JWTError, jwt
from app.core.config import settings

def hash_password(p): return bcrypt.hashpw(p.encode(), bcrypt.gensalt(settings.BCRYPT_ROUNDS)).decode()
def verify_password(p, h):
    try: return bcrypt.checkpw(p.encode(), h.encode())
    except: return False
def create_access_token(user_id, tenant_id, **kw):
    exp = datetime.now(timezone.utc)+timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {"sub":str(user_id),"tid":str(tenant_id),"exp":exp,"jti":secrets.token_urlsafe(16),"type":"access",**kw}
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
def create_refresh_token():
    raw = secrets.token_urlsafe(32)
    return raw, hashlib.sha256(raw.encode()).hexdigest()
def decode_token(t): return jwt.decode(t, settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
def generate_otp(): import random; return str(random.randint(100000, 999999))
def hash_otp(o): return hashlib.sha256(o.encode()).hexdigest()
def verify_otp(o, h): return hash_otp(o) == h
async def blacklist_token(j, t):
    from app.core.redis_client import redis_client
    await redis_client.setex(f"blacklist:{j}", t, "1")
async def get_current_user(): return {}
