import pygame
import constants
from assets import images, sounds
from .options_menu import show_options_menu

run = False

def show_start_menu():
    global run
    start_menu = True
    constants.MENU_SONG_CHANNEL.play(sounds.menu_song, loops=-1)
    
    while start_menu:
        constants.WIN.blit(constants.TOOLBAR, (0, 0))
        constants.WIN.blit(constants.BG, (0, 61))
        images.play_button.draw(constants.WIN)
        images.options_button.draw(constants.WIN)
        images.quit_button.draw(constants.WIN)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if images.play_button.draw(constants.WIN):
                constants.MENU_SONG_CHANNEL.stop()
                run = True
                start_menu = False

            if images.options_button.draw(constants.WIN):
                show_options_menu()