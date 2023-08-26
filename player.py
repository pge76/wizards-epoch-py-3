from typing import Any
import pygame as pg
from settings import *


class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill("yellow")

        self.pos = pg.math.Vector2(x, y) * TILESIZE

        self.dirvec = pg.math.Vector2(0, 0)
        self.walk_buffer = 50

        self.last_pos = self.pos
        self.next_pos = self.pos

        self.current_frame = 0
        self.last_update = pg.time.get_ticks()
        self.between_tiles = False

        self.rect = self.image.get_rect(topleft=(self.pos.x, self.pos.y))

    def get_keys(self):
        now = pg.time.get_ticks()
        keys = pg.key.get_pressed()

        if now - self.last_update > self.walk_buffer:
            self.last_update = now

            new_dir_vec = pg.math.Vector2(0, 0)
            if self.dirvec.y == 0:
                if keys[pg.K_LEFT] or keys[pg.K_a]:
                    new_dir_vec = pg.math.Vector2(-1, 0)
                elif keys[pg.K_RIGHT] or keys[pg.K_d]:
                    new_dir_vec = pg.math.Vector2(1, 0)
            if self.dirvec.x == 0:
                if keys[pg.K_UP] or keys[pg.K_w]:
                    new_dir_vec = pg.math.Vector2(0, -1)
                elif keys[pg.K_DOWN] or keys[pg.K_s]:
                    new_dir_vec = pg.math.Vector2(0, 1)

            if new_dir_vec != pg.math.Vector2(0, 0):
                self.dirvec = new_dir_vec
                self.between_tiles = True
                current_index = (
                    self.rect.centerx // TILESIZE,
                    self.rect.centery // TILESIZE,
                )
                self.last_pos = pg.math.Vector2(current_index) * TILESIZE
                self.next_pos = self.last_pos + self.dirvec * TILESIZE

    def update(self):
        self.get_keys()
        self.rect = self.image.get_rect(topleft=(self.pos.x, self.pos.y))

        if self.pos != self.next_pos:
            delta = self.next_pos - self.pos
            if delta.length() > (self.dirvec * PLAYER_SPEED * self.game.dt).length():
                self.pos += self.dirvec * PLAYER_SPEED * self.game.dt
            else:
                self.pos = self.next_pos
                self.dirvec = pg.math.Vector2(0, 0)
                self.between_tiles = False

        self.rect.topleft = self.pos
        if pg.sprite.spritecollide(self, self.game.walls, False):
            self.pos = self.last_pos
            self.next_pos = self.last_pos
            self.dirvec = pg.math.Vector2(0, 0)
            self.between_tiles = False
        self.rect.topleft = self.pos
