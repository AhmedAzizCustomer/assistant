"""Gmail integration service."""
from typing import List, Optional, Dict, Any
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from ..storage.models import EmailAccount


class GmailService:
    """Service for interacting with Gmail API."""

    def __init__(self, email_account: EmailAccount):
        """Initialize Gmail service."""
        self.account = email_account
        self.service = None

        if email_account.access_token:
            # Initialize Gmail API service
            credentials = Credentials(
                token=email_account.access_token,
                refresh_token=email_account.refresh_token,
            )
            self.service = build('gmail', 'v1', credentials=credentials)

    async def get_inbox(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Get inbox messages."""
        if not self.service:
            return []

        try:
            # Get message list
            results = self.service.users().messages().list(
                userId='me',
                maxResults=limit,
                labelIds=['INBOX']
            ).execute()

            messages = results.get('messages', [])

            # Get message details
            email_list = []
            for msg in messages:
                message = self.service.users().messages().get(
                    userId='me',
                    id=msg['id'],
                    format='metadata'
                ).execute()

                headers = message.get('payload', {}).get('headers', [])
                subject = next((h['value'] for h in headers if h['name'] == 'Subject'), 'No Subject')
                from_email = next((h['value'] for h in headers if h['name'] == 'From'), 'Unknown')
                date = next((h['value'] for h in headers if h['name'] == 'Date'), 'Unknown')

                email_list.append({
                    'id': message['id'],
                    'subject': subject,
                    'from': from_email,
                    'date': date,
                    'snippet': message.get('snippet', ''),
                    'account': self.account.email_address
                })

            return email_list

        except Exception as e:
            print(f"Error fetching Gmail inbox: {e}")
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
        if not self.service:
            raise Exception("Gmail service not initialized")

        try:
            from email.mime.text import MIMEText
            import base64

            message = MIMEText(body)
            message['to'] = to
            message['subject'] = subject

            if cc:
                message['cc'] = ', '.join(cc)
            if bcc:
                message['bcc'] = ', '.join(bcc)

            raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
            send_message = {'raw': raw}

            result = self.service.users().messages().send(
                userId='me',
                body=send_message
            ).execute()

            return result

        except Exception as e:
            print(f"Error sending email: {e}")
            raise

    async def get_message(self, message_id: str) -> Dict[str, Any]:
        """Get a specific email message."""
        if not self.service:
            raise Exception("Gmail service not initialized")

        try:
            message = self.service.users().messages().get(
                userId='me',
                id=message_id,
                format='full'
            ).execute()

            return message

        except Exception as e:
            print(f"Error fetching message: {e}")
            raise
