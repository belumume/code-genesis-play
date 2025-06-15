#!/usr/bin/env python3
"""
Production server for AI Genesis Engine FastAPI
Disables auto-reload for stable production deployment.
"""
import sys
import uvicorn
import os

def main():
    """Start the FastAPI server in production mode."""
    print(f"""
    ╔══════════════════════════════════════════╗
    ║   AI GENESIS ENGINE PRODUCTION SERVER    ║
    ║    Transform Ideas into Playable Games   ║
    ╚══════════════════════════════════════════╝
    
    🚀 Starting production server...
    🌐 Host: 0.0.0.0
    🔌 Port: {os.getenv('PORT', 8000)}
    📡 API docs: /docs
    🎮 Competition: $40,000 AI Showdown
    🤖 AI Model: Claude 4 Opus with Sonnet fallback
    """)
    
    # Get port from environment variable (for cloud deployments)
    port = int(os.getenv('PORT', 8000))
    
    # Run the server WITHOUT reload for production stability
    uvicorn.run(
        "src.genesis_engine.web_server:app",
        host="0.0.0.0",
        port=port,
        reload=False,  # Disable auto-reload in production
        log_level="info",
        access_log=True,
        workers=1  # Single worker for now, can increase based on needs
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