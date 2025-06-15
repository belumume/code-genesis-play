import pygame
import sys
import math
import random
import json
from enum import Enum
from typing import List, Optional, Tuple

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
GRAVITY = 980
JUMP_STRENGTH = -500
PLAYER_SPEED = 300
TERMINAL_VELOCITY = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (135, 206, 235)
DARK_BLUE = (0, 0, 139)
PURPLE = (147, 112, 219)
PINK = (255, 182, 193)
YELLOW = (255, 255, 0)
GOLD = (255, 215, 0)
GRAY = (128, 128, 128)
LIGHT_GRAY = (200, 200, 200)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Cloud Types
class CloudType(Enum):
    CUMULUS = 1
    CIRRUS = 2
    STORM = 3
    RAINBOW = 4

# Player States
class PlayerState(Enum):
    IDLE = 1
    JUMPING = 2
    FALLING = 3
    DASHING = 4

# Base Entity Class
class Entity(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        
# Player Class
class Player(Entity):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.width = 30
        self.height = 40
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(PURPLE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        self.state = PlayerState.IDLE
        self.lives = 3
        self.jump_count = 0
        self.max_jumps = 1
        self.on_ground = False
        self.stars_collected = 0
        self.power_up = None
        self.invulnerable_timer = 0
        
    def update(self, dt):
        # Update invulnerability
        if self.invulnerable_timer > 0:
            self.invulnerable_timer -= dt
            
        # Apply gravity
        if not self.on_ground:
            self.velocity.y += GRAVITY * dt
            self.velocity.y = min(self.velocity.y, TERMINAL_VELOCITY)
            
        # Update position
        self.position += self.velocity * dt
        self.rect.x = self.position.x
        self.rect.y = self.position.y
        
        # Update state
        if self.velocity.y < 0:
            self.state = PlayerState.JUMPING
        elif self.velocity.y > 0 and not self.on_ground:
            self.state = PlayerState.FALLING
        else:
            self.state = PlayerState.IDLE
            
        # Update color based on invulnerability
        if self.invulnerable_timer > 0 and int(self.invulnerable_timer * 10) % 2 == 0:
            self.image.fill(WHITE)
        else:
            self.image.fill(PURPLE)
            
    def jump(self):
        if self.jump_count < self.max_jumps:
            self.velocity.y = JUMP_STRENGTH
            self.jump_count += 1
            self.on_ground = False
            
    def move_left(self, dt):
        self.velocity.x = -PLAYER_SPEED
        
    def move_right(self, dt):
        self.velocity.x = PLAYER_SPEED
        
    def stop_horizontal(self):
        self.velocity.x = 0
        
    def take_damage(self):
        if self.invulnerable_timer <= 0:
            self.lives -= 1
            self.invulnerable_timer = 2.0
            return True
        return False

# Cloud Classes
class Cloud(Entity):
    def __init__(self, x, y, cloud_type):
        super().__init__(x, y)
        self.cloud_type = cloud_type
        self.width = 100
        self.height = 30
        self.image = pygame.Surface((self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.active = True
        
    def update(self, dt):
        self.rect.x = self.position.x
        self.rect.y = self.position.y
        
    def on_collision(self, player):
        pass

class CumulusCloud(Cloud):
    def __init__(self, x, y):
        super().__init__(x, y, CloudType.CUMULUS)
        self.image.fill(WHITE)
        
class CirrusCloud(Cloud):
    def __init__(self, x, y):
        super().__init__(x, y, CloudType.CIRRUS)
        self.image.fill(LIGHT_GRAY)
        self.fade_timer = 2.0
        self.touched = False
        
    def update(self, dt):
        super().update(dt)
        if self.touched:
            self.fade_timer -= dt
            if self.fade_timer <= 0:
                self.active = False
            else:
                # Fade effect
                alpha = int(255 * (self.fade_timer / 2.0))
                self.image.set_alpha(alpha)
                
    def on_collision(self, player):
        self.touched = True

class StormCloud(Cloud):
    def __init__(self, x, y):
        super().__init__(x, y, CloudType.STORM)
        self.image.fill(GRAY)
        self.damage_timer = 0
        self.bounce_force = 1.5
        
    def update(self, dt):
        super().update(dt)
        if self.damage_timer > 0:
            self.damage_timer -= dt
            
    def on_collision(self, player):
        if self.damage_timer <= 0:
            player.velocity.y = JUMP_STRENGTH * self.bounce_force
            self.damage_timer = 0.5
            if self.damage_timer > 0.4:  # Small window for damage
                player.take_damage()

class RainbowCloud(Cloud):
    def __init__(self, x, y):
        super().__init__(x, y, CloudType.RAINBOW)
        self.image.fill(PINK)
        self.move_range = 150
        self.move_speed = 50
        self.start_x = x
        self.direction = 1
        
    def update(self, dt):
        super().update(dt)
        # Move back and forth
        self.position.x += self.move_speed * self.direction * dt
        if abs(self.position.x - self.start_x) > self.move_range:
            self.direction *= -1

# Collectibles
class Star(Entity):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.width = 20
        self.height = 20
        self.image = pygame.Surface((self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.collected = False
        self.bob_offset = random.random() * math.pi * 2
        self.original_y = y
        
    def update(self, dt):
        # Bobbing animation
        self.position.y = self.original_y + math.sin(pygame.time.get_ticks() / 500 + self.bob_offset) * 5
        self.rect.y = self.position.y
        
        # Draw star shape
        self.image.fill(BLACK)
        center = (self.width // 2, self.height // 2)
        points = []
        for i in range(5):
            angle = math.pi * 2 * i / 5 - math.pi / 2
            x = center[0] + math.cos(angle) * 10
            y = center[1] + math.sin(angle) * 10
            points.append((x, y))
            angle += math.pi * 2 / 10
            x = center[0] + math.cos(angle) * 5
            y = center[1] + math.sin(angle) * 5
            points.append((x, y))
        pygame.draw.polygon(self.image, GOLD, points)

# Camera Class
class Camera:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.offset = pygame.Vector2(0, 0)
        self.target = None
        self.smoothing = 0.1
        
    def update(self, dt):
        if self.target:
            # Follow player vertically, keep centered horizontally
            target_x = self.width // 2 - self.target.rect.centerx
            target_y = self.height * 0.7 - self.target.rect.centery
            
            # Smooth camera movement
            self.offset.x += (target_x - self.offset.x) * self.smoothing
            self.offset.y += (target_y - self.offset.y) * self.smoothing
            
            # Limit camera to not go below starting position
            self.offset.y = min(self.offset.y, 0)
            
    def apply(self, entity):
        return pygame.Rect(entity.rect.x + self.offset.x, 
                          entity.rect.y + self.offset.y,
                          entity.rect.width, entity.rect.height)

# Particle Class
class Particle:
    def __init__(self, x, y, color, velocity, lifetime):
        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(velocity[0], velocity[1])
        self.color = color
        self.lifetime = lifetime
        self.max_lifetime = lifetime
        self.size = 3
        
    def update(self, dt):
        self.position += self.velocity * dt
        self.velocity.y += GRAVITY * 0.5 * dt
        self.lifetime -= dt
        
    def draw(self, screen, camera):
        if self.lifetime > 0:
            alpha = self.lifetime / self.max_lifetime
            size = int(self.size * alpha)
            pos = (int(self.position.x + camera.offset.x), 
                   int(self.position.y + camera.offset.y))
            pygame.draw.circle(screen, self.color, pos, size)

# Game Class
class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Cloud Hopper")
        self.clock = pygame.time.Clock()
        self.running = True
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        
        # Game state
        self.game_over = False
        self.level_complete = False
        self.paused = False
        
        # Initialize game objects
        self.player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100)
        self.camera = Camera(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.camera.target = self.player
        
        # Sprite groups
        self.all_sprites = pygame.sprite.Group()
        self.clouds = pygame.sprite.Group()
        self.stars = pygame.sprite.Group()
        self.particles = []
        
        self.all_sprites.add(self.player)
        
        # Level data
        self.min_stars_required = 3
        self.level_height = 0
        self.max_height_reached = 0
        
        # Generate initial level
        self.generate_level()
        
    def generate_level(self):
        # Generate clouds
        for i in range(50):
            x = random.randint(50, SCREEN_WIDTH - 150)
            y = SCREEN_HEIGHT - 200 - (i * 150)
            
            # Random cloud type
            cloud_type = random.choice([1, 1, 1, 2, 3, 4])  # More cumulus clouds
            
            if cloud_type == 1:
                cloud = CumulusCloud(x, y)
            elif cloud_type == 2:
                cloud = CirrusCloud(x, y)
            elif cloud_type == 3:
                cloud = StormCloud(x, y)
            else:
                cloud = RainbowCloud(x, y)
                
            self.clouds.add(cloud)
            self.all_sprites.add(cloud)
            
        # Generate stars
        for i in range(20):
            x = random.randint(50, SCREEN_WIDTH - 50)
            y = SCREEN_HEIGHT - 300 - (i * 300)
            star = Star(x, y)
            self.stars.add(star)
            self.all_sprites.add(star)
            
        # Add ground platform
        ground = CumulusCloud(SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT - 50)
        ground.width = 400
        ground.image = pygame.Surface((ground.width, ground.height))
        ground.image.fill(GREEN)
        ground.rect = ground.image.get_rect()
        ground.rect.x = ground.position.x
        ground.rect.y = ground.position.y
        self.clouds.add(ground)
        self.all_sprites.add(ground)
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not self.game_over:
                    self.player.jump()
                    # Create jump particles
                    for _ in range(5):
                        vel = (random.randint(-50, 50), random.randint(-100, -50))
                        self.particles.append(Particle(
                            self.player.rect.centerx,
                            self.player.rect.bottom,
                            WHITE,
                            vel,
                            0.5
                        ))
                        
                if event.key == pygame.K_p:
                    self.paused = not self.paused
                    
                if event.key == pygame.K_r and self.game_over:
                    self.reset_game()
                    
    def update(self, dt):
        if self.paused or self.game_over:
            return
            
        # Handle input
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.player.move_left(dt)
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.player.move_right(dt)
        else:
            self.player.stop_horizontal()
            
        # Update all sprites
        self.all_sprites.update(dt)
        
        # Update particles
        self.particles = [p for p in self.particles if p.lifetime > 0]
        for particle in self.particles:
            particle.update(dt)
            
        # Check collisions
        self.check_collisions()
        
        # Update camera
        self.camera.update(dt)
        
        # Track max height
        current_height = -self.player.position.y
        if current_height > self.max_height_reached:
            self.max_height_reached = current_height
            
        # Check win/loss conditions
        if self.player.lives <= 0:
            self.game_over = True
            
        if self.player.position.y > SCREEN_HEIGHT + 100:
            self.player.lives -= 1
            if self.player.lives > 0:
                self.player.position = pygame.Vector2(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100)
                self.player.velocity = pygame.Vector2(0, 0)
            else:
                self.game_over = True
                
        # Check level completion
        if self.player.stars_collected >= self.min_stars_required and self.max_height_reached > 5000:
            self.level_complete = True
            self.game_over = True
            
    def check_collisions(self):
        # Reset on_ground flag
        self.player.on_ground = False
        
        # Check cloud collisions
        for cloud in self.clouds:
            if not cloud.active:
                continue
                
            # Check if player is falling onto cloud
            if (self.player.rect.colliderect(cloud.rect) and 
                self.player.velocity.y > 0 and
                self.player.rect.bottom < cloud.rect.centery + 10):
                
                self.player.position.y = cloud.rect.top - self.player.height
                self.player.velocity.y = 0
                self.player.on_ground = True
                self.player.jump_count = 0
                
                # Cloud-specific effects
                cloud.on_collision(self.player)
                
        # Remove inactive clouds
        for cloud in self.clouds:
            if not cloud.active:
                self.clouds.remove(cloud)
                self.all_sprites.remove(cloud)
                
        # Check star collisions
        for star in self.stars:
            if not star.collected and self.player.rect.colliderect(star.rect):
                star.collected = True
                self.player.stars_collected += 1
                self.stars.remove(star)
                self.all_sprites.remove(star)
                
                # Create collection particles
                for _ in range(10):
                    vel = (random.randint(-100, 100), random.randint(-100, 100))
                    self.particles.append(Particle(
                        star.rect.centerx,
                        star.rect.centery,
                        GOLD,
                        vel,
                        1.0
                    ))
                    
    def draw(self):
        # Background gradient
        for i in range(SCREEN_HEIGHT):
            color_value = int(135 * (1 - i / SCREEN_HEIGHT))
            color = (color_value, color_value + 71, color_value + 100)
            pygame.draw.line(self.screen, color, (0, i), (SCREEN_WIDTH, i))
            
        # Draw all sprites with camera offset
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
            
        # Draw particles
        for particle in self.particles:
            particle.draw(self.screen, self.camera)
            
        # Draw HUD
        self.draw_hud()
        
        # Draw game over or pause screen
        if self.game_over:
            self.draw_game_over()
        elif self.paused:
            self.draw_pause()
            
        pygame.display.flip()
        
    def draw_hud(self):
        # Lives
        lives_text = self.font.render(f"Lives: {self.player.lives}", True, WHITE)
        self.screen.blit(lives_text, (10, 10))
        
        # Stars
        stars_text = self.font.render(f"Stars: {self.player.stars_collected}/{self.min_stars_required}", True, GOLD)
        self.screen.blit(stars_text, (10, 50))
        
        # Height
        height_text = self.small_font.render(f"Height: {int(self.max_height_reached)}m", True, WHITE)
        self.screen.blit(height_text, (10, 90))
        
        # Instructions
        if self.player.position.y > SCREEN_HEIGHT - 200:
            inst_text = self.small_font.render("Arrow Keys/WASD: Move, Space: Jump, P: Pause", True, WHITE)
            text_rect = inst_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 30))
            self.screen.blit(inst_text, text_rect)
            
    def draw_pause(self):
        # Darken screen
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        # Pause text
        pause_text = self.font.render("PAUSED", True, WHITE)
        text_rect = pause_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(pause_text, text_rect)
        
        continue_text = self.small_font.render("Press P to continue", True, WHITE)
        text_rect = continue_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40))
        self.screen.blit(continue_text, text_rect)
        
    def draw_game_over(self):
        # Darken screen
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        if self.level_complete:
            # Victory screen
            victory_text = self.font.render("LEVEL COMPLETE!", True, GOLD)
            text_rect = victory_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 40))
            self.screen.blit(victory_text, text_rect)
            
            score_text = self.small_font.render(f"Stars Collected: {self.player.stars_collected}", True, WHITE)
            text_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            self.screen.blit(score_text, text_rect)
        else:
            # Game over screen
            game_over_text = self.font.render("GAME OVER", True, RED)
            text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 40))
            self.screen.blit(game_over_text, text_rect)
            
            score_text = self.small_font.render(f"Max Height: {int(self.max_height_reached)}m", True, WHITE)
            text_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            self.screen.blit(score_text, text_rect)
            
        restart_text = self.small_font.render("Press R to restart", True, WHITE)
        text_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40))
        self.screen.blit(restart_text, text_rect)
        
    def reset_game(self):
        # Clear existing sprites
        self.all_sprites.empty()
        self.clouds.empty()
        self.stars.empty()
        self.particles.clear()
        
        # Reset player
        self.player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100)
        self.camera.target = self.player
        self.all_sprites.add(self.player)
        
        # Reset game state
        self.game_over = False
        self.level_complete = False
        self.max_height_reached = 0
        
        # Generate new level
        self.generate_level()
        
    def run(self):
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0  # Convert to seconds
            
            self.handle_events()
            self.update(dt)
            self.draw()
            
        pygame.quit()
        sys.exit()

def main():
    game = Game()
    game.run()

if __name__ == "__main__":
    main()