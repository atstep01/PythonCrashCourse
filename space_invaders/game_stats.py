#Class to handle game statistics
class GameStats:

    #init game stats
    def __init__(self, game):
        self.settings = game.settings
        self.game_active = False
        self.reset_stats()
        self.high_score = 0

    #reset game stats that can change
    def reset_stats(self):
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 0
