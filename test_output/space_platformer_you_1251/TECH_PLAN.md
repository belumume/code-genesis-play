# Technical Implementation Plan: Crystal Cosmos

## 1. File Structure

```
crystal_cosmos/
├── main.py                     # Entry point and game loop
├── requirements.txt            # Python dependencies
├── README.md                   # Project documentation
├── config/
│   ├── __init__.py
│   ├── settings.py            # Game configuration constants
│   └── controls.py            # Input mapping configuration
├── core/
│   ├── __init__.py
│   ├── game.py                # Main game state manager
│   ├── scene_manager.py       # Scene/state management
│   └── event_manager.py       # Global event system
├── entities/
│   ├── __init__.py
│   ├── player.py              # Player character class
│   ├── enemies/
│   │   ├── __init__.py
│   │   ├── base_enemy.py      # Base enemy class
│   │   ├── blob_alien.py      # Specific enemy implementations
│   │   ├── flying_sentinel.py
│   │   ├── spike_crawler.py
│   │   └── crystal_mimic.py
│   └── collectibles/
│       ├── __init__.py
│       ├── crystal.py         # Crystal collectible class
│       └── powerup.py         # Power-up items
├── systems/
│   ├── __init__.py
│   ├── physics.py             # Physics and collision system
│   ├── gravity.py             # Gravity manipulation system
│   ├── oxygen.py              # Oxygen management system
│   ├── particle.py            # Particle effects system
│   └── camera.py              # Camera and viewport system
├── levels/
│   ├── __init__.py
│   ├── level.py               # Base level class
│   ├── level_loader.py        # Level data parser
│   ├── tilemap.py             # Tile-based map system
│   └── level_data/            # JSON level definitions
│       ├── sector_1/
│       └── sector_2/
├── ui/
│   ├── __init__.py
│   ├── hud.py                 # In-game HUD
│   ├── menu.py                # Menu system
│   ├── dialog.py              # Dialog/notification system
│   └── widgets/               # Reusable UI components
├── utils/
│   ├── __init__.py
│   ├── vector2.py             # 2D vector math
│   ├── timer.py               # Timer utilities
│   ├── animation.py           # Animation system
│   └── resource_loader.py     # Asset loading system
├── assets/
│   ├── sprites/
│   │   ├── player/
│   │   ├── enemies/
│   │   ├── crystals/
│   │   └── tiles/
│   ├── sounds/
│   │   ├── sfx/
│   │   └── music/
│   ├── fonts/
│   └── data/
│       ├── levels/
│       └── localization/
└── tests/
    ├── __init__.py
    ├── test_physics.py
    ├── test_player.py
    └── test_levels.py
```

## 2. Core Classes and Functions

### 2.1 Main Game Class

```python
# core/game.py
import pygame
from core.scene_manager import SceneManager
from core.event_manager import EventManager
from config.settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.scene_manager = SceneManager()
        self.event_manager = EventManager()
        
    def run(self):
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0
            self.handle_events()
            self.update(dt)
            self.render()
            
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            self.event_manager.process(event)
            
    def update(self, dt):
        self.scene_manager.update(dt)
        
    def render(self):
        self.screen.fill((0, 0, 0))
        self.scene_manager.render(self.screen)
        pygame.display.flip()
```

### 2.2 Player Entity Class

```python
# entities/player.py
import pygame
from utils.vector2 import Vector2
from systems.gravity import GravityDirection

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.pos = Vector2(pos)
        self.velocity = Vector2(0, 0)
        self.gravity_direction = GravityDirection.DOWN
        
        # Movement properties
        self.move_speed = 300
        self.jump_force = 500
        self.jetpack_fuel = 100
        self.max_jetpack_fuel = 100
        
        # Health and oxygen
        self.health = 3
        self.oxygen = 100
        self.max_oxygen = 100
        
        # State management
        self.state = PlayerState.IDLE
        self.grounded = False
        self.facing_right = True
        
        # Collision
        self.rect = pygame.Rect(0, 0, 32, 48)
        self.collision_rect = self.rect.copy()
        
    def update(self, dt):
        self.handle_input()
        self.apply_gravity(dt)
        self.move(dt)
        self.update_animation(dt)
        
    def handle_input(self):
        keys = pygame.key.get_pressed()
        
        # Horizontal movement
        if keys[pygame.K_a]:
            self.velocity.x = -self.move_speed
            self.facing_right = False
        elif keys[pygame.K_d]:
            self.velocity.x = self.move_speed
            self.facing_right = True
        else:
            self.velocity.x *= 0.8  # Friction
            
        # Jump
        if keys[pygame.K_SPACE] and self.grounded:
            self.jump()
            
        # Gravity switch
        if keys[pygame.K_w]:
            self.switch_gravity()
            
        # Jetpack boost
        if keys[pygame.K_LSHIFT] and self.jetpack_fuel > 0:
            self.use_jetpack(dt)
```

