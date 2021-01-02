import arcade as arc

import engine
import gametools as gt
from views import end
LEFT = 0
RIGHT = 1
NUM_OF_LEVELS = 3


class Game(arc.View):
    def __init__(self):
        super().__init__()
        # Declare map variables
        self.level = 1
        self.eng = engine.Engine()
        self.eng.create_player()
        self.wall_list = None
        self.finish_list = None
        self.player_list = None
        self.total_time = 0.0
        self.setup()

    def setup(self):
        # Create our engine and player
        self.eng.reset_player()

        # Load the map and physics engine
        self.eng.load_map_game(self.level)

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
        arc.draw_text(level_text, 5 + self.eng.view_left, 10 + self.eng.view_bottom, arc.csscolor.MIDNIGHT_BLUE, 30,
                      font_name='Ubuntu Light')

        time_elapsed = gt.format_time(self.total_time)
        arc.draw_text(time_elapsed, 200 + self.eng.view_left, 10 + self.eng.view_bottom, arc.csscolor.MIDNIGHT_BLUE, 30,
                      font_name='Ubuntu Light')

    def on_key_press(self, key, modifiers):
        self.eng.key_pressed(key)

    def on_key_release(self, key, modifiers):
        self.eng.key_released(key)

    def update(self, delta_time):
        # Update the engine (effectively the gamestate)
        self.eng.update_player()
        self.eng.player_sprite.update_animation()
        self.total_time += delta_time
        if self.eng.collide_next_level():
            if self.level == NUM_OF_LEVELS:
                end_scr = end.End(self.total_time)
                self.window.show_view(end_scr)
            else:
                self.level += 1
                self.setup()
        # self.eng.update

    def show_next_level(self):
        pass
