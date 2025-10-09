import sys
import pygame
import constants
from assets import images, sounds

def show_start_menu():
    pygame.event.clear()
    constants.MENU_SONG_CHANNEL.play(sounds.menu_song, loops=-1)

    while True:
        # draw buttons
        constants.WIN.blit(constants.TOOLBAR, (0, 0))
        constants.WIN.blit(constants.BG, (0, 61))
        images.play_button.draw(constants.WIN)
        images.options_button.draw(constants.WIN)
        images.quit_button.draw(constants.WIN)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos()
                if images.play_button.rect.collidepoint(pos):
                    constants.MENU_SONG_CHANNEL.stop()
                    return "play"
                elif images.options_button.rect.collidepoint(pos):
                    constants.MENU_SONG_CHANNEL.stop()
                    return "options"  # do not call options here
                elif images.quit_button.rect.collidepoint(pos):
                    constants.MENU_SONG_CHANNEL.stop()
                    return "quit"