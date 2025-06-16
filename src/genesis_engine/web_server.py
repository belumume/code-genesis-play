"""
FastAPI Web Server for AI Genesis Engine v2.1
Bridges the React frontend with the Multi-Agent Python Genesis Engine backend.
Supports autonomous self-correcting JavaScript/HTML5 game generation.
"""
import asyncio
import json
import logging
import os
import uuid
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
from collections import defaultdict
import time

from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse, PlainTextResponse
from pydantic import BaseModel, validator

from .main import GenesisEngine
from .core.logger import EngineLogger

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# FastAPI app initialization
app = FastAPI(
    title="AI Genesis Engine v2.1 API",
    description="Transform single-sentence prompts into complete, playable JavaScript/HTML5 games using autonomous multi-agent AI",
    version="2.1.0"
)

# Get allowed origins from environment
ALLOWED_ORIGINS = [
    "http://localhost:8080", 
    "http://127.0.0.1:8080",
    "http://localhost:5173",
    "https://lovable.app",
    "https://code-genesis-play.lovable.app",
    "https://*.lovable.app"
]

# Add custom frontend URL if provided
custom_frontend = os.getenv("FRONTEND_URL", "").strip()
if custom_frontend:
    ALLOWED_ORIGINS.append(custom_frontend)

# CORS middleware with specific origins only
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# Rate limiting implementation
class RateLimiter:
    def __init__(self, requests_per_minute: int = 60):
        self.requests_per_minute = requests_per_minute
        self.requests = defaultdict(list)
    
    def is_allowed(self, client_ip: str) -> bool:
        now = time.time()
        minute_ago = now - 60
        
        # Clean old requests
        self.requests[client_ip] = [
            req_time for req_time in self.requests[client_ip] 
            if req_time > minute_ago
        ]
        
        # Check if limit exceeded
        if len(self.requests[client_ip]) >= self.requests_per_minute:
            return False
        
        # Add current request
        self.requests[client_ip].append(now)
        return True

# Initialize rate limiter
rate_limiter = RateLimiter(requests_per_minute=30)

# Middleware for security headers
@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    # Rate limiting check
    client_ip = request.client.host
    if not rate_limiter.is_allowed(client_ip):
        return JSONResponse(
            status_code=429,
            content={"error": "Rate limit exceeded. Please try again later."}
        )
    
    response = await call_next(request)
    
    # Add security headers
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    response.headers["Content-Security-Policy"] = "default-src 'self' https://cdn.jsdelivr.net; script-src 'self' 'unsafe-inline' 'unsafe-eval' https://cdn.jsdelivr.net; style-src 'self' 'unsafe-inline';"
    
    return response

# Request/Response models with validation
class GameGenerationRequest(BaseModel):
    prompt: str
    output_dir: Optional[str] = None
    
    @validator('prompt')
    def validate_prompt(cls, v):
        # Sanitize input
        v = v.strip()
        
        # Check length
        if len(v) < 10:
            raise ValueError('Prompt must be at least 10 characters')
        if len(v) > 500:
            raise ValueError('Prompt must be less than 500 characters')
        
        # Remove any potential script injection
        v = re.sub(r'<[^>]*>', '', v)
        v = re.sub(r'[<>\"\'`]', '', v)
        
        # Check for suspicious patterns
        suspicious_patterns = [
            r'javascript:', r'data:', r'vbscript:', r'onload=',
            r'onerror=', r'onclick=', r'<script', r'</script'
        ]
        for pattern in suspicious_patterns:
            if re.search(pattern, v, re.IGNORECASE):
                raise ValueError('Invalid characters in prompt')
        
        return v

class GameGenerationResponse(BaseModel):
    success: bool
    project_name: Optional[str] = None
    project_path: Optional[str] = None
    session_id: Optional[str] = None
    game_file: Optional[str] = None
    debug_cycles: Optional[int] = None
    multi_agent_demo: Optional[bool] = None
    output_format: Optional[str] = None
    error: Optional[str] = None

# Global storage for WebSocket connections and active generations
active_connections: Dict[str, WebSocket] = {}
active_generations: Dict[str, Dict] = {}

class WebSocketLogger:
    """Logger that sends real-time updates via WebSocket."""
    
    def __init__(self, websocket: WebSocket, connection_id: str):
        self.websocket = websocket
        self.connection_id = connection_id
        
    async def send_update(self, level: str, message: str, data: Optional[Dict] = None):
        """Send a log update via WebSocket."""
        try:
            update = {
                "type": "log",
                "level": level,
                "message": message,
                "timestamp": datetime.now().isoformat(),
                "data": data or {}
            }
            await self.websocket.send_text(json.dumps(update))
        except Exception as e:
            logger.warning(f"Failed to send WebSocket update: {str(e)}")

