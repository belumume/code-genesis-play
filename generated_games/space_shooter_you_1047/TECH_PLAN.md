# Stellar Drift: Technical Implementation Plan

## 1. File Structure

```
stellar_drift/
├── main.py                     # Entry point
├── requirements.txt            # Dependencies
├── config.py                   # Game configuration constants
├── 
├── core/
│   ├── __init__.py
│   ├── game.py                 # Main game class
│   ├── scene_manager.py        # Scene management system
│   ├── input_manager.py        # Input handling
│   ├── audio_manager.py        # Audio system
│   ├── particle_system.py      # Particle effects
│   └── collision_manager.py    # Collision detection
│
├── entities/
│   ├── __init__.py
│   ├── base_entity.py          # Base entity class
│   ├── player.py               # Player ship
│   ├── asteroid.py             # Asteroid variants
│   ├── projectile.py           # Bullets and lasers
│   ├── powerup.py              # Power-up items
│   └── particle.py             # Individual particles
│
├── components/
│   ├── __init__.py
│   ├── transform.py            # Position, rotation, scale
│   ├── physics.py              # Velocity, acceleration
│   ├── sprite.py               # Rendering component
│   ├── collider.py             # Collision boundaries
│   ├── health.py               # Health/damage system
│   └── weapon.py               # Weapon systems
│
├── systems/
│   ├── __init__.py
│   ├── movement_system.py      # Handle entity movement
│   ├── collision_system.py     # Process collisions
│   ├── rendering_system.py     # Draw entities
│   ├── weapon_system.py        # Handle shooting
│   ├── powerup_system.py       # Power-up effects
│   └── spawning_system.py      # Entity spawning
│
├── scenes/
│   ├── __init__.py
│   ├── base_scene.py           # Base scene class
│   ├── menu_scene.py           # Main menu
│   ├── game_scene.py           # Main gameplay
│   ├── pause_scene.py          # Pause overlay
│   ├── game_over_scene.py      # Game over screen
│   └── settings_scene.py       # Settings menu
│
├── ui/
│   ├── __init__.py
│   ├── hud.py                  # In-game HUD
│   ├── menu.py                 # Menu system
│   ├── button.py               # UI buttons
│   ├── progress_bar.py         # Progress bars
│   └── text_display.py         # Text rendering
│
├── utils/
│   ├── __init__.py
│   ├── math_utils.py           # Math utilities
│   ├── color_utils.py          # Color management
│   ├── save_manager.py         # Save/load system
│   ├── leaderboard.py          # Score tracking
│   └── procedural.py           # Procedural generation
│
├── data/
│   ├── saves/                  # Save files
│   ├── config.json             # User settings
│   └── leaderboard.json        # Local scores
│
└── assets/
    ├── sprites/                # Image files
    │   ├── ships/
    │   ├── asteroids/
    │   ├── effects/
    │   └── ui/
    ├── sounds/                 # Audio files
    │   ├── sfx/
    │   └── music/
    └── fonts/                  # Font files
```

## 2. Core Classes and Functions

### 2.1 Base Entity System

```python
# entities/base_entity.py
class BaseEntity:
    def __init__(self, x, y):
        self.components = {}
        self.active = True
        self.marked_for_deletion = False
        
    def add_component(self, component_type, component):
        self.components[component_type] = component
        
    def get_component(self, component_type):
        return self.components.get(component_type)
        
    def has_component(self, component_type):
        return component_type in self.components
        
    def update(self, dt):
        for component in self.components.values():
            if hasattr(component, 'update'):
                component.update(dt)
                
    def destroy(self):
        self.marked_for_deletion = True
```

### 2.2 Component System

```python
# components/transform.py
class Transform:
    def __init__(self, x=0, y=0, rotation=0, scale=1):
        self.position = pygame.Vector2(x, y)
        self.rotation = rotation
        self.scale = scale
        
    def translate(self, dx, dy):
        self.position.x += dx
        self.position.y += dy
        
    def rotate(self, angle):
        self.rotation += angle

# components/physics.py
class Physics:
    def __init__(self, mass=1, drag=0.98):
        self.velocity = pygame.Vector2(0, 0)
        self.acceleration = pygame.Vector2(0, 0)
        self.mass = mass
        self.drag = drag
        self.max_speed = 500
        
    def apply_force(self, force):
        self.acceleration += force / self.mass
        
    def update(self, dt):
        self.velocity += self.acceleration * dt
        self.velocity *= self.drag
        
        if self.velocity.length() > self.max_speed:
            self.velocity.scale_to_length(self.max_speed)
            
        self.acceleration *= 0

# components/collider.py
class Collider:
    def __init__(self, radius, collision_layer="default"):
        self.radius = radius
        self.collision_layer = collision_layer
        self.is_trigger = False
        self.enabled = True
```

