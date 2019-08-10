import sys

import pygame

import game_functions as gf
from pygame.sprite import Group
from settings import Settings
from ship import Ship
from alien import Alien
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard

def run_game():
	# Initailize the game and create a screen object
	pygame.init()
	ai_settings = Settings()
	screen = pygame.display.set_mode(
		(ai_settings.screen_width,ai_settings.screen_height))
	pygame.display.set_caption("Alien Invasion")
	
	# Set the background color
	bg_color = (230,230,230)
	
	# From ship to alien, we create a ship, a group of bullets, and a group of aliens	
	# Create a ship
	ship = Ship(ai_settings,screen)
	
	# Create a bullet group
	bullets = Group()
	
	# Create alien
	aliens = Group()
	
	# Create alien group
	gf.create_fleet(ai_settings,screen,ship,aliens)
	
	# Create a game statitics
	stats = GameStats(ai_settings)
	
	# Create a button
	play_button = Button(ai_settings,screen,"Play")
	
	# Create a scoreboard
	scoreboard = Scoreboard(ai_settings,screen,stats)
	
	# Main loop
	while True:
		
		# Monitoring the mouse and keyboard events
		# It works as a function
		gf.check_events(ai_settings,screen,stats,scoreboard,play_button,ship,aliens,bullets)
		
		if stats.game_active:
			# The ship_position change
			ship.update()
				
			# Update the bullets
			bullets.update()
		
			# Delete some bullets
			gf.update_bullets(ai_settings,screen,stats,scoreboard,ship,aliens,bullets)
		
			# Update the aliens
			gf.update_aliens(ai_settings,screen,stats,scoreboard,ship,aliens,bullets)
		
		# Update the screen
		# And it works as a function
		gf.update_screen(ai_settings,screen,stats,scoreboard,ship,aliens,bullets,play_button)
		
run_game()