# API Endpoints

@app.get("/")
async def root():
    """Root endpoint for basic health checks."""
    return {"message": "AI Genesis Engine API", "status": "healthy", "docs": "/docs"}

@app.get("/api/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "version": "2.1.0",
        "features": {
            "multi_agent_system": True,
            "javascript_output": True,
            "autonomous_debugging": True,
            "real_time_updates": True
        },
        "ai_available": True,
        "model": "claude-4-opus",
        "timestamp": datetime.now().isoformat()
    }

@app.post("/api/generate", response_model=GameGenerationResponse)
async def generate_game(request: GameGenerationRequest):
    """
    Generate a JavaScript/HTML5 game using the multi-agent system.
    This is a synchronous endpoint - for real-time updates, use WebSocket.
    """
    try:
        logger.info(f"Received generation request: {request.prompt}")
        
        # Additional validation
        if not request.prompt or len(request.prompt.strip()) < 10:
            raise HTTPException(status_code=400, detail="Prompt too short")
        
        # Initialize Genesis Engine
        engine = GenesisEngine()
        
        # Run generation (this will be synchronous for this endpoint)
        result = await engine.run_with_websocket(
            prompt=request.prompt,
            output_dir=request.output_dir
        )
        
        return GameGenerationResponse(
            success=result.get("success", False),
            project_name=result.get("project_name"),
            project_path=result.get("project_path"),
            session_id=result.get("session_id"),
            game_file=result.get("game_file"),
            debug_cycles=result.get("debug_cycles", 0),
            multi_agent_demo=result.get("multi_agent_demo", True),
            output_format=result.get("output_format", "javascript_html5"),
            error=result.get("error")
        )
        
    except Exception as e:
        logger.error(f"Generation failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.websocket("/ws/generate")
async def websocket_generate(websocket: WebSocket):
    """
    WebSocket endpoint for real-time game generation with multi-agent progress updates.
    """
    await websocket.accept()
    connection_id = str(uuid.uuid4())[:8]
    active_connections[connection_id] = websocket
    
    try:
        logger.info(f"WebSocket connection established: {connection_id}")
        
        # Wait for generation request
        data = await websocket.receive_text()
        request_data = json.loads(data)
        prompt = request_data.get("prompt", "").strip()
        
        # Validate prompt
        if not prompt:
            await websocket.send_text(json.dumps({
                "type": "error",
                "message": "Empty prompt provided"
            }))
            return
        
        # Sanitize prompt
        prompt = re.sub(r'<[^>]*>', '', prompt)
        prompt = re.sub(r'[<>\"\'`]', '', prompt)
        
        if len(prompt) < 10 or len(prompt) > 500:
            await websocket.send_text(json.dumps({
                "type": "error",
                "message": "Prompt must be between 10 and 500 characters"
            }))
            return
        
        # Create WebSocket logger
        ws_logger = WebSocketLogger(websocket, connection_id)
        
        # Send initial update
        await ws_logger.send_update("info", f"🚀 Starting multi-agent generation for: '{prompt}'")
        await ws_logger.send_update("info", "🤖 Initializing Architect, Engineer, Sentry, and Debugger agents...")
        
        # Initialize Genesis Engine
        engine = GenesisEngine()
        
        # Set up the logger to send WebSocket updates
        engine.logger.add_websocket_logger = lambda logger_obj: setattr(logger_obj, 'ws_logger', ws_logger)
        
        # Run generation with WebSocket logging
        result = await engine.run_with_websocket(
            prompt=prompt,
            output_dir=request_data.get("output_dir"),
            websocket_logger=ws_logger
        )
        
        # Send final result
        await websocket.send_text(json.dumps({
            "type": "result",
            "success": result.get("success", False),
            "project_name": result.get("project_name"),
            "project_path": result.get("project_path"),
            "session_id": result.get("session_id"),
            "game_file": result.get("game_file"),
            "debug_cycles": result.get("debug_cycles", 0),
            "multi_agent_demo": result.get("multi_agent_demo", True),
            "output_format": result.get("output_format", "javascript_html5"),
            "error": result.get("error")
        }))
        
        # Store generation info
        active_generations[connection_id] = result
        
    except WebSocketDisconnect:
        logger.info(f"WebSocket disconnected: {connection_id}")
    except Exception as e:
        logger.error(f"WebSocket error: {str(e)}")
        try:
            await websocket.send_text(json.dumps({
                "type": "error",
                "message": str(e)
            }))
        except:
            pass
    finally:
        if connection_id in active_connections:
            del active_connections[connection_id]
        if connection_id in active_generations:
            del active_generations[connection_id]

@app.get("/api/games")
async def list_games():
    """List all generated games."""
    try:
        games_dir = Path("generated_games")
        if not games_dir.exists():
            return {"games": []}
        
        games = []
        for game_dir in games_dir.iterdir():
            if game_dir.is_dir():
                game_html = game_dir / "game.html"  # Changed from main.py
                readme_file = game_dir / "README.md"
                
                game_info = {
                    "name": game_dir.name,
                    "path": str(game_dir),
                    "has_game_file": game_html.exists(),
                    "has_readme": readme_file.exists(),
                    "created": datetime.fromtimestamp(game_dir.stat().st_ctime).isoformat(),
                    "type": "javascript_html5"  # New output format
                }
                
                # Try to extract prompt from README
                if readme_file.exists():
                    try:
                        readme_content = readme_file.read_text(encoding='utf-8')
                        # Extract prompt from README
                        for line in readme_content.split('\n'):
                            if '**Prompt**:' in line:
                                game_info["prompt"] = line.split('**Prompt**:')[1].strip()
                                break
                    except:
                        pass
                
                games.append(game_info)
        
        # Sort by creation date, newest first
        games.sort(key=lambda x: x["created"], reverse=True)
        
        return {"games": games[:20]}  # Limit to 20 most recent
    except Exception as e:
        logger.error(f"Failed to list games: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/games/{game_name}/download")
async def download_game(game_name: str):
    """Download a generated game as HTML file."""
    try:
        game_dir = Path("generated_games") / game_name
        game_file = game_dir / "game.html"  # Changed from main.py
        
        if not game_file.exists():
            raise HTTPException(status_code=404, detail="Game file not found")
        
        return FileResponse(
            path=str(game_file),
            filename=f"{game_name}.html",
            media_type="text/html"
        )
    except Exception as e:
        logger.error(f"Download failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/games/{game_name}/play")
async def get_game_content(game_name: str):
    """Get the HTML content of a game for in-browser playing."""
    try:
        game_dir = Path("generated_games") / game_name
        game_file = game_dir / "game.html"
        
        if not game_file.exists():
            raise HTTPException(status_code=404, detail="Game file not found")
        
        # Read the HTML content
        html_content = game_file.read_text(encoding='utf-8')
        
        return PlainTextResponse(content=html_content, media_type="text/html")
        
    except Exception as e:
        logger.error(f"Failed to get game content: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/games/{game_name}/files")
async def list_game_files(game_name: str):
    """List all files in a generated game directory."""
    try:
        game_dir = Path("generated_games") / game_name
        if not game_dir.exists():
            raise HTTPException(status_code=404, detail="Game directory not found")
        
        files = []
        for file_path in game_dir.iterdir():
            if file_path.is_file():
                files.append({
                    "name": file_path.name,
                    "size": file_path.stat().st_size,
                    "modified": datetime.fromtimestamp(file_path.stat().st_mtime).isoformat()
                })
        
        return {"files": files}
    except Exception as e:
        logger.error(f"Failed to list game files: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/games/{game_name}/files/{file_name}")
async def get_game_file(game_name: str, file_name: str):
    """Get the contents of a specific game file."""
    try:
        game_dir = Path("generated_games") / game_name
        file_path = game_dir / file_name
        
        if not file_path.exists():
            raise HTTPException(status_code=404, detail="File not found")
        
        # Determine content type
        if file_name.endswith('.html'):
            media_type = "text/html"
        elif file_name.endswith('.md'):
            media_type = "text/markdown"
        elif file_name.endswith('.js'):
            media_type = "application/javascript"
        else:
            media_type = "text/plain"
        
        content = file_path.read_text(encoding='utf-8')
        return PlainTextResponse(content=content, media_type=media_type)
        
    except Exception as e:
        logger.error(f"Failed to get file: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/status")
async def get_server_status():
    """Get current server status and active connections."""
    return {
        "active_connections": len(active_connections),
        "active_generations": len(active_generations),
        "server_version": "2.1.0",
        "multi_agent_system": True,
        "output_format": "javascript_html5",
        "autonomous_debugging": True
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
