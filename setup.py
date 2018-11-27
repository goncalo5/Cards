#!/usr/bin/env python3
from os import path
import random
import pygame as pg

from settings import DISPLAY, PLAYER, YELLOW


class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = PLAYER['layer']
        self.groups = game.all_sprites
        super(Player, self).__init__(self.groups)
        self.game = game
        self.image = pg.Surface((DISPLAY['tilesize'], DISPLAY['tilesize']))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.dx = 0

    def events(self):
        self.dx = 0
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.dx = -5
        if keys[pg.K_RIGHT]:
            self.dx = 5

    def update(self):
        self.events()
        self.rect.x += self.dx
        if self.rect.left > DISPLAY['width']:
            self.rect.right = 0


class Game(object):
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((DISPLAY['width'], DISPLAY['height']))
        pg.display.set_caption(DISPLAY['title'])
        self.clock = pg.time.Clock()

        # variables
        self.cmd_key_down = False

        self.load_data()
        self.new()
        self.run()

        pg.quit()

    def load_data(self):
        self.dir = path.dirname(__file__)
        pg.mixer.init()  # for sound

    def new(self):
        # start a new game
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.player = Player(self, 100, 100)

    def run(self):
        # game loop - set  self.playing = False to end the game
        self.running = True
        while self.running:
            self.clock.tick(DISPLAY['fps'])
            self.events()
            self.update()
            self.draw()

    def events(self):
        for event in pg.event.get():
            self.handle_common_events(event)

    def handle_common_events(self, event):
        # check for closing window
        if event.type == pg.QUIT:
            # force quit
            quit()

        if event.type == pg.KEYDOWN:
            if event.key == 310:
                self.cmd_key_down = True
            if self.cmd_key_down and event.key == pg.K_q:
                # force quit
                quit()

        if event.type == pg.KEYUP:
            if event.key == 310:
                self.cmd_key_down = False

    def update(self):
        # update portion of the game loop
        self.all_sprites.update()

    def draw(self):
        self.screen.fill(DISPLAY['bgcolor'])
        self.all_sprites.draw(self.screen)

        pg.display.flip()

    def quit(self):
        self.running = False


Game()
