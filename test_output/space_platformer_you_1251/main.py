
import pygame
import sys
import math
import random
import json
from enum import Enum
from dataclasses import dataclass
from typing import List, Tuple, Optional

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
FPS = 60
GRAVITY = 980
PLAYER_SPEED = 300
JUMP_FORCE = 500
JETPACK_FORCE = 300
TILE_SIZE = 32

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (100, 150, 255)
GREEN = (100, 255, 100)
RED = (255, 100, 100)
YELLOW = (255, 255, 100)
PURPLE = (255, 100, 255)
CYAN = (100, 255, 255)
ORANGE = (255, 150, 50)
GRAY = (128, 128, 128)
DARK_GRAY = (64, 64, 64)

class GravityDirection(Enum):
    """Enum for gravity directions."""
    DOWN = (0, 1)
    UP = (0, -1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)

class EntityState(Enum):
    """Enum for entity states."""
    IDLE = "idle"
    MOVING = "moving"
    JUMPING = "jumping"
    FALLING = "falling"

@dataclass
class Vector2:
    """2D vector class for position and velocity."""
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
    
    def normalize(self):
        mag = self.magnitude()
        if mag > 0:
            return Vector2(self.x / mag, self.y / mag)
        return Vector2(0, 0)
    
    def magnitude(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)

