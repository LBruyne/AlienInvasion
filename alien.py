import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
	"""A class of alien"""
	def __init__(self,ai_settings,screen):
		"""Initialize aliens and its position"""
		super().__init__()
		self.screen = screen
		self.ai_settings = ai_settings
		
		# Update the image and its rect
		self.image = pygame.image.load('images/alien.bmp')
		self.rect = self.image.get_rect()
		
		# Initial the position
		self.rect.x = self.rect.width
		self.rect.y = self.rect.height
		
		# The accurate position
		self.x = float(self.rect.x)
		self.y = float(self.rect.y)
		
	def blitme(self):
		"""Draw the alien"""
		self.screen.blit(self.image,self.rect)
		
	def update(self):
		"""Alien move"""
		self.x += (self.ai_settings.alien_speed_factor * self.ai_settings.fleet_direction)
		self.rect.x = self.x

	def check_edges(self):
		"""If alien is on the edge, return True"""
		screen_rect = self.screen.get_rect()
		if self.rect.right >= screen_rect.right:
			return True
		elif self.rect.left <= 0:
			return True
			
