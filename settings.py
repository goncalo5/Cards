

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
    'width': 760,
    'height': 760,
    'bgcolor': DARKBLUE,
    'fps': 30
}
BUTTON = {
    'new_game': {
        'id': 'new_game',
        'name': 'New Game',
        'size': (300, 200),
        'font_size': 50,
        'color': YELLOW,
        'pos': (20, 200)
    },
    'deck': {
        'id': 'deck',
        'name': 'Deck',
        'size': (120, 200),
        'font_size': 40,
        'color': YELLOW,
        'pos': (20, 200)
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
    'life': 12,
    'hand': {
        'pos': (150, DISPLAY['height'] - 210)
    },
    'in_play': {
        'pos': (150, DISPLAY['height'] / 3)
    }
}

MOB = {
    'size': (100, 30),
    'pos': (10, 10),
    'life': 10,
    'in_play': {
        'pos': (150, 10)
    }
}

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
        'defense': 2
    },
    'bird_of_prey': {
        'id': 'bird_of_prey',
        'name': 'bird of prey',
        'type': 'bird',
        'img_dir': 'imgs',
        'img': 'ave-rapina.png',
        'size': (98, 96),
        'attack': 0,
        'defense': 1
    },
    'war_horse': {
        'id': 'war_horse',
        'name': 'War Horse',
        'type': 'horse',
        'img_dir': 'imgs',
        'img': 'cavalo.de.guerra.2.png',
        'size': (57, 100),
        'attack': 2,
        'defense': 3
    },
    'snake_constrictor': {
        'id': 'snake_constrictor',
        'name': 'Snake Constrictor',
        'type': 'snake',
        'img_dir': 'imgs',
        'img': 'cobra-constritora.6.png',
        'size': (80, 100),
        'attack': 2,
        'defense': 2
    },
    'bird': {
        'id': 'bird',
        'name': 'Bird',
        'type': 'vento',
        'img_dir': 'imgs',
        'img': 'vento-08.5.png',
        'size': (102, 100),
        'attack': 1,
        'defense': 2
    },
    'fire_salamander': {
        'id': 'fire_salamander',
        'name': 'Fire Salamander',
        'type': 'fire',
        'img_dir': 'imgs',
        'img': 'fogo-05.2.jpg',
        'size': (127, 74),
        'attack': 2,
        'defense': 1
    },
    'socket_man': {
        'id': 'socket_man',
        'name': 'Socket Man',
        'type': 'electric',
        'img_dir': 'imgs',
        'img': 'elétrico-02.5.png',
        'size': (101, 106),
        'attack': 5,
        'defense': 3
    },
    'electric_bird': {
        'id': 'electric_bird',
        'name': 'Electric Bird',
        'type': 'electric',
        'img_dir': 'imgs',
        'img': 'elétrico-03.png',
        'size': (117, 79),
        'attack': 3,
        'defense': 1
    },
    'electric_up_dog': {
        'id': 'electric_up_dog',
        'name': 'Electric Up Dog',
        'type': 'electric',
        'img_dir': 'imgs',
        'img': 'elétrico-04.png',
        'size': (89, 99),
        'attack': 3,
        'defense': 3
    },
    'electric_dog': {
        'id': 'electric_dog',
        'name': 'Electric Dog',
        'type': 'electric',
        'img_dir': 'imgs',
        'img': 'elétrico-08.png',
        'size': (103, 87),
        'attack': 3,
        'defense': 2
    },
    'electric_rat': {
        'id': 'electric_rat',
        'name': 'Electric Rat',
        'type': 'electric',
        'img_dir': 'imgs',
        'img': 'elétrico-10.png',
        'size': (67, 100),
        'attack': 2,
        'defense': 1
    },
}
