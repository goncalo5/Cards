#!/usr/bin/env python3
from os import path
import random
import pygame as pg

from settings import DISPLAY, BUTTON, PLAYER, MOB, CARDS, CARD, BLACK, RED, GREEN


def combat(creature1, creature2):
    first_die = creature2.atack >= creature1.defense
    second_die = creature1.atack >= creature2.defense
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
    def __init__(self, game, **kwargs):
        self.groups = game.all_sprites
        super(Button, self).__init__(self.groups)
        self.game = game
        self.id = kwargs.get('id')
        self.image = pg.Surface(kwargs.get('size'))
        self.image.fill(BLACK)

        self.rect = self.image.get_rect()
        self.rect.topleft = kwargs.get('pos')

        pos = (self.rect.width / 2, 10)
        draw_text(self.image, kwargs.get('name'), kwargs.get('font_size'),
                  kwargs.get('color'), pos)
        self.time_to_unpress = pg.time.get_ticks()

    def events(self):
        if pg.time.get_ticks() - self.time_to_unpress < 300:
            return

        if not self.rect.collidepoint(pg.mouse.get_pos()):
            return

        if pg.mouse.get_pressed() == (1, 0, 0):
            if self.id == 'deck':
                self.draw_a_card()
            if self.id == 'atack':
                creature1 = self.game.player.turned.get('ze_manel')
                creature2 = self.game.mob.in_play.get('ze_manel')
                if creature1 and not creature2:
                    self.game.mob.life -= creature1.atack
                    self.game.mob.step = 1
                if creature1 and creature2:
                    res = combat(creature1, creature2)
                    if res[0]:
                        creature1.kill()
                    if res[1]:
                        self.game.mob.kill()
            if self.id == 'block':
                print('block')

            self.time_to_unpress = pg.time.get_ticks()

    def update(self):
        self.events()

    def draw_a_card(self):
        new_card_template = self.game.player.deck.pop()
        self.game.player.hand[new_card_template.id] =\
            Card(self.game, new_card_template, PLAYER['hand']['pos'])


class Card(pg.sprite.Sprite):
    def __init__(self, game, template, pos=None):
        self.groups = game.all_sprites
        super(Card, self).__init__(self.groups)
        self.game = game
        self.template = template
        self.id = template.id
        self.atack = template.atack
        self.defense = template.defense
        self.image = template.image
        if pos is None:
            pos = (0, -300)
        self.rect = template.load_rect(self.image, template.draw, pos)

        for label in ['name', 'type', 'atack', 'defense']:
            draw_text(self.image, CARDS['ze_manel'][label], CARD['font_size'],
                      CARD[label]['color'], CARD[label]['pos'])

        self.time_to_unpress = pg.time.get_ticks()
        self.is_in_hand = 1
        self.is_in_play = 0
        self.is_up = 1
        self.is_moving = 0
        self.target_pos = pos

    def events(self):
        if pg.time.get_ticks() - self.time_to_unpress < 300:
            return

        if not self.rect.collidepoint(pg.mouse.get_pos()):
            return

        if pg.mouse.get_pressed() == (1, 0, 0):
            if self.is_in_play:
                self.rotate_a_card()
            if self.is_in_hand:
                self.is_in_hand = 0
                self.is_in_play = 1
                self.game.player.hand.pop(self.template.id)
                self.game.player.in_play[self.template.id] = self
                self.rect.topleft = PLAYER['in_play']['pos']

            self.time_to_unpress = pg.time.get_ticks()
        if pg.mouse.get_pressed() == (0, 0, 1):
            self.time_to_unpress = pg.time.get_ticks()

    def update(self):
        if self.is_moving:
            self.rect.x = self.target_pos[0]
            self.move_to_pos()

        self.events()

    def move_to_pos(self):
        if self.rect.y > self.target_pos[1]:
            self.is_moving = 0
        self.rect.y += 10

    def rotate_a_card(self):
        self.image = pg.transform.rotate(self.image, 90 * self.is_up)
        self.rect.y += (self.rect.height - self.rect.width) * self.is_up
        self.is_up *= -1
        if self.is_up == -1:
            self.game.player.turned[self.template.id] = self
        else:
            self.game.player.turned.pop(self.template.id)


class TemplateCard(object):
    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.name = kwargs.get('name')
        self.type = kwargs.get('type')
        self.atack = kwargs.get('atack')
        self.defense = kwargs.get('defense')

        self.load_a_card()

    def load_a_card(self):
        self.image = pg.Surface(CARD['size'])
        self.image.fill(BLACK)
        self.image_dir = path.join(path.dirname(__file__), CARDS[self.id]['img_dir'])
        self.image_path = path.join(self.image_dir, CARDS[self.id]['img'])
        self.draw = pg.image.load(self.image_path).convert()

    @classmethod
    def load_rect(cls, image, draw, pos):
        rect = image.get_rect()
        rect_draw = draw.get_rect()
        rect_draw.midtop = rect.midtop
        rect_draw.y += 30
        image.blit(draw, rect_draw)
        rect.topleft = pos
        return rect


