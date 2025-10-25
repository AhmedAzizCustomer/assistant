"""Email management API endpoints."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel

from ..storage.database import get_db
from ..storage.models import EmailAccount
from ..core.ai_engine import AIEngine
from ..integrations.gmail import GmailService
from ..integrations.outlook import OutlookService

router = APIRouter()
ai_engine = AIEngine()


class EmailAccountCreate(BaseModel):
    """Email account creation schema."""
    email_address: str
    provider: str  # gmail or outlook


class EmailAnalysisRequest(BaseModel):
    """Email analysis request schema."""
    email_content: str
    email_metadata: dict


class EmailDraftRequest(BaseModel):
    """Email draft request schema."""
    original_email: str
    instructions: str
    tone: str = "professional"


@router.get("/accounts")
async def get_email_accounts(db: Session = Depends(get_db)):
    """Get all connected email accounts."""
    accounts = db.query(EmailAccount).filter(EmailAccount.is_active == True).all()
    return accounts


@router.post("/accounts/connect")
async def connect_email_account(account: EmailAccountCreate, db: Session = Depends(get_db)):
    """
    Connect a new email account.
    This would typically redirect to OAuth flow for Gmail/Outlook.
    """
    # Check if account already exists
    existing = db.query(EmailAccount).filter(
        EmailAccount.email_address == account.email_address
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Email account already connected")

    # Create account record (OAuth tokens would be added after auth flow)
    db_account = EmailAccount(
        user_id=1,  # TODO: Get from authenticated user
        email_address=account.email_address,
        provider=account.provider,
        is_active=False  # Will be activated after OAuth
    )
    db.add(db_account)
    db.commit()
    db.refresh(db_account)

    return {
        "account_id": db_account.id,
        "message": f"Account created. Please complete OAuth flow for {account.provider}.",
        "oauth_url": f"/api/email/oauth/{account.provider}/authorize?account_id={db_account.id}"
    }


@router.get("/inbox")
async def get_inbox(
    account_id: Optional[int] = None,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """
    Get inbox emails from connected accounts.
    """
    if account_id:
        account = db.query(EmailAccount).filter(EmailAccount.id == account_id).first()
        if not account:
            raise HTTPException(status_code=404, detail="Email account not found")
        accounts = [account]
    else:
        accounts = db.query(EmailAccount).filter(
            EmailAccount.is_active == True,
            EmailAccount.sync_enabled == True
        ).all()

    all_emails = []
    for account in accounts:
        if account.provider == "gmail":
            service = GmailService(account)
            emails = await service.get_inbox(limit)
            all_emails.extend(emails)
        elif account.provider == "outlook":
            service = OutlookService(account)
            emails = await service.get_inbox(limit)
            all_emails.extend(emails)

    return {"emails": all_emails, "total": len(all_emails)}


@router.post("/analyze")
async def analyze_email(request: EmailAnalysisRequest):
    """Analyze an email using AI."""
    analysis = await ai_engine.analyze_email(
        email_content=request.email_content,
        email_metadata=request.email_metadata
    )
    return analysis


@router.post("/draft")
async def draft_email(request: EmailDraftRequest):
    """Draft an email response using AI."""
    draft = await ai_engine.draft_email_response(
        original_email=request.original_email,
        context=request.instructions,
        tone=request.tone
    )
    return {"draft": draft}


@router.post("/send")
async def send_email(
    account_id: int,
    to: str,
    subject: str,
    body: str,
    cc: Optional[List[str]] = None,
    bcc: Optional[List[str]] = None,
    db: Session = Depends(get_db)
):
    """Send an email."""
    account = db.query(EmailAccount).filter(EmailAccount.id == account_id).first()
    if not account:
        raise HTTPException(status_code=404, detail="Email account not found")

    if account.provider == "gmail":
        service = GmailService(account)
        result = await service.send_email(to, subject, body, cc, bcc)
    elif account.provider == "outlook":
        service = OutlookService(account)
        result = await service.send_email(to, subject, body, cc, bcc)
    else:
        raise HTTPException(status_code=400, detail="Unsupported email provider")

    return {"message": "Email sent successfully", "result": result}


@router.get("/summary")
async def get_email_summary(db: Session = Depends(get_db)):
    """Get a summary of inbox with AI-powered insights."""
    # Get recent emails from all accounts
    accounts = db.query(EmailAccount).filter(
        EmailAccount.is_active == True
    ).all()

    all_emails = []
    for account in accounts:
        if account.provider == "gmail":
            service = GmailService(account)
            emails = await service.get_inbox(20)
            all_emails.extend(emails)
        elif account.provider == "outlook":
            service = OutlookService(account)
            emails = await service.get_inbox(20)
            all_emails.extend(emails)

    # Generate AI summary
    prompt = f"""
    Summarize these emails and categorize by priority:
    {all_emails}

    Provide:
    1. High priority emails requiring immediate attention
    2. Medium priority emails
    3. Low priority emails (newsletters, promotions)
    4. Overall insights and action items

    Return as JSON.
    """

    summary = await ai_engine.generate_response(
        prompt,
        system_prompt="You are an email triage assistant. Provide concise summaries."
    )

    return {
        "total_emails": len(all_emails),
        "summary": summary
    }
