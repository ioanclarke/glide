import arcade as arc


class Window(arc.Window):
	def __init__(self, window_width, window_height, GAME_TITLE):
		super().__init__(window_width, window_height, GAME_TITLE, resizable=True)

	def on_resize(self, width, height):
		super().on_resize(width, height)
