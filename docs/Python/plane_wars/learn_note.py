import pygame
from plane_sprites import *
    
pygame.init()

screen = pygame.display.set_mode((400, 700))

# Create background
bg = pygame.image.load("./images/background.png")
screen.blit(bg, (0, 0))

# Create hero plane
hero = pygame.image.load("./images/me1.png")
screen.blit(hero, (150, 300))
hero_rect = pygame.Rect(150, 300, 102, 126)

# Enemy Sprite
enemy = GameSprite("./images/enemy1.png")
enemy1 = GameSprite("./images/enemy1.png", 2)

# Enemy Sprite Group
enemy_group = pygame.sprite.Group(enemy, enemy1)

# Refresh screen
pygame.display.update()

# Create a clock object
clock = pygame.time.Clock()

# Game start
while True:

    # Refresh Rate: 1/60
    clock.tick(60)

    # Listening CLOSE event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print("Game quit!")
            pygame.quit()
            exit()

    hero_rect.y -= 1

    # if hero_rect.y <= -126:
    if hero_rect.bottom <= 0:
        hero_rect.y = 700

    screen.blit(bg, (0, 0))
    screen.blit(hero, hero_rect)

    enemy_group.update()
    enemy_group.draw(screen)
    pygame.display.update()
