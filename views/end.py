import arcade as arc
from engine import Engine
from views import game
import gametools as gt

LEFT = 0
RIGHT = 1


class End(arc.View):
    def __init__(self, time_elapsed):
        super().__init__()
        self.time_elapsed = time_elapsed
        self.eng = Engine()

        self.width, self.height = gt.get_window_size()
        # Create player and put in location
        self.eng.create_player()
        self.eng.reset_player()

        # Load the map and physics engine
        self.eng.load_map_menu()

        # Load the walls and player
        self.wall_list = self.eng.wall_list
        self.play_list = self.eng.play_list
        self.quit_list = self.eng.quit_list
        self.player_list = self.eng.player_list
        arc.set_background_color(arc.color.LIGHT_YELLOW)

    def on_draw(self):
        # Clears the screen ready to draw
        arc.start_render()

        # Draw our sprites
        self.wall_list.draw()
        self.play_list.draw()
        self.quit_list.draw()
        self.player_list.draw()

        display_time = gt.format_time(self.time_elapsed, milli=True)
        # Display Play and Quit text on screen
        arc.draw_text('Restart', self.width * 0.48, self.height // 2.5, arc.csscolor.MIDNIGHT_BLUE, 32, font_name='Ubuntu-Th')
        arc.draw_text('Quit', self.width * 0.12, self.height // 2.5, arc.csscolor.MIDNIGHT_BLUE, 32, font_name='Ubuntu-Th')
        arc.draw_text(f'Time: {display_time}', self.width // 4.5, self.height // 2, arc.csscolor.CRIMSON, 40)

    def on_key_press(self, key, modifiers):
        self.eng.key_pressed(key)

    def on_key_release(self, key, modifiers):
        self.eng.key_released(key)

    def update(self, delta_time):
        # Update the engine (effectively the gamestate)
        self.eng.update_player()
        self.eng.player_sprite.update_animation()

        if self.eng.collide_play():
            game_scr = game.Game()
            self.window.show_view(game_scr)
        elif self.eng.collide_quit():
            exit()
