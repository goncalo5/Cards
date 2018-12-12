#!/usr/bin/env python3
from os import path
import random
import pygame as pg

from settings import DISPLAY, MENU, COMBAT, BUTTON, PLAYER, MOB, CARDS, CARD, BLACK, WHITE, RED, GREEN


def combat(attacking_creature, blockers):
    # combat(c1, [c2, c3]) -> (1, [1, 0])
    total_attacking_damage = attacking_creature.attack
    total_blocking_damage = 0
    attacking_creature_died = 0
    blocker_deads = []
    for blocker in blockers:
        total_blocking_damage += blocker.attack
        if total_blocking_damage >= attacking_creature.defense:
            attacking_creature_died = 1
        if total_attacking_damage >= blocker.defense:
            blocker_deads.append(1)
        else:
            blocker_deads.append(0)
        total_attacking_damage -= blocker.defense

    return (attacking_creature_died, blocker_deads)


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
            self.time_to_unpress = pg.time.get_ticks()
            if self.id == 'new_game':
                # self.game.new()
                self.game.combat = Combat(self.game)
                self.game.combat.new()
                self.game.menu.kill()
                self.kill()
            if self.id == 'deck':
                print('button deck')
                self.game.player.draw_a_card()
                if not self.game.player.deck:
                    self.kill()
            if self.id == 'attack':
                print('button attack')
                self.game.player.to_attack(self.game.mob)
            if self.id == 'block':
                print('button block')
                self.game.player.to_block(self.game.mob)
            if self.id == 'pass':
                print('button pass')
                self.game.player.pass_the_turn()

    def update(self):
        self.events()


class Card(pg.sprite.Sprite):
    def __init__(self, game, owner, template, pos=None):
        self.groups = game.all_sprites, game.cards
        super(Card, self).__init__(self.groups)
        self.game = game
        self.owner = owner
        self.template = template
        self.id = id
        self.name = template.name
        self.attack = template.attack
        self.defense = template.defense
        self.image = template.image
        self.speed = CARD['speed']
        self.rotate_speed = CARD['rotate_speed']
        if isinstance(self.owner, Mob):
            pos = (0, -300)
        else:
            pos = BUTTON['deck']['pos']
        self.rect = template.load_rect(self.image, template.draw, pos)

        for label in ['name', 'type', 'attack', 'defense']:
            draw_text(self.image, CARDS[template.id][label], CARD['font_size'],
                      CARD[label]['color'], CARD[label]['pos'])

        self.time_to_unpress = pg.time.get_ticks()
        self.is_in_hand = 1
        self.is_in_play = 0
        self.is_up = 1
        self.is_attacking = 0
        self.blockers = []
        self.is_moving = 0
        self.target_pos = pos
        self.target_angle = 0
        self.current_angle = 0
        self.is_rotating = 0

    def events(self):
        # print('events()', self.is_in_hand, self.is_in_play)
        if pg.time.get_ticks() - self.time_to_unpress < 300:
            return

        if not self.rect.collidepoint(pg.mouse.get_pos()):
            return

        if pg.mouse.get_pressed() == (1, 0, 0):
            self.time_to_unpress = pg.time.get_ticks()
            print('press card', self.is_attacking, self.owner.is_your_turn)

            if self.is_in_play:
                print(self.name, 'is_in_play', self.is_up, self.owner.name)
                if self.owner.name == 'Player':
                    print('player')
                    if self.is_up == 1 and not self.is_rotating and self.owner.is_your_turn:
                        self.game.player.turn_a_card(self)
                    elif self.is_up == -1 and not self.is_rotating and self.owner.is_your_turn:
                        self.game.player.unturn_a_card(self)
                # select attackers to block
                if self.is_up == -1 and self.owner.name == 'Mob':
                    print(self.id, 'is_attacking')
                    self.game.selected_card = self
                    print(self.game.selected_card.blockers)
                # select blockers
                if self.is_up == 1 and self.owner.name == 'Player' and not self.owner.is_your_turn:
                    print(self.id, 'block')
                    try:
                        self.game.selected_card.blockers.append(self)
                        print('selected_card', self.game.selected_card.name)
                        print('blockers', self.game.selected_card.blockers)
                    except AttributeError:
                        print('please insert the attacking to block first')
            if self.is_in_hand:
                print(self.id, 'is_in_hand')
                self.is_in_hand = 0
                self.is_in_play = 1
                self.game.player.play_a_card(self)

    def update(self):
        if self.is_moving:
            self.move_to_pos()
        if self.is_rotating:
            self.rotate_to_angle()

        self.events()

    def move_to_pos(self, target_pos=None):
        # print('move_to_pos()', self.rect, self.target_pos)
        self.is_moving = 1
        if target_pos is not None:
            self.target_pos = target_pos
        # check directions:
        self.dx =\
            self.speed if self.target_pos[0] >= self.rect.x else -self.speed
        self.dy =\
            self.speed if self.target_pos[1] >= self.rect.y else -self.speed

        if abs(self.rect.x - self.target_pos[0]) > self.speed / 2.:
            self.rect.x += self.dx
        if abs(self.rect.y - self.target_pos[1]) > self.speed / 2.:
            self.rect.y += self.dy

        # print(self.rect, self.target_pos, self.dx, self.dy)
        if abs(self.target_pos[0] - self.rect.x) < self.speed and \
                abs(self.target_pos[1] - self.rect.y) < self.speed:
            # print('STOP MOVING')
            self.is_moving = 0

    def rotate(self):
        print('rotate()')
        self.image = pg.transform.rotate(self.image, 90 * self.is_up)
        self.rect.y += (self.rect.height - self.rect.width) * self.is_up
        self.is_up *= -1

    def rotate_to_angle(self, target_angle=None):
        # print('rotate_to_angle()', self.rect, target_angle, self.target_angle, self.current_angle)
        self.is_rotating = 1
        self.is_moving = 1
        if target_angle is not None:
            self.target_angle = target_angle

        self.dalpha = self.rotate_speed if self.target_angle >= self.current_angle else -self.rotate_speed
        self.current_angle += self.dalpha
        self.current_angle %= 360
        self.image = pg.transform.rotate(self.template.image, self.current_angle)
        # self.rect.y += (self.rect.height - self.rect.width) * self.is_up
        if abs(self.target_angle - self.current_angle) <= 2:
            # print('STOP')
            self.is_up *= -1
            self.is_rotating = 0
            self.is_moving = 0


