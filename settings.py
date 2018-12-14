
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
LIGHTBLUE = (200, 200, 255)
DARKBLUE = (0, 0, 100)
YELLOW = (255, 255, 0)

# Screen
DISPLAY = {
    'title': "My Game",
    'width': 600,
    'height': 750,
    'bgcolor': DARKBLUE,
    'fps': 30
}

MENU = {
    'buttons': ['combat_menu', 'store', 'change_deck'],
    'color': LIGHTBLUE
}
STORE = {
    'buttons': ['menu'],
    'color': BLUE,
    'cards': {
        'pos': (200, 50),
        'margin': 10
    },
    'gold': {
        'size': 25,
        'color': YELLOW
    },
}
COMBAT_MENU = {
    'buttons': ['menu', 'mob1', 'mob2'],
    'color': BLUE,


}
DECK_MENU = {
    'buttons': ['menu'],
    'color': BLUE,
    'cards': {
        'margin': 10,
        'availables': {
            'pos': (200, 50),
        },
        'deck': {
            'pos': (200, 350),
        },
    },
    'text': {
        'size': 30,
        'color': WHITE,
        'pos': {
            'availables': (300, 20),
            'deck': (300, 320)
        }
    }
}
COMBAT = {
    'buttons': ['attack', 'deck', 'block', 'pass', 'quit_combat'],
    'color': DARKBLUE
}

BUTTON = {
    'menu': {
        'id': 'menu',
        'name': 'Menu',
        'size': (150, 75),
        'font_size': 40,
        'color': YELLOW,
        'pos': (20, 350)
    },
    'store': {
        'id': 'store',
        'name': 'Store',
        'size': (150, 75),
        'font_size': 40,
        'color': YELLOW,
        'pos': (20, 350)
    },
    'change_deck': {
        'id': 'change_deck',
        'name': 'Change Deck',
        'size': (150, 75),
        'font_size': 30,
        'color': YELLOW,
        'pos': (20, 500)
    },
    'combat_menu': {
        'id': 'combat_menu',
        'name': 'New Combat',
        'size': (150, 75),
        'font_size': 30,
        'color': YELLOW,
        'pos': (20, 200)
    },
    'mob1': {
        'id': 'mob1',
        'name': 'Mob 1',
        'size': (150, 75),
        'font_size': 30,
        'color': YELLOW,
        'pos': (220, 350)
    },
    'mob2': {
        'id': 'mob2',
        'name': 'Mob 2',
        'size': (150, 75),
        'font_size': 30,
        'color': YELLOW,
        'pos': (220, 500)
    },
    'deck': {
        'id': 'deck',
        'name': 'Deck',
        'size': (120, 200),
        'font_size': 40,
        'color': YELLOW,
        'pos': (20, 200)
    },
    'quit_combat': {
        'id': 'quit_combat',
        'name': 'Quit',
        'size': (100, 60),
        'font_size': 30,
        'color': RED,
        'pos': (DISPLAY['width'] - 120, DISPLAY['height'] - 100),
    },
    'attack': {
        'id': 'attack',
        'name': 'attack',
        'size': (100, 60),
        'font_size': 30,
        'color': RED,
        'pos': (DISPLAY['width'] - 120, 300),
    },
    'block': {
        'id': 'block',
        'name': 'Block',
        'size': (100, 60),
        'font_size': 30,
        'color': LIGHTBLUE,
        'pos': (DISPLAY['width'] - 120, 400),
    },
    'pass': {
        'id': 'pass',
        'name': 'Pass',
        'size': (100, 60),
        'font_size': 30,
        'color': WHITE,
        'pos': (DISPLAY['width'] - 120, 500),
    },
}


# Player
PLAYER = {
    'layer': 2,
    'size': (100, 30),
    'pos': (10, DISPLAY['height'] - 100),
    'life': {
        'init': 12,
        'size': 30,
        'color': GREEN,
        'pos': (40, 630)
    },
    'hand': {
        'pos': (150, DISPLAY['height'] - 210),
        'max': 3
    },
    'in_play': {
        'pos': (150, DISPLAY['height'] / 3),
        'max': 3
    },
    'graveyard': {'pos': (20, 420)},
    'gold': {
        'init': 100,
        'pos': (100, 100),
        'size': 30,
        'color': YELLOW
    },
    'available_cards': ['bird', 'bird_of_prey']
}

