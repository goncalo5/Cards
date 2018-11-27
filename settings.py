

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
DARKBLUE = (0, 0, 100)
YELLOW = (255, 255, 0)

# Screen
DISPLAY = {
    'title': "My Game",
    'width': 360,
    'height': 480,
    'bgcolor': DARKBLUE,
    'fps': 30
}

# Player
PLAYER = {
    'layer': 2
}

CARD = {
    'layer': 2,
    'width': 120,
    'height': 200,
    'pos': (100, 200)
}

CARDS = {
    1: {
        'name': 'ze manel',
        'type': 'human',
        'img_folder': 'imgs',
        'img': 'ze_manel.png',
        'atack': 7,
        'defense': 8
    }
}
