class GameStats():
	"""Trace the game statistics"""
	
	def __init__(self,ai_settings):
		"""Initialize the information"""
		self.ai_settings = ai_settings
		self.reset_stats()
		
		# Unfunction at first
		self.game_active = False
		
		self.high_score = 0
		
	def reset_stats(self):
		"""Initialize the innformation"""
		self.ships_left = self.ai_settings.ship_limit
		self.score = 0
		self.level = 1
