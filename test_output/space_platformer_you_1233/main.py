
import pygame
import json
import sys
import random

# Initialize Pygame
pygame.init()

# Set up the display
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Cosmic Crystal Caper")

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Define game constants
FPS = 60
PLAYER_SPEED = 5
PLAYER_JUMP_SPEED = -15
PLAYER_GRAVITY = 0.8
CRYSTAL_COLLECTION_RANGE = 50
ENEMY_SPEED = 3

# Define game states
STATE_MENU = 0
STATE_GAME = 1
STATE_GAME_OVER = 2
STATE_WIN = 3

# Define player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.centerx = screen_width // 2
        self.rect.bottom = screen_height - 50
        self.speed_x = 0
        self.speed_y = 0
        self.lives = 3
        self.on_ground = False

    def update(self):
        self.speed_x = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.speed_x = -PLAYER_SPEED
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.speed_x = PLAYER_SPEED
        
        self.rect.x += self.speed_x

        # Apply gravity
        self.speed_y += PLAYER_GRAVITY
        self.rect.y += self.speed_y

        # Keep player on screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > screen_width:
            self.rect.right = screen_width
        if self.rect.bottom > screen_height:
            self.rect.bottom = screen_height
            self.speed_y = 0
            self.on_ground = True

    def jump(self):
        if self.on_ground:
            self.speed_y = PLAYER_JUMP_SPEED
            self.on_ground = False

    def collect_crystal(self, crystal):
        if pygame.sprite.collide_rect(self, crystal):
            crystal.kill()
            return True
        return False

    def take_damage(self):
        self.lives -= 1
        if self.lives <= 0:
            self.kill()

# Define enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x=None, y=None):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        if x is not None and y is not None:
            self.rect.x = x
            self.rect.y = y
        else:
            self.rect.x = random.randint(0, screen_width - self.rect.width)
            self.rect.y = 0
        self.speed_y = ENEMY_SPEED

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.top > screen_height:
            self.kill()

# Define crystal class
class Crystal(pygame.sprite.Sprite):
    def __init__(self, x=None, y=None):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        if x is not None and y is not None:
            self.rect.x = x
            self.rect.y = y
        else:
            self.rect.x = random.randint(0, screen_width - self.rect.width)
            self.rect.y = random.randint(50, screen_height - 50)

# Define platform class
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# Define level class
class Level:
    def __init__(self):
        self.platforms = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.crystals = pygame.sprite.Group()
        self.player = Player()
        self.crystals_collected = 0
        self.create_level()

    def create_level(self):
        # Create some platforms
        self.platforms.add(Platform(100, 500, 200, 20))
        self.platforms.add(Platform(400, 400, 200, 20))
        self.platforms.add(Platform(600, 300, 150, 20))
        
        # Create crystals
        self.crystals.add(Crystal(150, 450))
        self.crystals.add(Crystal(450, 350))
        self.crystals.add(Crystal(650, 250))
        
        # Create enemies
        self.enemies.add(Enemy(200, 100))
        self.enemies.add(Enemy(500, 50))

    def update(self):
        self.player.update()
        self.enemies.update()

        # Check collision with platforms
        collided_platforms = pygame.sprite.spritecollide(self.player, self.platforms, False)
        if collided_platforms and self.player.speed_y > 0:
            self.player.rect.bottom = collided_platforms[0].rect.top
            self.player.speed_y = 0
            self.player.on_ground = True

        # Check collision with enemies
        if pygame.sprite.spritecollide(self.player, self.enemies, False):
            self.player.take_damage()

        # Check crystal collection
        for crystal in self.crystals:
            if self.player.collect_crystal(crystal):
                self.crystals_collected += 1
                break

        # Check if all crystals are collected
        if not self.crystals:
            return True

        return False

    def draw(self, screen):
        screen.fill(BLACK)
        self.platforms.draw(screen)
        self.enemies.draw(screen)
        self.crystals.draw(screen)
        screen.blit(self.player.image, self.player.rect)
        
        # Draw UI
        font = pygame.font.Font(None, 36)
        lives_text = font.render(f"Lives: {self.player.lives}", True, WHITE)
        crystals_text = font.render(f"Crystals: {self.crystals_collected}", True, WHITE)
        screen.blit(lives_text, (10, 10))
        screen.blit(crystals_text, (10, 50))

# Set up game variables
game_state = STATE_MENU
current_level = 1
max_levels = 1
clock = pygame.time.Clock()
level = None

# Game loop
running = True
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_state == STATE_GAME:
                level.player.jump()
            elif event.key == pygame.K_RETURN and game_state == STATE_MENU:
                game_state = STATE_GAME
                level = Level()
            elif event.key == pygame.K_RETURN and game_state in [STATE_GAME_OVER, STATE_WIN]:
                game_state = STATE_MENU
                current_level = 1
            elif event.key == pygame.K_ESCAPE:
                running = False

    # Update game state
    if game_state == STATE_GAME:
        level_complete = level.update()
        if not level.player.alive():
            game_state = STATE_GAME_OVER
        elif level_complete:
            game_state = STATE_WIN

    # Draw game objects
    if game_state == STATE_MENU:
        screen.fill(BLACK)
        title_font = pygame.font.Font(None, 48)
        title_text = title_font.render("Cosmic Crystal Caper", True, WHITE)
        title_rect = title_text.get_rect(center=(screen_width // 2, screen_height // 2 - 50))
        screen.blit(title_text, title_rect)

        start_font = pygame.font.Font(None, 24)
        start_text = start_font.render("Press Enter to Start", True, WHITE)
        start_rect = start_text.get_rect(center=(screen_width // 2, screen_height // 2))
        screen.blit(start_text, start_rect)

        controls_text = start_font.render("Arrow Keys/WASD to move, Space to jump", True, WHITE)
        controls_rect = controls_text.get_rect(center=(screen_width // 2, screen_height // 2 + 50))
        screen.blit(controls_text, controls_rect)
        
    elif game_state == STATE_GAME:
        level.draw(screen)
        
    elif game_state == STATE_GAME_OVER:
        screen.fill(BLACK)
        game_over_font = pygame.font.Font(None, 48)
        game_over_text = game_over_font.render("Game Over", True, WHITE)
        game_over_rect = game_over_text.get_rect(center=(screen_width // 2, screen_height // 2 - 50))
        screen.blit(game_over_text, game_over_rect)

        restart_font = pygame.font.Font(None, 24)
        restart_text = restart_font.render("Press Enter to Restart", True, WHITE)
        restart_rect = restart_text.get_rect(center=(screen_width // 2, screen_height // 2))
        screen.blit(restart_text, restart_rect)
        
    elif game_state == STATE_WIN:
        screen.fill(BLACK)
        win_font = pygame.font.Font(None, 48)
        win_text = win_font.render("You Win!", True, WHITE)
        win_rect = win_text.get_rect(center=(screen_width // 2, screen_height // 2 - 50))
        screen.blit(win_text, win_rect)

        restart_font = pygame.font.Font(None, 24)
        restart_text = restart_font.render("Press Enter to Restart", True, WHITE)
        restart_rect = restart_text.get_rect(center=(screen_width // 2, screen_height // 2))
        screen.blit(restart_text, restart_rect)

    pygame.display.flip()
    clock.tick(FPS)

# Quit the game
pygame.quit()
sys.exit()
