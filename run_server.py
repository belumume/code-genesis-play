
#!/usr/bin/env python3
"""
Run the AI Genesis Engine FastAPI Server
Provides API endpoints for the React frontend.
"""
import sys
import uvicorn

def main():
    """Start the FastAPI server."""
    print(f"""
    ╔══════════════════════════════════════════╗
    ║      AI GENESIS ENGINE WEB SERVER        ║
    ║    Transform Ideas into Playable Games   ║
    ╚══════════════════════════════════════════╝
    
    🚀 Starting server on http://localhost:8000
    📡 API docs available at http://localhost:8000/docs
    🎮 Competition: $40,000 AI Showdown
    🤖 AI Model: Claude Sonnet 4 (optimized for cost/performance)
    """)
    
    # Run the server
    uvicorn.run(
        "src.genesis_engine.web_server:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # Enable auto-reload in development
        log_level="info"
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
