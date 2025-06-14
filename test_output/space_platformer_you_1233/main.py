```python
# main.py
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

    def update(self):
        self.speed_x = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.speed_x = -PLAYER_SPEED
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.speed_x = PLAYER_SPEED
        self.rect.x += self.speed_x

        self.speed_y += PLAYER_GRAVITY
        self.rect.y += self.speed_y

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > screen_width:
            self.rect.right = screen_width
        if self.rect.bottom > screen_height:
            self.rect.bottom = screen_height
            self.speed_y = 0

    def jump(self):
        self.speed_y = PLAYER_JUMP_SPEED

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
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, screen_width - self.rect.width)
        self.rect.y = 0
        self.speed_y = ENEMY_SPEED

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.top > screen_height:
            self.kill()

# Define crystal class
class Crystal(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, screen_width - self.rect.width)
        self.rect.y = random.randint(50, screen_height - 50)

# Define level class
class Level:
    def __init__(self, file_path):
        self.platforms = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.crystals = pygame.sprite.Group()
        self.player = Player()
        self.load(file_path)

    def load(self, file_path):
        with open(file_path, 'r') as file:
            data = json.load(file)
            for platform_data in data['platforms']:
                platform = pygame.sprite.Sprite()
                platform.image = pygame.Surface((platform_data['width'], platform_data['height']))
                platform.image.fill(GREEN)
                platform.rect = platform.image.get_rect()
                platform.rect.x = platform_data['x']
                platform.rect.y = platform_data['y']
                self.platforms.add(platform)
            for enemy_data in data['enemies']:
                enemy = Enemy()
                enemy.rect.x = enemy_data['x']
                enemy.rect.y = enemy_data['y']
                self.enemies.add(enemy)
            for crystal_data in data['crystals']:
                crystal = Crystal()
                crystal.rect.x = crystal_data['x']
                crystal.rect.y = crystal_data['y']
                self.crystals.add(crystal)

    def update(self):
        self.player.update()
        self.enemies.update()

        # Check collision with platforms
        collided_platforms = pygame.sprite.spritecollide(self.player, self.platforms, False)
        if collided_platforms:
            self.player.rect.bottom = collided_platforms[0].rect.top
            self.player.speed_y = 0

        # Check collision with enemies
        if pygame.sprite.spritecollide(self.player, self.enemies, False):
            self.player.take_damage()

        # Check crystal collection
        for crystal in self.crystals:
            if self.player.collect_crystal(crystal):
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
        pygame.display.flip()

# Set up game variables
game_state = STATE_MENU
current_level = 1
max_levels = 3
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
                level = Level(f"levels/level_{current_level:02d}.json")
            elif event.key == pygame.K_RETURN and game_state in [STATE_GAME_OVER, STATE_WIN]:
                game_state = STATE_MENU
                current_level = 1

    # Update game state
    if game_state == STATE_GAME:
        level_complete = level.update()
        if not level.player.alive():
            game_state = STATE_GAME_OVER
        elif level_complete:
            current_level += 1
            if current_level > max_levels:
                game_state = STATE_WIN
            else:
                level = Level(f"levels/level_{current_level:02d}.json")

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

# game.py
import pygame
from player import Player
from enemy import Enemy
from level import Level
from crystal import Crystal
from power_up import PowerUp
from boss import Boss
from utilities import load_image, load_sound, collision_detection

class Game:
    def __init__(self):
        self.game_state = "menu"
        self.current_level = 1
        self.max_levels = 3
        self.player = Player()
        self.level = None
        self.crystals_collected = 0
        self.required_crystals = 0

    def run(self):
        if self.game_state == "menu":
            self.show_menu()
        elif self.game_state == "game":
            self.update()
            self.draw()
        elif self.game_state == "game_over":
            self.show_game_over()
        elif self.game_state == "win":
            self.show_win()

    def load_level(self, level_id):
        file_path = f"levels/level_{level_id:02d}.json"
        self.level = Level(file_path)
        self.player = self.level.player
        self.crystals_collected = 0
        self.required_crystals = len(self.level.crystals)

    def update(self):
        self.player.update()
        self.level.enemies.update()
        self.level.power_ups.update()
        self.level.boss.update()

        # Check collision with platforms
        collision_detection(self.player, self.level.platforms)

        # Check collision with enemies
        if pygame.sprite.spritecollide(self.player, self.level.enemies, False):
            self.player.take_damage()

        # Check collision with power-ups
        power_up_collisions = pygame.sprite.spritecollide(self.player, self.level.power_ups, True)
        for power_up in power_up_collisions:
            power_up.apply(self.player)

        # Check collision with boss
        if pygame.sprite.collide_rect(self.player, self.level.boss):
            self.player.take_damage()

        # Check crystal collection
        for crystal in self.level.crystals:
            if self.player.collect_crystal(crystal):
                self.crystals_collected += 1
                break

        # Check if all crystals are collected
        if self.crystals_collected >= self.required_crystals:
            self.current_level += 1
            if self.current_level > self.max_levels:
                self.game_state = "win"
            else:
                self.load_level(self.current_level)

        # Check if player is alive
        if not self.player.alive():
            self.game_state = "game_over"

    def draw(self):
        self.level.draw(screen)
        pygame.display.flip()

    def show_menu(self):
        # Render menu screen
        pass

    def show_game_over(self):
        # Render game over screen
        pass

    def show_win(self):
        # Render win screen
        pass

# player.py
import pygame
from utilities import load_image

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill((0, 0, 255))
        self.rect = self.image.get_rect()
        self.rect.centerx = screen_width // 2
        self.rect.bottom = screen_height - 50
        self.speed_x = 0
        self.speed_y = 0
        self.lives = 3

    def update(self):
        # Update player position and handle input
        pass

    def draw(self):
        # Render the player character on the screen
        pass

    def handle_collision(self, object):
        # Handle player collisions with game objects
        pass

# enemy.py
import pygame
import random

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, screen_width - self.rect.width)
        self.rect.y = 0
        self.speed_y = 3

    def update(self):
        # Update enemy position and AI behavior
        pass

    def draw(self):
        # Render the enemy character on the screen
        pass

# level.py
import pygame
import json

class Level:
    def __init__(self, file_path):
        self.platforms = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.crystals = pygame.sprite.Group()
        self.power_ups = pygame.sprite.Group()
        self.player = None
        self.boss = None
        self.load(file_path)

    def load(self, file_path):
        # Load level data from a JSON file
        pass

    def update(self):
        # Update level state and check for completion
        pass

    def draw(self):
        # Render level background and objects on the screen
        pass

# crystal.py
import pygame

class Crystal(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill((255, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, screen_width - self.rect.