class Crystal(pygame.sprite.Sprite):
    """Crystal collectible class."""
    def __init__(self, x, y, crystal_type="blue"):
        super().__init__()
        self.crystal_type = crystal_type
        self.pos = Vector2(x, y)
        
        # Set size and color based on type
        if crystal_type == "blue":
            self.size = 20
            self.color = CYAN
            self.value = 1
        elif crystal_type == "green":
            self.size = 24
            self.color = GREEN
            self.value = 5
        elif crystal_type == "red":
            self.size = 28
            self.color = RED
            self.value = 10
        else:  # rainbow
            self.size = 32
            self.color = PURPLE
            self.value = 25
            
        self.rect = pygame.Rect(x - self.size // 2, y - self.size // 2, self.size, self.size)
        self.collected = False
        self.pulse_timer = 0
        
    def update(self, dt):
        """Update crystal animation."""
        self.pulse_timer += dt * 3
        
    def draw(self, screen, camera_offset):
        """Draw the crystal."""
        if not self.collected:
            # Pulsing effect
            pulse = abs(math.sin(self.pulse_timer)) * 0.2 + 0.8
            size = int(self.size * pulse)
            
            pos = (self.rect.centerx - camera_offset[0], self.rect.centery - camera_offset[1])
            pygame.draw.circle(screen, self.color, pos, size // 2)
            pygame.draw.circle(screen, WHITE, pos, size // 4)

class Enemy(pygame.sprite.Sprite):
    """Base enemy class."""
    def __init__(self, x, y, width, height, color, speed=100):
        super().__init__()
        self.pos = Vector2(x, y)
        self.velocity = Vector2(0, 0)
        self.width = width
        self.height = height
        self.color = color
        self.speed = speed
        self.rect = pygame.Rect(x, y, width, height)
        self.direction = 1
        
    def update(self, dt, player, tiles):
        """Update enemy behavior."""
        pass
        
    def draw(self, screen, camera_offset):
        """Draw the enemy."""
        draw_rect = self.rect.copy()
        draw_rect.x -= camera_offset[0]
        draw_rect.y -= camera_offset[1]
        pygame.draw.rect(screen, self.color, draw_rect)

class BlobAlien(Enemy):
    """Blob alien that patrols platforms."""
    def __init__(self, x, y, patrol_distance=200):
        super().__init__(x, y, 30, 30, GREEN, 80)
        self.start_x = x
        self.patrol_distance = patrol_distance
        
    def update(self, dt, player, tiles):
        """Update blob movement."""
        # Simple patrol movement
        self.velocity.x = self.speed * self.direction
        self.pos.x += self.velocity.x * dt
        
        # Change direction at patrol boundaries
        if abs(self.pos.x - self.start_x) > self.patrol_distance:
            self.direction *= -1
            
        self.rect.x = int(self.pos.x)
        self.rect.y = int(self.pos.y)

class FlyingSentinel(Enemy):
    """Flying enemy that chases the player."""
    def __init__(self, x, y, chase_range=300):
        super().__init__(x, y, 40, 20, ORANGE, 120)
        self.chase_range = chase_range
        self.home_pos = Vector2(x, y)
        
    def update(self, dt, player, tiles):
        """Update sentinel behavior."""
        # Calculate distance to player
        dx = player.rect.centerx - self.rect.centerx
        dy = player.rect.centery - self.rect.centery
        distance = math.sqrt(dx ** 2 + dy ** 2)
        
        if distance < self.chase_range:
            # Chase player
            direction = Vector2(dx, dy).normalize()
            self.velocity = direction * self.speed
        else:
            # Return to home position
            dx = self.home_pos.x - self.pos.x
            dy = self.home_pos.y - self.pos.y
            if abs(dx) > 5 or abs(dy) > 5:
                direction = Vector2(dx, dy).normalize()
                self.velocity = direction * self.speed * 0.5
            else:
                self.velocity = Vector2(0, 0)
                
        self.pos += self.velocity * dt
        self.rect.x = int(self.pos.x)
        self.rect.y = int(self.pos.y)
        
    def draw(self, screen, camera_offset):
        """Draw the sentinel as a triangle."""
        points = [
            (self.rect.centerx - 20 - camera_offset[0], self.rect.centery - camera_offset[1]),
            (self.rect.centerx + 20 - camera_offset[0], self.rect.centery - camera_offset[1]),
            (self.rect.centerx - camera_offset[0], self.rect.centery - 10 - camera_offset[1])
        ]
        pygame.draw.polygon(screen, self.color, points)

class Player(pygame.sprite.Sprite):
    """Player character class."""
    def __init__(self, x, y):
        super().__init__()
        self.pos = Vector2(x, y)
        self.velocity = Vector2(0, 0)
        self.width = 32
        self.height = 48
        self.rect = pygame.Rect(x, y, self.width, self.height)
        
        # Movement properties
        self.speed = PLAYER_SPEED
        self.jump_force = JUMP_FORCE
        self.gravity_direction = GravityDirection.DOWN
        self.grounded = False
        self.can_jump = True
        
        # Resources
        self.health = 3
        self.max_health = 3
        self.oxygen = 100.0
        self.max_oxygen = 100.0
        self.jetpack_fuel = 100.0
        self.max_jetpack_fuel = 100.0
        
        # State
        self.state = EntityState.IDLE
        self.invulnerable_timer = 0
        self.gravity_switch_cooldown = 0
        
    def update(self, dt, keys, tiles):
        """Update player state and position."""
        # Update timers
        if self.invulnerable_timer > 0:
            self.invulnerable_timer -= dt
        if self.gravity_switch_cooldown > 0:
            self.gravity_switch_cooldown -= dt
            
        # Deplete oxygen
        self.oxygen -= 5 * dt
        if self.oxygen <= 0:
            self.health = 0
            
        # Handle input
        self.handle_input(keys, dt)
        
        # Apply gravity
        gravity_vec = Vector2(*self.gravity_direction.value) * GRAVITY
        self.velocity += gravity_vec * dt
        
        # Update position
        self.pos += self.velocity * dt
        
        # Check collisions
        self.check_collisions(tiles)
        
        # Update rect
        self.rect.x = int(self.pos.x)
        self.rect.y = int(self.pos.y)
        
        # Regenerate jetpack fuel when grounded
        if self.grounded and self.jetpack_fuel < self.max_jetpack_fuel:
            self.jetpack_fuel += 30 * dt
            self.jetpack_fuel = min(self.jetpack_fuel, self.max_jetpack_fuel)
        
    def handle_input(self, keys, dt):
        """Handle player input."""
        # Horizontal movement
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            if self.gravity_direction in [GravityDirection.DOWN, GravityDirection.UP]:
                self.velocity.x = -self.speed
            else:
                self.velocity.y = -self.speed
        elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            if self.gravity_direction in [GravityDirection.DOWN, GravityDirection.UP]:
                self.velocity.x = self.speed
            else:
                self.velocity.y = self.speed
        else:
            # Apply friction
            if self.gravity_direction in [GravityDirection.DOWN, GravityDirection.UP]:
                self.velocity.x *= 0.8
            else:
                self.velocity.y *= 0.8
                
        # Jump
        if (keys[pygame.K_SPACE] or keys[pygame.K_UP]) and self.grounded and self.can_jump:
            self.jump()
            self.can_jump = False
        elif not (keys[pygame.K_SPACE] or keys[pygame.K_UP]):
            self.can_jump = True
            
        # Gravity switch
        if keys[pygame.K_w] and self.gravity_switch_cooldown <= 0:
            self.switch_gravity()
            self.gravity_switch_cooldown = 0.5
            
        # Jetpack boost
        if keys[pygame.K_LSHIFT] and self.jetpack_fuel > 0:
            self.use_jetpack(dt)
            
    def jump(self):
        """Make the player jump."""
        jump_vec = Vector2(*self.gravity_direction.value) * -self.jump_force
        self.velocity += jump_vec
        self.grounded = False
        self.state = EntityState.JUMPING
        
    def switch_gravity(self):
        """Switch gravity direction."""
        directions = list(GravityDirection)
        current_index = directions.index(self.gravity_direction)
        self.gravity_direction = directions[(current_index + 1) % len(directions)]
        
    def use_jetpack(self, dt):
        """Use jetpack for boost."""
        if self.jetpack_fuel > 0:
            boost_vec = Vector2(*self.gravity_direction.value) * -JETPACK_FORCE
            self.velocity += boost_vec * dt
            self.jetpack_fuel -= 40 * dt
            self.jetpack_fuel = max(0, self.jetpack_fuel)
            
    def check_collisions(self, tiles):
        """Check and resolve collisions with tiles."""
        self.grounded = False
        
        for tile in tiles:
            if self.rect.colliderect(tile):
                # Determine collision direction based on gravity
                if self.gravity_direction == GravityDirection.DOWN:
                    if self.velocity.y > 0:  # Falling
                        self.rect.bottom = tile.top
                        self.pos.y = self.rect.y
                        self.velocity.y = 0
                        self.grounded = True
                    elif self.velocity.y < 0:  # Jumping
                        self.rect.top = tile.bottom
                        self.pos.y = self.rect.y
                        self.velocity.y = 0
                        
                elif self.gravity_direction == GravityDirection.UP:
                    if self.velocity.y < 0:  # Falling up
                        self.rect.top = tile.bottom
                        self.pos.y = self.rect.y
                        self.velocity.y = 0
                        self.grounded = True
                    elif self.velocity.y > 0:  # Jumping down
                        self.rect.bottom = tile.top
                        self.pos.y = self.rect.y
                        self.velocity.y = 0
                        
                elif self.gravity_direction == GravityDirection.RIGHT:
                    if self.velocity.x > 0:  # Falling right
                        self.rect.right = tile.left
                        self.pos.x = self.rect.x
                        self.velocity.x = 0
                        self.grounded = True
                    elif self.velocity.x < 0:  # Jumping left
                        self.rect.left = tile.right
                        self.pos.x = self.rect.x
                        self.velocity.x = 0
                        
                elif self.gravity_direction == GravityDirection.LEFT:
                    if self.velocity.x < 0:  # Falling left
                        self.rect.left = tile.right
                        self.pos.x = self.rect.x
                        self.velocity.x = 0
                        self.grounded = True
                    elif self.velocity.x > 0:  # Jumping right
                        self.rect.right = tile.left
                        self.pos.x = self.rect.x
                        self.velocity.x = 0
                        
                # Handle perpendicular collisions
                if self.gravity_direction in [GravityDirection.DOWN, GravityDirection.UP]:
                    if abs(self.velocity.x) > 0:
                        if self.rect.centerx < tile.centerx:
                            self.rect.right = tile.left
                        else:
                            self.rect.left = tile.right
                        self.pos.x = self.rect.x
                        self.velocity.x = 0
                else:
                    if abs(self.velocity.y) > 0:
                        if self.rect.centery < tile.centery:
                            self.rect.bottom = tile.top
                        else:
                            self.rect.top = tile.bottom
                        self.pos.y = self.rect.y
                        self.velocity.y = 0
                        
    def take_damage(self, damage=1):
        """Take damage if not invulnerable."""
        if self.invulnerable_timer <= 0:
            self.health -= damage
            self.invulnerable_timer = 1.0  # 1 second invulnerability
            
    def draw(self, screen, camera_offset):
        """Draw the player."""
        draw_rect = self.rect.copy()
        draw_rect.x -= camera_offset[0]
        draw_rect.y -= camera_offset[1]
        
        # Flash when invulnerable
        if self.invulnerable_timer > 0 and int(self.invulnerable_timer * 10) % 2:
            return
            
        pygame.draw.rect(screen, BLUE, draw_rect)
        pygame.draw.rect(screen, WHITE, draw_rect, 2)

class Game:
    """Main game class."""
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Crystal Cosmos: Galactic Harvest")
        self.clock = pygame.time.Clock()
        self.camera_offset = [0, 0]
        
        # Initialize game objects
        self.player = Player(100, 400)
        self.crystals = []
        self.enemies = []
        self.tiles = []
        
        # Game state
        self.score = 0
        self.level = 1
        self.game_state = "playing"  # playing, game_over, won
        self.font = pygame.font.Font(None, 36)
        
        self.setup_level()
        
    def setup_level(self):
        """Set up the current level."""
        self.tiles.clear()
        self.crystals.clear()
        self.enemies.clear()
        
        # Create platforms
        platforms = [
            pygame.Rect(0, SCREEN_HEIGHT - 50, SCREEN_WIDTH, 50),  # Ground
            pygame.Rect(200, 600, 200, 20),
            pygame.Rect(500, 500, 200, 20),
            pygame.Rect(800, 400, 200, 20),
            pygame.Rect(300, 300, 200, 20),
            pygame.Rect(600, 200, 200, 20),
        ]
        self.tiles.extend(platforms)
        
        # Create crystals
        crystal_positions = [
            (250, 550, "blue"),
            (550, 450, "blue"),
            (850, 350, "green"),
            (350, 250, "green"),
            (650, 150, "red"),
        ]
        
        for x, y, crystal_type in crystal_positions:
            self.crystals.append(Crystal(x, y, crystal_type))
            
        # Create enemies
        self.enemies.append(BlobAlien(220, 580))
        self.enemies.append(BlobAlien(520, 480))
        self.enemies.append(FlyingSentinel(400, 300))
        
    def update_camera(self):
        """Update camera to follow player."""
        target_x = self.player.rect.centerx - SCREEN_WIDTH // 2
        target_y = self.player.rect.centery - SCREEN_HEIGHT // 2
        
        # Smooth camera movement
        self.camera_offset[0] += (target_x - self.camera_offset[0]) * 0.05
        self.camera_offset[1] += (target_y - self.camera_offset[1]) * 0.05
        
    def handle_events(self):
        """Handle pygame events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r and self.game_state == "game_over":
                    self.restart_game()
                elif event.key == pygame.K_ESCAPE:
                    return False
        return True
        
    def restart_game(self):
        """Restart the game."""
        self.player = Player(100, 400)
        self.score = 0
        self.level = 1
        self.game_state = "playing"
        self.setup_level()
        
    def update(self, dt):
        """Update game state."""
        if self.game_state != "playing":
            return
            
        keys = pygame.key.get_pressed()
        
        # Update player
        self.player.update(dt, keys, self.tiles)
        
        # Update enemies
        for enemy in self.enemies:
            enemy.update(dt, self.player, self.tiles)
            
        # Update crystals
        for crystal in self.crystals:
            crystal.update(dt)
            
        # Check crystal collection
        for crystal in self.crystals[:]:
            if not crystal.collected and self.player.rect.colliderect(crystal.rect):
                crystal.collected = True
                self.score += crystal.value
                self.crystals.remove(crystal)
                
        # Check enemy collisions
        for enemy in self.enemies:
            if self.player.rect.colliderect(enemy.rect):
                self.player.take_damage()
                
        # Check win/lose conditions
        if self.player.health <= 0 or self.player.oxygen <= 0:
            self.game_state = "game_over"
        elif len(self.crystals) == 0:
            self.game_state = "won"
            
        # Update camera
        self.update_camera()
        
    def draw(self):
        """Draw everything."""
        self.screen.fill(BLACK)
        
        # Draw tiles
        for tile in self.tiles:
            draw_rect = tile.copy()
            draw_rect.x -= self.camera_offset[0]
            draw_rect.y -= self.camera_offset[1]
            pygame.draw.rect(self.screen, GRAY, draw_rect)
            
        # Draw crystals
        for crystal in self.crystals:
            crystal.draw(self.screen, self.camera_offset)
            
        # Draw enemies
        for enemy in self.enemies:
            enemy.draw(self.screen, self.camera_offset)
            
        # Draw player
        self.player.draw(self.screen, self.camera_offset)
        
        # Draw UI
        self.draw_ui()
        
        pygame.display.flip()
        
    def draw_ui(self):
        """Draw user interface."""
        # Health bar
        health_width = 200
        health_height = 20
        health_ratio = self.player.health / self.player.max_health
        pygame.draw.rect(self.screen, RED, (10, 10, health_width, health_height))
        pygame.draw.rect(self.screen, GREEN, (10, 10, health_width * health_ratio, health_height))
        
        # Oxygen bar
        oxygen_ratio = self.player.oxygen / self.player.max_oxygen
        pygame.draw.rect(self.screen, BLUE, (10, 40, health_width, health_height))
        pygame.draw.rect(self.screen, CYAN, (10, 40, health_width * oxygen_ratio, health_height))
        
        # Jetpack fuel bar
        fuel_ratio = self.player.jetpack_fuel / self.player.max_jetpack_fuel
        pygame.draw.rect(self.screen, GRAY, (10, 70, health_width, health_height))
        pygame.draw.rect(self.screen, YELLOW, (10, 70, health_width * fuel_ratio, health_height))
        
        # Score
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (10, 100))
        
        # Crystals remaining
        crystals_text = self.font.render(f"Crystals: {len(self.crystals)}", True, WHITE)
        self.screen.blit(crystals_text, (10, 140))
        
        # Game over screen
        if self.game_state == "game_over":
            game_over_text = self.font.render("GAME OVER - Press R to restart", True, RED)
            text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            self.screen.blit(game_over_text, text_rect)
        elif self.game_state == "won":
            win_text = self.font.render("YOU WON! - Press R to restart", True, GREEN)
            text_rect = win_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            self.screen.blit(win_text, text_rect)
            
        # Controls help
        help_text = [
            "Controls: A/D - Move, Space - Jump, W - Switch Gravity, Shift - Jetpack"
        ]
        for i, text in enumerate(help_text):
            help_surface = pygame.font.Font(None, 24).render(text, True, WHITE)
            self.screen.blit(help_surface, (10, SCREEN_HEIGHT - 30 + i * 20))
        
    def run(self):
        """Main game loop."""
        running = True
        while running:
            dt = self.clock.tick(FPS) / 1000.0
            
            running = self.handle_events()
            self.update(dt)
            self.draw()
            
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()
