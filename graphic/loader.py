from pathlib import Path
import pygame
from pygame.locals import *


def load_image(file, transparent=True):
    data_folder = Path("media")
    file_to_open = data_folder / file

    image = pygame.image.load(str(file_to_open))

    if transparent == True:
        image = image.convert()
        colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, RLEACCEL)
    else:
        image = image.convert_alpha()
    return image
