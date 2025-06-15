
"""
FastAPI Web Server for AI Genesis Engine
Bridges the React frontend with the Python Genesis Engine backend.
"""
import asyncio
import json
import logging
import os
import uuid
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel

from .main import GenesisEngine
from .core.logger import EngineLogger

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# FastAPI app initialization
app = FastAPI(
    title="AI Genesis Engine API",
    description="Transform single-sentence prompts into complete, playable 2D games",
    version="1.0.0"
)

# CORS middleware for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080", "http://127.0.0.1:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request/Response models
class GameGenerationRequest(BaseModel):
    prompt: str
    output_dir: Optional[str] = None

class GameGenerationResponse(BaseModel):
    session_id: str
    status: str
    message: str

class ProgressUpdate(BaseModel):
    session_id: str
    phase: str
    step: str
    progress: float
    message: str
    timestamp: str

# Global session management
active_sessions: Dict[str, Dict] = {}
websocket_connections: Dict[str, WebSocket] = {}

class WebSocketLogger(EngineLogger):
    """Custom logger that sends updates via WebSocket"""
    
    def __init__(self, session_id: str):
        super().__init__()
        self.session_id = session_id
    
    def _send_progress(self, phase: str, step: str, progress: float, message: str):
        """Send progress update via WebSocket"""
        if self.session_id in websocket_connections:
            update = ProgressUpdate(
                session_id=self.session_id,
                phase=phase,
                step=step,
                progress=progress,
                message=message,
                timestamp=datetime.now().isoformat()
            )
            
            # Store update in session for later retrieval
            if self.session_id in active_sessions:
                if 'progress_updates' not in active_sessions[self.session_id]:
                    active_sessions[self.session_id]['progress_updates'] = []
                active_sessions[self.session_id]['progress_updates'].append(update.dict())
            
            # Send via WebSocket
            try:
                asyncio.create_task(
                    websocket_connections[self.session_id].send_text(update.json())
                )
            except Exception as e:
                logger.error(f"Failed to send WebSocket update: {e}")
    
    def phase(self, phase_name: str, description: str):
        """Override phase method to send WebSocket updates"""
        super().phase(phase_name, description)
        progress = 0.0
        if phase_name == "DESIGN":
            progress = 0.1
        elif phase_name == "PLANNING":
            progress = 0.3
        elif phase_name == "CODING":
            progress = 0.6
        elif phase_name == "VERIFICATION":
            progress = 0.9
        
        self._send_progress(phase_name, "starting", progress, description)
    
    def step(self, category: str, description: str):
        """Override step method to send WebSocket updates"""
        super().step(category, description)
        self._send_progress(category, "processing", 0.0, description)
    
    def success(self, message: str):
        """Override success method to send WebSocket updates"""
        super().success(message)
        self._send_progress("SUCCESS", "completed", 1.0, message)
    
    def error(self, message: str):
        """Override error method to send WebSocket updates"""
        super().error(message)
        self._send_progress("ERROR", "failed", 0.0, message)

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "AI Genesis Engine API is running", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "active_sessions": len(active_sessions),
        "websocket_connections": len(websocket_connections)
    }