class TemplateCard(object):
    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.name = kwargs.get('name')
        self.type = kwargs.get('type')
        self.attack = kwargs.get('attack')
        self.defense = kwargs.get('defense')
        self.size = kwargs.get('size')

        self.load_a_card()

    def load_a_card(self):
        self.image = pg.Surface(CARD['size'], pg.SRCALPHA)
        self.image.fill(BLACK)
        self.image_dir = path.join(path.dirname(__file__), CARDS[self.id]['img_dir'])
        self.image_path = path.join(self.image_dir, CARDS[self.id]['img'])
        self.draw = pg.image.load(self.image_path).convert_alpha()
        self.draw = pg.transform.scale(self.draw, self.size)

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
        cls.fire_salamander = TemplateCard(**CARDS['fire_salamander'])
        cls.bird = TemplateCard(**CARDS['bird'])
        cls.bird_of_prey = TemplateCard(**CARDS['bird_of_prey'])
        # cls.war_horse = TemplateCard(**CARDS['war_horse'])
        # cls.snake_constrictor = TemplateCard(**CARDS['snake_constrictor'])
        # cls.socket_man = TemplateCard(**CARDS['socket_man'])
        # cls.electric_bird = TemplateCard(**CARDS['electric_bird'])
        # cls.electric_up_dog = TemplateCard(**CARDS['electric_up_dog'])
        # cls.electric_dog = TemplateCard(**CARDS['electric_dog'])
        # cls.electric_rat = TemplateCard(**CARDS['electric_rat'])


