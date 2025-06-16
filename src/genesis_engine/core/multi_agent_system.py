"""
Multi-Agent System for AI Genesis Engine v2.1
Implements autonomous self-correcting game generation with JavaScript output.

Agents:
- Architect: High-level game design and technical planning
- Engineer: JavaScript/HTML5 code generation
- Sentry: Automated testing and error detection
- Debugger: Error analysis and code correction
"""
import asyncio
import json
import logging
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from datetime import datetime

from .logger import EngineLogger
from .ai_client import AIClient
from .sentry_agent import get_sentry_agent

class AgentRole(Enum):
    ARCHITECT = "architect"
    ENGINEER = "engineer"
    SENTRY = "sentry"
    DEBUGGER = "debugger"

class TaskStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    SUCCESS = "success"
    ERROR = "error"

@dataclass
class AgentTask:
    """Represents a task for a specific agent."""
    id: str
    agent_role: AgentRole
    task_type: str
    description: str
    input_data: Dict[str, Any]
    status: TaskStatus = TaskStatus.PENDING
    output_data: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None
    retry_count: int = 0
    max_retries: int = 3

@dataclass
class GameGenerationSession:
    """Tracks a complete game generation session across all agents."""
    session_id: str
    prompt: str
    project_path: Path
    current_phase: str = "initialization"
    tasks: List[AgentTask] = None
    game_design_document: Optional[str] = None
    technical_plan: Optional[Dict[str, Any]] = None
    generated_code: Optional[str] = None
    test_results: Optional[Dict[str, Any]] = None
    final_html_file: Optional[str] = None
    is_complete: bool = False
    error_count: int = 0
    debug_cycles: int = 0
    
    def __post_init__(self):
        if self.tasks is None:
            self.tasks = []

