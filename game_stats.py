class GameStats:
    def __init__(self, settings):
        self.ships_left = None
        self.settings = settings
        self.reset_stats()
        self.game_active = False
        self.score = 0
        self.high_score = 0

    def reset_stats(self):
        self.ships_left = self.settings.ship_limit
        self.score = 0