### 2.3 Player Ship

```python
# entities/player.py
class Player(BaseEntity):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.setup_components()
        self.boost_meter = 100
        self.boost_recharge_rate = 20
        self.weapon_cooldown = 0
        self.active_powerups = {}
        
    def setup_components(self):
        self.add_component('transform', Transform(x, y))
        self.add_component('physics', Physics(mass=1, drag=0.95))
        self.add_component('sprite', SpriteComponent('ship_basic'))
        self.add_component('collider', Collider(radius=16, collision_layer="player"))
        self.add_component('health', Health(max_health=3))
        self.add_component('weapon', WeaponComponent())
        
    def handle_input(self, input_manager, dt):
        physics = self.get_component('physics')
        transform = self.get_component('transform')
        
        # Movement
        thrust = pygame.Vector2(0, 0)
        if input_manager.is_key_pressed(pygame.K_w):
            thrust.y -= 1
        if input_manager.is_key_pressed(pygame.K_s):
            thrust.y += 1
        if input_manager.is_key_pressed(pygame.K_a):
            thrust.x -= 1
        if input_manager.is_key_pressed(pygame.K_d):
            thrust.x += 1
            
        if thrust.length() > 0:
            thrust.normalize_ip()
            thrust *= 300  # Thrust force
            
        # Boost
        if input_manager.is_mouse_pressed(2) and self.boost_meter > 0:  # Right click
            thrust *= 2
            self.boost_meter -= 100 * dt
            
        physics.apply_force(thrust)
        
        # Rotation towards mouse
        mouse_pos = input_manager.get_mouse_pos()
        player_pos = transform.position
        direction = pygame.Vector2(mouse_pos) - player_pos
        if direction.length() > 0:
            transform.rotation = math.degrees(math.atan2(direction.y, direction.x))
            
        # Shooting
        if input_manager.is_mouse_pressed(0) and self.weapon_cooldown <= 0:  # Left click
            self.shoot()
            
    def shoot(self):
        weapon = self.get_component('weapon')
        transform = self.get_component('transform')
        
        # Create projectile based on current weapon type
        projectile_type = weapon.get_projectile_type()
        # Spawn projectile logic here
        
        self.weapon_cooldown = weapon.fire_rate
        
    def update(self, dt):
        super().update(dt)
        
        # Update boost meter
        if self.boost_meter < 100:
            self.boost_meter += self.boost_recharge_rate * dt
            self.boost_meter = min(100, self.boost_meter)
            
        # Update weapon cooldown
        if self.weapon_cooldown > 0:
            self.weapon_cooldown -= dt
            
        # Update power-ups
        self.update_powerups(dt)
```

### 2.4 Asteroid System

