import pygame.font
from pygame.sprite import Group, Sprite


class Scoreboard:
    """A class to report scoring information."""
    def __init__(self, settings, screen, stats):
        """Initialize scorekeeping attributes."""
        self.life = None
        self.high_score_rect = None
        self.high_score_image = None
        self.score_rect = None
        self.score_image = None
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.settings = settings
        self.stats = stats

        # Font settings for scoring information.
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(f'', 48)

        # Prepare the initial score image.
        self.prep_score()
        self.prep_high_score()
        self.prep_life()

    def prep_score(self):
        """Turn the score into a rendered image."""
        rounded_score = int(round(self.stats.score, -1))
        score_str = "{:,}".format(rounded_score)
        self.score_image = self.font.render(score_str, True, self.text_color,
                                            self.settings.bg_color)

        # Display the score at the top right of the screen.
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def show_score(self):
        """Draw score to the screen."""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.life.draw(self.screen)
    
    def prep_high_score(self):
        high_score = int(round(self.stats.high_score, -1))
        high_score_str = "{:,}".format(high_score)
        self.high_score_image = self.font.render(high_score_str, True, self.text_color,
                                                 self.settings.bg_color)
        
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def prep_life(self):
        self.life = Group()
        for life_number in range(self.stats.ships_left):
            ship_life = Life(self.settings)
            ship_life.rect.centerx += (life_number * 30)
            ship_life.rect.centery = 40
            self.life.add(ship_life)


class Life(Sprite):
    def __init__(self, settings):
        super().__init__()
        self.life_default_image = settings.image_life
        self.image = pygame.transform.scale(self.life_default_image, (40, 40))
        self.rect = self.image.get_rect()
        self.rect.centerx = 20
        self.rect.centery = 40
        self.centerx = self.rect.centerx
        self.centery = self.rect.centery