class PlayerTemplate(pg.sprite.Sprite):
    def __init__(self, game):
        self._layer = CARD['layer']
        self.groups = game.all_sprites
        super(PlayerTemplate, self).__init__(self.groups)
        self.game = game
        self.name = self.__class__.__name__
        self.init_life = self.settings.get('life').get('init')

        self.image = pg.Surface(self.settings['size'])
        self.rect = self.image.get_rect()
        self.rect.topleft = self.settings['pos']

        self.time_to_unpress = pg.time.get_ticks()

    def new_combat_template(self):
        self.life = self.init_life
        self.hand = set()
        self.in_play = set()
        self.turned = set()
        self.attacking = set()
        self.available_pos = {
            'hand': [0] * PLAYER['hand']['max'],
            'in_play': [0] * PLAYER['in_play']['max']}
        self.wait = 1
        self.step = 0

    def new_turn(self):
        print(self.name, 'new_turn()')
        self.can_draw = 1
        self.is_blocking = 0
        self.is_your_turn = 1
        self.step = 0
        self.wait = 0
        self.card_to_play = None
        self.game.selected_card = None
        for card in self.game.cards:
            card.blockers = []
        cards_to_unturn = []
        self.blockers = {}
        for turned_card in self.turned:
            cards_to_unturn.append(turned_card)
        [self.unturn_a_card(card) for card in cards_to_unturn]

    def draw_a_card(self):
        print(self.name, 'draw_a_card()')
        if not self.can_draw:
            return
        self.can_draw = 0
        try:
            new_card_template = self.deck.pop()
        except IndexError:
            return
        new_card = Card(self.game, self, new_card_template)
        target_pos = list(self.settings['hand']['pos'])

        print('self.available_pos', self.available_pos)
        offset = self.available_pos['hand'].index(0)
        self.available_pos['hand'][offset] = 1
        new_card.relative_pos = {'hand': offset, 'in_play': None}
        print('self.available_pos', self.available_pos)
        print('offset', offset)

        target_pos[0] += CARD['size'][1] * offset
        print('target_pos', target_pos)
        new_card.move_to_pos(target_pos)
        self.hand.add(new_card)
        self.card_to_play = new_card

    def play_a_card(self, card):
        print(self.name, 'play_a_card()', self.hand, card, card in self.hand)
        try:
            self.hand.remove(card)
            card_to_play = card
        except KeyError:
            return
        card_to_play.is_moving = True
        card_to_play.is_in_hand = 0
        card_to_play.is_in_play = 1
        if card_to_play is None:
            return
        self.in_play.add(card_to_play)
        card_to_play.image =\
            pg.transform.rotate(card_to_play.image, self.init_rotate_angle)
        card_to_play.current_angle = self.init_rotate_angle

        target_pos = list(self.settings['in_play']['pos'])
        self.available_pos['hand'][card.relative_pos['hand']] = 0
        card_to_play.relative_pos['hand'] = None
        card_to_play.relative_pos['in_play'] =\
            self.available_pos['in_play'].index(0)
        self.available_pos['in_play'][card.relative_pos['in_play']] = 1
        target_pos[0] += CARD['size'][1] * card_to_play.relative_pos['in_play']
        card_to_play.target_pos = target_pos

    def turn_a_card(self, card):
        print(self.name, 'turn_a_card()', card, card.name)
        try:
            card_to_turn = card
            self.in_play.remove(card)
        except KeyError:
            return
        if card_to_turn is None:
            return
        self.turned.add(card_to_turn)
        card_to_turn.rotate_to_angle(self.init_rotate_angle + 90)

    def unturn_a_card(self, card):
        print(self.name, 'unturn_a_card()', self.turned, card)
        if not self.is_your_turn:
            return
        new_card = card
        self.turned.remove(card)
        self.in_play.add(new_card)
        new_card.rotate_to_angle(self.init_rotate_angle)

    def end_turn(self):
        print(self.name, 'end_turn()')
        self.is_your_turn = 0
        self.step = 0
        self.wait = 1
        print()


