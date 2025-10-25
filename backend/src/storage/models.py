"""Database models for the personal assistant."""
from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, ForeignKey, Float, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base


class User(Base):
    """User model."""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Preferences
    preferences = Column(JSON, default={})

    # Relationships
    tasks = relationship("Task", back_populates="user")
    meals = relationship("Meal", back_populates="user")
    workouts = relationship("Workout", back_populates="user")
    events = relationship("Event", back_populates="user")
    email_accounts = relationship("EmailAccount", back_populates="user")
    calendar_accounts = relationship("CalendarAccount", back_populates="user")


class Task(Base):
    """Task model."""
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text)
    status = Column(String, default="pending")  # pending, in_progress, completed, cancelled
    priority = Column(String, default="medium")  # low, medium, high, urgent
    category = Column(String)  # work, personal, health, etc.
    due_date = Column(DateTime(timezone=True))
    completed_at = Column(DateTime(timezone=True))
    estimated_duration = Column(Integer)  # minutes
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # AI-generated metadata
    ai_insights = Column(JSON)

    # Relationships
    user = relationship("User", back_populates="tasks")


class Event(Base):
    """Event model for tracking personal and professional events."""
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text)
    location = Column(String)
    start_time = Column(DateTime(timezone=True), nullable=False)
    end_time = Column(DateTime(timezone=True))
    event_type = Column(String)  # meeting, appointment, deadline, social, etc.
    attendees = Column(JSON)  # List of attendees
    reminders = Column(JSON)  # Reminder settings
    is_all_day = Column(Boolean, default=False)
    external_id = Column(String)  # ID from calendar provider
    source = Column(String)  # google, outlook, manual
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="events")


class Meal(Base):
    """Meal tracking and planning model."""
    __tablename__ = "meals"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String, nullable=False)
    meal_type = Column(String)  # breakfast, lunch, dinner, snack
    date = Column(DateTime(timezone=True), nullable=False)
    description = Column(Text)
    recipe = Column(Text)

    # Nutritional information
    calories = Column(Float)
    protein = Column(Float)  # grams
    carbs = Column(Float)  # grams
    fat = Column(Float)  # grams
    fiber = Column(Float)  # grams

    # Ingredients and portions
    ingredients = Column(JSON)

    # Meal plan reference
    meal_plan_id = Column(Integer, ForeignKey("meal_plans.id"))

    # Metadata
    is_planned = Column(Boolean, default=False)  # Planned vs. actually eaten
    notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user = relationship("User", back_populates="meals")
    meal_plan = relationship("MealPlan", back_populates="meals")


class MealPlan(Base):
    """Meal plan model."""
    __tablename__ = "meal_plans"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String, nullable=False)
    start_date = Column(DateTime(timezone=True), nullable=False)
    end_date = Column(DateTime(timezone=True), nullable=False)

    # Dietary preferences and goals
    dietary_restrictions = Column(JSON)
    daily_calorie_target = Column(Float)
    macro_targets = Column(JSON)  # protein, carbs, fat percentages

    # AI-generated plan
    ai_generated_plan = Column(JSON)
    grocery_list = Column(JSON)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    meals = relationship("Meal", back_populates="meal_plan")


class Workout(Base):
    """Workout tracking and planning model."""
    __tablename__ = "workouts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String, nullable=False)
    workout_type = Column(String)  # strength, cardio, flexibility, sports, etc.
    date = Column(DateTime(timezone=True), nullable=False)
    duration = Column(Integer)  # minutes

    # Workout details
    exercises = Column(JSON)  # List of exercises with sets, reps, weight
    intensity = Column(String)  # low, moderate, high
    calories_burned = Column(Float)

    # Metrics
    heart_rate_avg = Column(Integer)
    distance = Column(Float)  # for cardio (km or miles)

    # Workout plan reference
    workout_plan_id = Column(Integer, ForeignKey("workout_plans.id"))

    # Metadata
    is_planned = Column(Boolean, default=False)
    is_completed = Column(Boolean, default=False)
    notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user = relationship("User", back_populates="workouts")
    workout_plan = relationship("WorkoutPlan", back_populates="workouts")


class WorkoutPlan(Base):
    """Workout plan model."""
    __tablename__ = "workout_plans"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String, nullable=False)
    start_date = Column(DateTime(timezone=True), nullable=False)
    end_date = Column(DateTime(timezone=True))

    # Fitness goals and level
    fitness_level = Column(String)  # beginner, intermediate, advanced
    goals = Column(JSON)  # weight loss, muscle gain, endurance, etc.

    # AI-generated plan
    ai_generated_plan = Column(JSON)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    workouts = relationship("Workout", back_populates="workout_plan")


class EmailAccount(Base):
    """Email account integration."""
    __tablename__ = "email_accounts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    email_address = Column(String, nullable=False)
    provider = Column(String, nullable=False)  # gmail, outlook
    access_token = Column(Text)  # Encrypted
    refresh_token = Column(Text)  # Encrypted
    token_expires_at = Column(DateTime(timezone=True))
    is_active = Column(Boolean, default=True)
    sync_enabled = Column(Boolean, default=True)
    last_sync = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user = relationship("User", back_populates="email_accounts")


class CalendarAccount(Base):
    """Calendar account integration."""
    __tablename__ = "calendar_accounts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    calendar_name = Column(String, nullable=False)
    provider = Column(String, nullable=False)  # google, outlook
    calendar_id = Column(String, nullable=False)  # External calendar ID
    access_token = Column(Text)  # Encrypted
    refresh_token = Column(Text)  # Encrypted
    token_expires_at = Column(DateTime(timezone=True))
    is_active = Column(Boolean, default=True)
    sync_enabled = Column(Boolean, default=True)
    last_sync = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user = relationship("User", back_populates="calendar_accounts")


class ChatMessage(Base):
    """Chat conversation history."""
    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    role = Column(String, nullable=False)  # user, assistant
    content = Column(Text, nullable=False)
    ai_provider = Column(String)  # anthropic, openai
    model_used = Column(String)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

    # Context at the time of message
    context_snapshot = Column(JSON)
