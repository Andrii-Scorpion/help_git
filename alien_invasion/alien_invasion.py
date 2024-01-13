import sys


from settings import Settings
from ship import Ship
from bullet import Bullet
# from scorpion import Scorpion
import pygame

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

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        # self.scorpion = Scorpion(self)

        # Set color background
        self.bg_color = (230, 230, 230)

    def run_game(self):
        """Start general cycle game"""
        while True:
            self._check_events()
            self.ship.update()
            self._update_bullets()
            self._update_screen()

            self._update_screen()


    def _check_events(self):
        """React for click keyboard and mouse events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)


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

    def _update_screen(self):
        """Update the picture on screen and turn on new screen"""
        # Again printing display on every iteration
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        # self.scorpion.blitme()

        # Show last draw display
        pygame.display.flip()

    def _update_bullets(self):
        self.bullets.update()

        # Delete bullets, if disappeared
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)


if __name__ == "__main__":
    # Create instance game and run game
    ai = AlienInvasion()
    ai.run_game()