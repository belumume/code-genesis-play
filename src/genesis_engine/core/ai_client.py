"""
AI Client for the Genesis Engine.
Handles all interactions with Claude 4 Opus API with fallback to Claude 4 Sonnet, then mock data.
Enhanced with better code validation to prevent recurring syntax errors.
"""
import os
import json
import aiohttp
import asyncio
import re
from typing import Optional, Dict, Any, List
import logging
from tenacity import retry, stop_after_attempt, wait_exponential

# Configure logging
logger = logging.getLogger(__name__)

class AIClient:
    """
    Client for interacting with Anthropic's Claude API.
    Uses the specified high-performance model for all tasks.
    """
    
    def __init__(self):
        self.api_key = self._get_api_key()
        self.base_url = "https://api.anthropic.com/v1/messages"
        
        # Use the single, specified top-tier model
        self.model = "claude-sonnet-4-20250514"
        
        # Try to use model from config, otherwise use the default
        try:
            from ..config import settings
            if hasattr(settings, 'anthropic_model'):
                self.model = settings.anthropic_model
        except ImportError:
            pass
        
        self.use_mock = not bool(self.api_key)
        self.timeout = aiohttp.ClientTimeout(total=120)

        if self.use_mock:
            print("⚠️  No Anthropic API key found. Using mock responses for testing.")
        else:
            print("✅ Anthropic API key found. Using real AI integration.")
            print(f"🎯 Using exclusive model: {self.model}")
    
    def _get_api_key(self) -> Optional[str]:
        """Get API key from multiple sources."""
        # Try environment variable first
        api_key = os.getenv('ANTHROPIC_API_KEY')
        if api_key:
            return api_key
            
        # Try Supabase secrets via the get-secret function
        try:
            import subprocess
            import shlex
            
            # Properly escape the JSON data to prevent injection
            json_data = json.dumps({"name": "ANTHROPIC_API_KEY"})
            cmd = ['supabase', 'functions', 'invoke', 'get-secret', '--data', json_data]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=10,
                check=False  # Don't raise on non-zero exit
            )
            
            if result.returncode == 0 and result.stdout:
                try:
                    response = json.loads(result.stdout)
                    return response.get('value')
                except json.JSONDecodeError:
                    pass
        except (subprocess.TimeoutExpired, FileNotFoundError):
            # Supabase CLI not installed or command timed out
            pass
            
        return None
    
    def _clean_code_response(self, response: str) -> str:
        """
        Clean the AI response to ensure it's valid Python code.
        Removes markdown code blocks and other formatting issues.
        Enhanced with multiple validation layers to prevent syntax errors.
        """
        print(f"🧹 Cleaning AI response (length: {len(response)})")
        
        # Step 1: Aggressive markdown removal
        # Remove everything before the first import statement
        lines = response.split('\n')
        
        # Find first line that starts with import/from
        first_code_line = 0
        for i, line in enumerate(lines):
            stripped = line.strip()
            if stripped.startswith(('import ', 'from ')) and not stripped.startswith('```'):
                first_code_line = i
                break
        
        # If we found Python code, start from there
        if first_code_line > 0:
            response = '\n'.join(lines[first_code_line:])
        
        # Remove any remaining markdown patterns
        patterns_to_remove = [
            r'```[a-zA-Z]*\n?',    # Code block starts
            r'```\n?',             # Code block ends
            r'^```.*$',            # Any line with just backticks
            r'^\s*```.*$',         # Lines with whitespace then backticks
        ]
        
        for pattern in patterns_to_remove:
            response = re.sub(pattern, '', response, flags=re.MULTILINE)
        
        # Remove any lines that are just backticks or markdown
        lines = response.split('\n')
        clean_lines = []
        
        for line in lines:
            # Skip any lines with backticks or markdown
            if '```' in line or line.strip().startswith('#') and not line.strip().startswith('# '):
                continue
            # Skip empty lines at the beginning
            if not clean_lines and not line.strip():
                continue
            clean_lines.append(line)
        
        response = '\n'.join(clean_lines)
        
        # Step 3: Find the first valid Python line
        lines = response.split('\n')
        python_start_idx = 0
        
        # Find the first line that looks like Python code
        for i, line in enumerate(lines):
            stripped = line.strip()
            if (stripped.startswith('import ') or 
                stripped.startswith('from ') or
                stripped.startswith('#') or
                stripped.startswith('"""') or
                stripped.startswith('class ') or
                stripped.startswith('def ') or
                stripped.startswith('if __name__') or
                stripped.startswith('try:') or
                stripped.startswith('with ')):
                python_start_idx = i
                break
        
        # Keep only Python code
        response = '\n'.join(lines[python_start_idx:])
        
        # Step 4: Remove trailing non-Python content
        lines = response.split('\n')
        python_end_idx = len(lines)
        
        # Find where Python code ends
        for i in range(len(lines) - 1, -1, -1):
            line = lines[i].strip()
            # If we find a line with just backticks or markdown, stop there
            if '```' in line or (line and not any(c in line for c in '()[]{}=#"\'')):
                python_end_idx = i
                break
            # If we find valid Python, keep going
            elif line and any(c in line for c in '()[]{}=#"\''):
                python_end_idx = i + 1
                break
                
        response = '\n'.join(lines[:python_end_idx])
        
        # Step 5: Final cleanup
        response = response.strip()
        
        # Step 6: Validation - ensure it starts with valid Python
        if not response:
            print("⚠️  Empty response after cleaning!")
            return self._get_fallback_python_code()
            
        first_line = response.split('\n')[0].strip()
        valid_starts = ['import', 'from', '#', '"""', "'''", 'class', 'def', 'if', 'try', 'with', '__']
        
        if not any(first_line.startswith(start) for start in valid_starts):
            print(f"⚠️  Response doesn't start with valid Python: '{first_line}'")
            return self._get_fallback_python_code()
        
        # Step 7: Final syntax validation
        try:
            compile(response, '<generated_code>', 'exec')
            print("✅ Code cleaned and validated successfully")
        except SyntaxError as e:
            print(f"⚠️  Syntax error after cleaning: {e}")
            print(f"Error at line {e.lineno}: {e.text}")
            # Try one more aggressive cleaning
            response = self._aggressive_clean(response)
            try:
                compile(response, '<generated_code>', 'exec')
                print("✅ Aggressive cleaning succeeded")
            except:
                print("❌ Unable to clean code properly, using fallback")
                return self._get_fallback_python_code()
        
        return response
    
    def _aggressive_clean(self, response: str) -> str:
        """More aggressive cleaning for stubborn cases."""
        lines = response.split('\n')
        clean_lines = []
        
        for line in lines:
            # Remove any line containing markdown indicators
            if '```' in line or line.strip().startswith('**') or line.strip().startswith('##'):
                continue
            # Remove lines that look like prose
            if line.strip() and not any(char in line for char in '()[]{}=:#"\','):
                if not line.strip().startswith(('import', 'from', 'class', 'def')):
                    continue
            clean_lines.append(line)
        
        return '\n'.join(clean_lines)
    
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

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=3, max=10),
        reraise=True
    )
    async def _make_api_call_with_retry(self, messages: list) -> str:
        """Make an API call with retry logic for the configured model."""
        headers = {
            'Content-Type': 'application/json',
            'x-api-key': self.api_key,
            'anthropic-version': '2023-06-01'
        }
        
        payload = {
            'model': self.model,
            'max_tokens': 64000, # Max for Sonnet 4
            'messages': messages,
            'temperature': 0.7
        }
        
        async with aiohttp.ClientSession(timeout=self.timeout) as session:
            async with session.post(self.base_url, headers=headers, json=payload) as response:
                if response.status == 200:
                    data = await response.json()
                    return data['content'][0]['text']
                elif response.status == 429:
                    retry_after = response.headers.get('Retry-After', 10)
                    logger.warning(f"Rate limited on {self.model}. Retrying after {retry_after} seconds")
                    await asyncio.sleep(int(retry_after))
                    raise Exception(f"Rate limited on {self.model}")
                else:
                    error_text = await response.text()
                    error_msg = f"API call failed for {self.model}: {response.status} - {error_text}"
                    logger.error(error_msg)
                    raise Exception(error_msg)
    
    async def _make_api_call(self, messages: list) -> str:
        """Make an async API call to the configured model."""
        if self.use_mock:
            return self._get_mock_response(messages[0]['content'])
        
        try:
            print(f"🤖 Using exclusive model: {self.model}...")
            return await self._make_api_call_with_retry(messages)
        except Exception as e:
            logger.error(f"Model {self.model} failed: {e}. Falling back to mock data.")
            print(f"❌  Model {self.model} failed. Falling back to mock data.")
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

