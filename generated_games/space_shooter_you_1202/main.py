import pygame
import math
import random
import sys
from enum import Enum
from typing import List, Tuple, Optional
from dataclasses import dataclass

# Initialize Pygame
pygame.init()

# Game Constants
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
FPS = 60
BACKGROUND_COLOR = (10, 10, 30)
WHITE = (255, 255, 255)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Ship Constants
SHIP_SIZE = 15
SHIP_ACCELERATION = 400
SHIP_MAX_SPEED = 300
SHIP_ROTATION_SPEED = 5
SHIP_DRAG = 0.98
BOOST_MULTIPLIER = 2.0
BOOST_DRAIN_RATE = 100
BOOST_RECHARGE_RATE = 50
MAX_BOOST = 100

# Weapon Constants
BULLET_SPEED = 500
BULLET_LIFETIME = 2.0
FIRE_RATE = 0.2

# Asteroid Constants
ASTEROID_SPAWN_RATE = 2.0
ASTEROID_MIN_SPEED = 50
ASTEROID_MAX_SPEED = 150
LARGE_ASTEROID_SIZE = 40
MEDIUM_ASTEROID_SIZE = 25
SMALL_ASTEROID_SIZE = 15

# Power-up Constants
POWERUP_SPAWN_RATE = 8.0
POWERUP_SIZE = 20

class PowerUpType(Enum):
    SHIELD = "shield"
    RAPID_FIRE = "rapid_fire"
    TIME_WARP = "time_warp"
    MAGNET = "magnet"
    LASER_BEAM = "laser_beam"

class AsteroidSize(Enum):
    LARGE = 3
    MEDIUM = 2
    SMALL = 1

@dataclass
class Vector2:
    x: float
    y: float
    
    def __add__(self, other):
        return Vector2(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other):
        return Vector2(self.x - other.x, self.y - other.y)
    
    def __mul__(self, scalar):
        return Vector2(self.x * scalar, self.y * scalar)
    
    def __truediv__(self, scalar):
        return Vector2(self.x / scalar, self.y / scalar)
    
    def length(self):
        return math.sqrt(self.x * self.x + self.y * self.y)
    
    def normalize(self):
        length = self.length()
        if length == 0:
            return Vector2(0, 0)
        return Vector2(self.x / length, self.y / length)
    
    def rotate(self, angle):
        cos_a = math.cos(angle)
        sin_a = math.sin(angle)
        return Vector2(
            self.x * cos_a - self.y * sin_a,
            self.x * sin_a + self.y * cos_a
        )
    
    def to_tuple(self):
        return (self.x, self.y)

class PowerUp:
    def __init__(self, powerup_type: PowerUpType, duration: float):
        self.type = powerup_type
        self.duration = duration
        self.remaining_time = duration
        
    def update(self, dt: float) -> bool:
        self.remaining_time -= dt
        return self.remaining_time > 0

class Bullet(pygame.sprite.Sprite):
    def __init__(self, position: Vector2, direction: Vector2):
        super().__init__()
        self.position = Vector2(position.x, position.y)
        self.velocity = direction.normalize() * BULLET_SPEED
        self.lifetime = BULLET_LIFETIME
        self.image = pygame.Surface((4, 4))
        self.image.fill(CYAN)
        self.rect = self.image.get_rect(center=self.position.to_tuple())
        
    def update(self, dt: float):
        self.lifetime -= dt
        if self.lifetime <= 0:
            self.kill()
            return
            
        self.position = self.position + self.velocity * dt
        self.rect.center = self.position.to_tuple()
        
        # Remove if off screen
        if (self.position.x < -10 or self.position.x > SCREEN_WIDTH + 10 or
            self.position.y < -10 or self.position.y > SCREEN_HEIGHT + 10):
            self.kill()

