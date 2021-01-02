import arcade as arc
from gametools import load_texture_pair

# Player size/scaling
PLAYER_SIZE = 64
PLAYER_SCALING = 0.6

LEFT = 0
RIGHT = 1


class Player(arc.Sprite):
    def __init__(self):
        super().__init__()
        self.direction = RIGHT

        # Load player textures
        self.idle_textures = load_texture_pair("images/player/player_idle.png")
        self.moving_textures = []
        for i in range(12):
            texture = load_texture_pair(f"images/player/player_{i}.png")
            self.moving_textures.append(texture)

        # Set player texture
        self.scale = PLAYER_SCALING
        self.texture = self.idle_textures[RIGHT]

    def update_facing(self, keypress):
        # Change player the face left or right
        self.direction = keypress

    def update_animation(self, delta_time: float = 1/60):
        if self.change_x == 0 and self.change_y == 0:
            self.texture = self.idle_textures[self.direction]

        self.texture = self.idle_textures[self.direction]
        print(f'direction {self.direction}')