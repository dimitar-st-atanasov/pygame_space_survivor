import pygame
pygame.font.init()
pygame.mixer.init()

GAME_NAME = "Space Survivor"

# Screen dimensions
WIDTH, HEIGHT = 1000, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

# Load and scale background and toolbar
BG = pygame.transform.scale(pygame.image.load("resources/images/space_background.jpg"), (WIDTH, HEIGHT - 60))
TOOLBAR = pygame.transform.scale(pygame.image.load("resources/images/toolbar.png"), (WIDTH, HEIGHT - 740))

LIFE_HEART_WIDTH = 30
LIFE_HEART_HEIGHT = 35
LIFE_HEART = pygame.transform.scale(pygame.image.load("resources/images/lifes.png"), (LIFE_HEART_WIDTH, LIFE_HEART_HEIGHT))

HIT_WIDTH = 35
HIT_HEIGHT = 45
HIT = pygame.transform.scale(pygame.image.load("resources/images/hit.png"), (HIT_WIDTH, HIT_HEIGHT))

# Player dimensions
SPACESHIP_WIDTH = 40
SPACESHIP_HEIGHT = 50

# Load and scale spaceship
SPACESHIP = pygame.transform.scale(pygame.image.load("resources/images/spaceship.png"), (SPACESHIP_WIDTH, SPACESHIP_HEIGHT))

SHIELD = pygame.transform.scale(pygame.image.load("resources/images/shield.png"), (SPACESHIP_WIDTH, SPACESHIP_HEIGHT))
SHIELD_HUNDRED_POINTS = pygame.transform.scale(pygame.image.load("resources/images/shield.png"), (50, 50))

# Velocity
PLAYER_VEL = 5
ASTEROID_VEL = 1
MISSILE_VEL = 4
LASER_VEL = 15
EXTRA_LIFE_HEART_VEL = 3

MISSILE_WIDTH = 20
MISSILE_HEIGHT = 45
MISSILE = pygame.transform.scale(pygame.image.load("resources/images/missile.png"), (MISSILE_WIDTH, MISSILE_HEIGHT))

ASTEROID_WIDTH = 120
ASTEROID_HEIGHT = 120
ASTEROID = pygame.transform.scale(pygame.image.load("resources/images/asteroid.png"), (ASTEROID_WIDTH, ASTEROID_HEIGHT))

LASER_WIDTH = 2
LASER_HEIGHT = 20

# Font for rendering text
FONT = pygame.font.SysFont("comicsans", 25)

# Initialize mixer with enough channels
pygame.mixer.set_num_channels(14)

# Assign channels for different sounds
SHOOT_SINGLE_CHANNEL = pygame.mixer.Channel(0)
SHOOT_DOUBLE_CHANNEL = pygame.mixer.Channel(1)
DESTROY_ASTEROID_CHANNEL = pygame.mixer.Channel(2)
DESTROY_MISSILE_CHANNEL = pygame.mixer.Channel(3)
GETTING_HIT_CHANNEL = pygame.mixer.Channel(4)
COLLECT_HEART_CHANNEL = pygame.mixer.Channel(5)
ACTIVATE_SHIELD_CHANNEL = pygame.mixer.Channel(6)
DEACTIVATE_SHIELD_CHANNEL = pygame.mixer.Channel(7)
COUNTDOWN_CHANNEL = pygame.mixer.Channel(8)
COLLECT_POINTS_CHANNEL = pygame.mixer.Channel(9)
GAME_OVER_CHANNEL = pygame.mixer.Channel(10)
UPGRADE_CHANNEL = pygame.mixer.Channel(11)
GENERATE_HEART_CHANNEL = pygame.mixer.Channel(12)
MENU_SONG_CHANNEL = pygame.mixer.Channel(13)