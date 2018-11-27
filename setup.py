#!/usr/bin/env python3
from os import path
import random
import pygame as pg

from settings import DISPLAY, CARD, BLACK


class Player(pg.sprite.Sprite):
    def __init__(self, game, pos):
        self._layer = CARD['layer']
        self.groups = game.all_sprites
        super(Player, self).__init__(self.groups)
        self.game = game
        self.image = pg.Surface((CARD['width'], CARD['height']))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.dx = 0
        self.time_to_unpress = pg.time.get_ticks()
        self.is_up = 1

    def events(self):
        self.dx = 0
        # print(pg.mouse.get_pressed())
        if pg.time.get_ticks() - self.time_to_unpress < 300:
            return

        if pg.mouse.get_pressed() == (1, 0, 0):
            print(1)
            # self.dx = -10
            self.image = pg.transform.rotate(self.image, 90)
            print(self.rect)
            print((self.rect.height - self.rect.width) * self.is_up)
            self.rect.y += (self.rect.height - self.rect.width) * self.is_up
            self.is_up *= -1
            self.time_to_unpress = pg.time.get_ticks()
        if pg.mouse.get_pressed() == (0, 0, 1):
            print(1)
            # self.dx = 10
            self.time_to_unpress = pg.time.get_ticks()

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
        self.player = Player(self, CARD['pos'])

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
