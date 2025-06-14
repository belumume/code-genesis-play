
"""
Memory management system for the Genesis Engine.
Handles persistent storage of design documents and project state.
"""
import json
import os
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime

class MemoryManager:
    """Manages persistent memory for the Genesis Engine."""
    
    def __init__(self, memory_dir: Optional[str] = None):
        if memory_dir:
            self.memory_dir = Path(memory_dir)
        else:
            self.memory_dir = Path.home() / ".genesis-engine" / "memory"
        
        self.memory_dir.mkdir(parents=True, exist_ok=True)
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    def store_document(self, doc_type: str, content: str, project_name: str) -> bool:
        """Store a generated document in memory."""
        try:
            session_dir = self.memory_dir / self.session_id / project_name
            session_dir.mkdir(parents=True, exist_ok=True)
            
            file_path = session_dir / f"{doc_type}.md"
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            # Also store metadata
            metadata = {
                "type": doc_type,
                "project": project_name,
                "timestamp": datetime.now().isoformat(),
                "session_id": self.session_id,
                "file_path": str(file_path)
            }
            
            metadata_path = session_dir / f"{doc_type}_meta.json"
            with open(metadata_path, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, indent=2)
            
            return True
            
        except Exception as e:
            print(f"Error storing document: {e}")
            return False
    
    def retrieve_document(self, doc_type: str, project_name: str) -> Optional[str]:
        """Retrieve a stored document from memory."""
        try:
            session_dir = self.memory_dir / self.session_id / project_name
            file_path = session_dir / f"{doc_type}.md"
            
            if file_path.exists():
                with open(file_path, 'r', encoding='utf-8') as f:
                    return f.read()
            
            return None
            
        except Exception as e:
            print(f"Error retrieving document: {e}")
            return None
    
    def store_project_state(self, project_name: str, state_data: Dict[str, Any]) -> bool:
        """Store the current state of a project."""
        try:
            session_dir = self.memory_dir / self.session_id / project_name
            session_dir.mkdir(parents=True, exist_ok=True)
            
            state_data['timestamp'] = datetime.now().isoformat()
            state_data['session_id'] = self.session_id
            
            state_path = session_dir / "project_state.json"
            with open(state_path, 'w', encoding='utf-8') as f:
                json.dump(state_data, f, indent=2)
            
            return True
            
        except Exception as e:
            print(f"Error storing project state: {e}")
            return False
    
    def get_project_state(self, project_name: str) -> Optional[Dict[str, Any]]:
        """Retrieve the current state of a project."""
        try:
            session_dir = self.memory_dir / self.session_id / project_name
            state_path = session_dir / "project_state.json"
            
            if state_path.exists():
                with open(state_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            
            return None
            
        except Exception as e:
            print(f"Error retrieving project state: {e}")
            return None
    
    def list_sessions(self) -> list:
        """List all stored sessions."""
        sessions = []
        try:
            for session_dir in self.memory_dir.iterdir():
                if session_dir.is_dir():
                    sessions.append({
                        'session_id': session_dir.name,
                        'created': datetime.fromtimestamp(session_dir.stat().st_ctime),
                        'projects': [p.name for p in session_dir.iterdir() if p.is_dir()]
                    })
        except Exception as e:
            print(f"Error listing sessions: {e}")
        
        return sorted(sessions, key=lambda x: x['created'], reverse=True)
    
    def cleanup_old_sessions(self, keep_last_n: int = 10):
        """Clean up old memory sessions, keeping only the most recent."""
        sessions = self.list_sessions()
        
        if len(sessions) > keep_last_n:
            for session in sessions[keep_last_n:]:
                session_path = self.memory_dir / session['session_id']
                try:
                    # Remove old session directory
                    import shutil
                    shutil.rmtree(session_path)
                except Exception as e:
                    print(f"Error cleaning up session {session['session_id']}: {e}")
