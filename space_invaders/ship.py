import pygame
from pygame.sprite import Sprite

#Class representing a ship
class Ship(Sprite):

    #init ship with starting position
    def __init__(self, game):
        super().__init__()
        self.screen = game.screen
        self.screen_rect = game.screen.get_rect()
        self.settings = game.settings

        #load ship and get the rect
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()

        #start at middle of bottom of window
        self.rect.midbottom = self.screen_rect.midbottom

        #store x val
        self.x = float(self.rect.x)

        #movement flag
        self.moving_right = False
        self.moving_left = False

    def update(self):
        if self.moving_right == True and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left == True and self.rect.left > 0:
            self.x -= self.settings.ship_speed

        self.rect.x = self.x

    #draw the ship at current location
    def blitme(self):
        self.screen.blit(self.image, self.rect)

    #Center ship on screen
    def center_ship(self):
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
