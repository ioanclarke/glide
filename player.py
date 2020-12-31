import arcade as arc

# Player size/scaling
PLAYER_SIZE = 64
PLAYER_SCALING = 0.6


class Player(arc.Sprite):
    def __init__(self):
        super().__init__()

        # Load player textures
        self.textures = []
        texture = arc.load_texture("images/player/player_idle.png", mirrored=True)
        self.textures.append(texture)
        texture = arc.load_texture("images/player/player_idle.png")
        self.textures.append(texture)

        # Set player texture
        self.scale = PLAYER_SCALING
        self.set_texture(1)

    def update_facing(self, keypress):
        # Change player the face left or right
        if keypress == 'left':
            self.set_texture(0)
        elif keypress == 'right':
            self.set_texture(1)

    def update_anim(self):
        pass
