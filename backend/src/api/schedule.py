"""Schedule planning and optimization API endpoints."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta
from pydantic import BaseModel

from ..storage.database import get_db
from ..storage.models import Task, Event, Workout, Meal
from ..core.ai_engine import AIEngine

router = APIRouter()
ai_engine = AIEngine()


class ScheduleOptimizationRequest(BaseModel):
    """Schedule optimization request schema."""
    start_date: datetime
    end_date: datetime
    work_hours_start: str = "09:00"
    work_hours_end: str = "17:00"
    break_duration: int = 60  # minutes
    include_tasks: bool = True
    include_workouts: bool = True
    include_meals: bool = True


class TimeBlock(BaseModel):
    """Time block schema."""
    start_time: datetime
    end_time: datetime
    activity: str
    type: str  # task, event, workout, meal, break
    details: Optional[dict] = None


@router.post("/optimize", response_model=dict)
async def optimize_schedule(
    request: ScheduleOptimizationRequest,
    db: Session = Depends(get_db)
):
    """Generate an optimized schedule using AI."""
    # Gather all items to schedule
    tasks_to_schedule = []
    if request.include_tasks:
        tasks = db.query(Task).filter(
            Task.status.in_(["pending", "in_progress"]),
            Task.due_date >= request.start_date,
            Task.due_date <= request.end_date
        ).all()

        tasks_to_schedule = [
            {
                "id": t.id,
                "title": t.title,
                "priority": t.priority,
                "estimated_duration": t.estimated_duration or 60,
                "due_date": t.due_date.isoformat() if t.due_date else None,
                "category": t.category
            }
            for t in tasks
        ]

    # Get fixed events (can't be moved)
    fixed_events = db.query(Event).filter(
        Event.start_time >= request.start_date,
        Event.start_time <= request.end_date
    ).all()

    fixed_blocks = [
        {
            "start": e.start_time.isoformat(),
            "end": e.end_time.isoformat() if e.end_time else (e.start_time + timedelta(hours=1)).isoformat(),
            "title": e.title,
            "type": "event"
        }
        for e in fixed_events
    ]

    # Get workouts if requested
    workouts = []
    if request.include_workouts:
        planned_workouts = db.query(Workout).filter(
            Workout.date >= request.start_date,
            Workout.date <= request.end_date,
            Workout.is_completed == False
        ).all()

        workouts = [
            {
                "id": w.id,
                "name": w.name,
                "duration": w.duration or 45,
                "type": w.workout_type
            }
            for w in planned_workouts
        ]

    # Get meal planning needs
    meals = []
    if request.include_meals:
        # Typically 3 meals per day
        num_days = (request.end_date - request.start_date).days + 1
        meals = [{"type": meal_type, "duration": 30} for _ in range(num_days) for meal_type in ["breakfast", "lunch", "dinner"]]

    # Prepare constraints
    constraints = {
        "work_hours": {
            "start": request.work_hours_start,
            "end": request.work_hours_end
        },
        "break_duration": request.break_duration,
        "fixed_events": fixed_blocks,
        "start_date": request.start_date.isoformat(),
        "end_date": request.end_date.isoformat()
    }

    # Use AI to optimize schedule
    optimized = await ai_engine.optimize_schedule(
        tasks=tasks_to_schedule + workouts + meals,
        constraints=constraints
    )

    return {
        "schedule": optimized,
        "summary": {
            "tasks_scheduled": len(tasks_to_schedule),
            "fixed_events": len(fixed_blocks),
            "workouts_scheduled": len(workouts),
            "period": {
                "start": request.start_date.isoformat(),
                "end": request.end_date.isoformat()
            }
        }
    }


@router.get("/daily/{date}")
async def get_daily_schedule(
    date: datetime,
    db: Session = Depends(get_db)
):
    """Get the schedule for a specific day."""
    start_of_day = date.replace(hour=0, minute=0, second=0, microsecond=0)
    end_of_day = start_of_day + timedelta(days=1)

    # Get all items for the day
    events = db.query(Event).filter(
        Event.start_time >= start_of_day,
        Event.start_time < end_of_day
    ).order_by(Event.start_time).all()

    tasks = db.query(Task).filter(
        Task.due_date >= start_of_day,
        Task.due_date < end_of_day,
        Task.status != "completed"
    ).all()

    workouts = db.query(Workout).filter(
        Workout.date >= start_of_day,
        Workout.date < end_of_day
    ).all()

    meals = db.query(Meal).filter(
        Meal.date >= start_of_day,
        Meal.date < end_of_day
    ).all()

    # Build time blocks
    time_blocks = []

    for event in events:
        time_blocks.append({
            "start_time": event.start_time,
            "end_time": event.end_time or event.start_time + timedelta(hours=1),
            "activity": event.title,
            "type": "event",
            "details": {
                "location": event.location,
                "description": event.description
            }
        })

    for task in tasks:
        time_blocks.append({
            "activity": task.title,
            "type": "task",
            "details": {
                "priority": task.priority,
                "estimated_duration": task.estimated_duration
            }
        })

    for workout in workouts:
        time_blocks.append({
            "start_time": workout.date,
            "end_time": workout.date + timedelta(minutes=workout.duration or 45),
            "activity": workout.name,
            "type": "workout",
            "details": {
                "workout_type": workout.workout_type,
                "duration": workout.duration
            }
        })

    for meal in meals:
        time_blocks.append({
            "start_time": meal.date,
            "activity": f"{meal.meal_type}: {meal.name}",
            "type": "meal",
            "details": {
                "calories": meal.calories,
                "meal_type": meal.meal_type
            }
        })

    return {
        "date": date.date().isoformat(),
        "time_blocks": sorted(time_blocks, key=lambda x: x.get("start_time", datetime.max)),
        "summary": {
            "events": len(events),
            "tasks": len(tasks),
            "workouts": len(workouts),
            "meals": len(meals)
        }
    }


@router.get("/weekly")
async def get_weekly_schedule(
    start_date: datetime,
    db: Session = Depends(get_db)
):
    """Get the schedule for a week."""
    end_date = start_date + timedelta(days=7)

    weekly_schedule = []
    current_date = start_date

    while current_date < end_date:
        daily = await get_daily_schedule(current_date, db)
        weekly_schedule.append(daily)
        current_date += timedelta(days=1)

    return {
        "week_start": start_date.date().isoformat(),
        "week_end": end_date.date().isoformat(),
        "daily_schedules": weekly_schedule
    }


@router.post("/suggest-time")
async def suggest_time_for_task(
    task_id: int,
    db: Session = Depends(get_db)
):
    """Suggest optimal time slots for a task."""
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Get schedule for next 7 days
    start = datetime.utcnow()
    end = start + timedelta(days=7)

    events = db.query(Event).filter(
        Event.start_time >= start,
        Event.start_time <= end
    ).order_by(Event.start_time).all()

    # Find available slots
    available_slots = []
    current_time = start

    for event in events:
        gap_minutes = (event.start_time - current_time).total_seconds() / 60
        estimated_duration = task.estimated_duration or 60

        if gap_minutes >= estimated_duration:
            available_slots.append({
                "start": current_time,
                "end": current_time + timedelta(minutes=estimated_duration),
                "duration_minutes": estimated_duration
            })

        if event.end_time:
            current_time = max(current_time, event.end_time)

    # Use AI to recommend best slot based on task characteristics
    prompt = f"""
    Given this task:
    - Title: {task.title}
    - Priority: {task.priority}
    - Category: {task.category}
    - Estimated Duration: {task.estimated_duration or 60} minutes

    And these available time slots:
    {available_slots[:10]}

    Recommend the top 3 best time slots and explain why.
    Consider factors like:
    - Time of day for optimal focus
    - Task priority and urgency
    - Productive hours

    Return as JSON with recommendations.
    """

    recommendation = await ai_engine.generate_response(
        prompt,
        system_prompt="You are a productivity and scheduling expert."
    )

    return {
        "task": {
            "id": task.id,
            "title": task.title
        },
        "available_slots": available_slots[:10],
        "ai_recommendations": recommendation
    }
