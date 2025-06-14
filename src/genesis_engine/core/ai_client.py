"""
AI Client for Genesis Engine
Handles communication with Claude 4 Opus for game generation.
"""
import json
from typing import Optional, Dict, Any

class AIClient:
    """
    Client for interacting with Claude 4 Opus API.
    Handles all AI reasoning, planning, and code generation.
    """
    
    def __init__(self):
        # API key will be fetched from Supabase secrets when needed
        self.model = "claude-4-opus-20250514"  # Using latest Claude 4 Opus
        self.base_url = "https://api.anthropic.com/v1/messages"
        
    async def _get_api_key(self) -> Optional[str]:
        """Fetch API key from Supabase secrets."""
        try:
            from supabase import create_client
            import os
            
            # Get Supabase credentials from environment
            supabase_url = os.getenv('VITE_SUPABASE_URL')
            supabase_key = os.getenv('VITE_SUPABASE_ANON_KEY')
            
            if not supabase_url or not supabase_key:
                print("❌ Supabase credentials not found in environment")
                return None
                
            supabase = create_client(supabase_url, supabase_key)
            
            # Fetch the secret
            response = supabase.functions.invoke('get-secret', {
                'name': 'ANTHROPIC_API_KEY'
            })
            
            if response.get('data'):
                return response['data'].get('value')
            else:
                print("❌ Failed to fetch ANTHROPIC_API_KEY from secrets")
                return None
                
        except Exception as e:
            print(f"❌ Error fetching API key: {str(e)}")
            return None
    
    def generate_game_design_document(self, prompt: str) -> str:
        """Generate a comprehensive Game Design Document from prompt."""
        system_prompt = """You are an expert game designer creating a Game Design Document. 
        Analyze the user's game concept and create a detailed, implementable GDD.
        Focus on simple, achievable mechanics that can be built with Python + Pygame.
        Use placeholder graphics (colored shapes) for all visual elements."""
        
        user_prompt = f"""
        Create a Game Design Document for this game concept: "{prompt}"
        
        The GDD should include:
        - Game Overview (genre, theme, target complexity)
        - Core Mechanics (movement, interactions, rules)
        - Game Loop (initialization, update cycle, win/lose conditions)
        - Controls (keyboard input mapping)
        - Technical Requirements (Python + Pygame, 800x600, 60 FPS)
        - Implementation Priority (ordered list of features to build)
        
        Keep it simple but complete. This will be used to generate actual Python code.
        """
        
        # For now, return mock response - will implement actual API call once we test the pipeline
        return self._mock_gdd_response(prompt)
    
    def generate_technical_plan(self, gdd_content: str) -> str:
        """Generate technical implementation plan from GDD."""
        system_prompt = """You are a senior Python engineer creating a technical plan for a Pygame game.
        Convert the game design into a concrete implementation strategy."""
        
        user_prompt = f"""
        Based on this Game Design Document, create a Technical Implementation Plan:
        
        {gdd_content}
        
        The plan should include:
        - Architecture Overview (class structure, file organization)
        - File Structure (detailed directory layout)
        - Core Classes (with responsibilities and methods)
        - Implementation Sequence (ordered development phases)
        - Dependencies (pygame and standard library only)
        - Placeholder Graphics (specific shapes and colors for each element)
        """
        
        return self._mock_tech_plan_response()
    
    def generate_asset_specifications(self, gdd_content: str) -> str:
        """Generate detailed asset specifications."""
        return self._mock_asset_specs_response()
    
    def generate_game_code(self, gdd_content: str, tech_plan: str) -> str:
        """Generate the complete Python game code."""
        system_prompt = """You are an expert Python game developer using Pygame.
        Create a complete, working game based on the design documents.
        Use only colored rectangles and circles for graphics.
        Follow clean code principles with proper error handling."""
        
        user_prompt = f"""
        Generate complete Python game code based on these documents:
        
        GAME DESIGN:
        {gdd_content[:1000]}...
        
        TECHNICAL PLAN:
        {tech_plan[:1000]}...
        
        Requirements:
        - Single main.py file with all code
        - Python 3.10+ with type hints
        - Pygame library only
        - 800x600 window, 60 FPS
        - Colored shapes for all graphics
        - Complete game loop with win/lose conditions
        - Error handling and clean shutdown
        """
        
        return self._mock_game_code_response()
    
    def _mock_gdd_response(self, prompt: str) -> str:
        """Mock GDD response - replace with actual AI call."""
        return f"""# Game Design Document

## Original Concept
"{prompt}"

## Game Overview
**Genre:** Platformer  
**Theme:** Space Adventure  
**Target Complexity:** Simple  

## Core Mechanics
- Player movement (WASD/Arrow keys)
- Jumping with gravity
- Collectible items (coins/gems)
- Basic enemies with collision
- Platform navigation
- Win condition: Collect all items
- Lose condition: Touch enemy or fall off screen

## Game Loop
1. Initialize Pygame and game objects
2. Handle input events
3. Update player physics and position
4. Update enemies and collectibles
5. Check collisions and game state
6. Render all objects
7. Check win/lose conditions
8. Repeat at 60 FPS

## Controls
- **Movement:** Arrow keys or WASD
- **Jump:** Spacebar
- **Quit:** ESC key

## Technical Requirements
- **Engine:** Python + Pygame
- **Resolution:** 800x600 pixels
- **Frame Rate:** 60 FPS target
- **Graphics:** Colored rectangles and circles
- **Dependencies:** pygame only

## Implementation Priority
1. Basic window and main game loop
2. Player character (blue rectangle) with movement
3. Platform environment (green rectangles)
4. Gravity and jumping mechanics
5. Collectible items (yellow circles)
6. Basic collision detection
7. Win/lose conditions and game over screen
8. Polish and bug fixes

---
*Generated by Genesis Engine v1.0*
"""
    
    def _mock_tech_plan_response(self) -> str:
        """Mock technical plan response."""
        return """# Technical Implementation Plan

## Architecture Overview
Component-based game architecture with clear separation of concerns.

## File Structure
```
main.py              # Complete game implementation
```

## Core Classes

### Game
- Main game controller
- Handles initialization, game loop, and shutdown
- Manages all game objects and state

### Player
- Player character with position and velocity
- Handles input and movement physics
- Collision detection with environment

### Platform
- Static platform objects for level geometry
- Simple rectangle collision bounds

### Collectible
- Items for player to collect
- Collision detection and collection logic

### Enemy
- Basic enemy with simple AI
- Collision detection with player

## Implementation Sequence
1. **Phase 1:** Basic Pygame window and main loop
2. **Phase 2:** Player character with movement
3. **Phase 3:** Platform level geometry
4. **Phase 4:** Collision detection system
5. **Phase 5:** Collectibles and win condition
6. **Phase 6:** Enemies and lose condition
7. **Phase 7:** Game over screens and restart

## Dependencies
- pygame: Game engine and graphics
- typing: Type hints for clean code
- sys: Clean application exit

## Placeholder Graphics
- Player: Blue rectangle (32x48 pixels)
- Platforms: Green rectangles (various sizes)
- Collectibles: Yellow circles (16 pixel radius)
- Enemies: Red rectangles (24x24 pixels)
- Background: Light blue solid color

---
*Generated by Genesis Engine v1.0*
"""
    
    def _mock_asset_specs_response(self) -> str:
        """Mock asset specifications response."""
        return """# Asset Specifications

## Visual Assets

### Player Character
**Type:** Rectangle  
**Size:** 32x48 pixels  
**Color:** Blue (#0066CC)  
**Details:** Simple filled rectangle representing the player

### Environment
**Platforms:** Green rectangles (#228B22)  
**Background:** Light blue (#87CEEB)  
**Boundaries:** Dark gray (#696969)

### Interactive Objects
**Collectibles:** Yellow circles (#FFD700), 16px radius  
**Enemies:** Red rectangles (#DC143C), 24x24 pixels  
**Goal:** Bright green rectangle (#00FF00), 48x48 pixels

### UI Elements
**Text:** White Arial font  
**Score:** Top-left corner  
**Game Over:** Center screen with semi-transparent background

## Audio Assets (Future)
**Jump Sound:** Short "boing" effect  
**Collect Sound:** Pleasant "ding" chime  
**Enemy Hit:** Brief impact sound  
**Background Music:** Simple loop (optional)

## Implementation Notes
- All graphics implemented as pygame.Rect and pygame.draw calls
- Colors defined as RGB tuples in constants
- No external image files required
- Consistent visual style with simple geometric shapes

---
*Generated by Genesis Engine v1.0*
"""
    
    def _mock_game_code_response(self) -> str:
        """Mock game code response."""
        return '''#!/usr/bin/env python3
"""
Auto-generated Space Platformer Game
Created by Genesis Engine v1.0
"""

import pygame
import sys
import random
from typing import List, Tuple
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
GRAY = (105, 105, 105)

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
    """Player character with physics and controls."""
    
    def __init__(self, x: float, y: float):
        self.position = Vector2(x, y)
        self.velocity = Vector2(0, 0)
        self.size = Vector2(32, 48)
        self.speed = 250
        self.jump_power = 400
        self.on_ground = False
        self.color = BLUE
        
    def update(self, dt: float, platforms: List['Platform']):
        """Update player physics and handle input."""
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
        self.velocity.y += 1200 * dt
        
        # Update position
        old_pos = Vector2(self.position.x, self.position.y)
        self.position = self.position + self.velocity * dt
        
        # Handle collisions
        self._handle_collisions(platforms, old_pos)
        
        # Keep player on screen horizontally
        self.position.x = max(0, min(SCREEN_WIDTH - self.size.x, self.position.x))
    
    def _handle_collisions(self, platforms: List['Platform'], old_pos: Vector2):
        """Handle collision with platforms."""
        player_rect = pygame.Rect(self.position.x, self.position.y, self.size.x, self.size.y)
        
        for platform in platforms:
            if player_rect.colliderect(platform.rect):
                # Vertical collision (landing on platform)
                if self.velocity.y > 0 and old_pos.y + self.size.y <= platform.rect.top + 5:
                    self.position.y = platform.rect.top - self.size.y
                    self.velocity.y = 0
                    self.on_ground = True
                # Horizontal collision
                elif self.velocity.x != 0:
                    self.position.x = old_pos.x
                    self.velocity.x = 0
    
    def get_rect(self) -> pygame.Rect:
        """Get player rectangle for collision detection."""
        return pygame.Rect(self.position.x, self.position.y, self.size.x, self.size.y)
    
    def render(self, screen: pygame.Surface):
        """Render the player."""
        pygame.draw.rect(screen, self.color, self.get_rect())

class Platform:
    """Static platform for level geometry."""
    
    def __init__(self, x: float, y: float, width: float, height: float):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = GREEN
    
    def render(self, screen: pygame.Surface):
        """Render the platform."""
        pygame.draw.rect(screen, self.color, self.rect)

class Collectible:
    """Collectible items for scoring."""
    
    def __init__(self, x: float, y: float):
        self.position = Vector2(x, y)
        self.radius = 16
        self.collected = False
        self.color = YELLOW
    
    def get_rect(self) -> pygame.Rect:
        """Get bounding rectangle for collision."""
        return pygame.Rect(
            self.position.x - self.radius,
            self.position.y - self.radius,
            self.radius * 2,
            self.radius * 2
        )
    
    def render(self, screen: pygame.Surface):
        """Render the collectible."""
        if not self.collected:
            pygame.draw.circle(
                screen,
                self.color,
                (int(self.position.x), int(self.position.y)),
                self.radius
            )

class Enemy:
    """Basic enemy with simple movement."""
    
    def __init__(self, x: float, y: float):
        self.position = Vector2(x, y)
        self.size = Vector2(24, 24)
        self.velocity = Vector2(50, 0)
        self.color = RED
        self.patrol_range = 100
        self.start_x = x
    
    def update(self, dt: float):
        """Update enemy movement."""
        self.position.x += self.velocity.x * dt
        
        # Simple patrol behavior
        if self.position.x <= self.start_x - self.patrol_range or \
           self.position.x >= self.start_x + self.patrol_range:
            self.velocity.x *= -1
    
    def get_rect(self) -> pygame.Rect:
        """Get enemy rectangle for collision."""
        return pygame.Rect(self.position.x, self.position.y, self.size.x, self.size.y)
    
    def render(self, screen: pygame.Surface):
        """Render the enemy."""
        pygame.draw.rect(screen, self.color, self.get_rect())

class Game:
    """Main game class."""
    
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Genesis Engine Game")
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = GameState.PLAYING
        
        # Initialize game objects
        self.player = Player(100, 300)
        self.platforms = self._create_platforms()
        self.collectibles = self._create_collectibles()
        self.enemies = self._create_enemies()
        self.score = 0
        self.font = pygame.font.Font(None, 36)
        
    def _create_platforms(self) -> List[Platform]:
        """Create level platforms."""
        return [
            # Ground platforms
            Platform(0, SCREEN_HEIGHT - 40, SCREEN_WIDTH, 40),
            # Floating platforms
            Platform(200, 450, 150, 20),
            Platform(400, 350, 150, 20),
            Platform(600, 250, 150, 20),
            Platform(150, 150, 100, 20),
            Platform(500, 150, 200, 20),
        ]
    
    def _create_collectibles(self) -> List[Collectible]:
        """Create collectible items."""
        return [
            Collectible(275, 420),
            Collectible(475, 320),
            Collectible(675, 220),
            Collectible(200, 120),
            Collectible(600, 120),
        ]
    
    def _create_enemies(self) -> List[Enemy]:
        """Create enemy objects."""
        return [
            Enemy(250, 426),
            Enemy(450, 326),
        ]
    
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
        """Update game state."""
        if self.state == GameState.PLAYING:
            # Update player
            self.player.update(dt, self.platforms)
            
            # Update enemies
            for enemy in self.enemies:
                enemy.update(dt)
            
            # Check collectible collisions
            player_rect = self.player.get_rect()
            for collectible in self.collectibles:
                if not collectible.collected and player_rect.colliderect(collectible.get_rect()):
                    collectible.collected = True
                    self.score += 100
            
            # Check enemy collisions
            for enemy in self.enemies:
                if player_rect.colliderect(enemy.get_rect()):
                    self.state = GameState.GAME_OVER
            
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
        
        # Render enemies
        for enemy in self.enemies:
            enemy.render(self.screen)
        
        # Render player
        if self.state == GameState.PLAYING:
            self.player.render(self.screen)
        
        # Render UI
        self._render_ui()
        
        pygame.display.flip()
    
    def _render_ui(self):
        """Render user interface."""
        # Score
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))
        
        # Game state messages
        if self.state == GameState.VICTORY:
            self._render_message("VICTORY! Press R to restart", GREEN)
        elif self.state == GameState.GAME_OVER:
            self._render_message("GAME OVER! Press R to restart", RED)
    
    def _render_message(self, text: str, color: Tuple[int, int, int]):
        """Render centered message with background."""
        message = self.font.render(text, True, WHITE)
        rect = message.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        
        # Semi-transparent background
        bg_rect = rect.inflate(40, 20)
        bg_surface = pygame.Surface(bg_rect.size)
        bg_surface.set_alpha(128)
        bg_surface.fill(BLACK)
        self.screen.blit(bg_surface, bg_rect)
        
        # Border
        pygame.draw.rect(self.screen, color, bg_rect, 3)
        
        # Text
        self.screen.blit(message, rect)
    
    def _restart_game(self):
        """Restart game to initial state."""
        self.player = Player(100, 300)
        self.collectibles = self._create_collectibles()
        self.enemies = self._create_enemies()
        self.score = 0
        self.state = GameState.PLAYING
    
    def run(self):
        """Main game loop."""
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0
            
            self.handle_events()
            self.update(dt)
            self.render()
        
        pygame.quit()
        sys.exit()

def main():
    """Entry point for the game."""
    try:
        game = Game()
        game.run()
    except Exception as e:
        print(f"Game error: {e}")
        pygame.quit()
        sys.exit(1)

if __name__ == "__main__":
    main()
