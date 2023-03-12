import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    """Manage bullets fired from the ship"""

    def __init__(self, settings, screen, ship):
        """Cria uma bala na posição atual da nave"""
        super().__init__()
        self.settings = settings
        self.screen = screen
        self.default_image = pygame.transform.smoothscale(settings.image_bullet, settings.bullet_size)
        self.rect = self.default_image.get_rect()
        self.screen_rect = screen.get_rect()

        # alinha posição da bala com a da nave
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top
        # torna velocidade mais sensível
        self.y = float(self.rect.y)
        # bullet's settings
        self.speed = settings.bullet_speed
        self.continuous_shot = False

    def update(self):
        # update bullet position
        self.y -= self.speed
        self.rect.y = self.y

    def blitme(self):
        self.screen.blit(self.default_image, self.rect)
