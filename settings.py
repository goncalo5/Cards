

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
    'height': 480,
    'bgcolor': DARKBLUE,
    'fps': 30
}
BUTTON = {
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
    }
}

# Player
PLAYER = {
    'layer': 2,
    'pos': (150, 250),
}

MOB = {
    'pos': (150, 20)
}

CARD = {
    'layer': 2,
    'size': (120, 200),
    'width': 120,
    'height': 200,
    'font_size': 20,
    'name': {
        'color': WHITE,
        'pos': (50, 10)
    },
    'type': {
        'color': WHITE,
        'pos': (50, 150)
    },
    'atack': {
        'color': RED,
        'pos': (60, 180)
    },
    'defense': {
        'color': LIGHTBLUE,
        'pos': (80, 180)
    }
}

CARDS = {
    'ze_manel': {
        'id': 'ze_manel',
        'name': 'ze manel',
        'type': 'human',
        'img_dir': 'imgs',
        'img': 'p1_front.png',
        'atack': 7,
        'defense': 6
    }
}
