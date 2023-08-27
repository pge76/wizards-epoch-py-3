import pygame
from settings import *


class SpriteSheet:
    def __init__(self, filename):
        """Load the sheet."""
        try:
            self.sheet = pygame.image.load(filename).convert()
        except pygame.error as e:
            print(f"Unable to load spritesheet image: {filename}")
            raise SystemExit(e)

    def image_at(self, index, colorkey=None):
        """Load a specific image from a specific spritesheet coordinate."""
        # Loads image from x, y, x+offset, y+offset.
        tiles_in_row = self.sheet.get_width() // TILESIZE
        rectangle = (
            (index % tiles_in_row) * TILESIZE,
            (index // tiles_in_row) * TILESIZE,
            TILESIZE,
            TILESIZE,
        )
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size).convert()
        image.blit(self.sheet, (0, 0), rect)
        if colorkey is not None:
            if colorkey is -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey, pygame.RLEACCEL)
        return image

    def images_at(self, indices, colorkey=None):
        """Load a whole bunch of images and return them as a list."""
        return [self.image_at(index, colorkey) for index in indices]
