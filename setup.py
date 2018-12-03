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
        self.groups = game.all_sprites, game.buttons
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
            if self.id == 'new_game':
                self.game.new()
                self.kill()
            if self.id == 'deck':
                if self.game.player.can_draw:
                    self.game.player.draw_a_card()
                    self.game.player.can_draw = 0
                if not self.game.player.deck:
                    self.kill()
            if self.id == 'atack':
                print('button atack')
                self.game.mob.calc_blockers()
                for atacking_creature in self.game.player.turned:
                    creature1 = self.game.player.turned[atacking_creature]
                    creature2 = self.game.mob.blockers[creature1.id]
                    print(creature1, creature2)
                    if creature1 and not creature2:
                        self.game.mob.life -= creature1.atack
                        self.game.mob.step = 1
                    if creature1 and creature2:
                        res = combat(creature1, creature2)
                        print(res)
                        if res[0]:
                            creature1.kill()
                        if res[1]:
                            creature2.kill()
            if self.id == 'block':
                self.game.player.is_blocking = 1
                print('button block')
                # if self.game.player.in_play:
                for blocking_creature in self.game.player.in_play.values():
                    for atacking_creature in self.game.mob.turned.values():
                        creature1 = atacking_creature
                        creature2 = blocking_creature
                        print(creature1, creature2)
                        res = combat(creature1, creature2)
                        print (res)
                        if res[0]:
                            creature1.kill()
                        if res[1]:
                            creature2.kill()
            if self.id == 'pass':
                print('button pass')
                self.game.mob.step += 1

            self.time_to_unpress = pg.time.get_ticks()

    def update(self):
        self.events()


