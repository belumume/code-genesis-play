"""
FastAPI Web Server for AI Genesis Engine
Provides REST API and WebSocket endpoints for the React frontend.
"""
import os
import json
import asyncio
from pathlib import Path
from typing import Optional, Dict, Any
from datetime import datetime
import uuid

from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel, Field

from .main import GenesisEngine
from .core.logger import EngineLogger
from .core.ai_client import AIClient
try:
    from .config import settings, COMPETITION_NAME, SHOWCASE_FEATURES
except ImportError:
    # Handle absolute import when running as a script
    from config import settings, COMPETITION_NAME, SHOWCASE_FEATURES

# Create FastAPI app
app = FastAPI(
    title="AI Genesis Engine API",
    description="Transform prompts into playable games using Claude AI",
    version="1.0.0"
)

# Configure CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request/Response models
class GenerateGameRequest(BaseModel):
    prompt: str = Field(..., min_length=10, max_length=500, description="Game concept description")
    session_id: Optional[str] = Field(None, description="Session ID for tracking")

class GenerateGameResponse(BaseModel):
    session_id: str
    project_path: str
    status: str
    message: str

class GameStatus(BaseModel):
    session_id: str
    status: str
    phase: str
    progress: int
    message: str
    project_path: Optional[str] = None
    error: Optional[str] = None

# In-memory session storage (in production, use Redis or similar)
sessions: Dict[str, Dict[str, Any]] = {}

# WebSocket connection manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}

    async def connect(self, websocket: WebSocket, session_id: str):
        await websocket.accept()
        self.active_connections[session_id] = websocket

    def disconnect(self, session_id: str):
        if session_id in self.active_connections:
            del self.active_connections[session_id]

    async def send_update(self, session_id: str, message: dict):
        if session_id in self.active_connections:
            try:
                await self.active_connections[session_id].send_json(message)
            except:
                # Connection might be closed
                self.disconnect(session_id)

manager = ConnectionManager()

# Custom logger that sends updates via WebSocket
class WebSocketLogger(EngineLogger):
    def __init__(self, session_id: str):
        super().__init__()
        self.session_id = session_id
        self.phase = "initializing"
        self.progress = 0

    async def _send_update(self, level: str, message: str):
        update = {
            "type": "log",
            "level": level,
            "message": message,
            "phase": self.phase,
            "progress": self.progress,
            "timestamp": datetime.now().isoformat()
        }
        await manager.send_update(self.session_id, update)
        
        # Update session state
        if self.session_id in sessions:
            sessions[self.session_id]["logs"].append(update)
            sessions[self.session_id]["phase"] = self.phase
            sessions[self.session_id]["progress"] = self.progress

    def info(self, message: str):
        super().info(message)
        asyncio.create_task(self._send_update("info", message))

    def success(self, message: str):
        super().success(message)
        asyncio.create_task(self._send_update("success", message))

    def error(self, message: str):
        super().error(message)
        asyncio.create_task(self._send_update("error", message))

    def phase(self, phase_name: str, description: str):
        super().phase(phase_name, description)
        self.phase = phase_name.lower()
        # Update progress based on phase
        phase_progress = {
            "design": 20,
            "planning": 40,
            "coding": 70,
            "verification": 90,
            "complete": 100
        }
        self.progress = phase_progress.get(self.phase, self.progress)
        asyncio.create_task(self._send_update("phase", f"{phase_name}: {description}"))

# API Endpoints
@app.get("/")
async def root():
    """Health check endpoint."""
    return {"status": "ok", "service": "AI Genesis Engine API"}

@app.get("/api/health")
async def health_check():
    """Detailed health check."""
    ai_client = AIClient()
    return {
        "status": "healthy",
        "ai_available": not ai_client.use_mock,
        "model": ai_client.model if not ai_client.use_mock else "mock",
        "version": "1.0.0"
    }

@app.post("/api/generate", response_model=GenerateGameResponse)
async def generate_game(request: GenerateGameRequest):
    """Start game generation process."""
    session_id = request.session_id or str(uuid.uuid4())
    
    # Initialize session
    sessions[session_id] = {
        "prompt": request.prompt,
        "status": "starting",
        "phase": "initializing",
        "progress": 0,
        "started_at": datetime.now().isoformat(),
        "logs": [],
        "project_path": None,
        "error": None
    }
    
    # Start generation in background
    asyncio.create_task(run_generation(session_id, request.prompt))
    
    return GenerateGameResponse(
        session_id=session_id,
        project_path="",
        status="started",
        message=f"Game generation started for: {request.prompt}"
    )

@app.get("/api/status/{session_id}", response_model=GameStatus)
async def get_status(session_id: str):
    """Get generation status."""
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    session = sessions[session_id]
    return GameStatus(
        session_id=session_id,
        status=session["status"],
        phase=session["phase"],
        progress=session["progress"],
        message=f"Phase: {session['phase']}",
        project_path=session.get("project_path"),
        error=session.get("error")
    )

@app.get("/api/download/{session_id}")
async def download_game(session_id: str):
    """Download generated game as ZIP."""
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    session = sessions[session_id]
    if session["status"] != "completed":
        raise HTTPException(status_code=400, detail="Game generation not completed")
    
    project_path = session.get("project_path")
    if not project_path or not Path(project_path).exists():
        raise HTTPException(status_code=404, detail="Generated game not found")
    
    # Create ZIP file
    import shutil
    zip_path = f"/tmp/{session_id}.zip"
    shutil.make_archive(f"/tmp/{session_id}", 'zip', project_path)
    
    return FileResponse(
        path=zip_path,
        media_type='application/zip',
        filename=f"game_{session_id}.zip"
    )

@app.websocket("/ws/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    """WebSocket endpoint for real-time updates."""
    await manager.connect(websocket, session_id)
    
    try:
        # Send initial status
        if session_id in sessions:
            await websocket.send_json({
                "type": "connected",
                "session": sessions[session_id]
            })
        
        # Keep connection alive
        while True:
            await asyncio.sleep(30)
            await websocket.send_json({"type": "ping"})
            
    except WebSocketDisconnect:
        manager.disconnect(session_id)

# Background task to run game generation
async def run_generation(session_id: str, prompt: str):
    """Run game generation with WebSocket updates."""
    try:
        # Create custom logger for this session
        logger = WebSocketLogger(session_id)
        
        # Create custom engine with WebSocket logger
        engine = GenesisEngine()
        engine.logger = logger
        engine.agent.logger = logger
        
        # Update status
        sessions[session_id]["status"] = "generating"
        
        # Run generation
        output_dir = Path("test_output")
        success = await asyncio.to_thread(engine.run, prompt, str(output_dir))
        
        if success:
            # Find the generated project path
            project_name = engine._generate_project_name(prompt)
            project_path = output_dir / project_name
            
            sessions[session_id]["status"] = "completed"
            sessions[session_id]["project_path"] = str(project_path)
            sessions[session_id]["progress"] = 100
            
            await manager.send_update(session_id, {
                "type": "completed",
                "project_path": str(project_path),
                "message": "Game generation completed successfully!"
            })
        else:
            sessions[session_id]["status"] = "failed"
            sessions[session_id]["error"] = "Game generation failed"
            
            await manager.send_update(session_id, {
                "type": "error",
                "message": "Game generation failed"
            })
            
    except Exception as e:
        sessions[session_id]["status"] = "error"
        sessions[session_id]["error"] = str(e)
        
        await manager.send_update(session_id, {
            "type": "error",
            "message": f"Error: {str(e)}"
        })

# Error handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail}
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error", "detail": str(exc)}
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 