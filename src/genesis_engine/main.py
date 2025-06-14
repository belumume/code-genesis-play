
"""
AI Genesis Engine - Main Entry Point
Transforms single-sentence prompts into complete, playable 2D games.
"""
import sys
import argparse
import os
from pathlib import Path
from typing import Optional
import json
from datetime import datetime

from .core.agent import GenesisAgent
from .core.logger import EngineLogger
from .core.memory import MemoryManager
from .utils.file_manager import FileManager

class GenesisEngine:
    """
    The main Genesis Engine orchestrator.
    Manages the end-to-end process from prompt to playable game.
    """
    
    def __init__(self):
        self.logger = EngineLogger()
        self.memory = MemoryManager()
        self.file_manager = FileManager()
        self.agent = GenesisAgent(self.logger, self.memory)
        
    def run(self, prompt: str, output_dir: Optional[str] = None) -> bool:
        """
        Execute the complete Genesis Engine workflow.
        
        Args:
            prompt: The game concept description
            output_dir: Optional custom output directory
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            self.logger.header("🚀 AI GENESIS ENGINE v1.0")
            self.logger.info(f"Processing prompt: '{prompt}'")
            
            # Initialize project workspace
            project_name = self._generate_project_name(prompt)
            if output_dir:
                project_path = Path(output_dir) / project_name
            else:
                project_path = Path("generated_games") / project_name
                
            self.file_manager.setup_project_structure(project_path)
            self.logger.success(f"Project workspace created: {project_path}")
            
            # Phase 1: Conceptualize
            self.logger.phase("DESIGN", "Conceptualizing game design...")
            gdd_success = self.agent.generate_game_design_document(prompt, project_path)
            if not gdd_success:
                self.logger.error("Failed to generate Game Design Document")
                return False
            
            # Phase 2: Plan
            self.logger.phase("PLANNING", "Creating technical specifications...")
            tech_success = self.agent.generate_technical_plan(project_path)
            assets_success = self.agent.generate_asset_specifications(project_path)
            
            if not (tech_success and assets_success):
                self.logger.error("Failed to generate planning documents")
                return False
            
            # Phase 3: Execute
            self.logger.phase("CODING", "Generating game code...")
            code_success = self.agent.generate_game_code(project_path)
            if not code_success:
                self.logger.error("Failed to generate game code")
                return False
            
            # Final verification
            self.logger.phase("VERIFICATION", "Verifying generated game...")
            if self._verify_game_structure(project_path):
                self.logger.header("✨ GENESIS COMPLETE!")
                self.logger.success(f"Game generated successfully!")
                self.logger.info(f"To play: cd {project_path} && python main.py")
                return True
            else:
                self.logger.error("Game structure verification failed")
                return False
                
        except Exception as e:
            self.logger.error(f"Genesis Engine failed: {str(e)}")
            return False
    
    def _generate_project_name(self, prompt: str) -> str:
        """Generate a clean project name from the prompt."""
        # Extract key words and create a clean name
        words = prompt.lower().split()
        # Remove common words
        stop_words = {'a', 'an', 'the', 'with', 'where', 'about', 'game', 'simple'}
        key_words = [w for w in words if w not in stop_words and w.isalpha()][:3]
        
        if not key_words:
            key_words = ['generated', 'game']
            
        timestamp = datetime.now().strftime("%H%M")
        return "_".join(key_words) + f"_{timestamp}"
    
    def _verify_game_structure(self, project_path: Path) -> bool:
        """Verify the generated game has all required files."""
        required_files = [
            "main.py",
            "GDD.md",
            "TECH_PLAN.md", 
            "ASSETS.md"
        ]
        
        for file_name in required_files:
            if not (project_path / file_name).exists():
                self.logger.error(f"Missing required file: {file_name}")
                return False
        
        return True

def main():
    """Main entry point for the Genesis Engine CLI."""
    parser = argparse.ArgumentParser(
        description="AI Genesis Engine - Generate complete 2D games from prompts",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python -m genesis_engine "A space shooter where you fight alien invaders"
  python -m genesis_engine "A platformer with a jumping character collecting coins" --output ./my_games
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
    
    # Initialize and run the Genesis Engine
    engine = GenesisEngine()
    success = engine.run(args.prompt, args.output)
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
