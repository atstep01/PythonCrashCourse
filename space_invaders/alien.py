import pygame
from pygame.sprite import Sprite

#Class to represent aliens in the fleet
class Alien(Sprite):

    #init everything for alien
    def __init__(self, game):
        #init the alien and set its starting position
        super().__init__()
        self.screen = game.screen
        self.settings = game.settings

        #load image and set rect
        self.image = pygame.image.load('images/alien.bmp')
        self.rect = self.image.get_rect()

        #start each new alien near the top left of the screen
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        #Store the aliens horizontal pos
        self.x = float(self.rect.x)

    #Update alien position
    def update(self):
        #Move aliens to the right
        self.x += (self.settings.alien_speed * self.settings.fleet_direction)
        self.rect.x = self.x

    #check edges, return true if alien is touching edge
    def check_edges(self):
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True
