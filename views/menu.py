import arcade as arc
#from views import game
import engine

class Menu(arc.View):
	# def __init__(self):
	# 	super().__init__()
		

	def setup_engine(self, eng):
		#Create our engine and player
		self.eng = eng


	def load_menu(self):
		self.eng.create_player()
		self.eng.reset_player()
		
		#Load the map and physics engine
		self.eng.load_map_menu()
		self.eng.physics_engine()

		#Load the walls and player
		self.wall_list = self.eng.wall_list
		self.play_list = self.eng.play_list
		self.quit_list = self.eng.quit_list
		self.player_list = self.eng.player_list
		arc.set_background_color(arc.color.LIGHT_YELLOW)

	def on_draw(self):
		#Clears the screen ready to draw
		arc.start_render()

		#Draw our sprites
		self.wall_list.draw()
		self.play_list.draw()
		self.quit_list.draw()
		self.player_list.draw()

		#Display Play and Quit text on screen
		arc.draw_text('Play', 765, 300, arc.csscolor.MIDNIGHT_BLUE, 32, font_name='Ubuntu-Th')
		arc.draw_text('Quit', 185, 300, arc.csscolor.MIDNIGHT_BLUE, 32, font_name='Ubuntu-Th')

	def on_key_press(self, key, modifiers):
		#Controls jumping
		if key == arc.key.SPACE:
			self.eng.jumping()

		#Set key press variables and update direction player is facing
		if key == arc.key.RIGHT:
			self.eng.right_pressed = True
			self.eng.player_sprite.update_facing('right')
		elif key == arc.key.LEFT:
			self.eng.left_pressed = True
			self.eng.player_sprite.update_facing('left')

		#Prints player's coordinated when P is pressed
		if key == arc.key.P:
			self.eng.devcoords()

		if key == arc.key.L:
			self.eng.physics_engine()
	def on_key_release(self, key, modifiers):
		#Set key press variables on release
		if key == arc.key.RIGHT:
			self.eng.right_pressed = False
		elif key == arc.key.LEFT:
			self.eng.left_pressed = False

	def update(self, delta_time):
		#Update the engine (effectively the gamestate)
		self.eng.update_player()
		self.eng.update_collide_menu()

	# def switch_to_game_view(self, gamescr):
	# 	#gamescr = game.Game()
	# 	self.window.show_view(gamescr)
	# 	gamescr.setup_engine()