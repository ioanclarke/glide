import arcade as arc
from gametools import load_texture_pair

# Player size/scaling
PLAYER_SIZE = 64
PLAYER_SCALING = 0.6

LEFT = 0
RIGHT = 1

UPDATES_PER_FRAME = 5
NUM_OF_ANIMATIONS = 6


class Player(arc.Sprite):
    def __init__(self):
        super().__init__()
        self.direction = RIGHT
        self.cur_texture = 0
        self.reverse_anim = False

        # Load player textures
        self.idle_textures = load_texture_pair("images/player/player_idle.png")
        self.moving_textures = []
        for i in range(NUM_OF_ANIMATIONS):
            texture = load_texture_pair(f"images/player/player_{i}.png")
            self.moving_textures.append(texture)

        # Set player texture
        self.scale = PLAYER_SCALING
        self.texture = self.idle_textures[RIGHT]

    def update_animation(self, delta_time: float = 1/60):
        if self.change_x == 0 and self.change_y == 0:
            self.texture = self.idle_textures[self.direction]
        else:
            if self.reverse_anim:
                self.cur_texture -= 1
            else:
                self.cur_texture += 1

            if self.cur_texture == NUM_OF_ANIMATIONS * UPDATES_PER_FRAME:
                self.reverse_anim = True
                self.cur_texture -= 1
            elif self.cur_texture == -1:
                self.reverse_anim = False
                self.cur_texture += 1

            frame = self.cur_texture // UPDATES_PER_FRAME
            direction = self.direction
            self.texture = self.moving_textures[frame][direction]