### 2.3 Physics System

```python
# systems/physics.py
import pygame
from utils.vector2 import Vector2

class PhysicsSystem:
    def __init__(self):
        self.gravity_strength = 980  # pixels/second^2
        self.collision_groups = {}
        
    def update(self, entities, tilemap, dt):
        for entity in entities:
            if hasattr(entity, 'velocity'):
                # Apply gravity based on entity's gravity direction
                self.apply_gravity(entity, dt)
                
                # Update position
                entity.pos += entity.velocity * dt
                
                # Check collisions
                self.check_collisions(entity, tilemap, entities)
                
    def apply_gravity(self, entity, dt):
        gravity_vector = self.get_gravity_vector(entity.gravity_direction)
        entity.velocity += gravity_vector * self.gravity_strength * dt
        
    def check_collisions(self, entity, tilemap, entities):
        # Tile collisions
        self.check_tile_collisions(entity, tilemap)
        
        # Entity-entity collisions
        self.check_entity_collisions(entity, entities)
        
    def check_tile_collisions(self, entity, tilemap):
        # Get potential collision tiles
        nearby_tiles = tilemap.get_nearby_tiles(entity.rect)
        
        for tile in nearby_tiles:
            if tile.solid and entity.rect.colliderect(tile.rect):
                self.resolve_collision(entity, tile)
```

### 2.4 Level System

```python
# levels/level.py
import json
from levels.tilemap import TileMap
from entities.enemies import enemy_factory
from entities.collectibles import Crystal

class Level:
    def __init__(self, level_data_path):
        self.load_level_data(level_data_path)
        self.tilemap = TileMap(self.tile_data)
        self.entities = pygame.sprite.Group()
        self.crystals = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        
        # Level properties
        self.crystal_quota = self.data.get('crystal_quota', 10)
        self.time_limit = self.data.get('time_limit', 300)
        self.oxygen_stations = []
        
        self.spawn_entities()
        
    def load_level_data(self, path):
        with open(path, 'r') as f:
            self.data = json.load(f)
            self.tile_data = self.data['tiles']
            self.entity_data = self.data['entities']
            
    def spawn_entities(self):
        # Spawn crystals
        for crystal_data in self.entity_data.get('crystals', []):
            crystal = Crystal(
                pos=(crystal_data['x'], crystal_data['y']),
                crystal_type=crystal_data['type'],
                groups=[self.entities, self.crystals]
            )
            
        # Spawn enemies
        for enemy_data in self.entity_data.get('enemies', []):
            enemy = enemy_factory.create(
                enemy_type=enemy_data['type'],
                pos=(enemy_data['x'], enemy_data['y']),
                groups=[self.entities, self.enemies]
            )
```

### 2.5 Camera System

```python
# systems/camera.py
import pygame
from utils.vector2 import Vector2

class Camera:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.pos = Vector2(0, 0)
        self.target = None
        self.bounds = None
        
        # Camera smoothing
        self.smoothing = 0.1
        self.deadzone = pygame.Rect(width//3, height//3, width//3, height//3)
        
    def update(self, dt):
        if self.target:
            # Calculate desired position
            target_pos = Vector2(
                self.target.rect.centerx - self.width // 2,
                self.target.rect.centery - self.height // 2
            )
            
            # Apply smoothing
            self.pos += (target_pos - self.pos) * self.smoothing
            
            # Constrain to level bounds
            if self.bounds:
                self.pos.x = max(0, min(self.pos.x, self.bounds.width - self.width))
                self.pos.y = max(0, min(self.pos.y, self.bounds.height - self.height))
                
    def apply(self, surface, target_surface):
        # Create camera view
        camera_rect = pygame.Rect(self.pos.x, self.pos.y, self.width, self.height)
        target_surface.blit(surface, (0, 0), camera_rect)
```

