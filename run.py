"""Startup script for Railway deployment."""
import os
import sys

def main():
    """Start the application with proper configuration."""
    # Get port from environment or use default
    port = int(os.getenv("PORT", 8000))

    print(f"🚀 Starting AI Personal Assistant...")
    print(f"📍 Port: {port}")
    print(f"🔧 Environment: {os.getenv('ENVIRONMENT', 'production')}")
    print(f"💾 Database: {os.getenv('DATABASE_URL', 'sqlite:////app/data/assistant.db')}")

    # Import uvicorn
    try:
        import uvicorn
    except ImportError:
        print("❌ Error: uvicorn not installed")
        sys.exit(1)

    # Run the app
    try:
        uvicorn.run(
            "backend.src.main:app",
            host="0.0.0.0",
            port=port,
            log_level="info",
            access_log=True
        )
    except Exception as e:
        print(f"❌ Failed to start server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
