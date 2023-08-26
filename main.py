import pygame as pg
import sys
from player import *
from wall import *
from settings import *
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

        # read file map.txt and add it to map_data
        self.map_data = []
        with open(path.join(game_folder, "map.txt"), "rt") as f:
            for line in f:
                self.map_data.append(line)

    def new(self):
        # initialize all variables and do all the setup for a new game
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        # draw walls
        for row, tiles in enumerate(self.map_data):
            for col, tile in enumerate(tiles):
                if tile == "1":
                    Wall(self, col, row)
                if (
                    tile == "P" and not self.player
                ):  # initialize player on the first 'p' in map.txt
                    self.player = Player(self, col, row)

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

    def draw(self):
        self.screen.fill(BGCOLOR)
        # draw grid
        self.draw_grid()

        self.all_sprites.draw(self.screen)
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
