"""Main FastAPI application."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path
import os
from .core.config import get_settings
from .api import tasks, meals, workouts, events, email, calendar, chat, schedule, settings as settings_router

config = get_settings()

# Create FastAPI app
app = FastAPI(
    title=config.app_name,
    description="AI-powered personal assistant for managing work and life",
    version="1.0.0"
)

# Configure CORS - allow all origins for deployed apps
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(settings_router.router, prefix="/api/settings", tags=["Settings"])
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
    try:
        from .storage.database import Base, engine
        from .storage.settings_model import Settings, SystemStatus
        Base.metadata.create_all(bind=engine)
        print("✅ Database initialized successfully")
    except Exception as e:
        print(f"⚠️  Database initialization error: {e}")
        # Continue anyway - database will be created on first request


@app.get("/api/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "version": "1.0.0"}


# Serve static files from React build
static_dir = Path(__file__).parent.parent.parent / "frontend" / "build"
if static_dir.exists():
    # Mount static files (js, css, etc)
    app.mount("/static", StaticFiles(directory=static_dir / "static"), name="static")

    # Serve React app for all other routes
    @app.get("/{full_path:path}")
    async def serve_react_app(full_path: str):
        """Serve React app for all non-API routes."""
        # If it's an API route, return 404
        if full_path.startswith("api/"):
            return {"error": "Not found"}, 404

        # Serve index.html for all other routes (React Router handles them)
        index_file = static_dir / "index.html"
        if index_file.exists():
            return FileResponse(index_file)
        return {"error": "Frontend not built"}
else:
    # If frontend build doesn't exist, just show API info
    @app.get("/")
    async def root():
        """Root endpoint when frontend is not available."""
        return {
            "message": "AI Personal Assistant API",
            "version": "1.0.0",
            "docs": "/docs",
            "health": "/api/health",
            "note": "Frontend not available - deploy with built frontend or access API directly"
        }


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", config.api_port))
    uvicorn.run(
        "backend.src.main:app",
        host="0.0.0.0",
        port=port,
        reload=config.environment == "development"
    )
