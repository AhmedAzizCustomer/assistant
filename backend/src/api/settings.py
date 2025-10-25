"""Settings and configuration API endpoints."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Dict, Any, List, Optional
from datetime import datetime
from pydantic import BaseModel

from ..storage.database import get_db
from ..storage.settings_model import Settings, SystemStatus
from ..core.encryption import encryptor

router = APIRouter()


class SettingCreate(BaseModel):
    """Setting creation schema."""
    key: str
    value: str
    category: str
    is_encrypted: bool = True


class SettingResponse(BaseModel):
    """Setting response schema."""
    key: str
    value: str
    category: str
    description: Optional[str]

    class Config:
        from_attributes = True


class BulkSettingsUpdate(BaseModel):
    """Bulk settings update schema."""
    settings: Dict[str, Any]


@router.get("/status")
async def get_system_status(db: Session = Depends(get_db)):
    """Check if system is configured."""
    status = db.query(SystemStatus).first()
    if not status:
        status = SystemStatus(is_configured=False)
        db.add(status)
        db.commit()

    # Check if we have essential settings
    anthropic_key = db.query(Settings).filter(Settings.key == "anthropic_api_key").first()
    openai_key = db.query(Settings).filter(Settings.key == "openai_api_key").first()

    has_ai_keys = bool(anthropic_key or openai_key)

    return {
        "is_configured": status.is_configured and has_ai_keys,
        "setup_completed": status.setup_completed_at.isoformat() if status.setup_completed_at else None,
        "version": status.version,
        "has_ai_keys": has_ai_keys
    }


@router.get("/", response_model=List[SettingResponse])
async def get_all_settings(
    category: Optional[str] = None,
    include_encrypted: bool = False,
    db: Session = Depends(get_db)
):
    """Get all settings (encrypted values are masked unless specified)."""
    query = db.query(Settings)

    if category:
        query = query.filter(Settings.category == category)

    settings = query.all()

    result = []
    for setting in settings:
        value = setting.value
        if setting.is_encrypted and value:
            if include_encrypted:
                try:
                    value = encryptor.decrypt(value)
                except Exception:
                    value = "***ENCRYPTED***"
            else:
                value = "***HIDDEN***"

        result.append(SettingResponse(
            key=setting.key,
            value=value,
            category=setting.category,
            description=setting.description
        ))

    return result


@router.get("/{key}")
async def get_setting(key: str, decrypt: bool = True, db: Session = Depends(get_db)):
    """Get a specific setting."""
    setting = db.query(Settings).filter(Settings.key == key).first()

    if not setting:
        raise HTTPException(status_code=404, detail="Setting not found")

    value = setting.value
    if setting.is_encrypted and decrypt and value:
        try:
            value = encryptor.decrypt(value)
        except Exception:
            pass

    return {
        "key": setting.key,
        "value": value,
        "category": setting.category,
        "is_encrypted": setting.is_encrypted
    }


@router.post("/")
async def create_or_update_setting(
    setting: SettingCreate,
    db: Session = Depends(get_db)
):
    """Create or update a setting."""
    existing = db.query(Settings).filter(Settings.key == setting.key).first()

    value = setting.value
    if setting.is_encrypted and value:
        value = encryptor.encrypt(value)

    if existing:
        existing.value = value
        existing.category = setting.category
        existing.is_encrypted = setting.is_encrypted
        db.commit()
        return {"message": "Setting updated", "key": setting.key}
    else:
        new_setting = Settings(
            key=setting.key,
            value=value,
            category=setting.category,
            is_encrypted=setting.is_encrypted
        )
        db.add(new_setting)
        db.commit()
        return {"message": "Setting created", "key": setting.key}


@router.post("/bulk")
async def update_settings_bulk(
    data: BulkSettingsUpdate,
    db: Session = Depends(get_db)
):
    """Update multiple settings at once."""
    updated = []

    # Define which settings should be encrypted
    encrypted_keys = {
        "anthropic_api_key", "openai_api_key",
        "gmail_client_secret", "outlook_client_secret",
        "google_calendar_client_secret", "database_url",
        "secret_key"
    }

    # Category mapping
    category_map = {
        "anthropic_api_key": "ai",
        "openai_api_key": "ai",
        "claude_model": "ai",
        "openai_model": "ai",
        "default_ai_provider": "ai",
        "gmail_client_id": "email",
        "gmail_client_secret": "email",
        "outlook_client_id": "email",
        "outlook_client_secret": "email",
        "google_calendar_client_id": "calendar",
        "google_calendar_client_secret": "calendar",
        "database_url": "database",
        "secret_key": "app",
        "environment": "app"
    }

    for key, value in data.settings.items():
        if not value:  # Skip empty values
            continue

        is_encrypted = key in encrypted_keys
        category = category_map.get(key, "other")

        existing = db.query(Settings).filter(Settings.key == key).first()

        encrypted_value = encryptor.encrypt(str(value)) if is_encrypted else str(value)

        if existing:
            existing.value = encrypted_value
            existing.category = category
            existing.is_encrypted = is_encrypted
        else:
            new_setting = Settings(
                key=key,
                value=encrypted_value,
                category=category,
                is_encrypted=is_encrypted
            )
            db.add(new_setting)

        updated.append(key)

    # Mark system as configured
    status = db.query(SystemStatus).first()
    if not status:
        status = SystemStatus()
        db.add(status)

    status.is_configured = True
    status.setup_completed_at = datetime.utcnow()

    db.commit()

    return {
        "message": "Settings updated successfully",
        "updated_keys": updated,
        "count": len(updated)
    }


@router.delete("/{key}")
async def delete_setting(key: str, db: Session = Depends(get_db)):
    """Delete a setting."""
    setting = db.query(Settings).filter(Settings.key == key).first()

    if not setting:
        raise HTTPException(status_code=404, detail="Setting not found")

    db.delete(setting)
    db.commit()

    return {"message": "Setting deleted", "key": key}


@router.post("/test-ai")
async def test_ai_connection(db: Session = Depends(get_db)):
    """Test AI API connection."""
    from ..core.ai_engine import AIEngine

    try:
        # Get API keys from database
        anthropic_key = db.query(Settings).filter(Settings.key == "anthropic_api_key").first()
        openai_key = db.query(Settings).filter(Settings.key == "openai_api_key").first()

        if not anthropic_key and not openai_key:
            return {"success": False, "message": "No AI API keys configured"}

        # Try to initialize AI engine
        ai = AIEngine()
        test_response = await ai.generate_response(
            "Say 'Hello' in one word.",
            max_tokens=10
        )

        return {
            "success": True,
            "message": "AI connection successful",
            "response": test_response
        }

    except Exception as e:
        return {
            "success": False,
            "message": f"AI connection failed: {str(e)}"
        }
