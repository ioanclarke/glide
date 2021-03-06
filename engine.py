import arcade as arc
from arcade.physics_engines import _move_sprite

import player
import gametools as gt

# Player movement
JUMP_SPEED = 16
MAX_SPEED = 9
GOD_MODE_SPEED = 18
ACCELERATION_RATE = 0.33
FRICTION = 0.15

# Player directions
LEFT = 0
RIGHT = 1

# Margin of pixels for every side of the player
LEFT_VIEWPORT_MARGIN = 700
RIGHT_VIEWPORT_MARGIN = 900
BOTTOM_VIEWPORT_MARGIN = 50
TOP_VIEWPORT_MARGIN = 300

GRAVITY = 0.9

# Tile size/scaling
TILE_SIZE = 64
TILE_SCALING = 1


class Engine:
    def __init__(self):
        self.G_pressed = False
        self.R_pressed = False
        self.right_pressed = False
        self.left_pressed = False
        self.can_jump = True
        self.view_left = 0
        self.view_bottom = 0
        self.wall_list = None
        self.play_list = None
        self.quit_list = None
        self.finish_list = None
        self.player_list = None
        self.player_sprite = None

    def load_map_menu(self):
        # map_name = (os.path.abspath('///home/ioan/binn/glide/maps/mapmenu.tmx'))
        map_name = 'maps/map0.tmx'
        print(f'Loading map: {map_name}\n')
        my_map = arc.tilemap.read_tmx(map_name)
        self.wall_list = arc.tilemap.process_layer(map_object=my_map, layer_name='platforms', scaling=TILE_SCALING)
        self.play_list = arc.tilemap.process_layer(map_object=my_map, layer_name='play', scaling=TILE_SCALING)
        self.quit_list = arc.tilemap.process_layer(map_object=my_map, layer_name='quit', scaling=TILE_SCALING)

    def load_map_game(self, level):
        # Load the map and set up variables
        map_name = f'maps/map{level}.tmx'
        print(f'Loading map: {map_name}\n')
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

    def collide_play(self):
        # Start game when user goes to Play
        if arc.check_for_collision_with_list(self.player_sprite, self.play_list):
            print('Starting game...\n')
            return True
        else:
            return False

    def collide_quit(self):
        # Exit game when user goes to Quit
        if arc.check_for_collision_with_list(self.player_sprite, self.quit_list):
            return True
        else:
            return False

    def collide_next_level(self):
        if arc.check_for_collision_with_list(self.player_sprite, self.finish_list):
            return True
        else:
            return False

    def create_player(self):
        # Create the player
        self.player_list = arc.SpriteList()
        self.player_sprite = player.Player()
        self.player_list.append(self.player_sprite)

    def update_player(self):
        # Add gravity
        self.player_sprite.change_y -= GRAVITY
        # Add friction
        self.friction()

        # Controls movement based on key pressed
        if self.right_pressed:
            self.gliding('right', self.wall_list)
        if self.left_pressed:
            self.gliding('left', self.wall_list)
        self.scrolling()

        # This code is taken from the Arcade module
        _move_sprite(self.player_sprite, self.wall_list, ramp_up=True)

        for platform in self.wall_list:
            if platform.change_x != 0 or platform.change_y != 0:
                platform.center_x += platform.change_x

                if platform.boundary_left is not None \
                        and platform.left <= platform.boundary_left:
                    platform.left = platform.boundary_left
                    if platform.change_x < 0:
                        platform.change_x *= -1

                if platform.boundary_right is not None \
                        and platform.right >= platform.boundary_right:
                    platform.right = platform.boundary_right
                    if platform.change_x > 0:
                        platform.change_x *= -1

                if arc.check_for_collision(self.player_sprite, platform):
                    if platform.change_x < 0:
                        self.player_sprite.right = platform.left
                    if platform.change_x > 0:
                        self.player_sprite.left = platform.right

                platform.center_y += platform.change_y

                if platform.boundary_top is not None \
                        and platform.top >= platform.boundary_top:
                    platform.top = platform.boundary_top
                    if platform.change_y > 0:
                        platform.change_y *= -1

                if platform.boundary_bottom is not None \
                        and platform.bottom <= platform.boundary_bottom:
                    platform.bottom = platform.boundary_bottom
                    if platform.change_y < 0:
                        platform.change_y *= -1
        # End of Arcade code

        self.fallreset()

    def update_player_facing(self, keypress):
        self.player_sprite.direction = keypress

    def reset_player(self):
        window_width, window_height = gt.get_window_size()
        self.player_sprite.center_x = window_width / 3
        self.player_sprite.center_y = window_height / 2
        self.player_sprite.change_x = 0
        self.player_sprite.change_y = 0

    def key_pressed(self, key):
        if key == arc.key.SPACE:
            self.jumping()

        # Sets key_press variables when pressed
        if key == arc.key.RIGHT:
            self.right_pressed = True
            self.update_player_facing(RIGHT)
        elif key == arc.key.LEFT:
            self.left_pressed = True
            self.update_player_facing(LEFT)

        if key == arc.key.R:
            self.devreset()
        if key == arc.key.G:
            self.G_pressed = not self.G_pressed

        # Outputs player's coordinates to screen when P is pressed
        if key == arc.key.P:
            self.devcoords()

    def key_released(self, key):
        # Set key press variables when released
        if key == arc.key.LEFT:
            self.left_pressed = False
        elif key == arc.key.RIGHT:
            self.right_pressed = False

    def gliding(self, direction, wall_list):
        # Controls player's horiztonal acceleration
        if direction == 'right':
            vel_dir = 1
        else:
            vel_dir = -1

        self.player_sprite.center_x += vel_dir
        if not arc.check_for_collision_with_list(self.player_sprite, wall_list):
            self.player_sprite.change_x += ACCELERATION_RATE * vel_dir
        self.player_sprite.center_x -= vel_dir

    def max_speed(self):
        # Controls maximum speed of player (including God mode)
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
        # Controls jumping (including God mode and double jumping)
        if not self.G_pressed:
            # Check to see if sprite is on floor
            self.player_sprite.center_y -= 5
            hit_list = arc.check_for_collision_with_list(self.player_sprite, self.wall_list)
            self.player_sprite.center_y += 5

            # Jump if sprite is on floor
            if len(hit_list) > 0:
                self.player_sprite.change_y = JUMP_SPEED
                self.can_jump = True
            # Controls double jumping
            if len(hit_list) == 0:
                if self.can_jump:
                    self.player_sprite.change_y = JUMP_SPEED
                    self.can_jump = False
        else:
            pass

    def friction(self):
        # Control how friction act's on player
        if self.player_sprite.change_x > FRICTION:
            self.player_sprite.change_x -= FRICTION
        elif self.player_sprite.change_x < -FRICTION:
            self.player_sprite.change_x += FRICTION
        else:
            self.player_sprite.change_x = 0

    def scrolling(self):
        changed = False
        window_width, window_height = gt.get_window_size()
        # Scroll left
        left_boundary = self.view_left + LEFT_VIEWPORT_MARGIN
        if self.player_sprite.left < left_boundary:
            self.view_left -= left_boundary - self.player_sprite.left
            changed = True

        # Scroll right
        right_boundary = self.view_left + window_width - RIGHT_VIEWPORT_MARGIN
        if self.player_sprite.right > right_boundary:
            self.view_left += self.player_sprite.right - right_boundary
            changed = True

        # Scroll up
        top_boundary = self.view_bottom + window_height - TOP_VIEWPORT_MARGIN
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
            arc.set_viewport(self.view_left, window_width * 0.8 + self.view_left, self.view_bottom,
                             window_height * 0.8 + self.view_bottom)

    def fallreset(self):
        # Reset the player if they fall off the map
        reset_distance = -500
        if self.player_sprite.center_y < reset_distance:
            print('off map')
            self.view_left = 0
            self.view_bottom = 0
            self.reset_player()
            # self.changed = True

    def godglide(self):
        # Controls God mode movement
        if self.G_pressed:
            if self.right_pressed:
                self.player_sprite.center_x += 1
                if not arc.check_for_collision_with_list(self.player_sprite, self.wall_list):
                    self.player_sprite.change_x += ACCELERATION_RATE * 10
                self.player_sprite.center_x -= 1
            if self.left_pressed and not self.right_pressed:
                self.player_sprite.center_x -= 1
                if not arc.check_for_collision_with_list(self.player_sprite, self.wall_list):
                    self.player_sprite.change_x -= ACCELERATION_RATE * 10
                self.player_sprite.center_x += 1

    def devreset(self):
        # Restart the view and player position by pressing R
        if self.R_pressed:
            self.view_left = 0
            self.view_bottom = 0
            self.R_pressed = False
            self.reset_player()

    def devcoords(self):
        # Prints player's position to the console
        print(f'x pos: {round(self.player_sprite.center_x, 2)}')
        print(f'y pos: {round(self.player_sprite.center_y, 2)}\n')