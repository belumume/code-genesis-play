
"""
Core AI Agent for the Genesis Engine.
Handles all AI reasoning, document generation, and code creation.
"""
from pathlib import Path
from typing import Optional, Dict, Any
import re

from .logger import EngineLogger
from .memory import MemoryManager
from .ai_client import AIClient

class GenesisAgent:
    """
    The core AI agent responsible for autonomous game generation.
    Handles conceptualization, planning, and code execution phases.
    """
    
    def __init__(self, logger: EngineLogger, memory: MemoryManager):
        self.logger = logger
        self.memory = memory
        self.ai_client = AIClient()
        self.current_project = None
        
    def generate_game_design_document(self, prompt: str, project_path: Path) -> bool:
        """
        Generate a comprehensive Game Design Document from the prompt.
        
        Args:
            prompt: The user's game concept
            project_path: Path to the project directory
            
        Returns:
            bool: Success status
        """
        try:
            self.logger.thinking("Analyzing game concept and extracting core mechanics...")
            
            self.logger.step("Document Generation", "Creating Game Design Document")
            
            # Generate comprehensive GDD using AI
            gdd_content = self.ai_client.generate_game_design_document(prompt)
            
            # Save to project directory
            gdd_path = project_path / "GDD.md"
            with open(gdd_path, 'w', encoding='utf-8') as f:
                f.write(gdd_content)
            
            # Store in memory
            project_name = project_path.name
            self.memory.store_document("GDD", gdd_content, project_name)
            
            self.logger.success("Game Design Document generated")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to generate GDD: {str(e)}")
            return False
    
    def generate_technical_plan(self, project_path: Path) -> bool:
        """Generate the technical implementation plan."""
        try:
            self.logger.step("Technical Planning", "Analyzing architecture requirements")
            
            # Read the GDD to understand requirements
            gdd_path = project_path / "GDD.md"
            with open(gdd_path, 'r', encoding='utf-8') as f:
                gdd_content = f.read()
            
            tech_plan = self.ai_client.generate_technical_plan(gdd_content)
            
            # Save technical plan
            tech_path = project_path / "TECH_PLAN.md"
            with open(tech_path, 'w', encoding='utf-8') as f:
                f.write(tech_plan)
            
            # Store in memory
            project_name = project_path.name
            self.memory.store_document("TECH_PLAN", tech_plan, project_name)
            
            self.logger.success("Technical plan generated")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to generate technical plan: {str(e)}")
            return False
    
    def generate_asset_specifications(self, project_path: Path) -> bool:
        """Generate detailed asset specifications."""
        try:
            self.logger.step("Asset Planning", "Defining visual and audio requirements")
            
            # Read GDD for context
            gdd_path = project_path / "GDD.md"
            with open(gdd_path, 'r', encoding='utf-8') as f:
                gdd_content = f.read()
            
            asset_specs = self.ai_client.generate_asset_specifications(gdd_content)
            
            # Save asset specifications
            assets_path = project_path / "ASSETS.md"
            with open(assets_path, 'w', encoding='utf-8') as f:
                f.write(asset_specs)
            
            # Store in memory
            project_name = project_path.name
            self.memory.store_document("ASSETS", asset_specs, project_name)
            
            self.logger.success("Asset specifications generated")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to generate asset specs: {str(e)}")
            return False
    
    def generate_game_code(self, project_path: Path) -> bool:
        """Generate the complete game code based on technical plan."""
        try:
            self.logger.step("Code Generation", "Creating game implementation")
            
            # Read planning documents
            tech_path = project_path / "TECH_PLAN.md"
            gdd_path = project_path / "GDD.md"
            
            with open(tech_path, 'r', encoding='utf-8') as f:
                tech_plan = f.read()
            with open(gdd_path, 'r', encoding='utf-8') as f:
                gdd_content = f.read()
            
            # Generate main game file using AI
            main_code = self.ai_client.generate_game_code(gdd_content, tech_plan)
            
            main_path = project_path / "main.py"
            with open(main_path, 'w', encoding='utf-8') as f:
                f.write(main_code)
            
            self.logger.success("Game code generated")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to generate game code: {str(e)}")
            return False

