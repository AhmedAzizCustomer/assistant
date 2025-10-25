"""Chat interface API endpoints."""
from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel

from ..storage.database import get_db
from ..storage.models import ChatMessage, Task, Event
from ..core.ai_engine import AIEngine

router = APIRouter()
ai_engine = AIEngine()


class ChatMessageCreate(BaseModel):
    """Chat message creation schema."""
    content: str
    ai_provider: Optional[str] = None


class ChatMessageResponse(BaseModel):
    """Chat message response schema."""
    id: int
    role: str
    content: str
    timestamp: datetime

    class Config:
        from_attributes = True


@router.get("/history", response_model=List[ChatMessageResponse])
async def get_chat_history(
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """Get chat conversation history."""
    messages = db.query(ChatMessage).order_by(
        ChatMessage.timestamp.desc()
    ).limit(limit).all()

    # Reverse to get chronological order
    return list(reversed(messages))


@router.post("/message", response_model=dict)
async def send_message(
    message: ChatMessageCreate,
    db: Session = Depends(get_db)
):
    """Send a chat message and get AI response."""
    # Save user message
    user_message = ChatMessage(
        user_id=1,  # TODO: Get from authenticated user
        role="user",
        content=message.content
    )
    db.add(user_message)
    db.commit()

    # Get conversation history
    history = db.query(ChatMessage).order_by(
        ChatMessage.timestamp.desc()
    ).limit(10).all()

    conversation_history = [
        {"role": msg.role, "content": msg.content}
        for msg in reversed(history)
    ]

    # Get user context
    user_context = await _get_user_context(db)

    # Generate AI response
    ai_response = await ai_engine.chat(
        message=message.content,
        conversation_history=conversation_history,
        user_context=user_context
    )

    # Save AI response
    assistant_message = ChatMessage(
        user_id=1,
        role="assistant",
        content=ai_response,
        ai_provider=message.ai_provider or "anthropic",
        context_snapshot=user_context
    )
    db.add(assistant_message)
    db.commit()

    return {
        "user_message": {
            "id": user_message.id,
            "content": user_message.content,
            "timestamp": user_message.timestamp
        },
        "assistant_message": {
            "id": assistant_message.id,
            "content": assistant_message.content,
            "timestamp": assistant_message.timestamp
        }
    }


@router.websocket("/ws")
async def websocket_chat(websocket: WebSocket, db: Session = Depends(get_db)):
    """WebSocket endpoint for real-time chat."""
    await websocket.accept()

    try:
        while True:
            # Receive message from client
            data = await websocket.receive_text()

            # Save user message
            user_message = ChatMessage(
                user_id=1,
                role="user",
                content=data
            )
            db.add(user_message)
            db.commit()

            # Get conversation history
            history = db.query(ChatMessage).order_by(
                ChatMessage.timestamp.desc()
            ).limit(10).all()

            conversation_history = [
                {"role": msg.role, "content": msg.content}
                for msg in reversed(history)
            ]

            # Get user context
            user_context = await _get_user_context(db)

            # Generate AI response
            ai_response = await ai_engine.chat(
                message=data,
                conversation_history=conversation_history,
                user_context=user_context
            )

            # Save AI response
            assistant_message = ChatMessage(
                user_id=1,
                role="assistant",
                content=ai_response,
                context_snapshot=user_context
            )
            db.add(assistant_message)
            db.commit()

            # Send response back to client
            await websocket.send_json({
                "role": "assistant",
                "content": ai_response,
                "timestamp": assistant_message.timestamp.isoformat()
            })

    except WebSocketDisconnect:
        print("Client disconnected")


@router.delete("/history")
async def clear_chat_history(db: Session = Depends(get_db)):
    """Clear chat history."""
    db.query(ChatMessage).delete()
    db.commit()
    return {"message": "Chat history cleared"}


async def _get_user_context(db: Session) -> dict:
    """Get user's current context for AI."""
    # Get upcoming tasks
    pending_tasks = db.query(Task).filter(
        Task.status.in_(["pending", "in_progress"])
    ).limit(5).all()

    # Get upcoming events
    upcoming_events = db.query(Event).filter(
        Event.start_time >= datetime.utcnow()
    ).order_by(Event.start_time).limit(5).all()

    context = {
        "pending_tasks": [
            {
                "title": t.title,
                "priority": t.priority,
                "due_date": t.due_date.isoformat() if t.due_date else None
            }
            for t in pending_tasks
        ],
        "upcoming_events": [
            {
                "title": e.title,
                "start_time": e.start_time.isoformat(),
                "event_type": e.event_type
            }
            for e in upcoming_events
        ],
        "current_time": datetime.utcnow().isoformat()
    }

    return context
