"""EduInsight AI — Public Schema Tables
Tenants, subscriptions, global config.
"""
from sqlalchemy import Column, String, Text, Integer, Boolean, DateTime, Date, Numeric, JSON
from sqlalchemy.dialects.postgresql import UUID, INET, JSONB
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Tenant(Base):
    __tablename__ = "tenants"
    __table_args__ = {"schema": "public"}

    id = Column(UUID(as_uuid=True), primary_key=True)
    name = Column(String(200), nullable=False)
    slug = Column(String(100), nullable=False, unique=True)
    schema_name = Column(String(100), nullable=False)
    status = Column(String(20), default="TRIAL")
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