class Card(pg.sprite.Sprite):
    def __init__(self, game, owner, template, pos=None):
        self.groups = game.all_sprites, game.cards
        super(Card, self).__init__(self.groups)
        self.game = game
        self.owner = owner
        self.template = template
        self.id = template.id
        self.atack = template.atack
        self.defense = template.defense
        self.image = template.image
        self.speed = CARD['speed']
        if pos is None:
            pos = (0, -300)
        self.rect = template.load_rect(self.image, template.draw, pos)

        for label in ['name', 'type', 'atack', 'defense']:
            draw_text(self.image, CARDS[self.id][label], CARD['font_size'],
                      CARD[label]['color'], CARD[label]['pos'])

        self.time_to_unpress = pg.time.get_ticks()
        self.is_in_hand = 1
        self.is_in_play = 0
        self.is_up = 1
        self.is_atacking = 0
        self.is_moving = 0
        self.target_pos = pos

    def events(self):
        if pg.time.get_ticks() - self.time_to_unpress < 300:
            return

        if not self.rect.collidepoint(pg.mouse.get_pos()):
            return

        if pg.mouse.get_pressed() == (1, 0, 0):
            self.time_to_unpress = pg.time.get_ticks()

            if self.is_in_play:
                # self.rotate()
                if self.is_up == 1:
                    self.game.player.turn_a_card(self)
                else:
                    self.game.player.unturn_a_card(self)
            if self.is_in_hand:
                self.is_in_hand = 0
                self.is_in_play = 1
                self.game.player.play_a_card(self)
                # self.rect.topleft = PLAYER['in_play']['pos']
                print(555)
                self.move_to_pos(PLAYER['in_play']['pos'])

    def update(self):
        if self.is_moving:
            self.move_to_pos()

        self.events()

    def move_to_pos(self, target_pos=None):
        print('move_to_pos()', self.rect, self.target_pos)
        self.is_moving = 1
        if target_pos is not None:
            self.target_pos = target_pos
        # check directions:
        self.dx =\
            self.speed if self.target_pos[0] >= self.rect.x else -self.speed
        self.dy =\
            self.speed if self.target_pos[1] >= self.rect.y else -self.speed

        if self.rect.x != self.target_pos[0]:
            self.rect.x += self.dx
        if self.rect.y != self.target_pos[1]:
            self.rect.y += self.dy

        print(self.rect, self.target_pos, self.dx, self.dy)
        if abs(self.target_pos[0] - self.rect.x) < self.speed and \
                abs(self.target_pos[1] - self.rect.y) < self.speed:
            print('STOP MOVING')
            self.is_moving = 0

    def rotate(self):
        self.image = pg.transform.rotate(self.image, 90 * self.is_up)
        self.rect.y += (self.rect.height - self.rect.width) * self.is_up
        self.is_up *= -1


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
        self.atacking = {}

        self.image = pg.Surface(MOB['size'])
        self.rect = self.image.get_rect()
        self.rect.topleft = MOB['pos']

        self.new_turn()

    def new_turn(self):
        self.step = 0
        self.wait = 1
        # self.game.player.is_your_turn = 0
        self.is_your_turn = 1
        self.card_to_play = None
        for turned_card in self.turned:
            self.unturn_a_card(turned_card)

    def draw_a_card(self):
        print('draw_a_card()')
        try:
            new_card_template = self.deck.pop()
        except IndexError:
            return
        new_card = Card(self.game, self, new_card_template)
        self.hand[new_card_template.id] = new_card
        self.card_to_play = self.hand[new_card.id]

    def play_a_card(self, card):
        print('play_a_card()')
        try:
            card_to_play = self.hand.pop(card)
        except KeyError:
            return
        card_to_play.is_moving = True
        if card_to_play is not None:
            self.in_play[card_to_play.id] = card_to_play
            card_to_play.image = pg.transform.rotate(card_to_play.image, 180)
            card_to_play.target_pos = MOB['in_play']['pos']

    def turn_a_card(self, card):
        print('turn_a_card()')
        try:
            card_to_turn = self.in_play.pop(card)
        except KeyError:
            return
        if card_to_turn is not None:
            self.turned[card_to_turn.id] = card_to_turn
            card_to_turn.rotate()

    def unturn_a_card(self, card):
        if type(card) != str:
            card = card.id
        new_card = self.turned.pop(card)
        self.in_play[new_card.id] = new_card

    def atack_the_player(self):
        print('atack_the_player()')
        for atacking_creature in self.turned.values():
            creature1 = atacking_creature
            if not self.game.player.is_blocking:
                self.game.player.life -= creature1.atack
                self.step = 0
                self.wait = 1
                continue
            for blocking_creature in self.game.player.in_play.values():
                creature2 = blocking_creature
                res = combat(creature1, creature2)
                print(res)
                if res[1]:
                    creature2.kill()
                if res[0]:
                    creature1.kill()
                continue
            self.game.player.life -= creature1.atack

    def calc_blockers(self):
        self.blockers = {}
        for atacker in self.game.player.turned:
            try:
                self.blockers[atacker] = self.in_play.pop()
            except TypeError:
                self.blockers[atacker] = None

    def update(self):
        self.image.fill(BLACK)
        draw_text(self.image, 'life: %s' % self.life, 30, GREEN,
                  (self.rect.width / 2, 10))
        if not self.wait:
            self.step += 1

        if self.step == 1:
            # print('step', self.step)
            self.draw_a_card()
            self.card_to_play.is_moving = True
            self.wait = 0
        if self.step == 2:
            # print('step', self.step)
            if not self.wait:
                self.wait = 1
                self.play_a_card(self.card_to_play.id)
            if not self.card_to_play.is_moving:
                self.wait = 0
        if self.step == 3:
            # print('step', self.step)
            if not self.wait:
                self.turn_a_card(self.card_to_play.id)
                self.wait = 1
            if not self.game.player.in_play:
                self.wait = 0
        if self.step == 4:
            # print('step', self.step)
            self.atack_the_player()
            self.game.player.new_turn()


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
        self.atacking = {}

        self.image = pg.Surface(PLAYER['size'])
        self.rect = self.image.get_rect()
        self.rect.topleft = PLAYER['pos']

        self.time_to_unpress = pg.time.get_ticks()

        self.new_turn()

    def update(self):
        self.image.fill(BLACK)
        draw_text(self.image, 'life: %s' % self.life, 30, GREEN, (self.rect.width / 2, 10))
        if self.life <= 0:
            print('Game Over')
            Menu(self.game)

    def new_turn(self):
        print('new_turn()')
        self.can_draw = 1
        self.is_blocking = 0
        self.game.mob.is_your_turn = 0
        self.is_your_turn = 1
        cards_to_unturn = []
        for turned_card in self.turned:
            cards_to_unturn.append(turned_card)
        print(5, cards_to_unturn)
        [self.unturn_a_card(card) for card in cards_to_unturn]

    def draw_a_card(self):
        new_card_template = self.deck.pop()
        deck_pos = BUTTON['deck']['pos']
        new_card = Card(self.game, self, new_card_template, deck_pos)
        new_card.move_to_pos(PLAYER['hand']['pos'])
        self.hand[new_card.id] = new_card

    def play_a_card(self, card):
        if type(card) != str:
            card = card.id
        new_card = self.hand.pop(card)
        self.in_play[new_card.id] = new_card

    def turn_a_card(self, card):
        print('turn_a_card()')
        if type(card) != str:
            card = card.id
        new_card = self.in_play.pop(card)
        self.turned[new_card.id] = new_card
        new_card.rotate()

    def unturn_a_card(self, card):
        print('unturn_a_card()')
        if type(card) != str:
            card = card.id
        new_card = self.turned.pop(card)
        self.in_play[new_card.id] = new_card
        new_card.rotate()

    def atack_the_player(self):
        pass


class Menu(object):
    def __init__(self, game):
        self.game = game

        self.clear_all()
        Button(game, **BUTTON['new_game'])

    def clear_all(self):
        for sprite in self.game.all_sprites:
            sprite.kill()


class Game(object):
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((DISPLAY['width'], DISPLAY['height']))
        pg.display.set_caption(DISPLAY['title'])
        self.clock = pg.time.Clock()

        # variables
        self.cmd_key_down = False

        self.load_data()
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.buttons = pg.sprite.Group()
        self.cards = pg.sprite.Group()
        Menu(self)
        # self.new()
        self.run()

        pg.quit()

    def load_data(self):
        self.dir = path.dirname(__file__)
        TemplateCards.load_all_cards()
        pg.mixer.init()  # for sound

    def new(self):
        print('new()')
        # start a new game
        # self.all_sprites = pg.sprite.LayeredUpdates()
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
