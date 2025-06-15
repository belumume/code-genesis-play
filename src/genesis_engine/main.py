"""
AI Genesis Engine - Main Entry Point v2.1
Transforms single-sentence prompts into complete, playable JavaScript/HTML5 games
using autonomous multi-agent collaboration.
"""
import sys
import argparse
import os
import uuid
from pathlib import Path
from typing import Optional
import json
from datetime import datetime
import asyncio

from .core.multi_agent_system import MultiAgentOrchestrator
from .core.logger import EngineLogger
from .core.memory import MemoryManager
from .utils.file_manager import FileManager

class GenesisEngine:
    """
    The main Genesis Engine orchestrator v2.1.
    Manages the multi-agent autonomous game generation process.
    """
    
    def __init__(self):
        self.logger = EngineLogger()
        self.memory = MemoryManager()
        self.file_manager = FileManager()
        self.multi_agent_orchestrator = MultiAgentOrchestrator(self.logger)
        
    async def run_async(self, prompt: str, output_dir: Optional[str] = None) -> bool:
        """
        Execute the complete Genesis Engine v2.1 workflow with multi-agent system.
        
        Args:
            prompt: The game concept description
            output_dir: Optional custom output directory
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            self.logger.header("🚀 AI GENESIS ENGINE v2.1 - MULTI-AGENT AUTONOMOUS SYSTEM")
            self.logger.info(f"Processing prompt: '{prompt}'")
            
            # Initialize project workspace
            project_name = self._generate_project_name(prompt)
            if output_dir:
                project_path = Path(output_dir) / project_name
            else:
                project_path = Path("generated_games") / project_name
                
            self.file_manager.setup_project_structure(project_path)
            self.logger.success(f"Project workspace created: {project_path}")
            
            # Generate unique session ID
            session_id = str(uuid.uuid4())[:8]
            
            # Start multi-agent generation session
            session = await self.multi_agent_orchestrator.start_generation_session(
                prompt=prompt,
                project_path=project_path,
                session_id=session_id
            )
            
            # Process the session through all agents
            success = await self.multi_agent_orchestrator.process_session(session_id)
            
            if success:
                self.logger.header("✨ MULTI-AGENT GENESIS COMPLETE!")
                self.logger.success(f"JavaScript/HTML5 game generated successfully!")
                self.logger.info(f"To play: Open {project_path}/game.html in your browser")
                
                # Print session summary
                status = self.multi_agent_orchestrator.get_session_status(session_id)
                self.logger.info(f"Debug cycles: {status['debug_cycles']}")
                self.logger.info(f"Multi-agent autonomous system demonstrated!")
                
                return True
            else:
                self.logger.error("Multi-agent generation failed")
                return False
                
        except Exception as e:
            self.logger.error(f"Genesis Engine v2.1 failed: {str(e)}")
            import traceback
            self.logger.error(f"Full traceback: {traceback.format_exc()}")
            return False
    
    def run(self, prompt: str, output_dir: Optional[str] = None) -> bool:
        """
        Synchronous wrapper for the async run method.
        """
        return asyncio.run(self.run_async(prompt, output_dir))
    
    async def run_with_websocket(self, prompt: str, output_dir: Optional[str] = None, websocket_logger=None) -> dict:
        """
        Execute the Genesis Engine with WebSocket logging for real-time updates.
        
        Returns:
            dict: Generation results with session information
        """
        try:
            # Set up WebSocket logging if provided
            if websocket_logger:
                self.logger.add_websocket_logger(websocket_logger)
            
            self.logger.header("🚀 AI GENESIS ENGINE v2.1 - MULTI-AGENT SYSTEM")
            self.logger.info(f"Processing prompt: '{prompt}'")
            
            # Initialize project workspace
            project_name = self._generate_project_name(prompt)
            if output_dir:
                project_path = Path(output_dir) / project_name
            else:
                project_path = Path("generated_games") / project_name
                
            self.file_manager.setup_project_structure(project_path)
            self.logger.success(f"Project workspace created: {project_path}")
            
            # Generate unique session ID
            session_id = str(uuid.uuid4())[:8]
            
            # Start multi-agent generation session
            session = await self.multi_agent_orchestrator.start_generation_session(
                prompt=prompt,
                project_path=project_path,
                session_id=session_id
            )
            
            # Process the session through all agents
            success = await self.multi_agent_orchestrator.process_session(session_id)
            
            # Get final session status
            final_status = self.multi_agent_orchestrator.get_session_status(session_id)
            
            if success:
                self.logger.header("✨ MULTI-AGENT GENESIS COMPLETE!")
                self.logger.success(f"JavaScript/HTML5 game generated successfully!")
                
                return {
                    "success": True,
                    "project_path": str(project_path),
                    "project_name": project_name,
                    "session_id": session_id,
                    "game_file": final_status.get("final_html_file"),
                    "debug_cycles": final_status.get("debug_cycles", 0),
                    "multi_agent_demo": True,
                    "output_format": "javascript_html5"
                }
            else:
                self.logger.error("Multi-agent generation failed")
                return {
                    "success": False,
                    "error": "Multi-agent generation failed",
                    "session_id": session_id,
                    "debug_cycles": final_status.get("debug_cycles", 0)
                }
                
        except Exception as e:
            self.logger.error(f"Genesis Engine v2.1 failed: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def _generate_project_name(self, prompt: str) -> str:
        """Generate a clean project name from the prompt."""
        # Extract key words and create a clean name
        words = prompt.lower().split()
        # Remove common words
        stop_words = {'a', 'an', 'the', 'with', 'where', 'about', 'game', 'simple'}
        key_words = [w for w in words if w not in stop_words and w.isalpha()][:3]
        
        if not key_words:
            key_words = ['js', 'game']
            
        timestamp = datetime.now().strftime("%H%M")
        return "_".join(key_words) + f"_js_{timestamp}"
    
    def _verify_game_structure(self, project_path: Path) -> bool:
        """Verify the generated game has all required files."""
        required_files = [
            "game.html",  # JavaScript/HTML5 game (changed from main.py)
            "GDD.md",
            "TECH_PLAN.md", 
            "README.md"
        ]
        
        for file_name in required_files:
            if not (project_path / file_name).exists():
                self.logger.error(f"Missing required file: {file_name}")
                return False
        
        return True

def main():
    """Main entry point for the Genesis Engine CLI."""
    parser = argparse.ArgumentParser(
        description="AI Genesis Engine v2.1 - Generate JavaScript/HTML5 games with multi-agent AI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python -m genesis_engine "A space shooter where you fight alien invaders"
  python -m genesis_engine "A platformer with a jumping character collecting coins" --output ./my_games

Multi-Agent System:
  - Architect Agent: Designs game mechanics and technical plans
  - Engineer Agent: Generates JavaScript/HTML5 code
  - Sentry Agent: Tests code automatically
  - Debugger Agent: Fixes errors autonomously

Output: Complete JavaScript/HTML5 games playable in browser
        """
    )
    
    parser.add_argument(
        "prompt",
        help="Single-sentence description of the game to generate"
    )
    
    parser.add_argument(
        "--output", "-o",
        help="Output directory for generated games (default: ./generated_games)"
    )
    
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose logging"
    )
    
    args = parser.parse_args()
    
    if not args.prompt.strip():
        print("Error: Please provide a game concept prompt")
        sys.exit(1)
    
    # Initialize and run the Genesis Engine v2.1
    engine = GenesisEngine()
    success = engine.run(args.prompt, args.output)
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
