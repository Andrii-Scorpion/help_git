import pygame

class Ship:
	"""Class for control ship"""
	def __init__(self, ai_game):
		"""Initialize the ship and set him start position"""
		self.screen = ai_game.screen
		self.settings = ai_game.settings
		self.screen_rect = ai_game.screen.get_rect()

		# Load picture ship and get that rect
		self.image = pygame.image.load('images/ship.bmp')
		self.rect = self.image.get_rect()

		# Create every new ship down display, around centre
		self.rect.midbottom = self.screen_rect.midbottom

		# Save decimal value for position ship, by horizontal
		self.x = float(self.rect.x)

		self.moving_right = False
		self.moving_left = False

	def update(self):
		"""Update the that position ship on general indicator move"""
		if self.moving_right and self.rect.right < self.screen_rect.right:
			self.x += self.settings.ship_speed
		if self.moving_left and self.rect.left > 0:
			self.x -= self.settings.ship_speed

		# Update object rect with self.x
		self.rect.x = self.x

	def blitme(self):
		"""Draw the ship in its current location"""
		self.screen.blit(self.image, self.rect)


