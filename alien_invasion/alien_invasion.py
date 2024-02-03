import sys

from time import sleep
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard
# from scorpion import Scorpion
import pygame
import pygame.mixer

class AlienInvasion:
    """General class, which to manage resources and bahavior game"""

    def __init__(self):
        """Initialize the game, create resources game"""

        pygame.init()
        self.settings = Settings()


        self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Alien Invasion")

        # Create exemplar for save game statistics and scoreboard
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()
        # self.scorpion = Scorpion(self)

        # Set color background
        self.bg_color = (230, 230, 230)

        # Create button Play.
        self.play_button = Button(self, "Play")



    def run_game(self):
        """Start general cycle game"""

        sound = pygame.mixer.Sound("sound.wav")

        while True:
            self._check_events()
            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()



            self._update_screen()
            sound.play()

    def _check_events(self):
        """React for click keyboard and mouse events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        """Start new game, when user press on the button Play"""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            # cancel games statistics
            self.settings.initialize_dynamic_settings()
            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()


            # Remove excess aliens and bullet
            self.aliens.empty()
            self.bullets.empty()

            # Create new fleet and centered ship
            self._create_fleet()
            self.ship.center_ship()

            # hide mouse cursor
            pygame.mouse.set_visible(False)



    def _check_keydown_events(self, event):
        """Reaction on click keyboard"""
        if event.key == pygame.K_RIGHT:
            # Turn ship right
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        """Reaction, when keyboard isn't pressed"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        """Create new bullet and add it to the group bullet"""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _create_fleet(self):
        """Create navy aliens"""
        # Create alien
        alien = Alien(self)
        alien_width,alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        # spot, which much row aliens stay in screen.
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height -
                             (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)

        # Create full navy aliens
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)


    def _create_alien(self, alien_number, row_number):
        """Create alien and stay on the row"""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien_width = alien.rect.width
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def _check_fleet_edges(self):
        """React according to what, if the aliens reached  edge of the screen"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Start all fleet and change the fleet direction"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1


    def _update_screen(self):
        """Update the picture on screen and turn on new screen"""
        # Again printing display on every iteration
        self.screen.fill(self.settings.bg_color)

        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)
        # self.scorpion.blitme()

        # Draw information about score
        self.sb.show_score()

        # Draw button Play, if game inactive
        if not self.stats.game_active:
            self.play_button.draw_button()

        # Show last draw display
        pygame.display.flip()

    def _update_bullets(self):
        self.bullets.update()

        # Delete bullets, if disappeared
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collision()

    def _update_aliens(self):
        """Check, if fleet edge of the screen, after update position all aliens from fleet"""
        self._check_fleet_edges()
        self.aliens.update()

        # find collision the bullet with aliens
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

    # Find, if some from alien down brink on the screen
        self._check_aliens_bottom()


    def _check_bullet_alien_collision(self):
        """React on collision the bullet with aliens"""
        # remove all bullet and aliens, if collision

        """Check, if the bullet found its alien. If got hit, remove the bullet and the alien"""
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)


        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
        self.sb.prep_score()
        self.sb.check_high_score()

        if not self.aliens:
            """remove the bullet and create a new fleet"""
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            # Increase level
            self.stats.level += 1
            self.sb.prep_level()



    def _ship_hit(self):
        """React on collision the ship with aliens"""
        # reduce ships_left and update table.
        if self.stats.ships_left > 0:
            self.stats.ships_left -= 1
            self.sb.prep_ships()

        # release from excess aliens and bullet
            self.aliens.empty()
            self.bullets.empty()

        # Create new fleet and centered ship
            self._create_fleet()
            self.ship.center_ship()

        # Pause
            sleep(0.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _check_aliens_bottom(self):
        """Check, if has not reached some alien down brink on the screen"""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                """React, if possible ship was destroyed"""
                self._ship_hit()
                break




if __name__ == "__main__":
    # Create instance game and run game
    ai = AlienInvasion()
    ai.run_game()