import pygame
import constants
from assets import images, sounds

audio_enabled = True
music_enabled = True

def show_options_menu():
    """Display the options menu and handle user input."""
    global audio_enabled, music_enabled
    pygame.event.clear()

    options_menu = True

    while options_menu:
        # --- Draw background and UI ---
        constants.WIN.blit(constants.TOOLBAR, (0, 0))
        constants.WIN.blit(constants.BG, (0, 61))

        # Draw buttons for visuals (no return value needed)
        if audio_enabled:
            images.audio_button.draw(constants.WIN)
        else:
            images.red_audio_button.draw(constants.WIN)

        if music_enabled:
            images.music_button.draw(constants.WIN)
        else:
            images.red_music_button.draw(constants.WIN)

        images.back_button.draw(constants.WIN)

        pygame.display.update()

        # --- Event handling ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()

                # Use the button's rect for collision
                if audio_enabled and images.audio_button.rect.collidepoint(mouse_pos):
                    audio_enabled = False
                    _disable_audio()
                elif not audio_enabled and images.red_audio_button.rect.collidepoint(mouse_pos):
                    audio_enabled = True
                    _enable_audio()

                if music_enabled and images.music_button.rect.collidepoint(mouse_pos):
                    music_enabled = False
                    _disable_music()
                elif not music_enabled and images.red_music_button.rect.collidepoint(mouse_pos):
                    music_enabled = True
                    _enable_music()

                if images.back_button.rect.collidepoint(mouse_pos):
                    return "back"



def _disable_audio():
    """Mute all sound effects."""
    for snd in [
        sounds.shoot_single,
        sounds.shoot_double,
        sounds.destroy_missile,
        sounds.getting_hit,
        sounds.collect_heart,
        sounds.activate_shield,
        sounds.deactivate_shield,
        sounds.countdown,
        sounds.collect_points,
        sounds.game_over,
        sounds.upgrade,
        sounds.generate_heart,
    ]:
        snd.set_volume(0.0)

def _enable_audio():
    """Restore sound effect volumes to defaults."""
    sounds.set_default_audio_volumes()

def _disable_music():
    """Mute background music."""
    sounds.menu_song.set_volume(0.0)

def _enable_music():
    """Restore music volumes to defaults."""
    sounds.set_default_music_volumes()