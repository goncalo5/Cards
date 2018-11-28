#!/usr/bin/env python3
from os import path
import random
import pygame as pg

from settings import DISPLAY, BUTTON, PLAYER, MOB, CARDS, CARD, BLACK, RED


def combat(atack1, defense1, atack2, defense2):
    first_die = atack2 > defense1
    second_die = atack1 > defense2
    return (first_die, second_die)


def draw_text(screen, text, size, color, pos, font='arial'):
    try:
        font = pg.font.Font(font, size)
    except IOError:
        font = pg.font.SysFont(font, size)
    text_surface = font.render(str(text), True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = pos
    screen.blit(text_surface, text_rect)


class Button(pg.sprite.Sprite):
    def __init__(self, game):
        self.groups = game.all_sprites
        super(Button, self).__init__(self.groups)
        self.game = game
        self.image = pg.Surface(BUTTON['atack']['size'])
        self.image.fill(BLACK)

        self.rect = self.image.get_rect()
        self.rect.topleft = BUTTON['atack']['pos']
        pos = (self.rect.width / 2, 10)
        draw_text(self.image, 'Atack', BUTTON['atack']['font_size'],
                  BUTTON['atack']['color'], pos)

    def events(self):
        if not self.rect.collidepoint(pg.mouse.get_pos()):
            return

        if pg.mouse.get_pressed() == (1, 0, 0):
            print(self.rect.collidepoint(pg.mouse.get_pos()))
            creature1 = self.game.player.creatures['ze_manel']
            creature2 = self.game.mob.creatures['ze_manel']
            res = combat(creature1['atack'], creature1['defense'],
                         creature2['atack'], creature2['defense'])
            if res[0]:
                self.game.player.kill()
            if res[1]:
                self.game.mob.kill()

    def update(self):
        self.events()


class Mob(pg.sprite.Sprite):
    def __init__(self, game):
        self.groups = game.all_sprites
        super(Mob, self).__init__(self.groups)
        self.game = game
        self.image = pg.Surface(CARD['size'])
        self.image.fill(BLACK)
        self.image_dir = path.join(path.dirname(__file__), CARDS[1]['img_dir'])
        self.image_path = path.join(self.image_dir, CARDS[1]['img'])
        self.draw = pg.image.load(self.image_path).convert()
        self.rect = self.image.get_rect()
        self.rect_draw = self.draw.get_rect()
        self.rect_draw.midtop = self.rect.midtop
        self.rect_draw.y += 30
        self.image.blit(self.draw, self.rect_draw)
        self.rect.topleft = MOB['pos']
        self.dx = 0
        self.time_to_unpress = pg.time.get_ticks()
        self.is_up = 1
        self.creatures = {
            'ze_manel': {
                'atack': CARDS[1]['atack'],
                'defense': CARDS[1]['defense'],
            }
        }
        for label in ['name', 'type', 'atack', 'defense']:
            draw_text(self.image, CARDS[1][label], CARD['font_size'],
                      CARD[label]['color'], CARD[label]['pos'])
        self.image = pg.transform.rotate(self.image, 180)


class Player(pg.sprite.Sprite):
    def __init__(self, game):
        self._layer = CARD['layer']
        self.groups = game.all_sprites
        super(Player, self).__init__(self.groups)
        self.game = game
        self.image = pg.Surface(CARD['size'])
        self.image.fill(BLACK)
        self.image_dir = path.join(path.dirname(__file__), CARDS[1]['img_dir'])
        self.image_path = path.join(self.image_dir, CARDS[1]['img'])
        self.draw = pg.image.load(self.image_path).convert()
        self.rect = self.image.get_rect()
        self.rect_draw = self.draw.get_rect()
        self.rect_draw.midtop = self.rect.midtop
        self.rect_draw.y += 30
        self.image.blit(self.draw, self.rect_draw)
        # self.image = pg.transform.scale(self.image, CARD.get('size'))
        # self.image.set_colorkey(BLACK)
        self.rect.topleft = PLAYER['pos']
        self.dx = 0
        self.time_to_unpress = pg.time.get_ticks()
        self.is_up = 1
        self.creatures = {
            'ze_manel': {
                'atack': CARDS[1]['atack'],
                'defense': CARDS[1]['defense'],
            }
        }
        for label in ['name', 'type', 'atack', 'defense']:
            draw_text(self.image, CARDS[1][label], CARD['font_size'],
                      CARD[label]['color'], CARD[label]['pos'])

    def events(self):
        # self.dx = 0
        # print(pg.mouse.get_pressed())
        if pg.time.get_ticks() - self.time_to_unpress < 300:
            return

        if not self.rect.collidepoint(pg.mouse.get_pos()):
            return

        if pg.mouse.get_pressed() == (1, 0, 0):
            print(self.rect.collidepoint(pg.mouse.get_pos()))
            # self.dx = -10
            self.image = pg.transform.rotate(self.image, 90 * self.is_up)
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
        # self.rect.x += self.dx


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
        self.player = Player(self)
        self.mob = Mob(self)
        Button(self)

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
