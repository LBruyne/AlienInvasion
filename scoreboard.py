import pygame.font
from pygame.sprite import Group
from ship import Ship

class Scoreboard():
	"""Display your score"""
	def __init__(self,ai_settings,screen,stats):
		"""Initialize the attributes"""
		self.screen = screen
		self.ai_settings = ai_settings
		self.stats = stats
		self.screen_rect = screen.get_rect()
		
		# Settings to display score
		self.text_color = (30,30,30)
		self.font = pygame.font.SysFont(None,48)
		
		# Image 
		self.prep_score()
		self.prep_high_score()
		self.prep_level()
		self.prep_ships()
		
	def prep_score(self):
		"""Translate score into image"""
		rounded_score = round(self.stats.score,-1)
		score_str = "{:,}".format(rounded_score)
		self.score_image = self.font.render(score_str,True,self.text_color,self.ai_settings.bg_color)
		
		# Put the image
		self.score_rect = self.score_image.get_rect()
		self.score_rect.right = self.screen_rect.right - 20
		self.score_rect.top = 20
		
	def prep_high_score(self):
		"""Translate high score into image"""
		high_score = round(self.stats.high_score,-1)
		high_score_str = "{:,}".format(high_score)
		self.high_score_image = self.font.render(high_score_str,True,self.text_color,self.ai_settings.bg_color)
		
		# Put the image
		self.high_score_rect = self.high_score_image.get_rect()
		self.high_score_rect.centerx = self.screen_rect.centerx
		self.high_score_rect.top = self.score_rect.top
		
	def show_score(self):
		"""Display the score"""
		self.screen.blit(self.score_image,self.score_rect)
		self.screen.blit(self.high_score_image,self.high_score_rect)
		self.screen.blit(self.level_image,self.level_rect)
		self.ships.draw(self.screen)
		
	def prep_level(self):
		"""Translate level into image"""
		self.level_image = self.font.render(str(self.stats.level),True,self.text_color,self.ai_settings.bg_color)
		self.level_rect = self.level_image.get_rect()
		self.level_rect.top = self.score_rect.bottom + 10
		self.level_rect.right = self.score_rect.right
		
	def prep_ships(self):
		"""Left ships"""
		self.ships = Group()
		for ship_number in range(self.stats.ships_left):
			ship = Ship(self.ai_settings,self.screen)
			ship.rect.x = 10 + ship_number * ship.rect.width
			ship.rect.y = 10
			self.ships.add(ship)
			
		
		