class Mob(PlayerTemplate):
    def __init__(self, game):
        # self.groups = game.all_sprites
        self.settings = MOB
        super(Mob, self).__init__(game)

        self.deck = [TemplateCards.fire_salamander, TemplateCards.fire_salamander]

        self.init_rotate_angle = 180
        self.new_combat_template()

    def attack_the_player(self):
        print('mob attack_the_player()', self.turned)
        attacking_cards_to_pop = []
        blocking_cards_to_pop = []
        for attacking_creature in self.game.mob.turned:
            print('attacking_creature', attacking_creature, attacking_creature.blockers)
            if len(attacking_creature.blockers) == 0:
                self.game.player.life -= attacking_creature.attack
                continue
            res = combat(attacking_creature, attacking_creature.blockers)
            print(res)
            if res[0] == 1:
                attacking_creature.move_to_pos(MOB['graveyard']['pos'])
                self.game.mob.available_pos['in_play'][attacking_creature.relative_pos['in_play']] = 0
                attacking_cards_to_pop.append(attacking_creature)
            for blocker_i, blocker_is_dead in enumerate(res[1]):
                print(blocker_i, blocker_is_dead)
                if blocker_is_dead == 1:
                    blocker = attacking_creature.blockers[blocker_i]
                    blocker.move_to_pos(PLAYER['graveyard']['pos'])
                    self.game.player.available_pos['in_play'][blocker.relative_pos['in_play']] = 0
                    blocking_cards_to_pop.append(blocker)
        print('attacking_cards_to_pop', attacking_cards_to_pop)
        for attacking in attacking_cards_to_pop:
            print(attacking, attacking.id)
            self.game.mob.turned.remove(attacking)
        print('blocking_cards_to_pop', blocking_cards_to_pop, self.game.player.in_play)
        for blocking in blocking_cards_to_pop:
            print(blocking.name, self.game.player.in_play, blocking in self.game.player.in_play)
            self.game.player.in_play.remove(blocking)

    def calc_blockers(self):
        self.blockers = {}
        for attacker in self.game.player.turned:
            try:
                self.blockers[attacker] = self.in_play.pop()
            except KeyError:
                self.blockers[attacker] = None

    def update(self):
        # self.image.fill(BLACK)
        # draw_text(self.image, 'life: %s' % self.life, 30, GREEN,
        #           (self.rect.width / 2, 10))
        # if self.life <= 0:
        #     print('Mob died Game Over')
        #     self.game.combat.end()
        #     self.game.menu = Menu(self.game)
        if not self.wait:
            self.step += 1

        if self.step == 1:
            # print('step', self.step, self.game.player.in_play)
            if not self.wait:
                self.wait = 1
                self.draw_a_card()
            if self.card_to_play is None or not self.card_to_play.is_moving:
                self.wait = 0
        if self.step == 2:
            # print('step', self.step, self.game.player.in_play)
            if not self.wait:
                self.wait = 1
                try:
                    self.play_a_card(self.card_to_play)
                except AttributeError:
                    print(self.name, 'cant buy more cards, deck is empty')
            if self.card_to_play is None or not self.card_to_play.is_moving:
                for turned_card in self.in_play:
                    print('turned_card.is_moving', turned_card.is_moving)
                    if turned_card.is_moving:
                        print(turned_card, 'is_moving')
                        break
                else:  # if no break
                    self.wait = 0
        if self.step == 3:
            # print('step', self.step, self.game.player.in_play)
            if not self.wait:
                to_turn = self.in_play.copy()
                print(to_turn)
                for card_to_turn in to_turn:
                    self.turn_a_card(card_to_turn)
                # self.turn_a_card(self.card_to_play.id)
                self.wait = 1
            if not self.game.player.in_play:
                self.wait = 0
        if self.step == 4:
            # print('step', self.step, self.game.player.in_play)
            self.attack_the_player()
            self.end_turn()
            self.game.player.new_turn()


class Player(PlayerTemplate):
    def __init__(self, game):
        # self._layer = CARD['layer']
        # self.groups = game.all_sprites
        self.settings = PLAYER
        super(Player, self).__init__(game)

        self.init_rotate_angle = 0
        self.gold = PLAYER['gold']['init']

    def new_combat(self):
        self.new_combat_template()
        self.new_deck()
        self.new_turn()

    def new_deck(self):
        self.deck = [TemplateCards.ze_manel, TemplateCards.fire_salamander,
                     TemplateCards.bird, TemplateCards.bird_of_prey,
                     TemplateCards.ze_manel, TemplateCards.fire_salamander,
                     # TemplateCards.war_horse, TemplateCards.snake_constrictor,
                     # TemplateCards.socket_man, TemplateCards.electric_bird,
                     # TemplateCards.electric_up_dog, TemplateCards.electric_dog,
                     # TemplateCards.electric_rat
                     ]

    # def update(self):
    #     self.image.fill(BLACK)
        # draw_text(self.image, 'life: %s' % self.life, 30, GREEN, (self.rect.width / 2, 10))
        # if self.life <= 0:
        #     print('Game Over')
        #     Menu(self.game)

    def to_attack(self, enemy):
        enemy.calc_blockers()
        for attacking_creature in self.turned:
            creature1 = attacking_creature
            print('blockers', enemy.blockers)
            creature2 = enemy.blockers.get(creature1)
            print(creature1, creature2)
            if creature1 and not creature2:
                enemy.life -= creature1.attack
                print('enemy.life', enemy.life)
                # enemy.step = 1
            if creature1 and creature2:
                res = combat(creature1, [creature2])
                print(res)
                if res[0]:
                    creature1.kill()
                if res[1]:
                    creature2.kill()
        self.end_turn()
        enemy.new_turn()

    def to_block(self, enemy):
        if enemy.is_your_turn:
            enemy.step += 1

    def pass_the_turn(self):
        if self.is_your_turn:
            self.end_turn()
            self.game.mob.new_turn()


