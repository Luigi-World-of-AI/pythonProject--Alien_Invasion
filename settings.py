import pygame.image
import pygame.transform
from pygame.sprite import Sprite


class Settings:
    # configurações
    def __init__(self, key_cap):
        # screen settings
        self.screen_width = 360
        self.screen_height = 700
        self.image_screen_size = (360, 700)
        self.bg_color = (230, 230, 230)
        self.space_image = pygame.image.load('images/space1.bmp')
        self.space_default_image = pygame.transform.scale(self.space_image, self.image_screen_size)
        self.space_rect = self.space_default_image.get_rect()
        self.alien_points = 50
        self.pause = True

        # ship settings
        self.ship_size = (60, 60)
        # vel. nave semmpre menor que da bala
        self.ship_speed = 6
        self.ship_limit = 3

        # aliens!
        self.alien_size = (60, 60)
        # self.alien_speed = 0
        self.fall_speed = 2.5
        self.move_down = True
        # fleet_direction => 1=right / -1=left
        # self.x_direction = 1
        # delay frames for fall aliens
        self.delay_set = 80
        self.actual_delay = self.delay_set

        # images
        self.image_ship = pygame.image.load('images/ship.bmp')
        self.image_alien = pygame.image.load('images/alien.bmp')
        self.image_bullet = pygame.image.load('images/bullet.bmp')
        self.image_life = pygame.image.load('images/life.bmp')

        # rock settings
        self.size_rocks = [(30, 30), (40, 40), (50, 50), (60, 60)]
        self.rocks = ['images/asteroid1.bmp', 'images/asteroid2.bmp',
                      'images/asteroid3.bmp', 'images/asteroid4.bmp']
        self.move_down_rocks = True
        self.delay_set_rock = 50
        self.actual_delay_rock = self.delay_set_rock
        self.fall_speed_rock = 3.5

        # cores da letra e do fundo
        self.letter = (0, 255, 0)
        self.background = (0, 0, 128)
        self.font = pygame.font.Font('freesansbold.ttf', 16)
        self.text = self.font.render(f'Key Pressed: {key_cap}', True, self.letter, self.background)

        # bullets!
        self.bullet_speed = self.ship_speed * 1.2
        self.bullets_allowed = 3
        self.bullet_size = (15, 60)

        # aliens explosions settings
        # duration of explosion
        self.delay_frame_explosion = 6
        # cronometer changing in loop
        self.actual_frame_explosion = self.delay_frame_explosion

        # rocks explosions settings
        # duration of explosion
        self.delay_frame_explosion_rock = 6
        # cronometer changing in loop
        self.actual_frame_explosion_rock = self.delay_frame_explosion_rock


class Explosion(Sprite):
    def __init__(self, center):
        super().__init__()
        self.image_explosion = pygame.image.load('images/explosion.bmp')
        self.size = (60, 60)
        self.image = pygame.transform.smoothscale(self.image_explosion, self.size)
        self.rect = self.image.get_rect()
        self.rect.center = center
