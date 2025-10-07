import pygame
import button

# Load button images
play_img = pygame.image.load("resources/buttons/play.png").convert_alpha()
resume_img = pygame.image.load("resources/buttons/resume.png").convert_alpha()
options_img = pygame.image.load("resources/buttons/options.png").convert_alpha()
quit_img = pygame.image.load("resources/buttons/quit.png").convert_alpha()
back_img = pygame.image.load("resources/buttons/back.png").convert_alpha()
audio_img = pygame.image.load("resources/buttons/audio.png").convert_alpha()
red_audio_img = pygame.image.load("resources/buttons/red_audio.png").convert_alpha()
music_img = pygame.image.load("resources/buttons/music.png").convert_alpha()
red_music_img = pygame.image.load("resources/buttons/red_music.png").convert_alpha()

# Button instances
play_button = button.Button(200, play_img, 1)
resume_button = button.Button(200, resume_img, 1)
options_button = button.Button(300, options_img, 1)
quit_button = button.Button(600, quit_img, 1)
back_button = button.Button(600, back_img, 1)
audio_button = button.Button(200, audio_img, 1)
red_audio_button = button.Button(200, red_audio_img, 1)
music_button = button.Button(300, music_img, 1)
red_music_button = button.Button(300, red_music_img, 1)