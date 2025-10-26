"""Startup script for Railway deployment."""
import os
import sys

def main():
    """Start the application with proper configuration."""
    # Debug: Print raw PORT value
    port_raw = os.getenv("PORT", "8000")
    print(f"🔍 DEBUG: Raw PORT environment variable: '{port_raw}'")
    print(f"🔍 DEBUG: Type of PORT: {type(port_raw)}")

    # Convert to integer
    try:
        port = int(port_raw)
        print(f"✅ Successfully parsed port as integer: {port}")
    except ValueError as e:
        print(f"❌ ERROR: Could not convert PORT to integer: {e}")
        print(f"❌ PORT value was: '{port_raw}'")
        # Fallback to 8000
        port = 8000
        print(f"⚠️  Using fallback port: {port}")

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
        print(f"🏃 Running uvicorn on 0.0.0.0:{port}")
        uvicorn.run(
            "backend.src.main:app",
            host="0.0.0.0",
            port=port,
            log_level="info",
            access_log=True
        )
    except Exception as e:
        print(f"❌ Failed to start server: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
