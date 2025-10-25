"""Meal planning and tracking API endpoints."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, date
from pydantic import BaseModel

from ..storage.database import get_db
from ..storage.models import Meal, MealPlan
from ..core.ai_engine import AIEngine

router = APIRouter()
ai_engine = AIEngine()


class MealCreate(BaseModel):
    """Meal creation schema."""
    name: str
    meal_type: str  # breakfast, lunch, dinner, snack
    date: datetime
    description: Optional[str] = None
    recipe: Optional[str] = None
    calories: Optional[float] = None
    protein: Optional[float] = None
    carbs: Optional[float] = None
    fat: Optional[float] = None
    fiber: Optional[float] = None
    ingredients: Optional[dict] = None
    is_planned: bool = False
    notes: Optional[str] = None


class MealPlanCreate(BaseModel):
    """Meal plan creation schema."""
    name: str
    start_date: datetime
    end_date: datetime
    dietary_restrictions: Optional[List[str]] = None
    daily_calorie_target: Optional[float] = None
    macro_targets: Optional[dict] = None


class MealResponse(BaseModel):
    """Meal response schema."""
    id: int
    name: str
    meal_type: str
    date: datetime
    calories: Optional[float]
    protein: Optional[float]
    carbs: Optional[float]
    fat: Optional[float]

    class Config:
        from_attributes = True


@router.get("/", response_model=List[MealResponse])
async def get_meals(
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    meal_type: Optional[str] = None,
    db: Session = Depends(get_db),
):
    """Get meals with optional filters."""
    query = db.query(Meal)

    if start_date:
        query = query.filter(Meal.date >= start_date)
    if end_date:
        query = query.filter(Meal.date <= end_date)
    if meal_type:
        query = query.filter(Meal.meal_type == meal_type)

    return query.all()


@router.post("/", response_model=MealResponse)
async def create_meal(meal: MealCreate, db: Session = Depends(get_db)):
    """Log a meal."""
    db_meal = Meal(
        user_id=1,  # TODO: Get from authenticated user
        **meal.model_dump()
    )
    db.add(db_meal)
    db.commit()
    db.refresh(db_meal)
    return db_meal


@router.post("/analyze")
async def analyze_meal(description: str):
    """Analyze a meal description and estimate nutritional content."""
    prompt = f"""
    Analyze this meal and provide nutritional information:
    {description}

    Provide estimated:
    - Calories
    - Protein (g)
    - Carbohydrates (g)
    - Fat (g)
    - Fiber (g)

    Also suggest if this is a healthy meal and any improvements.
    Return as JSON.
    """

    response = await ai_engine.generate_response(
        prompt,
        system_prompt="You are a nutrition expert. Provide accurate nutritional estimates."
    )

    return {"analysis": response}


@router.post("/plans", response_model=dict)
async def create_meal_plan(plan: MealPlanCreate, db: Session = Depends(get_db)):
    """Generate an AI-powered meal plan."""
    # Prepare preferences
    preferences = {
        "dietary_restrictions": plan.dietary_restrictions or [],
        "daily_calorie_target": plan.daily_calorie_target or 2000,
        "macro_targets": plan.macro_targets or {
            "protein": 30,
            "carbs": 40,
            "fat": 30
        }
    }

    # Calculate days
    days = (plan.end_date - plan.start_date).days + 1

    # Generate meal plan using AI
    ai_plan = await ai_engine.generate_meal_plan(preferences, days)

    # Create meal plan record
    db_meal_plan = MealPlan(
        user_id=1,  # TODO: Get from authenticated user
        name=plan.name,
        start_date=plan.start_date,
        end_date=plan.end_date,
        dietary_restrictions=plan.dietary_restrictions,
        daily_calorie_target=plan.daily_calorie_target,
        macro_targets=plan.macro_targets,
        ai_generated_plan=ai_plan
    )
    db.add(db_meal_plan)
    db.commit()
    db.refresh(db_meal_plan)

    return {
        "id": db_meal_plan.id,
        "meal_plan": ai_plan,
        "message": "Meal plan generated successfully"
    }


@router.get("/plans/{plan_id}")
async def get_meal_plan(plan_id: int, db: Session = Depends(get_db)):
    """Get a specific meal plan."""
    plan = db.query(MealPlan).filter(MealPlan.id == plan_id).first()
    if not plan:
        raise HTTPException(status_code=404, detail="Meal plan not found")
    return plan


@router.get("/nutrition/summary")
async def get_nutrition_summary(
    start_date: date,
    end_date: date,
    db: Session = Depends(get_db)
):
    """Get nutritional summary for a date range."""
    meals = db.query(Meal).filter(
        Meal.date >= start_date,
        Meal.date <= end_date,
        Meal.is_planned == False  # Only actual meals
    ).all()

    total_calories = sum(m.calories or 0 for m in meals)
    total_protein = sum(m.protein or 0 for m in meals)
    total_carbs = sum(m.carbs or 0 for m in meals)
    total_fat = sum(m.fat or 0 for m in meals)

    return {
        "period": {
            "start": start_date,
            "end": end_date
        },
        "summary": {
            "total_calories": total_calories,
            "total_protein": total_protein,
            "total_carbs": total_carbs,
            "total_fat": total_fat,
            "meals_count": len(meals)
        },
        "daily_average": {
            "calories": total_calories / max(1, (end_date - start_date).days + 1),
            "protein": total_protein / max(1, (end_date - start_date).days + 1),
            "carbs": total_carbs / max(1, (end_date - start_date).days + 1),
            "fat": total_fat / max(1, (end_date - start_date).days + 1),
        }
    }
