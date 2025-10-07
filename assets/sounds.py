import pygame

# Load sounds
shoot_single = pygame.mixer.Sound("resources/sounds/shoot_single.mp3")
shoot_double = pygame.mixer.Sound("resources/sounds/shoot_double.mp3")
destroy_missile = pygame.mixer.Sound("resources/sounds/destroy_missile.wav")
getting_hit = pygame.mixer.Sound("resources/sounds/getting_hit.wav")
collect_heart = pygame.mixer.Sound("resources/sounds/collect_heart.mp3")
activate_shield = pygame.mixer.Sound("resources/sounds/activate_shield.wav")
deactivate_shield = pygame.mixer.Sound("resources/sounds/deactivate_shield.wav")
countdown = pygame.mixer.Sound("resources/sounds/countdown.wav")
collect_points = pygame.mixer.Sound("resources/sounds/collect_points.wav")
game_over = pygame.mixer.Sound("resources/sounds/game_over.wav")
upgrade = pygame.mixer.Sound("resources/sounds/upgrade.wav")
generate_heart = pygame.mixer.Sound("resources/sounds/generate_heart.wav")
menu_song = pygame.mixer.Sound("resources/sounds/menu_song.wav")

# Volume setup
def set_default_volumes():
    shoot_single.set_volume(0.1)
    shoot_double.set_volume(0.1)
    destroy_missile.set_volume(1.0)
    getting_hit.set_volume(1.0)
    collect_heart.set_volume(0.8)
    activate_shield.set_volume(0.6)
    deactivate_shield.set_volume(1.0)
    countdown.set_volume(1.0)
    collect_points.set_volume(0.7)
    game_over.set_volume(1.0)
    upgrade.set_volume(0.8)
    generate_heart.set_volume(0.7)
    menu_song.set_volume(1.0)