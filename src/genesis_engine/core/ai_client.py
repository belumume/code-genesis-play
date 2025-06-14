"""
AI Client for the Genesis Engine.
Handles all interactions with Claude 4 Opus API with fallback to mock data.
Enhanced with better code validation to prevent recurring syntax errors.
"""
import os
import json
import aiohttp
import asyncio
import re
from typing import Optional

class AIClient:
    """
    Client for interacting with Anthropic's Claude 4 Opus API.
    Falls back to mock responses if API is unavailable.
    Enhanced with code validation to prevent syntax errors.
    """
    
    def __init__(self):
        # Try multiple sources for the API key
        self.api_key = self._get_api_key()
        self.base_url = "https://api.anthropic.com/v1/messages"
        self.model = "claude-opus-4-20250514"  # Using Claude 3 Opus for now
        self.use_mock = not bool(self.api_key)
        
        if self.use_mock:
            print("⚠️  No Anthropic API key found. Using mock responses for testing.")
        else:
            print("✅ Anthropic API key found. Using real AI integration.")
    
    def _get_api_key(self) -> Optional[str]:
        """Get API key from multiple sources."""
        # Try environment variable first
        api_key = os.getenv('ANTHROPIC_API_KEY')
        if api_key:
            return api_key
            
        # Try Supabase secrets via the get-secret function
        try:
            import subprocess
            result = subprocess.run([
                'supabase', 'functions', 'invoke', 'get-secret',
                '--data', '{"name":"ANTHROPIC_API_KEY"}'
            ], capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                response = json.loads(result.stdout)
                return response.get('value')
        except:
            pass
            
        return None
    
    def _clean_code_response(self, response: str) -> str:
        """
        Clean the AI response to ensure it's valid Python code.
        Removes markdown code blocks and other formatting issues.
        Enhanced with multiple validation layers to prevent syntax errors.
        """
        print(f"🧹 Cleaning AI response (length: {len(response)})")
        
        # Step 1: Remove all markdown code blocks (multiple patterns)
        patterns_to_remove = [
            r'```python\s*\n?',
            r'```\s*python\s*\n?',
            r'```\s*\n?',
            r'^```.*\n',  # Remove any line starting with ```
            r'\n```.*$',  # Remove any line ending with ```
        ]
        
        for pattern in patterns_to_remove:
            response = re.sub(pattern, '', response, flags=re.MULTILINE)
        
        # Step 2: Remove any explanatory text before Python code
        lines = response.split('\n')
        python_start_idx = 0
        
        # Find the first line that looks like Python code
        for i, line in enumerate(lines):
            stripped = line.strip()
            if (stripped.startswith('import ') or 
                stripped.startswith('from ') or
                stripped.startswith('# ') or
                stripped.startswith('"""') or
                stripped.startswith('class ') or
                stripped.startswith('def ') or
                stripped.startswith('if __name__')):
                python_start_idx = i
                break
        
        # Keep only Python code
        response = '\n'.join(lines[python_start_idx:])
        
        # Step 3: Remove trailing markdown or explanations
        lines = response.split('\n')
        python_end_idx = len(lines)
        
        # Find where Python code ends (look for markdown or explanations)
        for i in range(len(lines) - 1, -1, -1):
            line = lines[i].strip()
            if line and not line.startswith('#') and not line.startswith('```'):
                python_end_idx = i + 1
                break
                
        response = '\n'.join(lines[:python_end_idx])
        
        # Step 4: Final cleanup
        response = response.strip()
        
        # Step 5: Validation - ensure it starts with valid Python
        if not response:
            print("⚠️  Empty response after cleaning!")
            return self._get_fallback_python_code()
            
        first_line = response.split('\n')[0].strip()
        valid_starts = ['import', 'from', '#', '"""', 'class', 'def', 'if', 'try', 'with']
        
        if not any(first_line.startswith(start) for start in valid_starts):
            print(f"⚠️  Response doesn't start with valid Python: '{first_line}'")
            # Try to find and extract just the Python part
            for line in response.split('\n'):
                if any(line.strip().startswith(start) for start in valid_starts):
                    idx = response.find(line)
                    response = response[idx:]
                    break
            else:
                return self._get_fallback_python_code()
        
        print(f"✅ Code cleaned successfully (final length: {len(response)})")
        return response
    
    def _get_fallback_python_code(self) -> str:
        """Return a minimal working Python game as fallback."""
        return '''import pygame
import sys

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Generated Game")
clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
BLUE = (100, 150, 255)
RED = (255, 100, 100)

# Player
player_rect = pygame.Rect(100, 300, 40, 40)
player_speed = 200

# Game loop
running = True
while running:
    dt = clock.tick(60) / 1000.0
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Handle input
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_rect.x -= player_speed * dt
    if keys[pygame.K_RIGHT]:
        player_rect.x += player_speed * dt
    if keys[pygame.K_UP]:
        player_rect.y -= player_speed * dt
    if keys[pygame.K_DOWN]:
        player_rect.y += player_speed * dt
    
    # Keep player on screen
    player_rect.clamp_ip(pygame.Rect(0, 0, 800, 600))
    
    # Draw everything
    screen.fill(WHITE)
    pygame.draw.rect(screen, BLUE, player_rect)
    
    # Instructions
    font = pygame.font.Font(None, 36)
    text = font.render("Use arrow keys to move", True, RED)
    screen.blit(text, (10, 10))
    
    pygame.display.flip()

pygame.quit()
sys.exit()
'''

    def _make_api_call(self, messages: list) -> str:
        """Make an async API call to Claude."""
        if self.use_mock:
            return self._get_mock_response(messages[0]['content'])
        
        headers = {
            'Content-Type': 'application/json',
            'x-api-key': self.api_key,
            'anthropic-version': '2023-06-01'
        }
        
        payload = {
            'model': self.model,
            'max_tokens': 4000,
            'messages': messages
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(self.base_url, headers=headers, json=payload) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data['content'][0]['text']
                    else:
                        error_text = await response.text()
                        raise Exception(f"API call failed: {response.status} - {error_text}")
        except Exception as e:
            print(f"❌ API call failed, falling back to mock: {e}")
            return self._get_mock_response(messages[0]['content'])
    
    def _run_async(self, coro):
        """Safely run async code, handling existing event loops."""
        try:
            # Try to get the current event loop
            loop = asyncio.get_running_loop()
            # If we're in an existing loop, we need to use a different approach
            import concurrent.futures
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(asyncio.run, coro)
                return future.result()
        except RuntimeError:
            # No running loop, safe to use asyncio.run
            return asyncio.run(coro)
    
    def generate_game_design_document(self, prompt: str) -> str:
        """Generate a comprehensive Game Design Document."""
        messages = [{
            'role': 'user',
            'content': f"""You are an expert game designer. Create a comprehensive Game Design Document for this game concept: "{prompt}"

The GDD should include:
1. Game Title and Concept
2. Core Mechanics
3. Player Controls
4. Win/Loss Conditions
5. Visual Style
6. Target Audience
7. Technical Requirements

Format as Markdown. Be creative and detailed."""
        }]
        
        return self._run_async(self._make_api_call(messages))
    
    def generate_technical_plan(self, gdd_content: str) -> str:
        """Generate technical implementation plan."""
        messages = [{
            'role': 'user',
            'content': f"""Based on this Game Design Document, create a detailed technical implementation plan:

{gdd_content}

Create a technical plan that includes:
1. File Structure
2. Core Classes and Functions
3. Implementation Order
4. Key Technical Challenges
5. Dependencies and Libraries

Format as Markdown. Focus on Python/Pygame implementation."""
        }]
        
        return self._run_async(self._make_api_call(messages))
    
    def generate_asset_specifications(self, gdd_content: str) -> str:
        """Generate detailed asset specifications."""
        messages = [{
            'role': 'user',
            'content': f"""Based on this Game Design Document, create detailed asset specifications:

{gdd_content}

Create asset specifications that include:
1. Visual Assets (sprites, backgrounds, UI elements)
2. Audio Assets (sound effects, music)
3. Technical Specifications (dimensions, formats)
4. Style Guidelines

Format as Markdown. Be specific about colors, sizes, and styles."""
        }]
        
        return self._run_async(self._make_api_call(messages))
    
    def generate_game_code(self, gdd_content: str, tech_plan: str) -> str:
        """Generate complete game code with enhanced validation."""
        messages = [{
            'role': 'user',
            'content': f"""Generate complete Python game code using Pygame based on these documents:

GAME DESIGN DOCUMENT:
{gdd_content}

TECHNICAL PLAN:
{tech_plan}

CRITICAL REQUIREMENTS:
- Generate ONLY valid Python code - no markdown, no explanations, no code blocks
- Start immediately with 'import pygame' - no prefixes
- Use simple colored rectangles/circles for graphics (no external images)
- Include player movement, collision detection, win/loss conditions
- 60 FPS game loop with proper error handling
- Well-commented code following PEP 8
- Complete, fully playable game
- End with if __name__ == "__main__": main()

IMPORTANT: Your response must be pure Python code that can be executed directly. Do not include any markdown formatting, explanations, or code block markers. Start your response with the first import statement."""
        }]
        
        response = self._run_async(self._make_api_call(messages))
        cleaned_response = self._clean_code_response(response)
        
        # Additional validation: try to compile the code
        try:
            compile(cleaned_response, '<generated_code>', 'exec')
            print("✅ Generated code passes syntax validation")
        except SyntaxError as e:
            print(f"⚠️  Syntax error in generated code: {e}")
            print(f"Error at line {e.lineno}: {e.text}")
            # Return fallback code instead of broken code
            cleaned_response = self._get_fallback_python_code()
        
        return cleaned_response
    
    def _get_mock_response(self, prompt: str) -> str:
        """Fallback mock responses for testing."""
        if "design document" in prompt.lower() or "gdd" in prompt.lower():
            return """# MOCK Game Design Document

## Game Title: Space Adventure

## Core Mechanics
- MOCK: Player controls a spaceship
- MOCK: Collect crystals for points
- MOCK: Avoid enemy aliens

## Player Controls
- MOCK: Arrow keys for movement
- MOCK: Spacebar to jump/boost

## Win/Loss Conditions
- MOCK: Win by collecting all crystals
- MOCK: Lose by touching enemies

*Note: This is MOCK data for testing. Real AI integration will generate unique content.*
"""
        elif "technical plan" in prompt.lower():
            return """# MOCK Technical Plan

## File Structure
- MOCK: main.py (main game loop)
- MOCK: player.py (player class)
- MOCK: enemy.py (enemy class)

## Core Classes
- MOCK: Game class
- MOCK: Player class
- MOCK: Enemy class

*Note: This is MOCK data for testing.*
"""
        elif "asset" in prompt.lower():
            return """# MOCK Asset Specifications

## Visual Assets
- MOCK: Player sprite (32x32, blue rectangle)
- MOCK: Enemy sprite (24x24, red circle)
- MOCK: Crystal sprite (16x16, yellow diamond)

*Note: This is MOCK data for testing.*
"""
        else:
            # Return clean Python code without markdown for game code generation
            return """import pygame
import sys

# MOCK: Basic Pygame setup
pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    screen.fill((100, 150, 200))
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()

# Note: This is MOCK data for testing. Real AI will generate complete games."""
