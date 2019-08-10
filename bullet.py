import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
	"""Manage the bullets launched by spacecraft"""
	def __init__(self,ai_settings,screen,ship):
		"""Create a bullet object"""
		super().__init__()
		self.screen = screen
		
		# Create a rectangle represent bullet and set the correct position
		self.rect = pygame.Rect(0,0,ai_settings.bullet_width,ai_settings.bullet_height)
		self.rect.centerx = ship.rect.centerx
		self.rect.top = ship.rect.top
		
		# Store the bullet positon witn float
		self.y = float(self.rect.y)
		self.color = ai_settings.bullet_color
		self.speed_factor = ai_settings.bullet_speed_factor

	def update(self):
		"""Make the bullet forward"""
		# Update the self.y
		self.y -= self.speed_factor
		
		# Update the rect position
		self.rect.y = self.y
		
	def draw_bullet(self):
		"""Draw the bullet"""
		pygame.draw.rect(self.screen,self.color,self.rect)
		
