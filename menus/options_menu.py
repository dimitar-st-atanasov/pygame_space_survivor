import pygame
import constants
from assets import images, sounds

# Global toggles for audio and music
audio_enabled = True
music_enabled = True

def show_options_menu():
    """Display the options menu and handle user input."""
    global audio_enabled, music_enabled

    options_menu = True

    while options_menu:
        # Draw background and UI
        constants.WIN.blit(constants.TOOLBAR, (0, 0))
        constants.WIN.blit(constants.BG, (0, 61))

        # Draw buttons depending on toggle states
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

        # Event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            # --- Audio toggle ---
            if audio_enabled and images.audio_button.draw(constants.WIN):
                _disable_audio()
                audio_enabled = False

            elif not audio_enabled and images.red_audio_button.draw(constants.WIN):
                _enable_audio()
                audio_enabled = True

            # --- Music toggle ---
            if music_enabled and images.music_button.draw(constants.WIN):
                sounds.menu_song.set_volume(0.0)
                music_enabled = False

            elif not music_enabled and images.red_music_button.draw(constants.WIN):
                sounds.menu_song.set_volume(0.3)
                music_enabled = True

            # --- Back button ---
            if images.back_button.draw(constants.WIN):
                options_menu = False


# --- Helper functions ---

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
    sounds.set_default_volumes()
