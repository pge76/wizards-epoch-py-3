import pygame as pg
import sys

from player import *
from tile import *
from settings import *
from map import *
from camera import *
from spritesheet import *
from image_map import *
from pygame.math import Vector2

from os import path


class Game:
    def __init__(self):
        pg.init()
        self.player = None
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)

        pg.key.set_repeat(300, 100)

        self.clock = pg.time.Clock()
        self.load_data()

    def load_data(self):
        game_folder = path.dirname(__file__)

        self.sprite_folder = game_folder + SPRITES_FOLDER
        self.map_folder = game_folder + MAP_FOLDER

        # read file map.txt and add it to map_data
        self.map = Map(path.join(self.map_folder, "forest_a2.map"))

        self.image_map = ImageMap(self).init_imagemap()

    def new(self):
        # initialize all variables and do all the setup for a new game
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.walls = pg.sprite.Group()

        # draw initial map
        for row, tiles in enumerate(self.map.data):
            for col, tile in enumerate(tiles):
                if tile == "g":
                    Tile(
                        self,
                        Vector2(col, row),
                        self.image_map.get_image("grass"),
                        (self.all_sprites),
                    )
                if tile == "f":
                    Tile(
                        self,
                        Vector2(col, row),
                        self.image_map.get_image("forest"),
                        (self.all_sprites, self.walls),
                    )
                if tile == "s":
                    Tile(
                        self,
                        Vector2(col, row),
                        self.image_map.get_image("stone"),
                        (self.all_sprites, self.walls),
                    )
                if tile == "e":
                    Tile(
                        self,
                        Vector2(col, row),
                        self.image_map.get_image("empty"),
                        (self.all_sprites, self.walls),
                    )
                if tile == ".":
                    Tile(
                        self,
                        Vector2(col, row),
                        self.image_map.get_image("path"),
                        (self.all_sprites),
                    )
                if (
                    tile == "P" and not self.player
                ):  # initialize player on the first 'P' in map
                    Tile(
                        self,
                        Vector2(col, row),
                        self.image_map.get_image("path"),
                        (self.all_sprites),
                    )
                    self.player = Player(self, col, row)

        self.camera = Camera(self.map.width, self.map.height)

    def run(self):
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()

    def quit(self):
        self.playing = False
        pg.quit()
        sys.exit()

    def update(self):
        self.all_sprites.update()
        self.camera.update(self.player)

    def draw(self):
        self.screen.fill(BGCOLOR)
        # draw grid
        # self.draw_grid()

        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))

        pg.display.flip()

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()

    def draw_grid(self):
        # draw vertical lines
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, "darkgrey", (x, 0), (x, HEIGHT))

        # draw horizontal lines
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, "darkgrey", (0, y), (WIDTH, y))

    def show_start_screen(self):
        pass

    def show_go_screen(self):
        pass


g = Game()
g.show_start_screen()
while True:
    g.new()
    g.run()
    g.show_go_screen()
