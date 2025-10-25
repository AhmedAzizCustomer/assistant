"""Task management API endpoints."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel

from ..storage.database import get_db
from ..storage.models import Task, User
from ..core.ai_engine import AIEngine

router = APIRouter()
ai_engine = AIEngine()


class TaskCreate(BaseModel):
    """Task creation schema."""
    title: str
    description: Optional[str] = None
    priority: str = "medium"
    category: Optional[str] = None
    due_date: Optional[datetime] = None
    estimated_duration: Optional[int] = None


class TaskUpdate(BaseModel):
    """Task update schema."""
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[str] = None
    category: Optional[str] = None
    due_date: Optional[datetime] = None
    estimated_duration: Optional[int] = None


class TaskResponse(BaseModel):
    """Task response schema."""
    id: int
    title: str
    description: Optional[str]
    status: str
    priority: str
    category: Optional[str]
    due_date: Optional[datetime]
    estimated_duration: Optional[int]
    created_at: datetime
    ai_insights: Optional[dict]

    class Config:
        from_attributes = True


@router.get("/", response_model=List[TaskResponse])
async def get_tasks(
    status: Optional[str] = None,
    priority: Optional[str] = None,
    category: Optional[str] = None,
    db: Session = Depends(get_db),
):
    """Get all tasks with optional filters."""
    query = db.query(Task)

    if status:
        query = query.filter(Task.status == status)
    if priority:
        query = query.filter(Task.priority == priority)
    if category:
        query = query.filter(Task.category == category)

    return query.all()


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(task_id: int, db: Session = Depends(get_db)):
    """Get a specific task."""
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.post("/", response_model=TaskResponse)
async def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    """Create a new task."""
    # Create task
    db_task = Task(
        user_id=1,  # TODO: Get from authenticated user
        **task.model_dump()
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)

    # Generate AI insights asynchronously
    insights = await _generate_task_insights(db_task)
    db_task.ai_insights = insights
    db.commit()

    return db_task


@router.put("/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: int,
    task_update: TaskUpdate,
    db: Session = Depends(get_db)
):
    """Update a task."""
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Update fields
    update_data = task_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_task, field, value)

    # Mark completion timestamp
    if task_update.status == "completed" and not db_task.completed_at:
        db_task.completed_at = datetime.utcnow()

    db.commit()
    db.refresh(db_task)
    return db_task


@router.delete("/{task_id}")
async def delete_task(task_id: int, db: Session = Depends(get_db)):
    """Delete a task."""
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")

    db.delete(db_task)
    db.commit()
    return {"message": "Task deleted successfully"}


@router.post("/{task_id}/breakdown")
async def breakdown_task(task_id: int, db: Session = Depends(get_db)):
    """Use AI to break down a complex task into subtasks."""
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")

    prompt = f"""
    Break down this task into smaller, actionable subtasks:
    Title: {db_task.title}
    Description: {db_task.description}

    Provide 3-7 subtasks in a structured JSON format.
    """

    response = await ai_engine.generate_response(
        prompt,
        system_prompt="You are a task management expert. Break down complex tasks into manageable subtasks."
    )

    return {"subtasks": response}


async def _generate_task_insights(task: Task) -> dict:
    """Generate AI insights for a task."""
    prompt = f"""
    Analyze this task and provide insights:
    - Title: {task.title}
    - Description: {task.description}
    - Priority: {task.priority}
    - Due Date: {task.due_date}

    Provide:
    1. Estimated time to complete
    2. Suggested approach or steps
    3. Potential challenges
    4. Best time of day to work on this

    Return as JSON.
    """

    try:
        response = await ai_engine.generate_response(
            prompt,
            system_prompt="You are a productivity expert."
        )
        return {"raw_insights": response}
    except Exception as e:
        return {"error": str(e)}
