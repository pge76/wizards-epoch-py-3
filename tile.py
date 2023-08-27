import pygame as pg
from settings import *


class Tile(pg.sprite.Sprite):
    def __init__(self, game, pos, sprite, groups, layer=GROUND_LAYER):
        self.groups = groups
        self._layer = layer
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = sprite
        self.rect = self.image.get_rect()
        self.pos = pos

    def update(self):
        self.rect.x = self.pos.x * TILESIZE
        self.rect.y = self.pos.y * TILESIZE
