"""Settings storage model."""
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime
from sqlalchemy.sql import func
from .database import Base


class Settings(Base):
    """Application settings and credentials storage."""
    __tablename__ = "settings"

    id = Column(Integer, primary_key=True, index=True)
    key = Column(String, unique=True, nullable=False, index=True)
    value = Column(Text)
    is_encrypted = Column(Boolean, default=True)
    category = Column(String)  # ai, email, calendar, database
    description = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class SystemStatus(Base):
    """Track system configuration status."""
    __tablename__ = "system_status"

    id = Column(Integer, primary_key=True, index=True)
    is_configured = Column(Boolean, default=False)
    setup_completed_at = Column(DateTime(timezone=True))
    version = Column(String, default="1.0.0")
