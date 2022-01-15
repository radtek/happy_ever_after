import pygame
from plane_sprites import *


class PlaneWars(object):
    """The main class of Plane War"""

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(SCREEN_RECT.size)
        self.clock = pygame.time.Clock()
        self.__create_sprites()

        pygame.time.set_timer(CREATE_ENEMY_EVENT, 1000)
        pygame.time.set_timer(HERO_FIRE_EVENT, 500)

    def __create_sprites(self):
        bg1 = Background()
        bg2 = Background(True)
        self.bg_group = pygame.sprite.Group(bg1, bg2)

        self.enemy_group = pygame.sprite.Group()

        self.hero = Hero()
        self.hero_group = pygame.sprite.Group(self.hero)

    def start_game(self):
        while True:
            self.clock.tick(FRAME_PRE_SEC)
            self.__event_handler()
            self.__check_collide()
            self.__update_sprites()

            pygame.display.update()

    def __event_handler(self):
        for event in pygame.event.get():
            # Event: quit game
            if event.type == pygame.QUIT:
                PlaneWars.__game_over()

            # Event: create enemy
            elif event.type == CREATE_ENEMY_EVENT:
                enemy = Enemy()
                self.enemy_group.add(enemy)
            elif event.type == HERO_FIRE_EVENT:
                self.hero.fire()
                
        keys_pressed = pygame.key.get_pressed()
        
        if keys_pressed[pygame.K_RIGHT]:
            # Event: move right 
            self.hero.speed = 3

        elif keys_pressed[pygame.K_LEFT]:
            # Event: move left
            self.hero.speed = -3
        else:
            self.hero.speed = 0


    def __check_collide(self):
        pygame.sprite.groupcollide(self.hero.bullet_group, self.enemy_group, True, True)

        enemies = pygame.sprite.spritecollide(self.hero, self.enemy_group, True)
        if enemies:
            self.hero.kill()
            PlaneWars.__game_over()

    def __update_sprites(self):
        self.bg_group.update()
        self.bg_group.draw(self.screen)

        self.enemy_group.update()
        self.enemy_group.draw(self.screen)

        self.hero_group.update()
        self.hero_group.draw(self.screen)

        self.hero.bullet_group.update()
        self.hero.bullet_group.draw(self.screen)
    
    @staticmethod
    def __game_over():
        pygame.quit()
        exit()

if __name__ == "__main__":
    game = PlaneWars()
    game.start_game()