import random
import pygame

SCREEN_RECT = pygame.Rect(0, 0, 480, 700)
FRAME_PRE_SEC = 60
CREATE_ENEMY_EVENT = pygame.USEREVENT
HERO_FIRE_EVENT = pygame.USEREVENT + 1

class GameSprite(pygame.sprite.Sprite):
    """Sprites of Plane War"""
    
    def __init__(self, image_name, speed=1):
        super().__init__()
        
        self.image = pygame.image.load(image_name)
        self.rect = self.image.get_rect()
        self.speed = speed
    
    def update(self):
        self.rect.y += self.speed


class Background(GameSprite):
    """Background of Plane War"""

    def __init__(self, is_alt=False):
        super().__init__("./images/background.png")

        if is_alt:
            self.rect.y = -self.rect.height

    def update(self):
        super().update()
        if self.rect.y >= SCREEN_RECT.height:
            self.rect.y = -SCREEN_RECT.height


class Enemy(GameSprite):
    """Enemy of Plane War"""

    def __init__(self):
        super().__init__("./images/enemy1.png")
        self.speed = random.randint(1, 3)
        self.rect.bottom = 0
        self.rect.x = random.randint(0, SCREEN_RECT.width - self.rect.width)
    
    def update(self):
        super().update()
        if self.rect.y >= SCREEN_RECT.height:
            self.kill()


class Hero(GameSprite):
    """Hero of Plane War"""
    
    def __init__(self):
        super().__init__("./images/me1.png", 0)
        self.rect.centerx = SCREEN_RECT.centerx
        self.rect.bottom = SCREEN_RECT.bottom - 120

        self.bullet_group = pygame.sprite.Group()
    
    def update(self):   
        self.rect.x += self.speed
        if self.rect.right >= SCREEN_RECT.right:
            self.rect.right = SCREEN_RECT.right
        elif self.rect.x <= 0:
            self.rect.x = 0
        
    def fire(self):

        for i in (0, 1, 2):
            bullet = Bullet()

            bullet.rect.bottom = self.rect.y - i * 15
            bullet.rect.centerx = self.rect.centerx

            self.bullet_group.add(bullet)

class Bullet(GameSprite):
    """Bullet of Plane War"""

    def __init__(self):
        super().__init__("./images/bullet1.png", -2)
    
    def update(self):
        super().update()
        if self.rect.bottom <= 0:
            self.kill()

