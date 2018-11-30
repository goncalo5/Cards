

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
    'width': 640,
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
    'atack': {
        'id': 'atack',
        'name': 'Atack',
        'size': (100, 60),
        'font_size': 30,
        'color': RED,
        'pos': (520, 300),
    },
    'block': {
        'id': 'block',
        'name': 'Block',
        'size': (100, 60),
        'font_size': 30,
        'color': LIGHTBLUE,
        'pos': (520, 400),
    },
    'pass': {
        'id': 'pass',
        'name': 'Pass',
        'size': (100, 60),
        'font_size': 30,
        'color': WHITE,
        'pos': (520, 500),
    },
}

# Player
PLAYER = {
    'layer': 2,
    'size': (100, 30),
    'pos': (10, DISPLAY['height'] - 100),
    'life': 2,
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
    'life': 2,
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
    'speed': 10,
    'name': {
        'color': WHITE,
        'pos': (50, 10)
    },
    'type': {
        'color': WHITE,
        'pos': (30, 140)
    },
    'atack': {
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
        'name': 'ze manel',
        'type': 'human',
        'img_dir': 'imgs',
        'img': 'p1_front.png',
        'atack': 1,
        'defense': 1
    }
}