```python
# entities/asteroid.py
class Asteroid(BaseEntity):
    def __init__(self, x, y, size="large", asteroid_type="normal"):
        super().__init__(x, y)
        self.size = size
        self.asteroid_type = asteroid_type
        self.setup_components()
        self.rotation_speed = random.uniform(-90, 90)
        
    def setup_components(self):
        size_data = {
            "large": {"radius": 32, "health": 3, "speed": 50, "points": 200},
            "medium": {"radius": 20, "health": 2, "speed": 80, "points": 100},
            "small": {"radius": 12, "health": 1, "speed": 120, "points": 50}
        }
        
        data = size_data[self.size]
        
        self.add_component('transform', Transform(self.x, self.y))
        self.add_component('physics', Physics(mass=2, drag=1.0))
        self.add_component('sprite', SpriteComponent(f'asteroid_{self.size}_{self.asteroid_type}'))
        self.add_component('collider', Collider(radius=data["radius"], collision_layer="asteroid"))
        self.add_component('health', Health(max_health=data["health"]))
        
        # Set random velocity
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(data["speed"] * 0.5, data["speed"])
        physics = self.get_component('physics')
        physics.velocity = pygame.Vector2(math.cos(angle) * speed, math.sin(angle) * speed)
        
    def update(self, dt):
        super().update(dt)
        
        # Rotate asteroid
        transform = self.get_component('transform')
        transform.rotation += self.rotation_speed * dt
        
        # Screen wrapping
        self.wrap_around_screen()
        
    def take_damage(self, damage):
        health = self.get_component('health')
        health.take_damage(damage)
        
        if health.is_dead():
            self.break_apart()
            
    def break_apart(self):
        if self.size == "large":
            # Spawn 2-3 medium asteroids
            self.spawn_fragments("medium", random.randint(2, 3))
        elif self.size == "medium":
            # Spawn 2-4 small asteroids
            self.spawn_fragments("small", random.randint(2, 4))
        # Small asteroids just disappear
        
        self.destroy()
```

### 2.5 Game Scene Management

```python
# core/scene_manager.py
class SceneManager:
    def __init__(self):
        self.scenes = {}
        self.current_scene = None
        self.scene_stack = []
        
    def register_scene(self, name, scene):
        self.scenes[name] = scene
        
    def change_scene(self, scene_name):
        if self.current_scene:
            self.current_scene.on_exit()
            
        self.current_scene = self.scenes[scene_name]
        self.current_scene.on_enter()
        
    def push_scene(self, scene_name):
        if self.current_scene:
            self.scene_stack.append(self.current_scene)
            self.current_scene.on_pause()
            
        self.current_scene = self.scenes[scene_name]
        self.current_scene.on_enter()
        
    def pop_scene(self):
        if self.current_scene:
            self.current_scene.on_exit()
            
        if self.scene_stack:
            self.current_scene = self.scene_stack.pop()
            self.current_scene.on_resume()
            
    def update(self, dt):
        if self.current_scene:
            self.current_scene.update(dt)
            
    def render(self, screen):
        if self.current_scene:
            self.current_scene.render(screen)

# scenes/game_scene.py
class GameScene(BaseScene):
    def __init__(self, game):
        super().__init__(game)
        self.entities = []
        self.systems = []
        self.setup_systems()
        self.spawn_timer = 0
        self.difficulty_timer = 0
        self.score = 0
        
    def setup_systems(self):
        self.systems = [
            MovementSystem(),
            CollisionSystem(),
            WeaponSystem(),
            PowerupSystem(),
            SpawningSystem(),
            RenderingSystem()
        ]
        
    def on_enter(self):
        # Initialize player
        self.player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.entities.append(self.player)
        
        # Start background music
        self.game.audio_manager.play_music('game_music')
        
    def update(self, dt):
        # Handle input
        self.player.handle_input(self.game.input_manager, dt)
        
        # Update all systems
        for system in self.systems:
            system.update(self.entities, dt)
            
        # Update entities
        for entity in self.entities[:]:
            entity.update(dt)
            if entity.marked_for_deletion:
                self.entities.remove(entity)
                
        # Spawn asteroids
        self.update_spawning(dt)
        
        # Check game over
        if self.player.get_component('health').is_dead():
            self.game.scene_manager.change_scene('game_over')
```

### 2.6 Collision System

```python
# systems/collision_system.py
class CollisionSystem:
    def __init__(self):
        self.collision_pairs = [
            ('player', 'asteroid'),
            ('projectile', 'asteroid'),
            ('player', 'powerup'),
            ('player', 'enemy_projectile')
        ]
        
    def update(self, entities, dt):
        # Spatial partitioning for optimization
        spatial_grid = self.create_spatial_grid(entities)
        
        for layer1, layer2 in self.collision_pairs:
            entities1 = self.get_entities_by_layer(entities, layer1)
            entities2 = self.get_entities_by_layer(entities, layer2)
            
            for entity1 in entities1:
                for entity2 in entities2:
                    if self.check_collision(entity1, entity2):
                        self.handle_collision(entity1, entity2)
                        
    def check_collision(self, entity1, entity2):
        collider1 = entity1.get_component('collider')
        collider2 = entity