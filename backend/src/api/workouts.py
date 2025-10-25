"""Exercise and workout API endpoints."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, date
from pydantic import BaseModel

from ..storage.database import get_db
from ..storage.models import Workout, WorkoutPlan
from ..core.ai_engine import AIEngine

router = APIRouter()
ai_engine = AIEngine()


class WorkoutCreate(BaseModel):
    """Workout creation schema."""
    name: str
    workout_type: str
    date: datetime
    duration: Optional[int] = None
    exercises: Optional[dict] = None
    intensity: Optional[str] = None
    calories_burned: Optional[float] = None
    is_planned: bool = False
    is_completed: bool = False
    notes: Optional[str] = None


class WorkoutPlanCreate(BaseModel):
    """Workout plan creation schema."""
    name: str
    start_date: datetime
    end_date: Optional[datetime] = None
    fitness_level: str  # beginner, intermediate, advanced
    goals: List[str]  # weight_loss, muscle_gain, endurance, etc.
    constraints: Optional[dict] = None


class WorkoutResponse(BaseModel):
    """Workout response schema."""
    id: int
    name: str
    workout_type: str
    date: datetime
    duration: Optional[int]
    intensity: Optional[str]
    calories_burned: Optional[float]
    is_completed: bool

    class Config:
        from_attributes = True


@router.get("/", response_model=List[WorkoutResponse])
async def get_workouts(
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    workout_type: Optional[str] = None,
    db: Session = Depends(get_db),
):
    """Get workouts with optional filters."""
    query = db.query(Workout)

    if start_date:
        query = query.filter(Workout.date >= start_date)
    if end_date:
        query = query.filter(Workout.date <= end_date)
    if workout_type:
        query = query.filter(Workout.workout_type == workout_type)

    return query.all()


@router.post("/", response_model=WorkoutResponse)
async def create_workout(workout: WorkoutCreate, db: Session = Depends(get_db)):
    """Log a workout."""
    db_workout = Workout(
        user_id=1,  # TODO: Get from authenticated user
        **workout.model_dump()
    )
    db.add(db_workout)
    db.commit()
    db.refresh(db_workout)
    return db_workout


@router.put("/{workout_id}/complete")
async def complete_workout(workout_id: int, db: Session = Depends(get_db)):
    """Mark a workout as completed."""
    workout = db.query(Workout).filter(Workout.id == workout_id).first()
    if not workout:
        raise HTTPException(status_code=404, detail="Workout not found")

    workout.is_completed = True
    db.commit()
    return {"message": "Workout marked as completed"}


@router.post("/plans", response_model=dict)
async def create_workout_plan(plan: WorkoutPlanCreate, db: Session = Depends(get_db)):
    """Generate an AI-powered workout plan."""
    # Prepare constraints
    constraints = plan.constraints or {
        "days_per_week": 3,
        "session_duration": 60,
        "equipment": "basic"
    }

    # Generate workout plan using AI
    ai_plan = await ai_engine.create_workout_plan(
        fitness_level=plan.fitness_level,
        goals=", ".join(plan.goals),
        constraints=constraints
    )

    # Create workout plan record
    db_workout_plan = WorkoutPlan(
        user_id=1,  # TODO: Get from authenticated user
        name=plan.name,
        start_date=plan.start_date,
        end_date=plan.end_date,
        fitness_level=plan.fitness_level,
        goals=plan.goals,
        ai_generated_plan=ai_plan
    )
    db.add(db_workout_plan)
    db.commit()
    db.refresh(db_workout_plan)

    return {
        "id": db_workout_plan.id,
        "workout_plan": ai_plan,
        "message": "Workout plan generated successfully"
    }


@router.get("/plans/{plan_id}")
async def get_workout_plan(plan_id: int, db: Session = Depends(get_db)):
    """Get a specific workout plan."""
    plan = db.query(WorkoutPlan).filter(WorkoutPlan.id == plan_id).first()
    if not plan:
        raise HTTPException(status_code=404, detail="Workout plan not found")
    return plan


@router.get("/stats/summary")
async def get_workout_summary(
    start_date: date,
    end_date: date,
    db: Session = Depends(get_db)
):
    """Get workout statistics summary for a date range."""
    workouts = db.query(Workout).filter(
        Workout.date >= start_date,
        Workout.date <= end_date,
        Workout.is_completed == True
    ).all()

    total_duration = sum(w.duration or 0 for w in workouts)
    total_calories = sum(w.calories_burned or 0 for w in workouts)

    # Count by type
    by_type = {}
    for w in workouts:
        by_type[w.workout_type] = by_type.get(w.workout_type, 0) + 1

    return {
        "period": {
            "start": start_date,
            "end": end_date
        },
        "summary": {
            "total_workouts": len(workouts),
            "total_duration_minutes": total_duration,
            "total_calories_burned": total_calories,
            "by_type": by_type
        },
        "weekly_average": {
            "workouts": len(workouts) / max(1, (end_date - start_date).days / 7),
            "duration": total_duration / max(1, (end_date - start_date).days / 7),
        }
    }


@router.post("/recommend")
async def get_workout_recommendation(
    current_state: dict,
    preferences: Optional[dict] = None
):
    """Get AI workout recommendation based on current state."""
    prompt = f"""
    Based on the user's current state:
    {current_state}

    And preferences:
    {preferences or 'No specific preferences'}

    Recommend a workout for today including:
    - Type of workout
    - Duration
    - Specific exercises
    - Intensity level

    Return as JSON.
    """

    response = await ai_engine.generate_response(
        prompt,
        system_prompt="You are a fitness expert. Provide personalized workout recommendations."
    )

    return {"recommendation": response}
