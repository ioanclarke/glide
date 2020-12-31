import arcade as arc

import engine
import gametools as gt


class Game(arc.View):
    def __init__(self):
        super().__init__()
        # Declare map variables
        self.level = 1
        self.eng = engine.Engine()
        self.eng.create_player()
        self.setup()

    def setup(self):
        # Create our engine and player
        self.eng.reset_player()

        # Load the map and physics engine
        self.eng.load_map_game(self.level)
        self.eng.create_physics_engine()

        # Create the Sprite lists
        self.wall_list = self.eng.wall_list
        self.finish_list = self.eng.finish_list
        self.player_list = self.eng.player_list

        # Chooses random background colour from set
        colour = gt.choose_colour()
        arc.set_background_color(colour)

    # Updates game window

    def on_draw(self):
        # Clear the screen to the background color
        arc.start_render()

        # Draw our sprites
        self.wall_list.draw()
        self.finish_list.draw()
        self.player_list.draw()

        # Draw scrolling level indicator
        level_text = f'Level: {self.level}'
        arc.draw_text(level_text, 5, 10, arc.csscolor.MIDNIGHT_BLUE, 30, font_name='Ubuntu-Th')

    def on_key_press(self, key, modifiers):
        if key == arc.key.SPACE:
            self.eng.jumping()

        # Sets key_press variables when pressed
        if key == arc.key.RIGHT:
            self.eng.right_pressed = True
            self.eng.player_sprite.update_facing('right')
        elif key == arc.key.LEFT:
            self.eng.left_pressed = True
            self.eng.player_sprite.update_facing('left')

        if key == arc.key.R:
            self.eng.devreset()
        if key == arc.key.G:
            self.eng.G_pressed = not self.eng.G_pressed

        # Outputs player's coordinates to screen when P is pressed
        if key == arc.key.P:
            self.eng.devcoords()

    def on_key_release(self, key, modifiers):
        # Set key press variables when released
        if key == arc.key.LEFT:
            self.eng.left_pressed = False
        elif key == arc.key.RIGHT:
            self.eng.right_pressed = False

    def update(self, delta_time):
        # Update the engine (effectively the gamestate)
        self.eng.update_player()
        if self.eng.collide_next_level():
            self.level += 1
            self.setup()

    def show_next_level(self):
        pass