class Menu(pg.sprite.Sprite):
    def __init__(self, game):
        self.groups = game.all_sprites
        super(Menu, self).__init__(self.groups)
        self.game = game
        self.image = pg.Surface((1000, 1000))
        self.image.fill(MENU['color'])
        self.rect = self.image.get_rect()

        # self.clear_all()
        Button(game, **BUTTON['new_game'])

    def clear_all(self):
        for sprite in self.game.all_sprites:
            if sprite is self:
                continue
            sprite.kill()

    def update(self):
        draw_text(self.image, 'gold: %s' % self.game.player.gold,
                  PLAYER['gold']['size'], PLAYER['gold']['color'],
                  PLAYER['gold']['pos'])


class Combat(pg.sprite.Sprite):
    def __init__(self, game):
        self.groups = game.all_sprites
        super(Combat, self).__init__(self.groups)
        self.game = game
        self.color = COMBAT['color']
        self.image = pg.Surface((1000, 1000))
        self.image.fill(self.color)
        self.rect = self.image.get_rect()

    def new(self):
        print('new combat()')
        self.game.mob = Mob(self.game)
        self.game.player.new_combat()

        self.buttons = set()
        for button_name in ['attack', 'deck', 'block', 'pass']:
            self.buttons.add(Button(self.game, **BUTTON[button_name]))
        # Button(self.game, **BUTTON['attack'])
        # Button(self.game, **BUTTON['deck'])
        # Button(self.game, **BUTTON['block'])
        # Button(self.game, **BUTTON['pass'])

    def end(self):
        for sprite in self.game.all_sprites:
            sprite.kill()

    def update(self):
        self.image.fill(self.color)
        draw_text(self.image, 'life: %s' % self.game.player.life,
                  PLAYER['life']['size'], PLAYER['life']['color'],
                  PLAYER['life']['pos'])
        draw_text(self.image, 'life: %s' % self.game.mob.life,
                  MOB['life']['size'], MOB['life']['color'],
                  MOB['life']['pos'])
        if self.game.player.life <= 0:
            print('Player Game Over')
            self.game.combat.end()
            self.game.menu = Menu(self.game)
        if self.game.mob.life <= 0:
            print('Mob died Game Over')
            self.game.combat.end()
            self.game.menu = Menu(self.game)


class Game(object):
    def __init__(self):
        pg.init()
        # self.screen = pg.display.set_mode((0, 0))
        self.screen = pg.display.set_mode((DISPLAY['width'], DISPLAY['height']))
        pg.display.set_caption(DISPLAY['title'])
        self.clock = pg.time.Clock()

        # variables
        self.cmd_key_down = False

        self.load_data()
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.buttons = pg.sprite.Group()
        self.cards = pg.sprite.Group()
        self.selected_card = None
        self.player = Player(self)
        print(333, self.player)
        self.menu = Menu(self)
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
        print(4444, self.player)
        Button(self, **BUTTON['attack'])
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
        try:
            pass
            # print('player.can_draw:', self.player.can_draw,)
            # print('player.can_draw:', self.player.can_draw)
        except:
            pass

    def draw(self):
        pg.display.set_caption('%s - fps: %.5s' %
                               (DISPLAY['title'], self.clock.get_fps()))
        self.screen.fill(DISPLAY['bgcolor'])
        self.all_sprites.draw(self.screen)
        # draw_text(self.screen, 'life:', 30, RED, (100, 100))

        pg.display.flip()

    def quit(self):
        self.running = False


Game()
