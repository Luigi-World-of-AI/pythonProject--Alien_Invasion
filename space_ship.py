import pygame.image

from settings import Settings
from pygame.sprite import Sprite


class Ship(Settings, Sprite):

    def __init__(self, settings, screen, key_cap):
        # super = Settings
        super().__init__(key_cap)
        # define nave configurada em settings
        self.screen = screen
        self.settings = settings
        self.default_image = pygame.transform.smoothscale(self.image_ship, settings.ship_size)
        self.rect = self.default_image.get_rect()
        self.screen_rect = screen.get_rect()

        # alinha centro da tela com o da nave
        self.rect.centery = float(self.screen_rect.centery)
        self.rect.centerx = float(self.screen_rect.centerx)

        # nave sem movimento por padrão
        self.move_right = False
        self.move_left = False
        self.move_up = False
        self.move_down = False

    def update_movement(self):
        # direction movement's flags
        if self.move_up and self.rect.top >= 11:
            self.rect.centery -= self.settings.ship_speed

        if self.move_right and self.rect.right <= self.screen_rect.right - 11:
            self.rect.centerx += self.settings.ship_speed

        if self.move_down and self.rect.bottom <= self.screen_rect.bottom - 10:
            self.rect.centery += self.settings.ship_speed

        if self.move_left and self.rect.left >= 10:
            self.rect.centerx -= self.settings.ship_speed

    def blitme(self):
        # garante posição correta da imagem
        self.screen.blit(self.default_image, self.rect)
