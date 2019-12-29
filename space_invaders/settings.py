#game settings
class Settings:

    #init game settings
    def __init__(self):
        #Screen settings
        self.screen_width = 1200
        self.screen_height = 600
        self.bg_color = (230, 230, 230)

        #Ship settings
        self.bullet_capactiy = 3
        self.ship_limit = 3

        #Bullet settings
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (255, 0, 0)

        #Alien settings
        self.fleet_drop_speed = 10

        #How quickly does the game speed up
        self.speedup_scale = 1.1

        #How quickly alien point values increase
        self.score_scale = 1.5

        self.init_dynamic_settings()

    #init settings that change throughout the game
    def init_dynamic_settings(self):
        self.ship_speed = 1.5
        self.bullet_speed = 1.0
        self.alien_speed = 1.0
        #1 for right, -1 for left
        self.fleet_direction = 1

        #Scoring
        self.alien_points = 50

    #increase speed settings
    def increase_speed(self):
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)
