import pygame as pg
from settings import *
from spritesheet import SpriteSheet
from os import path
from enum import Enum
from pygame.math import Vector2


class ImageMap:
    def __init__(self, game):
        self.game = game
        self.image_map = {}

    def init_imagemap(self):
        self.sprite_sheet = SpriteSheet(
            path.join(self.game.sprite_folder, "main_sprite_sheet.png")
        )
        return self

    def get_image(self, type, colorkey=None):
        if type in self.image_map:
            return self.image_map[type]
        else:
            match type:
                case "forest":
                    self.set_image(type, 147, colorkey)
                case "grass":
                    self.set_image(type, 587, colorkey)
                case "path":
                    self.set_image(type, 211, colorkey)
                case "stone":
                    self.set_image(type, 1216, colorkey)
                case "empty":
                    self.set_image(type, 0, colorkey)
                case "player":
                    self.set_image(type, 3795, colorkey)
                case _:
                    self.set_image(type, 3241, colorkey)
            return self.image_map[type]

    def set_image(self, type, index, colorkey=None):
        self.image_map[type] = self.sprite_sheet.image_at(index, colorkey)
