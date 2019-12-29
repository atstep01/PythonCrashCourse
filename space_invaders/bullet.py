import pygame
from pygame.sprite import Sprite

#Class representing a bullet
class Bullet(Sprite):

    #create bullet at ships current pos
    def __init__(self, game):
        super().__init__()
        self.screen = game.screen
        self.settings = game.settings
        self.color = self.settings.bullet_color

        #Create bullet rect at (0,0) then set correct loc
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width, self.settings.bullet_height)
        self.rect.midtop = game.ship.rect.midtop

        #Store bullets pos as a decimal value
        self.y = float(self.rect.y)

    #Update bullet location
    def update(self):
        #update decimal pos of bullet
        self.y -= self.settings.bullet_speed
        #update rect pos
        self.rect.y = self.y

    #draw bullet
    def draw_bullet(self):
        pygame.draw.rect(self.screen, self.color, self.rect)
