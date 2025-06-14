
"""
Core AI Agent for the Genesis Engine.
Handles all AI reasoning, document generation, and code creation.
"""
from pathlib import Path
from typing import Optional, Dict, Any
import re

from .logger import EngineLogger
from .memory import MemoryManager

class GenesisAgent:
    """
    The core AI agent responsible for autonomous game generation.
    Handles conceptualization, planning, and code execution phases.
    """
    
    def __init__(self, logger: EngineLogger, memory: MemoryManager):
        self.logger = logger
        self.memory = memory
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
            
            # Analyze the prompt to extract game elements
            game_analysis = self._analyze_game_prompt(prompt)
            
            self.logger.step("Document Generation", "Creating Game Design Document")
            
            # Generate comprehensive GDD
            gdd_content = self._create_gdd_content(prompt, game_analysis)
            
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
            
            tech_plan = self._create_technical_plan(gdd_content)
            
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
            
            asset_specs = self._create_asset_specifications(gdd_content)
            
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
            
            # Generate main game file
            main_code = self._generate_main_game_code(gdd_content, tech_plan)
            
            main_path = project_path / "main.py"
            with open(main_path, 'w', encoding='utf-8') as f:
                f.write(main_code)
            
            # Generate additional game modules if needed
            self._generate_additional_modules(project_path, tech_plan)
            
            self.logger.success("Game code generated")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to generate game code: {str(e)}")
            return False
    
    def _analyze_game_prompt(self, prompt: str) -> Dict[str, Any]:
        """Analyze the game prompt to extract key elements."""
        analysis = {
            "genre": "action",
            "mechanics": [],
            "theme": "abstract",
            "complexity": "simple"
        }
        
        prompt_lower = prompt.lower()
        
        # Detect genre
        if any(word in prompt_lower for word in ["platform", "jump", "ledge"]):
            analysis["genre"] = "platformer"
        elif any(word in prompt_lower for word in ["shoot", "laser", "enemy", "invader"]):
            analysis["genre"] = "shooter"
        elif any(word in prompt_lower for word in ["puzzle", "solve", "match"]):
            analysis["genre"] = "puzzle"
        elif any(word in prompt_lower for word in ["collect", "coin", "gem", "item"]):
            analysis["mechanics"].append("collection")
        
        # Detect theme
        if any(word in prompt_lower for word in ["space", "alien", "star", "rocket"]):
            analysis["theme"] = "space"
        elif any(word in prompt_lower for word in ["medieval", "knight", "castle", "sword"]):
            analysis["theme"] = "medieval"
        elif any(word in prompt_lower for word in ["pixel", "retro", "8-bit"]):
            analysis["theme"] = "retro"
        
        return analysis
    
    def _create_gdd_content(self, prompt: str, analysis: Dict[str, Any]) -> str:
        """Create the Game Design Document content."""
        return f"""# Game Design Document

## Original Concept
"{prompt}"

## Game Overview
**Genre:** {analysis['genre'].title()}  
**Theme:** {analysis['theme'].title()}  
**Target Complexity:** {analysis['complexity'].title()}  

## Core Mechanics
- Basic player movement (arrow keys or WASD)
- Collision detection with environment
- Win/lose conditions
{f"- {', '.join(analysis['mechanics'])}" if analysis['mechanics'] else ""}

## Game Loop
1. Initialize game world
2. Handle player input
3. Update game state
4. Check win/lose conditions
5. Render frame
6. Repeat

## Controls
- **Movement:** Arrow keys or WASD
- **Action:** Spacebar (if needed)
- **Quit:** ESC or close window

## Win Condition
Player successfully completes the primary objective defined in the game concept.

## Lose Condition
Player fails to meet the objective within constraints (lives, time, etc.).

## Technical Requirements
- **Engine:** Python + Pygame
- **Resolution:** 800x600 pixels
- **Frame Rate:** 60 FPS target
- **Graphics:** Simple geometric shapes (rectangles, circles)
- **Sound:** Optional placeholder sounds

## Implementation Priority
1. Basic window and game loop
2. Player character and movement
3. Basic environment/obstacles
4. Core game mechanics
5. Win/lose detection
6. Polish and refinement

---
*Generated by Genesis Engine v1.0*
"""
    
    def _create_technical_plan(self, gdd_content: str) -> str:
        """Create the technical implementation plan."""
        return """# Technical Implementation Plan

## Architecture Overview
The game will be built using a component-based architecture with clear separation of concerns.

## File Structure
```
main.py              # Entry point and main game loop
game/
├── __init__.py      # Package initialization
├── player.py        # Player character class
├── world.py         # Game world and environment
├── entities.py      # Game objects and entities
└── utils.py         # Utility functions
```

## Core Classes

### GameEngine (main.py)
- Initialize Pygame
- Manage main game loop
- Handle events and input
- Coordinate between systems

### Player (game/player.py)
- Player position and movement
- Input handling
- Collision detection
- State management

### World (game/world.py)
- Level geometry
- Background rendering
- Environmental objects
- Spatial organization

### Entity (game/entities.py)
- Base class for game objects
- Position, velocity, collision bounds
- Update and render methods

## Implementation Sequence
1. **Phase 1:** Basic window and input handling
2. **Phase 2:** Player character with movement
3. **Phase 3:** World geometry and collision
4. **Phase 4:** Game mechanics implementation
5. **Phase 5:** Win/lose conditions
6. **Phase 6:** Polish and optimization

## Dependencies
- pygame: Game engine and graphics
- Standard library only for everything else

## Placeholder Graphics
- Player: Blue rectangle (20x30 pixels)
- Environment: Green rectangles for platforms
- Collectibles: Yellow circles
- Enemies: Red rectangles

---
*Generated by Genesis Engine v1.0*
"""
    
    def _create_asset_specifications(self, gdd_content: str) -> str:
        """Create detailed asset specifications."""
        return """# Asset Specifications

## Visual Assets

### Player Character
**Description:** The main character controlled by the player  
**Type:** Sprite/Rectangle  
**Size:** 20x30 pixels  
**Color:** Blue (#0066CC)  
**Animation:** Optional walking animation (2-3 frames)  
**Format:** PNG or simple colored rectangle  

### Environment
**Platforms/Ground:** Green rectangles (#228B22)  
**Walls:** Dark gray rectangles (#696969)  
**Background:** Light blue (#87CEEB) or solid color  

### Interactive Objects
**Collectibles:** Yellow circles (#FFD700), 16x16 pixels  
**Enemies:** Red rectangles (#DC143C), 24x24 pixels  
**Goal/Exit:** Bright green rectangle (#00FF00), 32x32 pixels  

### UI Elements
**Score Display:** White text on dark background  
**Lives/Health:** Simple icons or text  
**Game Over Screen:** Centered text with restart option  

## Audio Assets

### Sound Effects
**Jump:** Short, light "boing" sound (0.2s)  
**Collect Item:** Pleasant "ping" or "ding" (0.1s)  
**Enemy Hit:** Brief "thud" or "hit" sound (0.1s)  
**Game Over:** Descending tone sequence (0.5s)  
**Victory:** Ascending celebratory melody (1.0s)  

### Background Music
**Game Theme:** Simple, looping 8-bit style melody  
**Length:** 30-60 seconds, seamless loop  
**Tempo:** Medium-paced, non-intrusive  
**Format:** OGG or WAV  

## Implementation Notes
- All assets start as placeholders (colored shapes)
- Actual assets can be created/sourced later
- Maintain consistent color palette
- Keep file sizes small for quick loading
- Ensure all assets are properly licensed

---
*Generated by Genesis Engine v1.0*
"""
    
    def _generate_main_game_code(self, gdd_content: str, tech_plan: str) -> str:
        """Generate the main game code file."""
        return '''#!/usr/bin/env python3
"""
Auto-generated game by Genesis Engine v1.0
A complete, playable 2D game created from a simple prompt.
"""

import pygame
import sys
from typing import Tuple, List
from dataclasses import dataclass
from enum import Enum

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 102, 204)
GREEN = (34, 139, 34)
RED = (220, 20, 60)
YELLOW = (255, 215, 0)
LIGHT_BLUE = (135, 206, 235)

class GameState(Enum):
    PLAYING = "playing"
    GAME_OVER = "game_over"
    VICTORY = "victory"

@dataclass
class Vector2:
    x: float
    y: float
    
    def __add__(self, other):
        return Vector2(self.x + other.x, self.y + other.y)
    
    def __mul__(self, scalar: float):
        return Vector2(self.x * scalar, self.y * scalar)

class Player:
    """Player character with movement and collision."""
    
    def __init__(self, x: float, y: float):
        self.position = Vector2(x, y)
        self.velocity = Vector2(0, 0)
        self.size = Vector2(20, 30)
        self.speed = 200
        self.jump_power = 300
        self.on_ground = False
        self.color = BLUE
        
    def update(self, dt: float, platforms: List['Platform']):
        """Update player physics and handle input."""
        # Handle input
        keys = pygame.key.get_pressed()
        
        # Horizontal movement
        self.velocity.x = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.velocity.x = -self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.velocity.x = self.speed
            
        # Jumping
        if (keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_w]) and self.on_ground:
            self.velocity.y = -self.jump_power
            self.on_ground = False
        
        # Apply gravity
        self.velocity.y += 800 * dt  # Gravity
        
        # Update position
        self.position = self.position + self.velocity * dt
        
        # Handle collisions
        self._handle_collisions(platforms)
        
        # Keep player on screen
        self.position.x = max(0, min(SCREEN_WIDTH - self.size.x, self.position.x))
    
    def _handle_collisions(self, platforms: List['Platform']):
        """Handle collision with platforms."""
        player_rect = pygame.Rect(self.position.x, self.position.y, self.size.x, self.size.y)
        
        for platform in platforms:
            if player_rect.colliderect(platform.rect):
                # Landing on top of platform
                if self.velocity.y > 0 and self.position.y < platform.rect.top:
                    self.position.y = platform.rect.top - self.size.y
                    self.velocity.y = 0
                    self.on_ground = True
    
    def get_rect(self) -> pygame.Rect:
        """Get player rectangle for collision detection."""
        return pygame.Rect(self.position.x, self.position.y, self.size.x, self.size.y)
    
    def render(self, screen: pygame.Surface):
        """Render the player."""
        pygame.draw.rect(screen, self.color, self.get_rect())

class Platform:
    """Static platform for jumping and collision."""
    
    def __init__(self, x: float, y: float, width: float, height: float):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = GREEN
    
    def render(self, screen: pygame.Surface):
        """Render the platform."""
        pygame.draw.rect(screen, self.color, self.rect)

class Collectible:
    """Items for the player to collect."""
    
    def __init__(self, x: float, y: float):
        self.position = Vector2(x, y)
        self.size = 16
        self.collected = False
        self.color = YELLOW
    
    def get_rect(self) -> pygame.Rect:
        """Get collectible rectangle."""
        return pygame.Rect(self.position.x - self.size//2, self.position.y - self.size//2, 
                          self.size, self.size)
    
    def render(self, screen: pygame.Surface):
        """Render the collectible."""
        if not self.collected:
            pygame.draw.circle(screen, self.color, 
                             (int(self.position.x), int(self.position.y)), self.size//2)

class Game:
    """Main game class managing all game systems."""
    
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Genesis Engine Game")
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = GameState.PLAYING
        
        # Initialize game objects
        self.player = Player(100, 400)
        self.platforms = self._create_platforms()
        self.collectibles = self._create_collectibles()
        self.score = 0
        self.font = pygame.font.Font(None, 36)
        
    def _create_platforms(self) -> List[Platform]:
        """Create the game level platforms."""
        platforms = [
            # Ground platforms
            Platform(0, SCREEN_HEIGHT - 40, SCREEN_WIDTH, 40),
            # Floating platforms
            Platform(200, 450, 150, 20),
            Platform(400, 350, 150, 20),
            Platform(600, 250, 150, 20),
            Platform(150, 200, 100, 20),
        ]
        return platforms
    
    def _create_collectibles(self) -> List[Collectible]:
        """Create collectible items."""
        collectibles = [
            Collectible(275, 420),
            Collectible(475, 320),
            Collectible(675, 220),
            Collectible(200, 170),
            Collectible(700, 100),
        ]
        return collectibles
    
    def handle_events(self):
        """Handle pygame events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_r and self.state != GameState.PLAYING:
                    self._restart_game()
    
    def update(self, dt: float):
        """Update all game systems."""
        if self.state == GameState.PLAYING:
            # Update player
            self.player.update(dt, self.platforms)
            
            # Check collectible collisions
            player_rect = self.player.get_rect()
            for collectible in self.collectibles:
                if not collectible.collected and player_rect.colliderect(collectible.get_rect()):
                    collectible.collected = True
                    self.score += 10
            
            # Check win condition
            if all(c.collected for c in self.collectibles):
                self.state = GameState.VICTORY
            
            # Check lose condition (fall off screen)
            if self.player.position.y > SCREEN_HEIGHT:
                self.state = GameState.GAME_OVER
    
    def render(self):
        """Render all game objects."""
        # Clear screen
        self.screen.fill(LIGHT_BLUE)
        
        # Render platforms
        for platform in self.platforms:
            platform.render(self.screen)
        
        # Render collectibles
        for collectible in self.collectibles:
            collectible.render(self.screen)
        
        # Render player
        if self.state == GameState.PLAYING:
            self.player.render(self.screen)
        
        # Render UI
        self._render_ui()
        
        # Update display
        pygame.display.flip()
    
    def _render_ui(self):
        """Render user interface elements."""
        # Score
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))
        
        # Game state messages
        if self.state == GameState.VICTORY:
            victory_text = self.font.render("VICTORY! Press R to restart", True, WHITE)
            text_rect = victory_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
            pygame.draw.rect(self.screen, BLACK, text_rect.inflate(20, 10))
            self.screen.blit(victory_text, text_rect)
        
        elif self.state == GameState.GAME_OVER:
            game_over_text = self.font.render("GAME OVER! Press R to restart", True, WHITE)
            text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
            pygame.draw.rect(self.screen, BLACK, text_rect.inflate(20, 10))
            self.screen.blit(game_over_text, text_rect)
    
    def _restart_game(self):
        """Restart the game to initial state."""
        self.player = Player(100, 400)
        self.collectibles = self._create_collectibles()
        self.score = 0
        self.state = GameState.PLAYING
    
    def run(self):
        """Main game loop."""
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0  # Delta time in seconds
            
            self.handle_events()
            self.update(dt)
            self.render()
        
        pygame.quit()
        sys.exit()

def main():
    """Entry point for the game."""
    game = Game()
    game.run()

if __name__ == "__main__":
    main()
'''
    
    def _generate_additional_modules(self, project_path: Path, tech_plan: str):
        """Generate any additional required modules."""
        # For this implementation, everything is in main.py
        # In a more complex version, we would generate separate modules
        pass
