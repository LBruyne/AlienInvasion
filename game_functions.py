import sys

import pygame

from bullet import Bullet

from alien import Alien

from time import sleep

def check_keydown_events(event,ai_settings,screen,ship,bullets):
	"""Respond to the keyboard_down event"""
	if event.key == pygame.K_RIGHT:
		ship.moving_right = True
	elif event.key == pygame.K_LEFT:
		ship.moving_left = True
	elif event.key == pygame.K_SPACE:
		fire_bullet(ai_settings,screen,ship,bullets)
	elif event.key == pygame.K_q:
		sys.exit()
		
def check_keyup_events(event,ship):
	"""Respond to the keyboard_up event"""
	if event.key == pygame.K_RIGHT:
		ship.moving_right = False
	elif event.key == pygame.K_LEFT:
		ship.moving_left = False

def check_events(ai_settings,screen,stats,scoreboard,play_button,ship,aliens,bullets):
	"""Respond to mouse and keyboard events"""
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
		elif event.type == pygame.KEYDOWN:
			check_keydown_events(event,ai_settings,screen,ship,bullets)
		elif event.type == pygame.KEYUP:
			check_keyup_events(event,ship)
		elif event.type == pygame.MOUSEBUTTONDOWN:
			mouse_x,mouse_y = pygame.mouse.get_pos()
			check_play_button(ai_settings,screen,stats,scoreboard,play_button,ship,aliens,bullets,mouse_x,mouse_y)

def update_screen(ai_settings,screen,stats,scoreboard,ship,aliens,bullets,play_button):
	"""Update the screen and switch to a new screen"""
	# Redraw the screen when starting every cycle
	screen.fill(ai_settings.bg_color)
	
	# Redraw all the bullets
	for bullet in bullets.sprites():
		bullet.draw_bullet()
	
	# Redraw the ship
	ship.blitme()
	
	# Redraw the alien
	aliens.draw(screen)
	
	# Display scoreboard
	scoreboard.show_score()
	
	# Display a button
	if not stats.game_active:
		play_button.draw_button()
	
	# Let rhe recent screen visible
	pygame.display.flip()
	
def update_bullets(ai_settings,screen,stats,scoreboard,ship,aliens,bullets):
	"""Update the position of bullets and delete bullets that has missed"""
	# Update the position of bullets
	bullets.update()
	
	# Delete bullets
	for bullet in bullets.copy():
		if bullet.rect.bottom <= 0:
			bullets.remove(bullet)
			
	# Check if collision
	check_bullet_alien_collisions(ai_settings,screen,stats,scoreboard,ship,aliens,bullets)
		
def check_bullet_alien_collisions(ai_settings,screen,stats,scoreboard,ship,aliens,bullets):
	"""Respond to collison"""
	# Delete things that collide others
	collisions = pygame.sprite.groupcollide(bullets,aliens,True,True) 
	
	if collisions :
		for aliens in collisions.values():
			stats.score += ai_settings.alien_points * len(aliens)
			scoreboard.prep_score()
		check_high_score(stats,scoreboard)
	
	if len(aliens) == 0:
		bullets.empty()
		ai_settings.increase_speed()
		stats.level += 1
		scoreboard.prep_level()
		create_fleet(ai_settings,screen,ship,aliens)

def fire_bullet(ai_settings,screen,ship,bullets):
	"""Fire a bullet when number is not limited"""
	# Create new bullet and add it into the group:bullets when it is not limited
	if len(bullets) < ai_settings.bullets_allowed:
			new_bullet = Bullet(ai_settings,screen,ship)
			bullets.add(new_bullet)

def create_fleet(ai_settings,screen,ship,aliens):
	"""Create alien group"""
	# Create a alien, and calculate the number
	alien = Alien(ai_settings,screen)
	number_aliens_x = get_number_aliens_x(ai_settings,alien.rect.width)
	number_rows = get_number_rows(ai_settings,ship.rect.height,alien.rect.height)
	
	# Create a row of alien
	for row_number in range(number_rows):
		for alien_number in range(number_aliens_x):
			create_alien(ai_settings,screen,aliens,alien_number,row_number)

