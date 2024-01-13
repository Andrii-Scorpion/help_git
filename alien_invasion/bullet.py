import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
	"""Class for control bullet, released from ship"""
	def __init__(self, ai_game):
		"""Create object of bullet current position ship"""
		super().__init__()
		self.screen = ai_game.screen
		self.settings = ai_game.settings
		self.color = self.settings.bullet_color

		# Create rect bullet of (0,0) and control right position
		self.rect = pygame.Rect(0, 0, self.settings.bullet_width,
		                        self.settings.bullet_height)
		self.rect.midtop = ai_game.ship.rect.midtop

		# Save position bullet as float value
		self.y = float(self.rect.y)


	def update(self):
		"""Turn bullet up screen"""
		# Update float position bullet
		self.y -= self.settings.bullet_speed
		# Update position rect.
		self.rect.y = self.y

	def draw_bullet(self):
		"""Draw bullet on screen"""
		pygame.draw.rect(self.screen, self.color, self.rect)