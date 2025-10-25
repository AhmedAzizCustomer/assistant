"""Events tracking API endpoints."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel

from ..storage.database import get_db
from ..storage.models import Event

router = APIRouter()


class EventCreate(BaseModel):
    """Event creation schema."""
    title: str
    description: Optional[str] = None
    location: Optional[str] = None
    start_time: datetime
    end_time: Optional[datetime] = None
    event_type: Optional[str] = None
    attendees: Optional[List[dict]] = None
    reminders: Optional[List[dict]] = None
    is_all_day: bool = False


class EventUpdate(BaseModel):
    """Event update schema."""
    title: Optional[str] = None
    description: Optional[str] = None
    location: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    event_type: Optional[str] = None
    attendees: Optional[List[dict]] = None
    reminders: Optional[List[dict]] = None


class EventResponse(BaseModel):
    """Event response schema."""
    id: int
    title: str
    description: Optional[str]
    location: Optional[str]
    start_time: datetime
    end_time: Optional[datetime]
    event_type: Optional[str]
    is_all_day: bool

    class Config:
        from_attributes = True


@router.get("/", response_model=List[EventResponse])
async def get_events(
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    event_type: Optional[str] = None,
    db: Session = Depends(get_db),
):
    """Get events with optional filters."""
    query = db.query(Event)

    if start_date:
        query = query.filter(Event.start_time >= start_date)
    if end_date:
        query = query.filter(Event.start_time <= end_date)
    if event_type:
        query = query.filter(Event.event_type == event_type)

    return query.order_by(Event.start_time).all()


@router.get("/{event_id}", response_model=EventResponse)
async def get_event(event_id: int, db: Session = Depends(get_db)):
    """Get a specific event."""
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event


@router.post("/", response_model=EventResponse)
async def create_event(event: EventCreate, db: Session = Depends(get_db)):
    """Create a new event."""
    db_event = Event(
        user_id=1,  # TODO: Get from authenticated user
        **event.model_dump()
    )
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event


@router.put("/{event_id}", response_model=EventResponse)
async def update_event(
    event_id: int,
    event_update: EventUpdate,
    db: Session = Depends(get_db)
):
    """Update an event."""
    db_event = db.query(Event).filter(Event.id == event_id).first()
    if not db_event:
        raise HTTPException(status_code=404, detail="Event not found")

    update_data = event_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_event, field, value)

    db.commit()
    db.refresh(db_event)
    return db_event


@router.delete("/{event_id}")
async def delete_event(event_id: int, db: Session = Depends(get_db)):
    """Delete an event."""
    db_event = db.query(Event).filter(Event.id == event_id).first()
    if not db_event:
        raise HTTPException(status_code=404, detail="Event not found")

    db.delete(db_event)
    db.commit()
    return {"message": "Event deleted successfully"}


@router.get("/upcoming/next")
async def get_upcoming_events(limit: int = 5, db: Session = Depends(get_db)):
    """Get upcoming events."""
    events = db.query(Event).filter(
        Event.start_time >= datetime.utcnow()
    ).order_by(Event.start_time).limit(limit).all()

    return events
