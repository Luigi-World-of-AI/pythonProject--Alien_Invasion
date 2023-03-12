from pygame.sprite import Sprite
import pygame.transform
import random


# noinspection PyTypeChecker
class Rock(Sprite):
    def __init__(self, settings, screen):
        super().__init__()
        self.screen = screen
        self.settings = settings

        # Sprite.Group.draw() exige que: a imagem se chame exatamente 'image'
        #                                rect se chame exatamente 'rect'
        self.image_rocks = pygame.image.load(random.choice(settings.rocks))
        self.image = pygame.transform.smoothscale(self.image_rocks, random.choice(settings.size_rocks))
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        self.rect.centerx = random.randint(30, settings.screen_width - 30)
        self.rect.centery = 0
        self.rect.y = 0

    def update(self):
        if self.settings.move_down_rocks:
            self.rect.y += self.settings.fall_speed_rock