MOB = {
    'size': (100, 30),
    'pos': (10, 10),
    'life': {
        'init': 10,
        'size': 30,
        'color': GREEN,
        'pos': (40, 40)
    },
    'hand': {
        'pos': (150, -210),
        'max': 3
    },
    'in_play': {
        'pos': (150, 10),
        'max': 3
    },
    'graveyard': {'pos': (20, -200)},
    'available_cards': ['ze_manel', 'fire_salamander'],
    'reward': 10
}
MOBS = [
    {
        'available_cards': {
            'ze_manel': 1,
            'fire_salamander': 1
        },
        'reward': 10
    },
    {
        'available_cards': {
            'ze_manel': 2,
            'fire_salamander': 2
        },
        'reward': 20
    },


]


CARD = {
    'layer': 2,
    'size': (120, 160),
    'width': 120,
    'height': 160,
    'font_size': 20,
    'speed': 15,
    'rotate_speed': 5,
    'name': {
        'color': WHITE,
        'pos': (50, 10)
    },
    'type': {
        'color': WHITE,
        'pos': (30, 140)
    },
    'attack': {
        'color': RED,
        'pos': (80, 140)
    },
    'defense': {
        'color': LIGHTBLUE,
        'pos': (100, 140)
    }
}

CARDS = {
    'ze_manel': {
        'id': 'ze_manel',
        'name': 'Ze Manel',
        'type': 'human',
        'img_dir': 'imgs',
        'img': 'p1_front.png',
        'size': (66, 92),
        'attack': 2,
        'defense': 2,
        'prize': 40
    },
    'bird_of_prey': {
        'id': 'bird_of_prey',
        'name': 'bird of prey',
        'type': 'bird',
        'img_dir': 'imgs',
        'img': 'ave-rapina.png',
        'size': (98, 96),
        'attack': 0,
        'defense': 1,
        'prize': 10
    },
    'war_horse': {
        'id': 'war_horse',
        'name': 'War Horse',
        'type': 'horse',
        'img_dir': 'imgs',
        'img': 'cavalo.de.guerra.2.png',
        'size': (57, 100),
        'attack': 2,
        'defense': 3,
        'prize': 50
    },
    'snake_constrictor': {
        'id': 'snake_constrictor',
        'name': 'Snake Constrictor',
        'type': 'snake',
        'img_dir': 'imgs',
        'img': 'cobra-constritora.6.png',
        'size': (80, 100),
        'attack': 2,
        'defense': 2,
        'prize': 40
    },
    'bird': {
        'id': 'bird',
        'name': 'Bird',
        'type': 'vento',
        'img_dir': 'imgs',
        'img': 'vento-08.5.png',
        'size': (102, 100),
        'attack': 1,
        'defense': 2,
        'prize': 30
    },
    'fire_salamander': {
        'id': 'fire_salamander',
        'name': 'Fire Salamander',
        'type': 'fire',
        'img_dir': 'imgs',
        'img': 'fogo-05.2.jpg',
        'size': (127, 74),
        'attack': 2,
        'defense': 1,
        'prize': 30
    },
    'socket_man': {
        'id': 'socket_man',
        'name': 'Socket Man',
        'type': 'electric',
        'img_dir': 'imgs',
        'img': 'elétrico-02.5.png',
        'size': (101, 106),
        'attack': 5,
        'defense': 3,
        'prize': 80
    },
    'electric_bird': {
        'id': 'electric_bird',
        'name': 'Electric Bird',
        'type': 'electric',
        'img_dir': 'imgs',
        'img': 'elétrico-03.png',
        'size': (117, 79),
        'attack': 3,
        'defense': 1,
        'prize': 40
    },
    'electric_up_dog': {
        'id': 'electric_up_dog',
        'name': 'Electric Up Dog',
        'type': 'electric',
        'img_dir': 'imgs',
        'img': 'elétrico-04.png',
        'size': (89, 99),
        'attack': 3,
        'defense': 3,
        'prize': 60
    },
    'electric_dog': {
        'id': 'electric_dog',
        'name': 'Electric Dog',
        'type': 'electric',
        'img_dir': 'imgs',
        'img': 'elétrico-08.png',
        'size': (103, 87),
        'attack': 3,
        'defense': 2,
        'prize': 50
    },
    'electric_rat': {
        'id': 'electric_rat',
        'name': 'Electric Rat',
        'type': 'electric',
        'img_dir': 'imgs',
        'img': 'elétrico-10.png',
        'size': (67, 100),
        'attack': 2,
        'defense': 1,
        'prize': 30
    },
}
