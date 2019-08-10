import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
	"""Control the ships"""
	def __init__(self,ai_settings,screen):
		"""Initialize the ship and set its position"""
		super().__init__()
		self.screen = screen
		self.ai_settings = ai_settings
		
		# Loading the spacecraft image and obtaining its outer rectangle
		self.image = pygame.image.load('images/ship.bmp')
		self.rect = self.image.get_rect()
		self.screen_rect = screen.get_rect()
		
		# Place each new spaceship in the center of the bottom of the screen
		self.rect.centerx = self.screen_rect.centerx
		self.rect.bottom = self.screen_rect.bottom
		
		# Store float in setting/center/
		self.center = float(self.rect.centerx)
		
		# A sign for movement
		self.moving_right = False
		self.moving_left = False
	
	def blitme(self):
		"""Draw the spaceship in the specific position"""
		self.screen.blit(self.image,self.rect)

	def update(self):
		"""Adjust the position according to the sign"""
		if self.moving_right == True and self.rect.right < self.screen_rect.right:
			self.center += self.ai_settings.ship_speed_factor
		if self.moving_left == True and self.rect.left > self.screen_rect.left:
			self.center -= self.ai_settings.ship_speed_factor
			
		# Update the rect
		self.rect.centerx = self.center
		
	def center_ship(self):
		"""Put the ship in the middle"""
		self.center = self.screen_rect.centerx