class Particle(pygame.sprite.Sprite):
    def __init__(self, position: Vector2, velocity: Vector2, color: Tuple[int, int, int], lifetime: float):
        super().__init__()
        self.position = Vector2(position.x, position.y)
        self.velocity = velocity
        self.lifetime = lifetime
        self.max_lifetime = lifetime
        self.color = color
        self.image = pygame.Surface((3, 3))
        self.image.fill(color)
        self.rect = self.image.get_rect(center=self.position.to_tuple())
        
    def update(self, dt: float):
        self.lifetime -= dt
        if self.lifetime <= 0:
            self.kill()
            return
            
        self.position = self.position + self.velocity * dt
        self.velocity = self.velocity * 0.95  # Slow down over time
        self.rect.center = self.position.to_tuple()
        
        # Fade out
        alpha = int(255 * (self.lifetime / self.max_lifetime))
        self.image.set_alpha(alpha)

class PowerUpEntity(pygame.sprite.Sprite):
    def __init__(self, position: Vector2, powerup_type: PowerUpType):
        super().__init__()
        self.position = Vector2(position.x, position.y)
        self.type = powerup_type
        self.velocity = Vector2(0, 50)  # Slow downward drift
        self.rotation = 0
        self.rotation_speed = 2
        
        # Color based on type
        color_map = {
            PowerUpType.SHIELD: BLUE,
            PowerUpType.RAPID_FIRE: RED,
            PowerUpType.TIME_WARP: MAGENTA,
            PowerUpType.MAGNET: YELLOW,
            PowerUpType.LASER_BEAM: GREEN
        }
        
        self.image = pygame.Surface((POWERUP_SIZE, POWERUP_SIZE))
        self.image.fill(color_map[powerup_type])
        self.rect = self.image.get_rect(center=self.position.to_tuple())
        
    def update(self, dt: float):
        self.position = self.position + self.velocity * dt
        self.rotation += self.rotation_speed * dt
        self.rect.center = self.position.to_tuple()
        
        # Remove if off screen
        if self.position.y > SCREEN_HEIGHT + 50:
            self.kill()

class Asteroid(pygame.sprite.Sprite):
    def __init__(self, position: Vector2, velocity: Vector2, size: AsteroidSize):
        super().__init__()
        self.position = Vector2(position.x, position.y)
        self.velocity = velocity
        self.size = size
        self.rotation = 0
        self.rotation_speed = random.uniform(-2, 2)
        
        # Size mapping
        size_map = {
            AsteroidSize.LARGE: LARGE_ASTEROID_SIZE,
            AsteroidSize.MEDIUM: MEDIUM_ASTEROID_SIZE,
            AsteroidSize.SMALL: SMALL_ASTEROID_SIZE
        }
        
        self.radius = size_map[size]
        self.image = pygame.Surface((self.radius * 2, self.radius * 2))
        self.image.fill(BACKGROUND_COLOR)
        pygame.draw.circle(self.image, WHITE, (self.radius, self.radius), self.radius, 2)
        self.rect = self.image.get_rect(center=self.position.to_tuple())
        
    def update(self, dt: float, time_scale: float = 1.0):
        self.position = self.position + self.velocity * dt * time_scale
        self.rotation += self.rotation_speed * dt * time_scale
        self.rect.center = self.position.to_tuple()
        
        # Wrap around screen
        if self.position.x < -self.radius:
            self.position.x = SCREEN_WIDTH + self.radius
        elif self.position.x > SCREEN_WIDTH + self.radius:
            self.position.x = -self.radius
        if self.position.y < -self.radius:
            self.position.y = SCREEN_HEIGHT + self.radius
        elif self.position.y > SCREEN_HEIGHT + self.radius:
            self.position.y = -self.radius
            
    def split(self) -> List['Asteroid']:
        if self.size == AsteroidSize.SMALL:
            return []
            
        new_size = AsteroidSize.MEDIUM if self.size == AsteroidSize.LARGE else AsteroidSize.SMALL
        asteroids = []
        
        for i in range(2):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(ASTEROID_MIN_SPEED, ASTEROID_MAX_SPEED) * 1.5
            velocity = Vector2(math.cos(angle) * speed, math.sin(angle) * speed)
            
            offset = Vector2(random.uniform(-20, 20), random.uniform(-20, 20))
            position = self.position + offset
            
            asteroids.append(Asteroid(position, velocity, new_size))
            
        return asteroids