Format as Markdown. Be creative and detailed, but keep it concise for faster processing."""
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

Format as Markdown. Focus on Python/Pygame implementation. Be specific but concise."""
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

Format as Markdown. Be specific about colors, sizes, and styles. Keep it concise."""
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
    
    def generate_javascript_game(self, gdd_content: str, tech_plan: str) -> str:
        """Generate complete JavaScript/HTML5 game using p5.js."""
        messages = [{
            'role': 'user',
            'content': f"""Generate a complete HTML file with embedded JavaScript game using p5.js based on these documents:

GAME DESIGN DOCUMENT:
{gdd_content}

TECHNICAL PLAN:
{tech_plan}

CRITICAL REQUIREMENTS:
- Generate a COMPLETE HTML file with embedded JavaScript
- Use p5.js library loaded from CDN
- Include proper HTML structure with <!DOCTYPE html>
- Embed ALL JavaScript code within <script> tags
- Use simple geometric shapes for graphics (rectangles, circles, lines)
- Include player controls (arrow keys or WASD)
- Implement win/loss conditions
- Use p5.js functions: setup(), draw(), createCanvas()
- Well-commented code
- Complete, fully playable game in browser

IMPORTANT: Your response must be a complete HTML file that can be saved and opened in a browser. Start with <!DOCTYPE html> and end with </html>."""
        }]
        
        response = self._run_async(self._make_api_call(messages))
        
        # Clean the response for HTML/JavaScript
        cleaned_response = self._clean_html_response(response)
        
        # Validate HTML structure
        if not self._validate_html_structure(cleaned_response):
            print("⚠️  Generated HTML failed validation, using fallback")
            cleaned_response = self._get_fallback_html_game()
        
        return cleaned_response
    
    def _clean_html_response(self, response: str) -> str:
        """Clean the AI response to ensure it's valid HTML/JavaScript."""
        print(f"🧹 Cleaning HTML response (length: {len(response)})")
        
        # Remove markdown code blocks
        response = re.sub(r'```[a-zA-Z]*\n?', '', response)
        response = re.sub(r'```\n?', '', response)
        
        # Find the start of HTML
        if '<!DOCTYPE html>' in response:
            start_index = response.find('<!DOCTYPE html>')
            response = response[start_index:]
        elif '<html>' in response:
            start_index = response.find('<html>')
            response = response[start_index:]
        elif '<HTML>' in response:
            start_index = response.find('<HTML>')
            response = response[start_index:]
        
        # Find the end of HTML
        if '</html>' in response:
            end_index = response.rfind('</html>') + 7
            response = response[:end_index]
        elif '</HTML>' in response:
            end_index = response.rfind('</HTML>') + 7
            response = response[:end_index]
        
        return response.strip()
    
    def _validate_html_structure(self, html_content: str) -> bool:
        """Validate basic HTML structure."""
        if not html_content:
            return False
        
        required_elements = [
            '<!DOCTYPE html>' or '<html>',
            '</html>',
            '<script>',
            '</script>',
            'function setup(',
            'function draw(',
            'createCanvas('
        ]
        
        content_lower = html_content.lower()
        
        for element in required_elements:
            if element.lower() not in content_lower:
                print(f"Missing required element: {element}")
                return False
        
        return True
    
    def _get_fallback_html_game(self) -> str:
        """Return a minimal working HTML/JavaScript game as fallback."""
        return '''<!DOCTYPE html>
<html>
<head>
    <title>Simple Space Shooter</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/p5.js/1.7.0/p5.min.js"></script>
    <style>
        body {
            margin: 0;
            padding: 20px;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            background-color: #222;
            font-family: Arial, sans-serif;
        }
        main {
            text-align: center;
        }
        h1 {
            color: white;
            margin-bottom: 10px;
        }
    </style>
</head>
<body>
    <main>
        <h1>Simple Space Shooter</h1>
        <div id="game-container"></div>
        <p style="color: white; font-size: 14px; margin-top: 10px;">
            Use ARROW KEYS to move • SPACEBAR to shoot
        </p>
    </main>

    <script>
        let player;
        let bullets = [];
        let enemies = [];
        let score = 0;
        let gameOver = false;

        function setup() {
            let canvas = createCanvas(800, 600);
            canvas.parent('game-container');
            
            // Initialize player
            player = {
                x: width / 2,
                y: height - 50,
                size: 30,
                speed: 5
            };
            
            // Spawn initial enemies
            for (let i = 0; i < 5; i++) {
                spawnEnemy();
            }
        }

        function draw() {
            background(0, 0, 50);
            
            if (gameOver) {
                drawGameOver();
                return;
            }
            
            // Update and draw player
            updatePlayer();
            drawPlayer();
            
            // Update and draw bullets
            updateBullets();
            drawBullets();
            
            // Update and draw enemies
            updateEnemies();
            drawEnemies();
            
            // Check collisions
            checkCollisions();
            
            // Draw UI
            drawUI();
            
            // Spawn new enemies
            if (frameCount % 120 === 0) {
                spawnEnemy();
            }
        }

        function updatePlayer() {
            if (keyIsDown(LEFT_ARROW) && player.x > player.size/2) {
                player.x -= player.speed;
            }
            if (keyIsDown(RIGHT_ARROW) && player.x < width - player.size/2) {
                player.x += player.speed;
            }
            if (keyIsDown(UP_ARROW) && player.y > player.size/2) {
                player.y -= player.speed;
            }
            if (keyIsDown(DOWN_ARROW) && player.y < height - player.size/2) {
                player.y += player.speed;
            }
        }

        function drawPlayer() {
            fill(100, 200, 255);
            stroke(255);
            strokeWeight(2);
            triangle(player.x, player.y - player.size/2, 
                    player.x - player.size/2, player.y + player.size/2,
                    player.x + player.size/2, player.y + player.size/2);
        }

        function updateBullets() {
            for (let i = bullets.length - 1; i >= 0; i--) {
                bullets[i].y -= bullets[i].speed;
                if (bullets[i].y < 0) {
                    bullets.splice(i, 1);
                }
            }
        }

        function drawBullets() {
            fill(255, 255, 0);
            noStroke();
            for (let bullet of bullets) {
                ellipse(bullet.x, bullet.y, bullet.size);
            }
        }

        function updateEnemies() {
            for (let i = enemies.length - 1; i >= 0; i--) {
                enemies[i].y += enemies[i].speed;
                if (enemies[i].y > height + 50) {
                    enemies.splice(i, 1);
                }
            }
        }

        function drawEnemies() {
            fill(255, 100, 100);
            stroke(255);
            strokeWeight(1);
            for (let enemy of enemies) {
                rect(enemy.x - enemy.size/2, enemy.y - enemy.size/2, enemy.size, enemy.size);
            }
        }

        function spawnEnemy() {
            enemies.push({
                x: random(50, width - 50),
                y: -30,
                size: 25,
                speed: random(1, 3)
            });
        }

        function checkCollisions() {
            // Bullet-enemy collisions
            for (let i = bullets.length - 1; i >= 0; i--) {
                for (let j = enemies.length - 1; j >= 0; j--) {
                    let bullet = bullets[i];
                    let enemy = enemies[j];
                    let distance = dist(bullet.x, bullet.y, enemy.x, enemy.y);
                    
                    if (distance < bullet.size/2 + enemy.size/2) {
                        bullets.splice(i, 1);
                        enemies.splice(j, 1);
                        score += 10;
                        break;
                    }
                }
            }
            
            // Player-enemy collisions
            for (let enemy of enemies) {
                let distance = dist(player.x, player.y, enemy.x, enemy.y);
                if (distance < player.size/2 + enemy.size/2) {
                    gameOver = true;
                }
            }
        }

        function drawUI() {
            fill(255);
            textAlign(LEFT);
            textSize(20);
            text("Score: " + score, 20, 30);
        }

        function drawGameOver() {
            fill(255, 0, 0, 150);
            rect(0, 0, width, height);
            
            fill(255);
            textAlign(CENTER);
            textSize(48);
            text("GAME OVER", width/2, height/2 - 50);
            textSize(24);
            text("Final Score: " + score, width/2, height/2);
            text("Press R to restart", width/2, height/2 + 40);
        }

        function keyPressed() {
            if (key === ' ' && !gameOver) {
                bullets.push({
                    x: player.x,
                    y: player.y - player.size/2,
                    size: 8,
                    speed: 7
                });
            }
            
            if (key === 'r' || key === 'R') {
                if (gameOver) {
                    // Restart game
                    gameOver = false;
                    score = 0;
                    bullets = [];
                    enemies = [];
                    player.x = width / 2;
                    player.y = height - 50;
                    for (let i = 0; i < 5; i++) {
                        spawnEnemy();
                    }
                }
            }
        }
    </script>
</body>
</html>'''
    
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