@app.post("/generate", response_model=GameGenerationResponse)
async def start_game_generation(request: GameGenerationRequest):
    """Start a new game generation session"""
    try:
        # Create new session
        session_id = str(uuid.uuid4())
        
        # Validate prompt
        if not request.prompt or not request.prompt.strip():
            raise HTTPException(status_code=400, detail="Prompt cannot be empty")
        
        # Initialize session
        active_sessions[session_id] = {
            "prompt": request.prompt,
            "status": "started",
            "created_at": datetime.now().isoformat(),
            "progress_updates": [],
            "output_dir": request.output_dir
        }
        
        logger.info(f"Started generation session {session_id} with prompt: {request.prompt}")
        
        return GameGenerationResponse(
            session_id=session_id,
            status="started",
            message=f"Game generation started for prompt: {request.prompt}"
        )
        
    except Exception as e:
        logger.error(f"Failed to start generation: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.websocket("/ws/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    """WebSocket endpoint for real-time progress updates"""
    await websocket.accept()
    websocket_connections[session_id] = websocket
    
    try:
        # Check if session exists
        if session_id not in active_sessions:
            await websocket.send_text(json.dumps({
                "error": "Session not found",
                "session_id": session_id
            }))
            return
        
        session = active_sessions[session_id]
        
        # Send any existing progress updates
        for update in session.get('progress_updates', []):
            await websocket.send_text(json.dumps(update))
        
        # Start generation if not already started
        if session['status'] == 'started':
            session['status'] = 'generating'
            
            # Run generation in background
            asyncio.create_task(run_generation(session_id, session['prompt'], session.get('output_dir')))
        
        # Keep connection alive
        while True:
            try:
                # Wait for any message from client (ping/pong)
                await websocket.receive_text()
            except WebSocketDisconnect:
                break
                
    except WebSocketDisconnect:
        logger.info(f"WebSocket disconnected for session {session_id}")
    except Exception as e:
        logger.error(f"WebSocket error for session {session_id}: {e}")
        await websocket.send_text(json.dumps({
            "error": str(e),
            "session_id": session_id
        }))
    finally:
        # Clean up connection
        if session_id in websocket_connections:
            del websocket_connections[session_id]

async def run_generation(session_id: str, prompt: str, output_dir: Optional[str] = None):
    """Run the actual game generation process"""
    try:
        # Create custom logger for this session
        ws_logger = WebSocketLogger(session_id)
        
        # Initialize Genesis Engine with custom logger
        engine = GenesisEngine()
        engine.logger = ws_logger
        
        # Update session status
        active_sessions[session_id]['status'] = 'generating'
        
        # Run generation
        success = engine.run(prompt, output_dir)
        
        # Update final status
        if success:
            active_sessions[session_id]['status'] = 'completed'
            active_sessions[session_id]['completed_at'] = datetime.now().isoformat()
            
            # Send completion update
            ws_logger._send_progress("COMPLETED", "finished", 1.0, "Game generation completed successfully!")
        else:
            active_sessions[session_id]['status'] = 'failed'
            active_sessions[session_id]['failed_at'] = datetime.now().isoformat()
            
            # Send failure update
            ws_logger._send_progress("FAILED", "error", 0.0, "Game generation failed")
            
    except Exception as e:
        logger.error(f"Generation failed for session {session_id}: {e}")
        active_sessions[session_id]['status'] = 'failed'
        active_sessions[session_id]['error'] = str(e)
        
        # Send error update
        if session_id in websocket_connections:
            try:
                await websocket_connections[session_id].send_text(json.dumps({
                    "error": str(e),
                    "session_id": session_id,
                    "phase": "ERROR",
                    "progress": 0.0
                }))
            except:
                pass

@app.get("/sessions/{session_id}")
async def get_session_status(session_id: str):
    """Get the current status of a generation session"""
    if session_id not in active_sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    return active_sessions[session_id]

@app.get("/sessions")
async def list_sessions():
    """List all active sessions"""
    return {
        "sessions": list(active_sessions.keys()),
        "total": len(active_sessions)
    }

@app.delete("/sessions/{session_id}")
async def cleanup_session(session_id: str):
    """Clean up a completed session"""
    if session_id in active_sessions:
        del active_sessions[session_id]
    
    if session_id in websocket_connections:
        try:
            await websocket_connections[session_id].close()
        except:
            pass
        del websocket_connections[session_id]
    
    return {"message": f"Session {session_id} cleaned up"}

@app.get("/games")
async def list_generated_games():
    """List all generated games"""
    games_dir = Path("generated_games")
    if not games_dir.exists():
        return {"games": []}
    
    games = []
    for game_dir in games_dir.iterdir():
        if game_dir.is_dir():
            main_py = game_dir / "main.py"
            gdd_md = game_dir / "GDD.md"
            
            if main_py.exists():
                games.append({
                    "name": game_dir.name,
                    "path": str(game_dir),
                    "has_main": True,
                    "has_gdd": gdd_md.exists(),
                    "created": datetime.fromtimestamp(game_dir.stat().st_ctime).isoformat()
                })
    
    return {"games": games}

@app.get("/games/{game_name}/download")
async def download_game(game_name: str):
    """Download a generated game"""
    game_path = Path("generated_games") / game_name / "main.py"
    
    if not game_path.exists():
        raise HTTPException(status_code=404, detail="Game not found")
    
    return FileResponse(
        path=str(game_path),
        filename=f"{game_name}_main.py",
        media_type="text/plain"
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
