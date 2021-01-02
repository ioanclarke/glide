import random

import arcade as arc
import pyautogui as pyg


def get_window_size():
    width, height = pyg.size()
    if width > 3000:
        width = width / 2

    ratio = 0.8
    return int(width * ratio), int(height * ratio)


def choose_colour():
    background_colours = [arc.color.LIGHT_FUCHSIA_PINK, arc.color.LIGHT_GREEN, arc.color.DARK_VIOLET,
                          arc.csscolor.DARK_ORANGE, arc.csscolor.TURQUOISE, arc.color.BANANA_YELLOW]
    colour = random.choice(background_colours)
    return colour


def load_texture_pair(filename):
    return (arc.load_texture(filename, mirrored=True),
            arc.load_texture(filename))


def format_time(time, milli=False):
    minutes = int(time) // 60
    seconds = int(time) % 60
    if milli:
        time_str = str(time)
        pos = time_str.find('.')
        milli = int(time_str[pos + 1: pos + 3])
        return f'{minutes:02d}:{seconds:02d}.{milli:02d}'
    else:
        return f'{minutes:02d}:{seconds:02d}'