## 3. Implementation Order

### Phase 1: Core Foundation (Week 1-2)
1. **Project Setup**
   - Initialize repository and file structure
   - Set up virtual environment and dependencies
   - Create basic Pygame window and game loop

2. **Basic Systems**
   - Implement Vector2 math utilities
   - Create basic sprite and animation system
   - Set up resource loader for assets

3. **Player Movement**
   - Basic player class with movement
   - Simple collision detection with rectangles
   - Keyboard input handling

### Phase 2: Core Mechanics (Week 3-4)
1. **Physics System**
   - Gravity implementation
   - Collision detection and response
   - Platform collision resolution

2. **Gravity Switching**
   - Implement gravity direction enum
   - Add gravity switching mechanic
   - Update collision system for all orientations

3. **Level System**
   - Tilemap implementation
   - Level loader from JSON
   - Basic tile rendering

### Phase 3: Game Elements (Week 5-6)
1. **Collectibles**
   - Crystal entity implementation
   - Collection mechanics
   - Score/point system

2. **Enemies**
   - Base enemy class
   - Implement Blob Alien with patrol AI
   - Basic enemy-player collision

3. **Camera System**
   - Following camera
   - Smooth camera movement
   - Level bounds constraints

### Phase 4: Advanced Features (Week 7-8)
1. **Additional Mechanics**
   - Jetpack system with fuel
   - Oxygen system and stations
   - Moving platforms

2. **More Enemies**
   - Flying Sentinel with chase AI
   - Spike Crawler wall movement
   - Crystal Mimic implementation

3. **UI Implementation**
   - HUD with health, oxygen, crystals
   - Pause menu
   - Level complete screen

### Phase 5: Polish and Optimization (Week 9-10)
1. **Visual Effects**
   - Particle system
   - Screen shake effects
   - Transition animations

2. **Audio System**
   - Sound effect integration
   - Background music
   - Dynamic audio based on gameplay

3. **Performance Optimization**
   - Sprite batching
   - Efficient collision detection
   - Memory management

## 4. Key Technical Challenges

### 4.1 Gravity System Implementation
**Challenge**: Implementing omnidirectional gravity that affects all game systems
**Solution**:
- Use a gravity direction enum (UP, DOWN, LEFT, RIGHT)
- Rotate collision detection logic based on gravity
- Transform input based on current gravity orientation
- Update sprite rendering to match gravity direction

### 4.2 Complex Collision Detection
**Challenge**: Handling collisions for various entity types with different behaviors
**Solution**:
- Implement spatial hashing for efficient broad-phase detection
- Use collision layers and masks for selective collision
- Create separate collision resolution for each entity type
- Implement swept collision detection for fast-moving objects

### 4.3 Level Design Tools
**Challenge**: Creating an efficient workflow for level creation
**Solution**:
- Use Tiled map editor for level design
- Create custom Python scripts to convert Tiled files to game format
- Implement hot-reloading for rapid iteration
- Build debug visualization tools

### 4.4 Enemy AI Patterns
**Challenge**: Creating diverse and interesting enemy behaviors
**Solution**:
- Implement finite state machines for enemy AI
- Use behavior trees for complex enemy patterns
- Create reusable AI components (patrol, chase, flee)
- Implement A* pathfinding for intelligent navigation

### 4.5 Performance on Multiple Platforms
**Challenge**: Maintaining 60 FPS across different hardware
**Solution**:
- Implement adjustable quality settings
- Use object pooling for frequently created/destroyed objects
- Optimize sprite rendering with dirty rect updates
- Profile and optimize bottlenecks

## 5. Dependencies and Libraries

### Core Dependencies
```txt
# requirements.txt
pygame==2.5.2          # Game framework
numpy==1.24.3          # Efficient array operations
pytmx==3.32           # Tiled map loader
pygame-gui==0.6.9      # Advanced UI elements
```

### Development Dependencies
```txt
# requirements-dev.txt
pytest==7.4.0          # Testing framework
black==23.7.0          # Code formatting
pylint==2.17.5         # Code linting
pyinstaller==5.13.0    # Executable building
```

### Optional Libraries
```txt
# requirements-optional.txt
numba==0.57.1          #