import pygame
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
