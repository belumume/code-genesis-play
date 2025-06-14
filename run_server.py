#!/usr/bin/env python3
"""
Run the AI Genesis Engine Web Server
Provides API endpoints for the React frontend.
"""
import sys
import uvicorn
try:
    from src.genesis_engine.config import settings, COMPETITION_NAME
except ImportError:
    # Handle running from different directory structures
    import sys
    sys.path.append('.')
    from src.genesis_engine.config import settings, COMPETITION_NAME

def main():
    """Start the FastAPI server."""
    print(f"""
    ╔══════════════════════════════════════════╗
    ║      AI GENESIS ENGINE WEB SERVER        ║
    ║    Transform Ideas into Playable Games   ║
    ╚══════════════════════════════════════════╝
    
    🚀 Starting server on http://{settings.server_host}:{settings.server_port}
    📡 API docs available at http://localhost:{settings.server_port}/docs
    🎮 Competition: {COMPETITION_NAME}
    🤖 Model: {settings.anthropic_model}
    """)
    
    # Run the server
    uvicorn.run(
        "src.genesis_engine.web_server:app",
        host=settings.server_host,
        port=settings.server_port,
        reload=True,  # Enable auto-reload in development
        log_level=settings.log_level.lower()
    )

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Server error: {e}")
        sys.exit(1) 