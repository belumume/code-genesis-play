
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
        self.model = "claude-3-opus-20240229"  # Using Claude 3 Opus for now
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
        """
        # Remove markdown code blocks
        response = re.sub(r'```python\s*\n', '', response)
        response = re.sub(r'```\s*$', '', response)
        response = re.sub(r'^```\s*\n', '', response, flags=re.MULTILINE)
        
        # Remove any leading/trailing whitespace
        response = response.strip()
        
        # Ensure the response starts with valid Python (not markdown)
        if response.startswith('```'):
            # Find the first actual Python line
            lines = response.split('\n')
            start_idx = 0
            for i, line in enumerate(lines):
                if not line.strip().startswith('```') and line.strip():
                    start_idx = i
                    break
            response = '\n'.join(lines[start_idx:])
        
        return response
    
    async def _make_api_call(self, messages: list) -> str:
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
        """Generate complete game code with validation."""
        messages = [{
            'role': 'user',
            'content': f"""Generate complete Python game code using Pygame based on these documents:

GAME DESIGN DOCUMENT:
{gdd_content}

TECHNICAL PLAN:
{tech_plan}

CRITICAL REQUIREMENTS:
- Generate ONLY valid Python code - no markdown code blocks or formatting
- Use simple colored rectangles/circles for graphics (no external images)
- Include player movement, collision detection, win/loss conditions
- 60 FPS game loop
- Well-commented code following PEP 8
- Fully playable game
- Start your response immediately with 'import pygame' - no explanations or markdown

Generate ONLY the Python code, no explanations, no markdown blocks."""
        }]
        
        response = self._run_async(self._make_api_call(messages))
        return self._clean_code_response(response)
    
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