class Ship(pygame.sprite.Sprite):
    def __init__(self, position: Vector2):
        super().__init__()
        self.position = Vector2(position.x, position.y)
        self.velocity = Vector2(0, 0)
        self.rotation = 0
        self.health = 3
        self.boost_meter = MAX_BOOST
        self.fire_timer = 0
        self.active_powerups: List[PowerUp] = []
        self.shield_hits = 0
        
        # Create ship image
        self.image = pygame.Surface((SHIP_SIZE * 2, SHIP_SIZE * 2), pygame.SRCALPHA)
        self.original_image = self.image.copy()
        self.rect = self.image.get_rect(center=self.position.to_tuple())
        self.radius = SHIP_SIZE
        
        self._draw_ship()
        
    def _draw_ship(self):
        self.image.fill((0, 0, 0, 0))
        # Draw triangle ship
        points = [
            (SHIP_SIZE * 2, SHIP_SIZE),  # Tip
            (SHIP_SIZE // 2, SHIP_SIZE + SHIP_SIZE // 2),  # Bottom left
            (SHIP_SIZE // 2, SHIP_SIZE - SHIP_SIZE // 2)   # Bottom right
        ]
        
        color = CYAN
        if self.has_powerup(PowerUpType.SHIELD):
            color = BLUE
            
        pygame.draw.polygon(self.image, color, points)
        
    def update(self, dt: float, input_state: dict):
        # Update power-ups
        self.active_powerups = [p for p in self.active_powerups if p.update(dt)]
        
        # Handle input
        thrust = Vector2(0, 0)
        if input_state.get('up', False):
            thrust.y -= 1
        if input_state.get('down', False):
            thrust.y += 1
        if input_state.get('left', False):
            thrust.x -= 1
        if input_state.get('right', False):
            thrust.x += 1
            
        # Apply thrust
        if thrust.length() > 0:
            thrust = thrust.normalize()
            acceleration = SHIP_ACCELERATION
            
            # Boost
            if input_state.get('boost', False) and self.boost_meter > 0:
                acceleration *= BOOST_MULTIPLIER
                self.boost_meter -= BOOST_DRAIN_RATE * dt
                self.boost_meter = max(0, self.boost_meter)
            else:
                self.boost_meter += BOOST_RECHARGE_RATE * dt
                self.boost_meter = min(MAX_BOOST, self.boost_meter)
                
            self.velocity = self.velocity + thrust * acceleration * dt
            
        # Apply drag
        self.velocity = self.velocity * SHIP_DRAG
        
        # Limit speed
        if self.velocity.length() > SHIP_MAX_SPEED:
            self.velocity = self.velocity.normalize() * SHIP_MAX_SPEED
            
        # Update position
        self.position = self.position + self.velocity * dt
        
        # Keep on screen
        self.position.x = max(SHIP_SIZE, min(SCREEN_WIDTH - SHIP_SIZE, self.position.x))
        self.position.y = max(SHIP_SIZE, min(SCREEN_HEIGHT - SHIP_SIZE, self.position.y))
        
        # Update fire timer
        if self.fire_timer > 0:
            fire_rate = FIRE_RATE
            if self.has_powerup(PowerUpType.RAPID_FIRE):
                fire_rate /= 3
            self.fire_timer -= dt
            
        # Redraw ship
        self._draw_ship()
        self.rect.center = self.position.to_tuple()
        
    def fire(self) -> Optional[Bullet]:
        if self.fire_timer <= 0:
            fire_rate = FIRE_RATE
            if self.has_powerup(PowerUpType.RAPID_FIRE):
                fire_rate /= 3
            self.fire_timer = fire_rate
            
            # Fire direction (up)
            direction = Vector2(0, -1)
            bullet_pos = Vector2(self.position.x, self.position.y - SHIP_SIZE)
            return Bullet(bullet_pos, direction)
        return None
        
    def add_powerup(self, powerup_type: PowerUpType):
        duration_map = {
            PowerUpType.SHIELD: float('inf'),  # Until depleted
            PowerUpType.RAPID_FIRE: 15.0,
            PowerUpType.TIME_WARP: 10.0,
            PowerUpType.MAGNET: 20.0,
            PowerUpType.LASER_BEAM: 12.0
        }
        
        # Remove existing powerup of same type
        self.active_powerups = [p for p in self.active_powerups if p.type != powerup_type]
        
        # Add new powerup
        if powerup_type == PowerUpType.SHIELD:
            self.shield_hits = 3
        self.active_powerups.append(PowerUp(powerup_type, duration_map[powerup_type]))
        
    def has_powerup(self, powerup_type: PowerUpType) -> bool:
        return any(p.type == powerup_type for p in self.active_powerups)
        
    def take_damage(self) -> bool:
        if self.has_powerup(PowerUpType.SHIELD):
            self.shield_hits -= 1
            if self.shield_hits <= 0:
                self.active_powerups = [p for p in self.active_powerups if p.type != PowerUpType.SHIELD]
            return False
        else:
            self.health -= 1
            return self.health <= 0

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Stellar Drift")
        self.clock = pygame.time.Clock()
        self.running = True
        self.paused = False
        
        # Game state
        self.score = 0
        self.survival_time = 0
        self.game_over = False
        self.time_scale = 1.0
        
        # Sprite groups
        self.all_sprites = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.asteroids = pygame.sprite.Group()
        self.powerups = pygame.sprite.Group()
        self.particles = pygame.sprite.Group()
        
        # Create ship
        self.ship = Ship(Vector2(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.all_sprites.add(self.ship)
        
        # Spawn timers
        self.asteroid_spawn_timer = 0
        self.powerup_spawn_timer = 0
        
        # Font for UI
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.paused = not self.paused
                elif event.key == pygame.K_r and self.game_over:
                    self.restart_game()
                    
    def get_input_state(self) -> dict:
        keys = pygame.key.get_pressed()
        return {
            'up': keys[pygame.K_w] or keys[pygame.K_UP],
            'down': keys[pygame.K_s] or keys[pygame.K_DOWN],
            'left': keys[pygame.K_a] or keys[pygame.K_LEFT],
            'right': keys[pygame.K_d] or keys[pygame.K_RIGHT],
            'fire': keys[pygame.K_SPACE],
            'boost': keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]
        }
        
    def spawn_asteroid(self):
        # Choose spawn edge
        edge = random.randint(0, 3)
        if edge == 0:  # Top
            pos = Vector2(random.uniform(0, SCREEN_WIDTH), -50)
            vel = Vector2(random.uniform(-50, 50), random.uniform(50, 150))
        elif edge == 1:  # Right
            pos = Vector2(SCREEN_WIDTH + 50, random.uniform(0, SCREEN_HEIGHT))
            vel = Vector2(random.uniform(-150, -50), random.uniform(-50, 50))
        elif edge == 2:  # Bottom
            pos = Vector2(random.uniform(0, SCREEN_WIDTH), SCREEN_HEIGHT + 50)
            vel = Vector2(random.uniform(-50, 50), random.uniform(-150, -50))
        else:  # Left
            pos = Vector2(-50, random.uniform(0, SCREEN_HEIGHT))
            vel = Vector2(random.uniform(50, 150), random.uniform(-50, 50))
            
        # Random size (favor larger asteroids early)
        size_weights = [0.3, 0.4, 0.3]  # Large, Medium, Small
        size = random.choices(list(AsteroidSize), weights=size_weights)[0]
        
        asteroid = Asteroid(pos, vel, size)
        self.asteroids.add(asteroid)
        self.all_sprites.add(asteroid)
        
    def spawn_powerup(self):
        pos = Vector2(
            random.uniform(50, SCREEN_WIDTH - 50),
            -30
        )
        powerup_type = random.choice(list(PowerUpType))
        powerup = PowerUpEntity(pos, powerup_type)
        self.powerups.add(powerup)
        self.all_sprites.add(powerup)
        
    def create_explosion(self, position: Vector2, color: Tuple[int, int, int] = WHITE):
        for _ in range(10):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(50, 200)
            velocity = Vector2(math.cos(angle) * speed, math.sin(angle) * speed)
            lifetime = random.uniform(0.5, 1.5)
            
            particle = Particle(position, velocity, color, lifetime)
            self.particles.add(particle)
            self.all_sprites.add(particle)
            
    def check_collisions(self):
        # Bullet-asteroid collisions
        for bullet in self.bullets:
            hit_asteroids = pygame.sprite.spritecollide(bullet, self.asteroids, False)
            for asteroid in hit_asteroids:
                bullet.kill()
                asteroid.kill()
                
                # Score based on size
                score_map = {
                    AsteroidSize.SMALL: 50,
                    AsteroidSize.MEDIUM: 100,
                    AsteroidSize.LARGE: 200
                }
                self.score += score_map[asteroid.size]
                
                # Create explosion
                self.create_explosion(asteroid.position)
                
                # Split asteroid
                new_asteroids = asteroid.split()
                for new_asteroid in new_asteroids:
                    self.asteroids.add(new_asteroid)
                    self.all_sprites.add(new_asteroid)
                    
        # Ship-asteroid collisions
        hit_asteroids = pygame.sprite.spritecollide(self.ship, self.asteroids, False)
        for asteroid in hit_asteroids:
            if self.ship.take_damage():
                self.game_over = True
            asteroid.kill()
            self.create_explosion(asteroid.position, RED)
            
            # Split asteroid
            new_asteroids = asteroid.split()
            for new_asteroid in new_asteroids:
                self.asteroids.add(new_asteroid)
                self.all_sprites.add(new_asteroid)
                
        # Ship-powerup collisions
        hit_powerups = pygame.sprite.spritecollide(self.ship, self.powerups, True)
        for powerup in hit_powerups:
            self.ship.add_powerup(powerup.type)
            self.score += 250
            self.create_explosion(powerup.position, YELLOW)
            
    def update(self, dt: float):
        if self.paused or self.game_over:
            return
            
        # Update time scale for time warp
        self.time_scale = 0.5 if self.ship.has_powerup(PowerUpType.TIME_WARP) else 1.0
        
        # Update survival time and score
        self.survival_time += dt
        self.score += int(10 * dt)  # 10 points per second
        
        # Get input and update ship
        input_state = self.get_input_state()
        self.ship.update(dt, input_state)
        
        # Fire weapon
        if input_state['fire']:
            bullet = self.ship.fire()
            if bullet:
                self.bullets.add(bullet)
                self.all_sprites.add(bullet)
                
        # Update sprites
        self.bullets.update(dt)
        self.asteroids.update(dt, self.time_scale)
        self.powerups.update(dt)
        self.particles.update(dt)
        
        # Spawn asteroids
        spawn_rate = ASTEROID_SPAWN_RATE * (1 + self.survival_time / 60)  # Increase over time
        self.asteroid_spawn_timer -= dt
        if self.asteroid_spawn_timer <= 0:
            self.spawn_asteroid()
            self.asteroid_spawn_timer = 1.0 / spawn_rate
            
        # Spawn powerups
        self.powerup_spawn_timer -= dt
        if self.powerup_spawn_timer <= 0:
            self.spawn_powerup()
            self.powerup_spawn_timer = POWERUP_SPAWN_RATE
            
        # Check collisions
        self.check_collisions()
        
    def draw_hud(self):
        # Score
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))
        
        # Health
        health_text = self.font.render(f"Health: {self.ship.health}", True, WHITE)
        self.screen.blit(health_text, (10, 50))
        
        # Boost meter
        boost_percent = self.ship.boost_meter / MAX_BOOST
        boost_bar_width = 200
        boost_bar_height = 20
        boost_bar_rect = pygame.Rect(10, 90, boost_bar_width, boost_bar_height)
        pygame.draw.rect(self.screen, WHITE, boost_bar_rect, 2)
        boost_fill_rect = pygame.Rect(10, 90, int(boost_bar_width * boost_percent), boost_bar_height)
        pygame.draw.rect(self.screen, CYAN, boost_fill_rect)
        
        # Active power-ups
        y_offset = 120
        for powerup in self.ship.active_powerups:
            if powerup.type == PowerUpType.SHIELD:
                text = f"Shield: {self.ship.shield_hits} hits"
            else:
                text = f"{powerup.type.value.replace('_', ' ').title()}: {powerup.remaining_time:.1f}s"
            powerup_text = self.small_font.render(text, True, YELLOW)
            self.screen.blit(powerup_text, (10, y_offset))
            y_offset += 25
            
        # Survival time
        time_text = self.font.render(f"Time: {self.survival_time:.1f}s", True, WHITE)
        self.screen.blit(time_text, (SCREEN_WIDTH - 200, 10))
        
    def draw_game_over(self):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))
        
        game_over_text = self.font.render("GAME OVER", True, RED)
        score_text = self.font.render(f"Final Score: {self.score}", True, WHITE)
        time_text = self.font.render(f"Survival Time: {self.survival_time:.1f}s", True, WHITE)
        restart_text = self.small_font.render("Press R to restart or ESC to quit", True, WHITE)
        
        # Center text
        game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 60))
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20))
        time_rect = time_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60))
        
        self.screen.blit(game_over_text, game_over_rect)
        self.screen.blit(score_text, score_rect)
        self.screen.blit(time_text, time_rect)
        self.screen.blit(restart_text, restart_rect)
        
    def draw_pause(self):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))
        
        pause_text = self.font.render("PAUSED", True, WHITE)
        continue_text = self.small_font.render("Press ESC to continue", True, WHITE)
        
        pause_rect = pause_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20))
        continue_rect = continue_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))
        
        self.screen.blit(pause_text, pause_rect)
        self.screen.blit(continue_text, continue_rect)
        
    def restart_game(self):
        # Clear all sprites
        self.all_sprites.empty()
        self.bullets.empty()
        self.asteroids.empty()
        self.powerups.empty()
        self.particles.empty()
        
        # Reset game state
        self.score = 0
        self.survival_time = 0
        self.game_over = False
        self.time_scale = 1.0
        
        # Create new ship
        self.ship = Ship(Vector2(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.all_sprites.add(self.ship)
        
        # Reset timers
        self.asteroid_spawn_timer = 0
        self.powerup_spawn_timer = 0
        
    def render(self):
        self.screen.fill(BACKGROUND_COLOR)
        
        # Draw stars background
        for _ in range(100):
            x = random.randint(0, SCREEN_WIDTH)
            y = random.randint(0, SCREEN_HEIGHT)
            pygame.draw.circle(self.screen, WHITE, (x, y), 1)
        
        # Draw all sprites
        self.all_sprites.draw(self.screen)
        
        # Draw HUD
        self.draw_hud()
        
        # Draw overlays
        if self.game_over:
            self.draw_game_over()
        elif self.paused:
            self.draw_pause()
            
        pygame.display.flip()
        
    def run(self):
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0  # Delta time in seconds
            
            self.handle_events()
            self.update(dt)
            self.render()
            
        pygame.quit()
        sys.exit()

def main():
    game = Game()
    game.run()

if __name__ == "__main__":
    main()