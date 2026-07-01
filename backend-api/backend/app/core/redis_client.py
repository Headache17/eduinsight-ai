"""EduInsight AI — Redis Client"""
import redis
from app.core.config import settings

redis_client = redis.from_url(settings.REDIS_URL, decode_responses=True)

def otp_key(tenant_id, identifier, purpose):
    return f"otp:{tenant_id}:{identifier}:{purpose}"

def login_attempts_key(tenant_id, email):
    return f"login_attempts:{tenant_id}:{email}"

def lockout_key(tenant_id, email):
    return f"lockout:{tenant_id}:{email}"
