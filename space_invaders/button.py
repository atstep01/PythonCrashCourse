import pygame.font

#Class representing a button
class Button:

    #init button stuff
    def __init__(self, game, message):
        self.screen = game.screen
        self.screen_rect = self.screen.get_rect()

        #set the dims and properties of the button
        self.width, self.height = 200, 50
        self.button_color = (0, 255, 0)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)

        #Build and center rect object
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        #prep message
        self._prep_message(message)

    #turn message into an image and center the text on the button
    def _prep_message(self, message):
        self.message_image = self.font.render(message, True, self.text_color, self.button_color)
        self.message_image_rect = self.message_image.get_rect()
        self.message_image_rect.center = self.rect.center

    #draw button and then the text associated with it
    def draw_button(self):
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.message_image, self.message_image_rect)
