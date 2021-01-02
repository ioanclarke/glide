from gametools import get_window_size
import arcade as arc
from views import menu


GAME_TITLE = 'glide'


def main():
	# Create engine and window
	window_width, window_height = get_window_size()
	title = GAME_TITLE
	game_window = arc.Window(window_width, window_height, title)
	menu_scr = menu.Menu()
	game_window.show_view(menu_scr)

	# Run the game
	arc.run()


if __name__ == "__main__":
	main()
