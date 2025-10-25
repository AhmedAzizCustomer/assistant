"""Google Calendar integration service."""
from typing import List, Dict, Any
from datetime import datetime
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from ..storage.models import CalendarAccount


class GoogleCalendarService:
    """Service for interacting with Google Calendar API."""

    def __init__(self, calendar_account: CalendarAccount):
        """Initialize Google Calendar service."""
        self.account = calendar_account
        self.service = None

        if calendar_account.access_token:
            credentials = Credentials(
                token=calendar_account.access_token,
                refresh_token=calendar_account.refresh_token,
            )
            self.service = build('calendar', 'v3', credentials=credentials)

    async def get_events(
        self,
        start_date: datetime,
        end_date: datetime
    ) -> List[Dict[str, Any]]:
        """Get calendar events in a date range."""
        if not self.service:
            return []

        try:
            events_result = self.service.events().list(
                calendarId=self.account.calendar_id or 'primary',
                timeMin=start_date.isoformat() + 'Z',
                timeMax=end_date.isoformat() + 'Z',
                singleEvents=True,
                orderBy='startTime'
            ).execute()

            events = events_result.get('items', [])

            event_list = []
            for event in events:
                start = event['start'].get('dateTime', event['start'].get('date'))
                end = event['end'].get('dateTime', event['end'].get('date'))

                event_list.append({
                    'id': event['id'],
                    'title': event.get('summary', 'No Title'),
                    'description': event.get('description', ''),
                    'location': event.get('location', ''),
                    'start': start,
                    'end': end,
                    'attendees': event.get('attendees', []),
                    'source': 'google',
                    'calendar': self.account.calendar_name
                })

            return event_list

        except Exception as e:
            print(f"Error fetching Google Calendar events: {e}")
            return []

    async def create_event(self, event_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new calendar event."""
        if not self.service:
            raise Exception("Google Calendar service not initialized")

        try:
            event = {
                'summary': event_data.get('title'),
                'description': event_data.get('description', ''),
                'location': event_data.get('location', ''),
                'start': {
                    'dateTime': event_data.get('start_time').isoformat(),
                    'timeZone': 'UTC',
                },
                'end': {
                    'dateTime': event_data.get('end_time').isoformat() if event_data.get('end_time') else event_data.get('start_time').isoformat(),
                    'timeZone': 'UTC',
                },
            }

            if event_data.get('attendees'):
                event['attendees'] = [
                    {'email': email} for email in event_data.get('attendees', [])
                ]

            created_event = self.service.events().insert(
                calendarId=self.account.calendar_id or 'primary',
                body=event
            ).execute()

            return created_event

        except Exception as e:
            print(f"Error creating event: {e}")
            raise

    async def update_event(
        self,
        event_id: str,
        event_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Update an existing calendar event."""
        if not self.service:
            raise Exception("Google Calendar service not initialized")

        try:
            # Get existing event
            event = self.service.events().get(
                calendarId=self.account.calendar_id or 'primary',
                eventId=event_id
            ).execute()

            # Update fields
            if 'title' in event_data:
                event['summary'] = event_data['title']
            if 'description' in event_data:
                event['description'] = event_data['description']
            if 'location' in event_data:
                event['location'] = event_data['location']
            if 'start_time' in event_data:
                event['start']['dateTime'] = event_data['start_time'].isoformat()
            if 'end_time' in event_data:
                event['end']['dateTime'] = event_data['end_time'].isoformat()

            updated_event = self.service.events().update(
                calendarId=self.account.calendar_id or 'primary',
                eventId=event_id,
                body=event
            ).execute()

            return updated_event

        except Exception as e:
            print(f"Error updating event: {e}")
            raise

    async def delete_event(self, event_id: str) -> None:
        """Delete a calendar event."""
        if not self.service:
            raise Exception("Google Calendar service not initialized")

        try:
            self.service.events().delete(
                calendarId=self.account.calendar_id or 'primary',
                eventId=event_id
            ).execute()

        except Exception as e:
            print(f"Error deleting event: {e}")
            raise

    async def sync(self) -> None:
        """Sync calendar events."""
        # This would implement incremental sync using sync tokens
        # For simplicity, we'll skip the full implementation
        pass
