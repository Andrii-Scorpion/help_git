import pygame

class Scorpion:
	def __init__(self, ai_game):
		"""Initialize the ship and set him start position"""
		self.screen = ai_game.screen
		self.screen_rect = ai_game.screen.get_rect()

		# Load picture ship and get that rect
		self.image = pygame.image.load('images/scorpion.bmp')
		self.rect = self.image.get_rect()

		# Create every new ship down display, around centre
		self.rect.midbottom = self.screen_rect.midbottom

	def blitme(self):
		"""Draw the ship in its current location"""
		self.screen.blit(self.image, self.rect)