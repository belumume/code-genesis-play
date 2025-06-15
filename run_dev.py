
#!/usr/bin/env python3
"""
Development script to run both FastAPI backend and React frontend
"""
import subprocess
import sys
import time
import os
from pathlib import Path

def run_fastapi():
    """Run the FastAPI server"""
    try:
        print("🚀 Starting FastAPI server on http://localhost:8000")
        
        # Run FastAPI server
        subprocess.run([
            sys.executable, "-m", "uvicorn", 
            "src.genesis_engine.web_server:app",
            "--host", "0.0.0.0",
            "--port", "8000",
            "--reload"
        ], check=True)
        
    except subprocess.CalledProcessError as e:
        print(f"❌ FastAPI server failed: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("👋 FastAPI server stopped")

def run_react():
    """Run the React development server"""
    try:
        print("⚛️  Starting React dev server on http://localhost:8080")
        
        # Check if node_modules exists
        if not Path("node_modules").exists():
            print("📦 Installing npm dependencies...")
            subprocess.run(["npm", "install"], check=True)
        
        # Run React dev server
        subprocess.run(["npm", "run", "dev"], check=True)
        
    except subprocess.CalledProcessError as e:
        print(f"❌ React dev server failed: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("👋 React dev server stopped")

def main():
    """Main function to run both servers"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Run AI Genesis Engine development servers")
    parser.add_argument("--backend-only", action="store_true", help="Run only FastAPI backend")
    parser.add_argument("--frontend-only", action="store_true", help="Run only React frontend")
    
    args = parser.parse_args()
    
    print("""
    ╔══════════════════════════════════════════╗
    ║        AI GENESIS ENGINE DEV MODE        ║
    ║    Full-Stack Game Generation System     ║
    ╚══════════════════════════════════════════╝
    """)
    
    if args.backend_only:
        print("🔧 Running backend only...")
        run_fastapi()
    elif args.frontend_only:
        print("🔧 Running frontend only...")
        run_react()
    else:
        print("🔧 Starting both backend and frontend...")
        print("📡 FastAPI: http://localhost:8000")
        print("⚛️  React: http://localhost:8080")
        print("📚 API Docs: http://localhost:8000/docs")
        print("\n🚨 Run servers in separate terminals:")
        print("   python run_dev.py --backend-only")
        print("   python run_dev.py --frontend-only")
        print("\nOr use the run scripts directly:")
        print("   python run_server.py")
        print("   npm run dev")

if __name__ == "__main__":
    main()