class TemplateCards(object):
    @classmethod
    def load_all_cards(cls):

        cls.ze_manel = TemplateCard(**CARDS['ze_manel'])


class Mob(pg.sprite.Sprite):
    def __init__(self, game):
        self.groups = game.all_sprites
        super(Mob, self).__init__(self.groups)
        self.game = game
        self.life = MOB['life']

        self.deck = [TemplateCards.ze_manel]
        self.hand = {}
        self.in_play = {}
        self.turned = {}

        self.image = pg.Surface(MOB['size'])
        self.rect = self.image.get_rect()
        self.rect.topleft = MOB['pos']

        self.step = 0
        self.wait = 1
        self.steps = ['drawing', 'playing', 'turning', 'atacking']
        self.card_to_play = None

    def draw_a_card(self):
        new_card_template = self.deck.pop()
        new_card = Card(self.game, new_card_template)
        self.hand[new_card_template.id] = new_card
        self.card_to_play = self.hand[new_card.id]

    def play_a_card(self, card):
        card_to_play = self.hand.pop(card)
        card_to_play.is_moving = True
        if card_to_play is not None:
            self.in_play[card_to_play.id] = card_to_play
            card_to_play.image = pg.transform.rotate(card_to_play.image, 180)
            card_to_play.target_pos = MOB['in_play']['pos']

    def turn_a_card(self, card):
        card_to_turn = self.in_play.get(card)
        if card_to_turn is not None:
            self.turned[card_to_turn.id] = card_to_turn
            card_to_turn.rotate_a_card()

    def atack_the_player(self):
        creature1 = self.turned['ze_manel']
        creature2 = self.game.player.in_play['ze_manel']
        res = combat(creature1, creature2)
        if res[1]:
            creature2.kill()
        if res[0]:
            creature1.kill()

    def update(self):
        self.image.fill(BLACK)
        draw_text(self.image, 'life: %s' % self.life, 30, GREEN,
                  (self.rect.width / 2, 10))
        if not self.wait:
            self.step += 1

        if self.step == 1:
            self.draw_a_card()
            self.card_to_play.is_moving = True
            self.wait = 0
        if self.step == 2:
            if not self.wait:
                self.wait = 1
                self.play_a_card(self.card_to_play.id)
            if not self.card_to_play.is_moving:
                self.wait = 0
        if self.step == 3:
            if not self.wait:
                self.turn_a_card(self.card_to_play.id)
                self.wait = 1
        if self.step == 4:
            print(self.step)
            self.atack_the_player()


class Player(pg.sprite.Sprite):
    def __init__(self, game):
        self._layer = CARD['layer']
        self.groups = game.all_sprites
        super(Player, self).__init__(self.groups)
        self.game = game
        self.life = PLAYER['life']

        self.deck = [TemplateCards.ze_manel]
        self.hand = {}
        self.in_play = {}
        self.turned = {}

        self.image = pg.Surface(PLAYER['size'])
        self.rect = self.image.get_rect()
        self.rect.topleft = PLAYER['pos']

        # draw_text(self.image, 'life: %s' % self.life, 20, GREEN, (self.rect.width / 2, 10))

        self.time_to_unpress = pg.time.get_ticks()

    # def events(self):
        # print(pg.mouse.get_pressed())
        # if pg.time.get_ticks() - self.time_to_unpress < 300:
        #     return

        # if not self.rect.collidepoint(pg.mouse.get_pos()):
        #     return

        # if pg.mouse.get_pressed() == (1, 0, 0):

    def update(self):
        self.image.fill(BLACK)
        draw_text(self.image, 'life: %s' % self.life, 30, GREEN, (self.rect.width / 2, 10))

    #     self.events()


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
        TemplateCards.load_all_cards()
        pg.mixer.init()  # for sound

    def new(self):
        # start a new game
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.mob = Mob(self)
        self.player = Player(self)
        Button(self, **BUTTON['atack'])
        Button(self, **BUTTON['deck'])
        Button(self, **BUTTON['block'])
        Button(self, **BUTTON['pass'])

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
        pg.display.set_caption('%s - fps: %.5s' %
                               (DISPLAY['title'], self.clock.get_fps()))
        self.screen.fill(DISPLAY['bgcolor'])
        self.all_sprites.draw(self.screen)

        pg.display.flip()

    def quit(self):
        self.running = False


Game()
