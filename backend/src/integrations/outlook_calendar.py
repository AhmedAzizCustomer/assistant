"""Outlook Calendar integration service."""
from typing import List, Dict, Any
from datetime import datetime
import requests
from ..storage.models import CalendarAccount


class OutlookCalendarService:
    """Service for interacting with Microsoft Graph API (Outlook Calendar)."""

    def __init__(self, calendar_account: CalendarAccount):
        """Initialize Outlook Calendar service."""
        self.account = calendar_account
        self.access_token = calendar_account.access_token
        self.graph_endpoint = "https://graph.microsoft.com/v1.0"

    def _get_headers(self) -> Dict[str, str]:
        """Get headers for Graph API requests."""
        return {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }

    async def get_events(
        self,
        start_date: datetime,
        end_date: datetime
    ) -> List[Dict[str, Any]]:
        """Get calendar events in a date range."""
        if not self.access_token:
            return []

        try:
            url = f"{self.graph_endpoint}/me/calendar/events"
            params = {
                '$filter': f"start/dateTime ge '{start_date.isoformat()}' and end/dateTime le '{end_date.isoformat()}'",
                '$orderby': 'start/dateTime',
                '$select': 'subject,start,end,location,attendees,bodyPreview'
            }

            response = requests.get(
                url,
                headers=self._get_headers(),
                params=params
            )
            response.raise_for_status()

            events = response.json().get('value', [])

            event_list = []
            for event in events:
                event_list.append({
                    'id': event.get('id'),
                    'title': event.get('subject', 'No Title'),
                    'description': event.get('bodyPreview', ''),
                    'location': event.get('location', {}).get('displayName', ''),
                    'start': event.get('start', {}).get('dateTime'),
                    'end': event.get('end', {}).get('dateTime'),
                    'attendees': [
                        a.get('emailAddress', {}).get('address')
                        for a in event.get('attendees', [])
                    ],
                    'source': 'outlook',
                    'calendar': self.account.calendar_name
                })

            return event_list

        except Exception as e:
            print(f"Error fetching Outlook Calendar events: {e}")
            return []

    async def create_event(self, event_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new calendar event."""
        if not self.access_token:
            raise Exception("Outlook Calendar service not initialized")

        try:
            url = f"{self.graph_endpoint}/me/calendar/events"

            event = {
                'subject': event_data.get('title'),
                'body': {
                    'contentType': 'Text',
                    'content': event_data.get('description', '')
                },
                'start': {
                    'dateTime': event_data.get('start_time').isoformat(),
                    'timeZone': 'UTC'
                },
                'end': {
                    'dateTime': (event_data.get('end_time') or event_data.get('start_time')).isoformat(),
                    'timeZone': 'UTC'
                }
            }

            if event_data.get('location'):
                event['location'] = {'displayName': event_data.get('location')}

            if event_data.get('attendees'):
                event['attendees'] = [
                    {
                        'emailAddress': {'address': email},
                        'type': 'required'
                    }
                    for email in event_data.get('attendees', [])
                ]

            response = requests.post(
                url,
                headers=self._get_headers(),
                json=event
            )
            response.raise_for_status()

            return response.json()

        except Exception as e:
            print(f"Error creating event: {e}")
            raise

    async def update_event(
        self,
        event_id: str,
        event_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Update an existing calendar event."""
        if not self.access_token:
            raise Exception("Outlook Calendar service not initialized")

        try:
            url = f"{self.graph_endpoint}/me/calendar/events/{event_id}"

            update_data = {}

            if 'title' in event_data:
                update_data['subject'] = event_data['title']
            if 'description' in event_data:
                update_data['body'] = {
                    'contentType': 'Text',
                    'content': event_data['description']
                }
            if 'location' in event_data:
                update_data['location'] = {'displayName': event_data['location']}
            if 'start_time' in event_data:
                update_data['start'] = {
                    'dateTime': event_data['start_time'].isoformat(),
                    'timeZone': 'UTC'
                }
            if 'end_time' in event_data:
                update_data['end'] = {
                    'dateTime': event_data['end_time'].isoformat(),
                    'timeZone': 'UTC'
                }

            response = requests.patch(
                url,
                headers=self._get_headers(),
                json=update_data
            )
            response.raise_for_status()

            return response.json()

        except Exception as e:
            print(f"Error updating event: {e}")
            raise

    async def delete_event(self, event_id: str) -> None:
        """Delete a calendar event."""
        if not self.access_token:
            raise Exception("Outlook Calendar service not initialized")

        try:
            url = f"{self.graph_endpoint}/me/calendar/events/{event_id}"

            response = requests.delete(url, headers=self._get_headers())
            response.raise_for_status()

        except Exception as e:
            print(f"Error deleting event: {e}")
            raise

    async def sync(self) -> None:
        """Sync calendar events."""
        # This would implement incremental sync using delta queries
        # For simplicity, we'll skip the full implementation
        pass
