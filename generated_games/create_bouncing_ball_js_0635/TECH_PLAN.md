# Technical Implementation Plan: Bounce Lab

## 1. File Structure

```
bounce-lab/
├── main.py                 # Entry point and game loop
├── config.py              # Game constants and settings
├── requirements.txt       # Python dependencies
├── assets/
│   ├── fonts/
│   │   └── roboto.ttf
│   ├── sounds/
│   │   ├── bounce.wav
│   │   └── spawn.wav
│   └── images/
│       └── icon.png
├── src/
│   ├── __init__.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── ball.py       # Ball class
│   │   ├── physics.py    # Physics engine
│   │   └── trail.py      # Trail system
│   ├── ui/
│   │   ├── __init__.py
│   │   ├── gui.py        # GUI controls
│   │   ├── hud.py        # HUD display
│   │   └── effects.py    # Visual effects
│   ├── modes/
│   │   ├── __init__.py
│   │   ├── sandbox.py    # Sandbox mode
│   │   └── challenge.py  # Challenge mode
│   └── utils/
│       ├── __init__.py
│       ├── colors.py     # Color utilities
│       └── export.py     # Screenshot/GIF export
└── tests/
    ├── test_physics.py
    └── test_ball.py
```

## 2. Core Classes and Functions

### Ball Class (src/core/ball.py)
```python
class Ball:
    def __init__(self, x, y, vx, vy, radius=20, color=(0, 128, 255)):
        self.pos = pygame.Vector2(x, y)
        self.vel = pygame.Vector2(vx, vy)
        self.radius = radius
        self.color = color
        self.trail = Trail(max_points=30)
        
    def update(self, dt, gravity, dampening):
        # Apply physics
        self.vel.y += gravity * dt
        self.pos += self.vel * dt
        self.trail.add_point(self.pos.x, self.pos.y)
        
    def check_boundaries(self, width, height, dampening):
        # Boundary collision detection and response
        
    def draw(self, surface):
        # Render ball with shadow effect
```

### Physics Engine (src/core/physics.py)
```python
class PhysicsEngine:
    def __init__(self):
        self.gravity = 500  # pixels/s²
        self.dampening = 0.85
        self.balls = []
        
    def add_ball(self, ball):
        self.balls.append(ball)
        
    def update(self, dt, screen_width, screen_height):
        for ball in self.balls:
            ball.update(dt, self.gravity, self.dampening)
            ball.check_boundaries(screen_width, screen_height, self.dampening)
            
    def check_collisions(self):
        # Ball-to-ball collision detection (optional)
```

### Trail System (src/core/trail.py)
```python
class Trail:
    def __init__(self, max_points=30):
        self.points = deque(maxlen=max_points)
        self.max_alpha = 128
        
    def add_point(self, x, y):
        self.points.append((x, y, time.time()))
        
    def draw(self, surface, color):
        # Draw fading trail with gradient
```

### GUI Manager (src/ui/gui.py)
```python
class GUIManager:
    def __init__(self, screen):
        self.screen = screen
        self.sliders = {
            'gravity': Slider(10, 10, 200, 20, 0.1, 2.0, 1.0),
            'dampening': Slider(10, 40, 200, 20, 0.5, 1.0, 0.85),
            'ball_size': Slider(10, 70, 200, 20, 10, 50, 20)
        }
        
    def handle_event(self, event):
        # Process slider interactions
        
    def draw(self):
        # Render GUI elements
```

## 3. Implementation Order

### Phase 1: Core Foundation (Week 1)
1. Set up project structure and Pygame window
2. Implement basic Ball class with position/velocity
3. Create simple physics update loop
4. Add boundary collision detection
5. Implement basic rendering

### Phase 2: Physics Enhancement (Week 2)
1. Add gravity and dampening parameters
2. Implement trail system
3. Add visual effects for collisions
4. Create color mode system
5. Optimize physics calculations

### Phase 3: User Interface (Week 3)
1. Implement GUI slider system
2. Add keyboard controls
3. Create HUD for displaying parameters
4. Implement pause/resume functionality
5. Add preset configurations

### Phase 4: Game Modes (Week 4)
1. Create mode manager system
2. Implement sandbox mode
3. Add challenge mode framework
4. Create target zone system
5. Implement pattern matching

### Phase 5: Polish & Export (Week 5)
1. Add particle effects
2. Implement sound system
3. Create screenshot functionality
4. Add GIF export capability
5. Performance optimization

## 4. Key Technical Challenges

### Performance Optimization
- **Challenge**: Maintaining 60 FPS with 100+ balls
- **Solution**: 
  - Use spatial partitioning for collision detection
  - Implement object pooling for particles
  - Use pygame.sprite.Group for batch rendering
  - Profile and optimize trail rendering

### Trail Rendering
- **Challenge**: Smooth, gradient trails without performance impact
- **Solution**:
  - Limit trail points per ball
  - Use pygame.gfxdraw for antialiased lines
  - Pre-calculate alpha values
  - Consider using surfaces for complex effects

### GUI Integration
- **Challenge**: Clean GUI without external heavy libraries
- **Solution**:
  - Build lightweight custom slider class
  - Use pygame_gui for complex elements only
  - Implement glass-morphism with surface blending

### Export Functionality
- **Challenge**: Creating GIFs from gameplay
- **Solution**:
  - Use imageio library for GIF creation
  - Implement frame buffer system
  - Limit recording duration/resolution

## 5. Dependencies and Libraries

### requirements.txt
```
pygame==2.5.2
numpy==1.24.3          # For physics calculations
imageio==2.31.1        # For GIF export
pillow==10.0.0         # For image processing
pygame-gui==0.6.9      # Optional: for complex UI
```

### Core Dependencies
- **Pygame**: Main game framework
- **NumPy**: Efficient vector math operations
- **ImageIO**: GIF export functionality

### Optional Dependencies
- **pygame-gui**: Advanced UI elements (if needed)
- **pyinstaller**: For creating standalone executables

### Development Tools
```bash
# Virtual environment setup
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Development dependencies
pip install pytest black pylint
```