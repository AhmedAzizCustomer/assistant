"""Outlook integration service."""
from typing import List, Optional, Dict, Any
import requests
from msal import ConfidentialClientApplication
from ..storage.models import EmailAccount


class OutlookService:
    """Service for interacting with Microsoft Graph API (Outlook)."""

    def __init__(self, email_account: EmailAccount):
        """Initialize Outlook service."""
        self.account = email_account
        self.access_token = email_account.access_token
        self.graph_endpoint = "https://graph.microsoft.com/v1.0"

    def _get_headers(self) -> Dict[str, str]:
        """Get headers for Graph API requests."""
        return {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }

    async def get_inbox(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Get inbox messages."""
        if not self.access_token:
            return []

        try:
            url = f"{self.graph_endpoint}/me/messages"
            params = {
                '$top': limit,
                '$select': 'subject,from,receivedDateTime,bodyPreview',
                '$orderby': 'receivedDateTime DESC'
            }

            response = requests.get(
                url,
                headers=self._get_headers(),
                params=params
            )
            response.raise_for_status()

            messages = response.json().get('value', [])

            email_list = []
            for msg in messages:
                email_list.append({
                    'id': msg.get('id'),
                    'subject': msg.get('subject', 'No Subject'),
                    'from': msg.get('from', {}).get('emailAddress', {}).get('address', 'Unknown'),
                    'date': msg.get('receivedDateTime', 'Unknown'),
                    'snippet': msg.get('bodyPreview', ''),
                    'account': self.account.email_address
                })

            return email_list

        except Exception as e:
            print(f"Error fetching Outlook inbox: {e}")
            return []

    async def send_email(
        self,
        to: str,
        subject: str,
        body: str,
        cc: Optional[List[str]] = None,
        bcc: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Send an email."""
        if not self.access_token:
            raise Exception("Outlook service not initialized")

        try:
            url = f"{self.graph_endpoint}/me/sendMail"

            message = {
                'message': {
                    'subject': subject,
                    'body': {
                        'contentType': 'Text',
                        'content': body
                    },
                    'toRecipients': [
                        {'emailAddress': {'address': to}}
                    ]
                }
            }

            if cc:
                message['message']['ccRecipients'] = [
                    {'emailAddress': {'address': addr}} for addr in cc
                ]

            if bcc:
                message['message']['bccRecipients'] = [
                    {'emailAddress': {'address': addr}} for addr in bcc
                ]

            response = requests.post(
                url,
                headers=self._get_headers(),
                json=message
            )
            response.raise_for_status()

            return {'status': 'sent'}

        except Exception as e:
            print(f"Error sending email: {e}")
            raise

    async def get_message(self, message_id: str) -> Dict[str, Any]:
        """Get a specific email message."""
        if not self.access_token:
            raise Exception("Outlook service not initialized")

        try:
            url = f"{self.graph_endpoint}/me/messages/{message_id}"

            response = requests.get(url, headers=self._get_headers())
            response.raise_for_status()

            return response.json()

        except Exception as e:
            print(f"Error fetching message: {e}")
            raise
