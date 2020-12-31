import pyautogui as pyg
import arcade as arc
import random


def get_window_size():
    width, height = pyg.size()
    if width > 3000:
        width = width / 2

    ratio = 0.8
    return int(width * ratio), int(height * ratio)


def choose_colour():
    background_colours = [arc.color.LIGHT_FUCHSIA_PINK, arc.color.LIGHT_GREEN, arc.color.LIGHT_PASTEL_PURPLE]
    colour = random.choice(background_colours)
    return colour

