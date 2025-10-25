"""Calendar integration API endpoints."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta
from pydantic import BaseModel

from ..storage.database import get_db
from ..storage.models import CalendarAccount, Event
from ..integrations.google_calendar import GoogleCalendarService
from ..integrations.outlook_calendar import OutlookCalendarService

router = APIRouter()


class CalendarAccountCreate(BaseModel):
    """Calendar account creation schema."""
    calendar_name: str
    provider: str  # google or outlook


class EventCreateFromCalendar(BaseModel):
    """Event creation from calendar schema."""
    calendar_id: str
    title: str
    start_time: datetime
    end_time: Optional[datetime] = None
    description: Optional[str] = None
    location: Optional[str] = None
    attendees: Optional[List[str]] = None


@router.get("/accounts")
async def get_calendar_accounts(db: Session = Depends(get_db)):
    """Get all connected calendar accounts."""
    accounts = db.query(CalendarAccount).filter(CalendarAccount.is_active == True).all()
    return accounts


@router.post("/accounts/connect")
async def connect_calendar_account(
    account: CalendarAccountCreate,
    db: Session = Depends(get_db)
):
    """
    Connect a new calendar account.
    This would redirect to OAuth flow for Google/Outlook Calendar.
    """
    # Create account record
    db_account = CalendarAccount(
        user_id=1,  # TODO: Get from authenticated user
        calendar_name=account.calendar_name,
        provider=account.provider,
        calendar_id="",  # Will be set after OAuth
        is_active=False
    )
    db.add(db_account)
    db.commit()
    db.refresh(db_account)

    return {
        "account_id": db_account.id,
        "message": f"Calendar account created. Please complete OAuth flow for {account.provider}.",
        "oauth_url": f"/api/calendar/oauth/{account.provider}/authorize?account_id={db_account.id}"
    }


@router.get("/events")
async def get_calendar_events(
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    account_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """Get calendar events from connected accounts."""
    # Default to next 7 days if not specified
    if not start_date:
        start_date = datetime.utcnow()
    if not end_date:
        end_date = start_date + timedelta(days=7)

    if account_id:
        account = db.query(CalendarAccount).filter(CalendarAccount.id == account_id).first()
        if not account:
            raise HTTPException(status_code=404, detail="Calendar account not found")
        accounts = [account]
    else:
        accounts = db.query(CalendarAccount).filter(
            CalendarAccount.is_active == True,
            CalendarAccount.sync_enabled == True
        ).all()

    all_events = []
    for account in accounts:
        if account.provider == "google":
            service = GoogleCalendarService(account)
            events = await service.get_events(start_date, end_date)
            all_events.extend(events)
        elif account.provider == "outlook":
            service = OutlookCalendarService(account)
            events = await service.get_events(start_date, end_date)
            all_events.extend(events)

    return {"events": all_events, "total": len(all_events)}


@router.post("/events")
async def create_calendar_event(
    event: EventCreateFromCalendar,
    account_id: int,
    db: Session = Depends(get_db)
):
    """Create a new calendar event."""
    account = db.query(CalendarAccount).filter(CalendarAccount.id == account_id).first()
    if not account:
        raise HTTPException(status_code=404, detail="Calendar account not found")

    if account.provider == "google":
        service = GoogleCalendarService(account)
        created_event = await service.create_event(event.model_dump())
    elif account.provider == "outlook":
        service = OutlookCalendarService(account)
        created_event = await service.create_event(event.model_dump())
    else:
        raise HTTPException(status_code=400, detail="Unsupported calendar provider")

    # Also save to local database
    db_event = Event(
        user_id=1,  # TODO: Get from authenticated user
        title=event.title,
        start_time=event.start_time,
        end_time=event.end_time,
        description=event.description,
        location=event.location,
        external_id=created_event.get("id"),
        source=account.provider
    )
    db.add(db_event)
    db.commit()

    return {"message": "Event created successfully", "event": created_event}


@router.post("/sync")
async def sync_calendars(db: Session = Depends(get_db)):
    """Sync all connected calendars."""
    accounts = db.query(CalendarAccount).filter(
        CalendarAccount.is_active == True,
        CalendarAccount.sync_enabled == True
    ).all()

    synced_count = 0
    for account in accounts:
        try:
            if account.provider == "google":
                service = GoogleCalendarService(account)
                await service.sync()
            elif account.provider == "outlook":
                service = OutlookCalendarService(account)
                await service.sync()

            account.last_sync = datetime.utcnow()
            synced_count += 1
        except Exception as e:
            print(f"Error syncing calendar {account.id}: {e}")

    db.commit()

    return {
        "message": "Calendar sync completed",
        "synced_accounts": synced_count
    }


@router.get("/availability")
async def check_availability(
    start_time: datetime,
    end_time: datetime,
    db: Session = Depends(get_db)
):
    """Check availability for a time slot."""
    # Get events in the time range
    events = db.query(Event).filter(
        Event.start_time < end_time,
        Event.end_time > start_time
    ).all()

    is_available = len(events) == 0

    return {
        "is_available": is_available,
        "conflicting_events": [
            {
                "title": e.title,
                "start": e.start_time,
                "end": e.end_time
            }
            for e in events
        ]
    }


@router.post("/find-time")
async def find_available_time(
    duration_minutes: int,
    start_search: datetime,
    end_search: datetime,
    db: Session = Depends(get_db)
):
    """Find available time slots for a meeting."""
    # Get all events in the search range
    events = db.query(Event).filter(
        Event.start_time >= start_search,
        Event.start_time <= end_search
    ).order_by(Event.start_time).all()

    # Find gaps
    available_slots = []
    current_time = start_search

    for event in events:
        # Check if there's a gap before this event
        gap_duration = (event.start_time - current_time).total_seconds() / 60
        if gap_duration >= duration_minutes:
            available_slots.append({
                "start": current_time,
                "end": current_time + timedelta(minutes=duration_minutes)
            })

        # Move current time to after this event
        if event.end_time:
            current_time = max(current_time, event.end_time)

    # Check if there's time after the last event
    gap_duration = (end_search - current_time).total_seconds() / 60
    if gap_duration >= duration_minutes:
        available_slots.append({
            "start": current_time,
            "end": current_time + timedelta(minutes=duration_minutes)
        })

    return {
        "available_slots": available_slots[:5],  # Return top 5
        "total_found": len(available_slots)
    }
