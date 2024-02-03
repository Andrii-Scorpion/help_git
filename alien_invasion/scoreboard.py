import io

import pygame.font
from pygame.sprite import Group

from ship import Ship

class Scoreboard:
	"""Class, which represents score"""

	def __init__(self, ai_game):
		"""Initialize attributes, connected with score"""

		"""line from 14-19 created AI Bard on my request"""
		self.high_score = 0

		with io.open("my_record.txt", "r") as f:
			record = f.read()
		self.high_score = int(record)

		self.ai_game = ai_game
		self.screen = ai_game.screen
		self.screen_rect = ai_game.screen.get_rect()
		self.settings = ai_game.settings
		self.stats = ai_game.stats
		self.prep_ships()

		# Settings font for get on the screen score
		self.text_color = (30,30,30)
		self.font = pygame.font.SysFont(None, 48)

		# Prepare image from start score
		self.prep_score()
		self.prep_high_score()
		self.prep_level()



	def prep_score(self):
		"""Prepare score on image"""
		rounded_score = round(self.stats.score)
		score_str = "Score {:,}".format(rounded_score)
		self.score_image = self.font.render(score_str, True, self.text_color, self.settings.bg_color)

		# Show score up on the right corner on screen
		self.score_rect = self.score_image.get_rect()
		self.score_rect.right = self.screen_rect.right - 20
		self.score_rect.top = 20


	def show_score(self):
		"""Draw score,level and ship on the screen"""
		self.screen.blit(self.score_image, self.score_rect)
		self.screen.blit(self.high_score_image, self.high_score_rect)
		self.screen.blit(self.level_image, self.level_rect)
		self.ships.draw(self.screen)

	def prep_high_score(self):
		"""Generate record in the image"""
		"""line 63 I comment, because it don't need to"""
		# self.high_score = round(self.stats.high_score, -1)
		high_score_str = "{:,}".format(self.high_score)
		self.high_score_image = self.font.render(high_score_str, True,
		                        self.text_color, self.settings.bg_color)



		"""This code I used to write the high score"""
		# with open("my_record.txt", "w") as file:
		# 	for record in high_score_str:
		# 		file.write(record)


		# Centered record around horizontal
		self.high_score_rect = self.high_score_image.get_rect()
		self.high_score_rect.centerx = self.screen_rect.centerx
		self.high_score_rect.top = self.score_rect.top


	def check_high_score(self):
		"""Check, if update new record"""
		# if self.stats.score > self.stats.high_score:
		# 	self.stats.high_score = self.stats.score
		"""This code I used to write the high score, but helped me AI Bard"""
		if self.stats.score > self.high_score:
			self.high_score = self.stats.score
			with open("my_record.txt", "w") as f:
				f.write(str(self.high_score))
			self.prep_high_score()



	def prep_level(self):
		"""Prepare level into image"""
		level_score = round(self.stats.level)
		level_score_str = "Level {}".format(level_score)
		# level_str = str(self.stats.level)

		self.level_image = self.font.render(level_score_str, True,
		                                    self.text_color, self.settings.bg_color)
		# Arrange the level below the score
		self.level_rect = self.level_image.get_rect()
		self.level_rect.right = self.score_rect.right
		self.level_rect.top = self.score_rect.bottom + 10

	def prep_ships(self):
		"""Showed, how much stay ships"""
		self.ships = Group()
		for ship_number in range(self.stats.ships_left):
			ship = Ship(self.ai_game)
			ship.rect.x = 10 + ship_number * ship.rect.width
			ship.rect.y = 10
			self.ships.add(ship)













