import sys
from time import sleep

import pygame

from settings import Settings
from game_stats import GameStats
from ship import Ship
from bullet import Bullet
from alien import Alien
from button import Button
from scoreboard import Scoreboard


#Main game logic
class AlienInvasion:

    #init game resources
    def __init__(self):
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")

        #create an instance to store game stats and scoreboard
        self.stats = GameStats(self)
        self.scoreboard = Scoreboard(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

        #Make play button
        self.play_button = Button(self, "Play")

    #game loop
    def run_game(self):
        while True:
            self._check_events()

            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()

            self._update_screen()

    #update bullets helper
    def _update_bullets(self):
        self.bullets.update()

        #Eradicate bulets after they've left the screen
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()

    #Respond to collisions between aliens and bullets
    def _check_bullet_alien_collisions(self):
        #If a bullet hits an alien remove the alien and the bullet
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)

        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points
            self.scoreboard.prep_score()
            self.scoreboard.check_high_score()

        #when the fleet is dead get rid of bullets and regenerate fleet
        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            #increase level
            self.stats.level += 1
            self.scoreboard.prep_level()

    #update aliens helper
    def _update_aliens(self):
        self._check_fleet_edges()
        self.aliens.update()

        #handle alien and ship collision
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        self._check_aliens_bottom()

    #Respond if ship is hit by alien
    def _ship_hit(self):
        if self.stats.ships_left > 0:
            #decrement ships_left
            self.stats.ships_left -= 1
            self.scoreboard.prep_ships()

            #get rid of any remaining aliens and bullets
            self.aliens.empty()
            self.bullets.empty()

            #create a new fleet and center the ship
            self._create_fleet()
            self.ship.center_ship()

            #Pause
            sleep(0.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    #handle event input
    def _check_events(self):
        #user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                self._check_keydown_event(event)

            elif event.type == pygame.KEYUP:
                self._check_keyup_event(event)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    #handle keydown events
    def _check_keydown_event(self, event):
        if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
            self.ship.moving_left = True
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_q:
            sys.exit()

    #handle keyup events
    def _check_keyup_event(self, event):
        if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
            self.ship.moving_left = False

    #Start new game when player presses play
    def _check_play_button(self, mouse_pos):
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            #reset game settings
            self.settings.init_dynamic_settings()

            #reset game stats
            self.stats.reset_stats()
            self.stats.game_active = True
            self.scoreboard.prep_score()
            self.scoreboard.prep_level()
            self.scoreboard.prep_ships()

            #get rid of remaining aliens and bullets
            self.aliens.empty()
            self.bullets.empty()

            #create new fleet and center the ship
            self._create_fleet()
            self.ship.center_ship()

            #hide mouse
            pygame.mouse.set_visible(False)

    #create new bullet and add it to group
    def _fire_bullet(self):
        if len(self.bullets) < self.settings.bullet_capactiy:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    #create fleet of aliens
    def _create_fleet(self):
        #create an alien and find the number of aliens in a row
        #spacing between each alien is equal to one alien width
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        #determine number of rows of aliens that fit on screen
        ship_height = self.ship.rect.height
        available_space_y = self.settings.screen_height - (3 * alien_height) - ship_height
        number_rows = available_space_y // (2 * alien_height)

        #create fleets of aliens
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    #create a single alien and place it accordingly
    def _create_alien(self, alien_number, row_number):
        #Create alien and place it the row
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    #Check if aliens have reached bottom of the screen
    def _check_aliens_bottom(self):
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self._ship_hit()
                break

    #change direction if aliens have reached edge
    def _check_fleet_edges(self):
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    #change fleet direction and drop them down
    def _change_fleet_direction(self):
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _update_screen(self):
        #redraw screen
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()

        #draw bullets
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)

        #draw score inforation
        self.scoreboard.show_score()

        #draw play button when game is inactive
        if not self.stats.game_active:
            self.play_button.draw_button()

        #draw new screen
        pygame.display.flip()

if __name__ == '__main__':
    #create and run game instance
    game = AlienInvasion()
    game.run_game()
