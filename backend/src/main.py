"""Main FastAPI application."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .core.config import get_settings
from .api import tasks, meals, workouts, events, email, calendar, chat, schedule, settings

settings = get_settings()

# Create FastAPI app
app = FastAPI(
    title=settings.app_name,
    description="AI-powered personal assistant for managing work and life",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_url, "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(settings.router, prefix="/api/settings", tags=["Settings"])
app.include_router(tasks.router, prefix="/api/tasks", tags=["Tasks"])
app.include_router(meals.router, prefix="/api/meals", tags=["Meals"])
app.include_router(workouts.router, prefix="/api/workouts", tags=["Workouts"])
app.include_router(events.router, prefix="/api/events", tags=["Events"])
app.include_router(email.router, prefix="/api/email", tags=["Email"])
app.include_router(calendar.router, prefix="/api/calendar", tags=["Calendar"])
app.include_router(chat.router, prefix="/api/chat", tags=["Chat"])
app.include_router(schedule.router, prefix="/api/schedule", tags=["Schedule"])


# Initialize database tables on startup
@app.on_event("startup")
async def startup_event():
    """Initialize database tables."""
    from .storage.database import Base, engine
    Base.metadata.create_all(bind=engine)


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Welcome to AI Personal Assistant API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "src.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.environment == "development"
    )