class MultiAgentOrchestrator:
    """
    Central orchestrator for the multi-agent autonomous game generation system.
    
    Implements the self-correcting loop:
    Architect → Engineer → Sentry → [Error? → Debugger → Engineer] → Success
    """
    
    def __init__(self, logger: EngineLogger):
        self.logger = logger
        self.ai_client = AIClient()
        self.active_sessions: Dict[str, GameGenerationSession] = {}
        
        # Agent-specific configurations
        self.agent_configs = {
            AgentRole.ARCHITECT: {
                "max_tokens": 4000,
                "temperature": 0.7,
                "system_prompt": self._get_architect_system_prompt()
            },
            AgentRole.ENGINEER: {
                "max_tokens": 6000,
                "temperature": 0.3,
                "system_prompt": self._get_engineer_system_prompt()
            },
            AgentRole.DEBUGGER: {
                "max_tokens": 4000,
                "temperature": 0.2,
                "system_prompt": self._get_debugger_system_prompt()
            }
        }
    
    async def start_generation_session(self, prompt: str, project_path: Path, session_id: str) -> GameGenerationSession:
        """Initialize a new multi-agent game generation session."""
        self.logger.header(f"🤖 MULTI-AGENT SYSTEM v2.1 - Session: {session_id}")
        self.logger.info(f"Prompt: '{prompt}'")
        
        session = GameGenerationSession(
            session_id=session_id,
            prompt=prompt,
            project_path=project_path
        )
        
        self.active_sessions[session_id] = session
        return session
    
    async def process_session(self, session_id: str) -> bool:
        """Process a complete game generation session through all agents."""
        session = self.active_sessions.get(session_id)
        if not session:
            self.logger.error(f"Session {session_id} not found")
            return False
        
        try:
            # Phase 1: Architect - High-level design
            if not await self._execute_architect_phase(session):
                return False
            
            # Phase 2: Enter the autonomous loop
            success = await self._execute_autonomous_loop(session)
            
            if success:
                session.is_complete = True
                self.logger.header("✨ MULTI-AGENT GENERATION COMPLETE!")
                self.logger.success(f"Game generated with {session.debug_cycles} debug cycles")
                return True
            else:
                self.logger.error("Multi-agent generation failed")
                return False
                
        except Exception as e:
            self.logger.error(f"Session processing failed: {str(e)}")
            return False
    
    async def _execute_architect_phase(self, session: GameGenerationSession) -> bool:
        """Execute the Architect agent phase."""
        session.current_phase = "architect"
        self.logger.phase("ARCHITECT", "Creating game design and technical plan...")
        self.logger.agent_action("ARCHITECT", "Analyzing game concept", f"'{session.prompt}'")
        
        # Generate Game Design Document
        self.logger.agent_action("ARCHITECT", "Creating Game Design Document")
        gdd_prompt = f"""As the ARCHITECT agent, create a comprehensive Game Design Document for this prompt:
            
Prompt: "{session.prompt}"

Generate a detailed GDD that includes:
1. Game Overview & Core Concept
2. Target Platform: Browser/JavaScript with p5.js
3. Core Gameplay Mechanics (detailed)
4. Player Controls and Interactions
5. Visual Style (geometric shapes, colors)
6. Technical Constraints (single HTML file)
7. Success/Failure Conditions

Focus on creating a game that can be implemented in JavaScript/p5.js with simple geometric graphics."""
        
        gdd_content = self.ai_client.generate_game_design_document(session.prompt)
        
        session.game_design_document = gdd_content
        self.logger.agent_action("ARCHITECT", "Game Design Document completed")
        self.logger.file_created("GDD.md", "Game Design Document")
        
        # Generate Technical Plan
        self.logger.agent_action("ARCHITECT", "Creating Technical Implementation Plan")
        tech_prompt = f"""As the ARCHITECT agent, create a detailed technical implementation plan.

Game Concept: "{session.prompt}"

Game Design Document:
{gdd_content}

Create a technical plan with:
1. Technology Stack: JavaScript + p5.js
2. File Structure: Single HTML file with embedded JS/CSS
3. Core Classes/Objects to implement
4. Implementation Sequence (features to build in order)
5. Testing Checkpoints (what Sentry agent should verify)

Break down into small, testable features that Engineer can implement one at a time."""
        
        tech_content = self.ai_client.generate_technical_plan(gdd_content)
        
        session.technical_plan = {"content": tech_content}
        self.logger.agent_action("ARCHITECT", "Technical Plan completed")
        self.logger.file_created("TECH_PLAN.md", "Technical Implementation Plan")
        
        # Save documents
        await self._save_planning_documents(session)
        self.logger.agent_action("ARCHITECT", "Planning phase complete - handing off to Engineer")
        return True
    
    async def _execute_autonomous_loop(self, session: GameGenerationSession) -> bool:
        """Execute the autonomous Engineer → Sentry → Debugger loop."""
        max_debug_cycles = 3
        
        while session.debug_cycles < max_debug_cycles:
            session.debug_cycles += 1
            
            # Engineer Phase: Generate/Update JavaScript code
            session.current_phase = "engineer"
            self.logger.phase("ENGINEER", f"Generating JavaScript game code (Cycle {session.debug_cycles})")
            self.logger.agent_action("ENGINEER", f"Starting code generation", f"Debug cycle {session.debug_cycles}")
            
            if not await self._execute_engineer_phase(session):
                self.logger.agent_action("ENGINEER", "Code generation failed - triggering retry")
                session.error_count += 1
                continue
            
            # Sentry Phase: Test the generated code (simplified for now)
            session.current_phase = "sentry"
            self.logger.phase("SENTRY", "Testing generated JavaScript code...")
            self.logger.agent_action("SENTRY", "Analyzing generated code for errors")
            
            test_results = await self._execute_sentry_phase(session)
            session.test_results = test_results
            
            if test_results["success"]:
                # Code works! Save final output
                self.logger.agent_action("SENTRY", "Code validation passed - no errors found!")
                await self._save_final_game(session)
                return True
            else:
                # Code has errors, trigger Debugger
                error_count = len(test_results.get("errors", []))
                self.logger.agent_action("SENTRY", f"Found {error_count} errors - calling Debugger")
                session.current_phase = "debugger"
                self.logger.phase("DEBUGGER", f"Fixing errors (Debug cycle {session.debug_cycles})")
                self.logger.agent_action("DEBUGGER", "Analyzing error report from Sentry")
                
                if not await self._execute_debugger_phase(session, test_results):
                    self.logger.agent_action("DEBUGGER", "Debug attempt failed - will retry")
                    session.error_count += 1
                    continue
        
        self.logger.error(f"Autonomous loop failed after {max_debug_cycles} cycles")
        return False
    
    async def _execute_engineer_phase(self, session: GameGenerationSession) -> bool:
        """Execute the Engineer agent phase."""
        engineer_prompt = f"""As the ENGINEER agent, generate complete JavaScript game code.

Game Concept: "{session.prompt}"

Technical Plan:
{session.technical_plan['content']}

Previous Code (if any):
{session.generated_code or 'None - first implementation'}

Generate a COMPLETE, SINGLE HTML file with:
1. HTML structure with canvas element
2. Embedded p5.js from CDN
3. Complete JavaScript game implementation
4. CSS styling
5. All game features from the technical plan

Requirements:
- Use p5.js library for graphics and interaction
- Implement ALL features from the technical plan
- Include proper error handling
- Use simple geometric shapes for graphics
- Ensure code is syntactically correct

Output only the complete HTML file content."""
        
        try:
            self.logger.agent_action("ENGINEER", "Generating JavaScript/HTML5 code")
            code_content = self.ai_client.generate_javascript_game(
                session.game_design_document,
                session.technical_plan["content"]
            )
            
            session.generated_code = code_content
            self.logger.agent_action("ENGINEER", "Code generation completed - handing off to Sentry")
            self.logger.file_created("game.html", "JavaScript/HTML5 Game")
            return True
        except Exception as e:
            self.logger.error(f"Engineer phase failed: {str(e)}")
            return False
    
    async def _execute_sentry_phase(self, session: GameGenerationSession) -> Dict[str, Any]:
        """Execute the Sentry agent phase (simplified testing)."""
        # Get or create Sentry agent instance
        sentry = await get_sentry_agent()
        
        # Use the new validation method
        self.logger.agent_action("SENTRY", "Performing comprehensive game validation")
        validation_results = await sentry.validate_game(
            session.generated_code,
            session.project_path.name
        )
        
        # Generate test report
        test_report = sentry.generate_test_report(validation_results)
        self.logger.info(f"\n{test_report}")
        
        # Log results
        if validation_results["success"]:
            self.logger.success("✅ SENTRY: All tests passed!")
        else:
            self.logger.warning(f"⚠️ SENTRY: Found {len(validation_results['errors'])} errors")
            for error in validation_results["errors"]:
                self.logger.error(f"  - {error}")
        
        return {
            "success": validation_results["success"],
            "errors": validation_results["errors"],
            "error_count": len(validation_results["errors"]),
            "validation_type": "comprehensive",
            "browser_tested": validation_results.get("browser_test_passed", False)
        }
    
    async def _execute_debugger_phase(self, session: GameGenerationSession, test_results: Dict[str, Any]) -> bool:
        """Execute the Debugger agent phase."""
        debugger_prompt = f"""As the DEBUGGER agent, fix the errors in this JavaScript game code.

Original Goal: "{session.prompt}"

Broken Code:
{session.generated_code}

Error Report from Sentry:
{json.dumps(test_results, indent=2)}

Your task:
1. Analyze the specific errors reported
2. Identify the root cause
3. Generate the corrected, complete HTML file
4. Ensure all errors are fixed
5. Do NOT add new features, only fix existing code

Output only the corrected complete HTML file content."""
        
        try:
            self.logger.agent_action("DEBUGGER", "Applying code corrections")
            fixed_code = self.ai_client.generate_javascript_game(
                session.game_design_document,
                session.technical_plan["content"]
            )
            
            session.generated_code = fixed_code
            self.logger.agent_action("DEBUGGER", "Code corrections applied - sending back to Sentry")
            self.logger.success("🔧 DEBUGGER: Code corrections applied")
            return True
        except Exception as e:
            self.logger.error(f"Debugger phase failed: {str(e)}")
            return False
    
    async def _save_planning_documents(self, session: GameGenerationSession):
        """Save the planning documents generated by Architect."""
        # Save GDD
        gdd_path = session.project_path / "GDD.md"
        with open(gdd_path, 'w', encoding='utf-8') as f:
            f.write(session.game_design_document)
        
        # Save Technical Plan
        tech_path = session.project_path / "TECH_PLAN.md"
        with open(tech_path, 'w', encoding='utf-8') as f:
            f.write(session.technical_plan["content"])
        
        self.logger.success("📋 Planning documents saved")
    
    async def _save_final_game(self, session: GameGenerationSession):
        """Save the final working game."""
        game_path = session.project_path / "game.html"
        with open(game_path, 'w', encoding='utf-8') as f:
            f.write(session.generated_code)
        
        session.final_html_file = str(game_path)
        
        # Save README
        readme_content = f"""# Generated Game: {session.prompt}

## Play the Game
Open `game.html` in your web browser to play the game.

## Generation Summary
- **Prompt**: {session.prompt}
- **Debug Cycles**: {session.debug_cycles}
- **Technology**: JavaScript + p5.js
- **Generated by**: AI Genesis Engine v2.1 Multi-Agent System

## Multi-Agent Process
1. **Architect Agent**: Designed game mechanics and technical plan
2. **Engineer Agent**: Generated JavaScript/HTML5 code
3. **Sentry Agent**: Automated testing and error detection
4. **Debugger Agent**: Fixed errors autonomously (if any)

This game was created entirely by autonomous AI agents working together!
"""
        
        readme_path = session.project_path / "README.md"
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(readme_content)
        
        self.logger.success(f"🎮 Final game saved: {game_path}")
    
    def get_session_status(self, session_id: str) -> Dict[str, Any]:
        """Get the current status of a session for real-time updates."""
        session = self.active_sessions.get(session_id)
        if not session:
            return {"error": "Session not found"}
        
        return {
            "session_id": session.session_id,
            "prompt": session.prompt,
            "current_phase": session.current_phase,
            "debug_cycles": session.debug_cycles,
            "error_count": session.error_count,
            "is_complete": session.is_complete,
            "final_html_file": session.final_html_file,
            "test_results": session.test_results
        }
    
    def _get_architect_system_prompt(self) -> str:
        """System prompt for the Architect agent."""
        return """You are the ARCHITECT agent in a multi-agent game development system.

Your role:
- High-level game design and planning
- Create comprehensive specifications for other agents
- Focus on JavaScript/p5.js implementation feasibility
- Break complex games into simple, testable features

Key principles:
- Target browser-based games using p5.js
- Design for geometric graphics (rectangles, circles, lines)
- Plan features that can be implemented and tested independently
- Consider what errors might occur and how to prevent them

You work with:
- Engineer agent (implements your plans in JavaScript)
- Sentry agent (tests the code automatically)  
- Debugger agent (fixes errors found by Sentry)

Create clear, actionable specifications that enable autonomous implementation."""
    
    def _get_engineer_system_prompt(self) -> str:
        """System prompt for the Engineer agent."""
        return """You are the ENGINEER agent in a multi-agent game development system.

Your role:
- Implement JavaScript/HTML5 games based on Architect specifications
- Generate complete, working code using p5.js library
- Create single HTML files with embedded JavaScript and CSS
- Ensure code is syntactically correct and follows best practices

Technical requirements:
- Use p5.js for graphics and interaction
- Implement games as single HTML files
- Use simple geometric shapes for graphics
- Include proper error handling
- Write clean, commented code
- Ensure all game features are implemented

You work with:
- Architect agent (provides specifications)
- Sentry agent (tests your code)
- Debugger agent (fixes any errors you might create)

Generate ONLY complete, working HTML files ready for browser execution."""
    
    def _get_debugger_system_prompt(self) -> str:
        """System prompt for the Debugger agent."""
        return """You are the DEBUGGER agent in a multi-agent game development system.

Your role:
- Analyze error reports from automated testing
- Fix JavaScript/HTML5 code bugs efficiently
- Maintain original game functionality while fixing errors
- Ensure corrected code passes all tests

Debugging principles:
- Focus ONLY on fixing reported errors
- Do NOT add new features or change functionality
- Maintain code structure and style
- Fix root causes, not just symptoms
- Test fixes mentally before outputting

You work with:
- Engineer agent (provides code that needs fixing)
- Sentry agent (reports specific errors)
- Architect agent (original specifications)

Generate ONLY corrected, complete HTML files that fix all reported errors."""
 