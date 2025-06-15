# Cloud Hopper - Technical Implementation Plan

## 1. File Structure

```
cloud_hopper/
├── main.py                 # Entry point and game loop
├── requirements.txt        # Python dependencies
├── config.py              # Game constants and settings
├── README.md
│
├── core/
│   ├── __init__.py
│   ├── game.py            # Main game class
│   ├── scene_manager.py   # Scene/state management
│   └── input_handler.py   # Input processing
│
├── entities/
│   ├── __init__.py
│   ├── player.py          # Luna character class
│   ├── cloud.py           # Base cloud class and variants
│   ├── collectibles.py    # Stars, stardust, fragments
│   └── powerups.py        # Power-up implementations
│
├── systems/
│   ├── __init__.py
│   ├── physics.py         # Physics and collision system
│   ├── camera.py          # Camera and viewport management
│   ├── particle.py        # Particle effects system
│   └── save_system.py     # Save/load functionality
│
├── scenes/
│   ├── __init__.py
│   ├── menu.py            # Main menu scene
│   ├── gameplay.py        # Core gameplay scene
│   ├── level_select.py    # Constellation map scene
│   └── pause.py           # Pause menu scene
│
├── ui/
│   ├── __init__.py
│   ├── hud.py             # In-game HUD elements
│   ├── button.py          # Reusable button class
│   └── transitions.py     # Scene transition effects
│
├── utils/
│   ├── __init__.py
│   ├── resource_loader.py # Asset loading and caching
│   ├── timer.py           # Timer utilities
│   └── math_helpers.py    # Vector math, interpolation
│
├── assets/
│   ├── sprites/
│   ├── sounds/
│   ├── music/
│   ├── fonts/
│   └── levels/
│
└── tests/
    ├── test_physics.py
    ├── test_player.py
    └── test_clouds.py
```

## 2. Core Classes and Functions

### Main Game Class
```python
# core/game.py
class Game:
    def __init__(self):
        self.screen: pygame.Surface
        self.clock: pygame.time.Clock
        self.scene_manager: SceneManager
        self.resource_loader: ResourceLoader
        self.running: bool
        
    def run(self):
        """Main game loop"""
    def update(self, dt: float):
        """Update current scene"""
    def render(self):
        """Render current scene"""
    def handle_events(self):
        """Process pygame events"""
```

### Player Entity
```python
# entities/player.py
class Player(pygame.sprite.Sprite):
    def __init__(self, x: float, y: float):
        self.position: pygame.Vector2
        self.velocity: pygame.Vector2
        self.state: PlayerState  # IDLE, JUMPING, FALLING, DASHING
        self.lives: int
        self.jump_count: int
        self.power_up: Optional[PowerUp]
        
    def update(self, dt: float):
        """Update physics and animation"""
    def jump(self):
        """Handle jump mechanics"""
    def collect(self, collectible: Collectible):
        """Handle collection logic"""
```

### Cloud System
```python
# entities/cloud.py
class Cloud(pygame.sprite.Sprite):
    def __init__(self, x: float, y: float, cloud_type: CloudType):
        self.position: pygame.Vector2
        self.cloud_type: CloudType
        self.durability: float
        
    def on_collision(self, player: Player):
        """Handle player landing"""
    def update(self, dt: float):
        """Update cloud behavior"""

class CumulusCloud(Cloud):
    """Stable platform"""

class CirrusCloud(Cloud):
    """Disappearing platform"""
    def __init__(self, x: float, y: float):
        self.fade_timer: float = 2.0

class StormCloud(Cloud):
    """Bouncy but damaging"""
    def __init__(self, x: float, y: float):
        self.damage_timer: float = 1.0
        self.bounce_force: float = 1.5
```

### Physics System
```python
# systems/physics.py
class PhysicsSystem:
    def __init__(self):
        self.gravity: float = 980.0  # pixels/s²
        self.terminal_velocity: float = 600.0
        
    def update(self, entities: List[Entity], dt: float):
        """Apply physics to all entities"""
    def check_collisions(self, player: Player, platforms: pygame.sprite.Group):
        """Detect and resolve collisions"""
    def apply_gravity(self, entity: Entity, dt: float):
        """Apply gravity to entity"""
```

### Camera System
```python
# systems/camera.py
class Camera:
    def __init__(self, width: int, height: int):
        self.viewport: pygame.Rect
        self.target: Optional[Player]
        self.offset: pygame.Vector2
        self.smoothing: float = 0.1
        
    def update(self, dt: float):
        """Smooth follow target"""
    def apply(self, entity: Entity) -> pygame.Vector2:
        """Convert world to screen coordinates"""
    def apply_parallax(self, layer: int, position: pygame.Vector2):
        """Calculate parallax offset for background layers"""
```

