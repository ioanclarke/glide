import arcade as arc
import player
import os
import sys
import window
import pyautogui as pyg
import random
from views import game, menu

#Game window features
GAME_TITLE = "Glide"

#Player movement
JUMP_SPEED = 16
MAX_SPEED = 9
GOD_MODE_SPEED = 18
ACCELERATION_RATE = 0.33
FRICTION = 0.15


#Margin of pixels for every side of the player
LEFT_VIEWPORT_MARGIN = 700
RIGHT_VIEWPORT_MARGIN = 900
BOTTOM_VIEWPORT_MARGIN = 50
TOP_VIEWPORT_MARGIN = 300

GRAVITY = 0.9

#Tile size/scaling
TILE_SIZE = 64
TILE_SCALING = 1

class Engine:
	def __init__(self):
		self.G_pressed = False
		self.right_pressed = False
		self.left_pressed = False
		self.can_jump = True
		self.view_left = 0
		self.view_bottom = 0
		self.level = 1


	def create_window(self):
		#Get user's screen size
		screen_width, screen_height = self.get_screen_size()
		window_width = int(screen_width * 0.8)
		window_height = int(screen_height * 0.8)

		#Create main window
		self.game_window = window.Window(window_width, window_height, GAME_TITLE)

	def setup_menu(self, eng):
		#Create menu screen and set it to be displayed
		menuscr = menu.Menu()
		menuscr.setup_engine(eng)
		self.game_window.show_view(menuscr)
		
		#Setup menu screen
		menuscr.load_menu()

	def setup_game(self):
		gamescr = game.Game()
		gamescr.setup_engine(gamescr)
		self.game_window.show_view(gamescr)
		gamescr.setup()

	def assign_gamescr(self, gamescr):
		self.gamescr = gamescr


	def physics_engine(self):
		#Create physics engine
		print(repr(self.player_sprite))
		print(repr(self.wall_list))
		print(GRAVITY)
		print('calling physics engine...')
		self.physics_engine = arc.PhysicsEnginePlatformer(self.player_sprite, self.wall_list, GRAVITY)
		#pass

	def get_screen_size(self):
		screen_width, screen_height = pyg.size()
		if screen_width > 3000:
			screen_width = int(screen_width/2)
		screen_height = int(screen_height)
		return screen_width, screen_height

	def load_map_menu(self):
		#map_name = (os.path.abspath('///home/ioan/binn/glide/maps/mapmenu.tmx'))
		map_name = ('maps/map0.tmx')
		print(f'\n\n\nLoading map: {map_name}')
		my_map = arc.tilemap.read_tmx(map_name)
		self.wall_list = arc.tilemap.process_layer(map_object=my_map, layer_name='platforms', scaling=TILE_SCALING)
		self.play_list = arc.tilemap.process_layer(map_object=my_map, layer_name='play', scaling=TILE_SCALING)
		self.quit_list = arc.tilemap.process_layer(map_object=my_map, layer_name='quit', scaling=TILE_SCALING)
		# self.wall_list.append(self.play_list)
		# self.wall_list.append(self.quit_list)


	def load_map_game(self, level):
		#Load the map and set up variables
		map_name = f'maps/map{level}.tmx'
		print(f'Loading map: {map_name}')
		my_map = arc.tilemap.read_tmx(map_name)
		self.wall_list = arc.tilemap.process_layer(map_object=my_map, layer_name='platforms', scaling=TILE_SCALING)
		self.finish_list = arc.tilemap.process_layer(map_object=my_map, layer_name='finish', scaling=TILE_SCALING)

		# #Creates the moving platform on level 1
		# if self.level == 1:      
		# 	moving_box = arc.Sprite('images/box/box.png', TILE_SCALING)
		# 	moving_box.center_x = 7.5*TILE_SIZE
		# 	moving_box.center_y = 1.5*TILE_SIZE
		# 	moving_box.boundary_left = 42*TILE_SIZE
		# 	moving_box.boundary_right = 54*TILE_SIZE
		# 	moving_box.change_x = -2
		# 	self.wall_list.append(moving_box)


	def create_player(self):
		#Create the player
		self.player_list = arc.SpriteList()
		self.player_sprite = player.Player()
		self.player_list.append(self.player_sprite)


	def reset_player(self):
		screen_width, screen_height = self.get_screen_size()
		window_width = int(screen_width * 0.8)
		window_height = int(screen_height * 0.8)
		self.player_sprite.center_x = window_width/3
		self.player_sprite.center_y = window_height/2


	def gliding(self, direction, wall_list):
		#Controls player's horiztonal acceleration
		if direction == 'right':
			self.player_sprite.center_x += 1
			if not arc.check_for_collision_with_list(self.player_sprite, wall_list):
				self.player_sprite.change_x += ACCELERATION_RATE
			self.player_sprite.center_x -= 1

		if direction == 'left':
			self.player_sprite.center_x -= 1
			if not arc.check_for_collision_with_list(self.player_sprite, wall_list):
				self.player_sprite.change_x -= ACCELERATION_RATE
			self.player_sprite.center_x += 1


	def max_speed(self):
		#Controls maximum speed of player (including God mode)
		if not self.G_pressed:
			if self.player_sprite.change_x > MAX_SPEED:
				self.player_sprite.change_x = MAX_SPEED
			elif self.player_sprite.change_x < -MAX_SPEED:
				self.player_sprite.change_x = -MAX_SPEED
		else:
			if self.player_sprite.change_x > GOD_MODE_SPEED:
				self.player_sprite.change_x = GOD_MODE_SPEED
			elif self.player_sprite.change_x < -GOD_MODE_SPEED:
				self.player_sprite.change_x = -GOD_MODE_SPEED


	def jumping(self):
		#Controls jumping (including God mode and double jumping)
			if not self.G_pressed:
				#Check for  jump
				self.player_sprite.center_y -= 5
				hit_list = arc.check_for_collision_with_list(self.player_sprite, self.wall_list)
				self.player_sprite.center_y += 5

				if len(hit_list)>0:
					self.player_sprite.change_y = JUMP_SPEED
					self.can_jump = True
				if len(hit_list)==0:
					if self.can_jump == True:
						self.player_sprite.change_y = JUMP_SPEED
						self.can_jump = False
			else:
				pass


	def friction(self):
		#Control how friction act's on player
		if self.player_sprite.change_x > FRICTION:
			self.player_sprite.change_x -= FRICTION
		elif self.player_sprite.change_x < -FRICTION:
			self.player_sprite.change_x += FRICTION
		else:
			self.player_sprite.change_x = 0


	def scrolling(self):
		changed = False
		screen_width, screen_height = self.get_screen_size()
		#Scroll left
		left_boundary = self.view_left + LEFT_VIEWPORT_MARGIN
		if self.player_sprite.left < left_boundary:
			self.view_left -= left_boundary - self.player_sprite.left
			changed = True

		# Scroll right
		right_boundary = self.view_left + screen_width - RIGHT_VIEWPORT_MARGIN
		if self.player_sprite.right > right_boundary:
			self.view_left += self.player_sprite.right - right_boundary
			changed = True

		# Scroll up
		top_boundary = self.view_bottom + screen_height - TOP_VIEWPORT_MARGIN
		if self.player_sprite.top > top_boundary:
			self.view_bottom += self.player_sprite.top - top_boundary
			changed = True

		# Scroll down
		bottom_boundary = self.view_bottom + BOTTOM_VIEWPORT_MARGIN
		if self.player_sprite.bottom < bottom_boundary:
			self.view_bottom -= bottom_boundary - self.player_sprite.bottom
			changed = True

		# Make sure our boundaries are integer values. While the view port does
		# support floating point numbers, for this application we want every pixel
		# in the view port to map directly onto a pixel on the screen. We don't want
		# any rounding errors.
		self.view_left = int(self.view_left)
		self.view_bottom = int(self.view_bottom)

		# If we changed the boundary values, update the view port to match
		if changed:
			#print(f'left: {self.view_left}\nright: {screen_width + self.view_left}\nbottom: {self.view_bottom}\ntop: {screen_height + self.view_bottom}\n')
			arc.set_viewport(self.view_left, screen_width*0.8 + self.view_left, self.view_bottom, screen_height*0.8 + self.view_bottom)


	def fallreset(self):
		#Reset the player if they fall off the map
		if self.player_sprite.center_y < -1000:
			self.view_left = 0
			self.view_bottom = 0
			self.player_sprite.center_x = PLAYER_START_X
			self.player_sprite.center_y = PLAYER_START_Y
			changed = True


	def godglide(self):
		#Controls God mode movement
		if self.G_pressed:
			if self.right_pressed:
				self.player_sprite.center_x += 1
				if not arc.check_for_collision_with_list(self.player_sprite, self.wall_list):
					self.player_sprite.change_x += ACCELERATION_RATE*10
				self.player_sprite.center_x -= 1
			if self.left_pressed and not self.right_pressed:
				self.player_sprite.center_x -= 1
				if not arc.check_for_collision_with_list(self.player_sprite, self.wall_list):
					self.player_sprite.change_x -= ACCELERATION_RATE*10
				self.player_sprite.center_x += 1


	def devreset(self):
		#Restart the view and player position by pressing R
		if self.R_pressed:
			self.view_left = 0
			self.view_bottom = 0
			self.player_sprite.center_x = PLAYER_START_X
			self.player_sprite.center_y = PLAYER_START_Y
			changed = True
			self.R_pressed = False


	def devcoords(self):
		#Prints player's position to the console
		print(f'x pos: {round(self.player_sprite.center_x, 2)}')
		print(f'y pos: {round(self.player_sprite.center_y, 2)}\n')


	def update_player(self):
		#Updates physics
		self.physics_engine.update()
		self.friction()

		#Controls movement based on key pressed
		if self.right_pressed:
			self.gliding('right', self.wall_list)
		if self.left_pressed:
			self.gliding('left', self.wall_list)
		# self.scrolling()
		if self.level > 0:
			self.scrolling()

	def update_collide_menu(self):
		#Controls player falling due to gravity
		#self.player_sprite.change_y -= GRAVITY
		#Start game when user goes to Play
		if arc.check_for_collision_with_list(self.player_sprite, self.play_list):
			print('Starting game...\n')
			self.level = 1

			self.setup_game()
			# menuscr = menu.Menu()

			# menuscr.switch_to_game_view(gamescr)

			
			#print(repr(game_window))

			#Get user's screen size
			# screen_width, screen_height = self.get_screen_size()
			# window_width = int(screen_width * 0.8)
			# window_height = int(screen_height * 0.8)
			#gamescr.setup()

		#Exit game when user goes to Quit
		if arc.check_for_collision_with_list(self.player_sprite, self.quit_list):
			exit()

	def update_collide_game(self):
		if arc.check_for_collision_with_list(self.player_sprite, self.finish_list):
			self.level += 1
			print(f'Proceeding to level: {self.level}')

			self.gamescr.setup()
			# self.game_window.show_view(gamescr)

			# #Get user's screen size
			# screen_width, screen_height = self.get_screen_size()
			# window_width = int(screen_width * 0.8)
			# window_height = int(screen_height * 0.8)
			# gamescr.setup(window_width, window_height)

	def choose_colour(self):
		background_colours = [arc.color.LIGHT_FUCHSIA_PINK, arc.color.LIGHT_GREEN, arc.color.LIGHT_PASTEL_PURPLE]
		colour = random.choice(background_colours)
		return colour

	# def initialize_game(self):
	# 	self.gamescr = game.Game()
	# 	self.gamescr.setup()