def get_number_aliens_x(ai_settings,alien_width):
	"""Calculate the number of alien that are in one row"""
	available_space_x = ai_settings.screen_width - 2 * alien_width
	number_aliens_x = int(available_space_x / (2 * alien_width))
	return number_aliens_x
	
def create_alien(ai_settings,screen,aliens,alien_number,row_number):
	"""Create a alien and put it in the current row"""
	alien = Alien(ai_settings,screen)
	alien_width = alien.rect.width
	alien.x = alien_width + 2 * alien_width * alien_number
	alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
	alien.rect.x = alien.x
	aliens.add(alien)
	
def get_number_rows(ai_settings,ship_height,alien_height):
	"""Calculate rows"""
	available_space_y = (ai_settings.screen_height - 3 * alien_height - ship_height)
	number_rows = int(available_space_y / (2 * alien_height))
	return number_rows
	
def update_aliens(ai_settings,screen,stats,scoreboard,ship,aliens,bullets):
	"""Update all aliens position"""
	check_fleet_edges(ai_settings,aliens)
	aliens.update()
	
	# Check ship collision
	if pygame.sprite.spritecollideany(ship,aliens):
		ship_hit(ai_settings,screen,stats,scoreboard,ship,aliens,bullets)
	# Check bottom
	check_aliens_bottom(ai_settings,screen,stats,scoreboard,ship,aliens,bullets)
	
def check_fleet_edges(ai_settings,aliens):
	"""Check if the alien is on the edge"""
	for alien in aliens.sprites():
		if alien.check_edges():
			change_fleet_direction(ai_settings,aliens)
			break
			
def change_fleet_direction(ai_settings,aliens):
	"""Move down, and change the direction"""
	for alien in aliens.sprites():
		alien.rect.y += ai_settings.fleet_drop_speed
	ai_settings.fleet_direction *= -1
	

def ship_hit(ai_settings,screen,stats,scoreboard,ship,aliens,bullets):
	"""Respond to ship hitted"""
	if stats.ships_left > 0:
		# Lose a chance
		stats.ships_left -=1
	
		# Clear all the things 
		aliens.empty()
		bullets.empty()
		
		# Update the ships
		scoreboard.prep_ships()
	
		# Create a new group of aliens and put the ship again
		create_fleet(ai_settings,screen,ship,aliens)
		ship.center_ship()
	
		# Stop
		sleep(1)
	 
	else:
		stats.game_active = False
		pygame.mouse.set_visible(True)

def check_aliens_bottom(ai_settings,screen,stats,scoreboard,ship,aliens,bullets):
	"""Check if alien get the bottom"""
	screen_rect = screen.get_rect()
	for alien in aliens.sprites():
		if alien.rect.bottom >= screen_rect.bottom:
			ship_hit(ai_settings,screen,stats,scoreboard,ship,aliens,bullets)
			break

def check_play_button(ai_settings,screen,stats,scoreboard,play_button,ship,aliens,bullets,mouse_x,mouse_y):
	"""Start the game when Play"""
	button_clicked = play_button.rect.collidepoint(mouse_x,mouse_y)
	if button_clicked and not stats.game_active:
		# Reset the game
		ai_settings.initialize_dynamic_settings()
		
		# Hide cursor
		pygame.mouse.set_visible(False)
		
		# Reset the game
		stats.reset_stats()
		bullets.empty()
		aliens.empty()
		
		# Make the game active
		stats.game_active = True
		
		# Reset the scoreboard
		scoreboard.prep_score()
		scoreboard.prep_high_score()
		scoreboard.prep_level()
		scoreboard.prep_ships()
		
		# Create new aliens and ship
		create_fleet(ai_settings,screen,ship,aliens)
		ship.center_ship()

def check_high_score(stats,scoreboard):
	"""Check if a new high score"""
	if stats.score > stats.high_score:
		stats.high_score = stats.score
		scoreboard.prep_high_score()