## 3. Implementation Order

### Phase 1: Core Foundation (Week 1-2)
1. **Project Setup**
   - Initialize pygame project structure
   - Set up config.py with constants
   - Create basic game loop in main.py

2. **Basic Systems**
   - Implement Scene Manager
   - Create Input Handler
   - Set up Resource Loader

3. **Player Movement**
   - Basic Player class with movement
   - Simple physics (gravity, jumping)
   - Placeholder sprite rendering

### Phase 2: Cloud Mechanics (Week 3-4)
1. **Cloud Implementation**
   - Base Cloud class
   - Cumulus clouds (basic platforms)
   - Collision detection system

2. **Cloud Variants**
   - Cirrus clouds with fade timer
   - Storm clouds with bounce/damage
   - Rainbow clouds with movement paths

3. **Camera System**
   - Vertical scrolling camera
   - Player following logic
   - Boundary constraints

### Phase 3: Collectibles & UI (Week 5-6)
1. **Collectible System**
   - Star collection mechanics
   - Stardust currency
   - Constellation fragments

2. **HUD Implementation**
   - Star counter display
   - Life indicator
   - Timer display

3. **Power-ups**
   - Wind Burst (double jump)
   - Cloud Shoes (duration boost)
   - Star Magnet (attraction radius)

### Phase 4: Game Flow (Week 7-8)
1. **Menu System**
   - Main menu scene
   - Level select (constellation map)
   - Pause functionality

2. **Level Management**
   - Level loading from JSON
   - Win/loss conditions
   - Progress tracking

3. **Save System**
   - Player progress saving
   - Settings persistence
   - High score tracking

### Phase 5: Polish & Effects (Week 9-10)
1. **Visual Effects**
   - Particle system for jumps
   - Star collection effects
   - Cloud puff animations

2. **Audio Integration**
   - Sound effect manager
   - Background music system
   - Dynamic audio based on height

3. **Optimization**
   - Sprite batching
   - Object pooling for clouds
   - Performance profiling

## 4. Key Technical Challenges

### 1. Vertical Infinite Scrolling
**Challenge:** Efficiently manage clouds and objects in vertical space
**Solution:**
- Implement object pooling for clouds
- Only update/render objects within extended viewport
- Procedural generation with predetermined patterns

### 2. Smooth Platform Collision
**Challenge:** Prevent player from clipping through fast-moving platforms
**Solution:**
- Use swept AABB collision detection
- Implement platform snapping when landing
- Multiple collision checks per frame for fast objects

### 3. Touch Controls Responsiveness
**Challenge:** Make touch controls feel as responsive as keyboard
**Solution:**
- Larger touch areas than visual buttons
- Input prediction for jump timing
- Adjustable sensitivity settings

### 4. Performance on Mobile
**Challenge:** Maintain 60 FPS on lower-end devices
**Solution:**
- Level-of-detail system for particles
- Reduce parallax layers on mobile
- Aggressive sprite atlasing

### 5. Save System Compatibility
**Challenge:** Cross-platform save compatibility
**Solution:**
- Use JSON for save data
- Version save files for backward compatibility
- Implement save data validation

## 5. Dependencies and Libraries

### Core Dependencies
```txt
# requirements.txt
pygame==2.5.0          # Main game framework
numpy==1.24.0          # Vector math operations
pytmx==3.32.0          # Tiled map loader (for level design)
```

### Development Dependencies
```txt
# requirements-dev.txt
pytest==7.4.0          # Testing framework
black==23.7.0          # Code formatting
pylint==2.17.0         # Code linting
pygame-gui==0.6.9      # Advanced UI elements (optional)
```

### Optional Libraries
```txt
# For enhanced features
pyinstaller==5.13.0    # Building executables
pygame_sdl2            # Mobile deployment
pyyaml==6.0            # YAML level files (alternative to JSON)
noise==1.2.2           # Perlin noise for cloud generation
```

### Platform-Specific Considerations
- **Windows:** Use cx_Freeze for distribution
- **macOS:** py2app for .app bundle creation  
- **Linux:** AppImage for universal packaging
- **Mobile:** Kivy or BeeWare as alternatives to pygame

### Asset Pipeline Tools
- **Tiled:** Level design and export to JSON/TMX
- **TexturePacker:** Sprite atlas generation
- **Audacity:** Sound effect editing
- **BFXR:** Retro sound effect generation