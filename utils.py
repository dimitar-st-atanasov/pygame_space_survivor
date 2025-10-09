import pygame
import random
import time

import constants
from assets import images, sounds, texts


def draw(player, elapsed_time, asteroids, missiles, lasers, life_hearts, hit, combo_missile_destroyed, shield_enabled, extra_life_hearts):

    # Render and display background
    constants.WIN.blit(constants.BG, (0, constants.TOOLBAR.get_height()))

    # Render and display the falling missiles
    for missile in missiles:
        constants.WIN.blit(constants.MISSILE, (missile.x, missile.y))
        # pygame.draw.rect(constants.WIN, (255, 0, 0), missile, 2) # for debugging

    # Render and display the falling asteroids
    for asteroid in asteroids:
        rect, hp = asteroid
        constants.WIN.blit(constants.ASTEROID, (rect.x, rect.y))
        # pygame.draw.rect(constants.WIN, (255, 0, 0),asteroid, 2) # for debugging

    # Render and display toolbar
    constants.WIN.blit(constants.TOOLBAR, (0, 0))

    # Render and display destroyed missiles number
    if combo_missile_destroyed < 15:
        show_destroyed_missiles_number_text = constants.FONT.render(f"{combo_missile_destroyed}", 1, "white")
    elif combo_missile_destroyed >= 15 and combo_missile_destroyed < 30:
        show_destroyed_missiles_number_text = constants.FONT.render(f"{combo_missile_destroyed}", 1, "yellow")
    elif combo_missile_destroyed >= 30 and combo_missile_destroyed < 50:
        show_destroyed_missiles_number_text = constants.FONT.render(f"{combo_missile_destroyed}", 1, "light blue")
    elif combo_missile_destroyed >= 50:
        show_destroyed_missiles_number_text = constants.FONT.render(f"{combo_missile_destroyed}", 1, "green")   
    
    show_destroyed_missiles_text = constants.FONT.render(f"Combo:", 1, "white")
    constants.WIN.blit(show_destroyed_missiles_text, (810, 15))
    constants.WIN.blit(show_destroyed_missiles_number_text, (900, 15))

    # Render and display life hearts
    for i in range(life_hearts):
        constants.WIN.blit(constants.LIFE_HEART, (23 + i * 40, 13))

    # Render and display elapsed time
    time_text = constants.FONT.render(f"Time: {round(elapsed_time)}s", 1, "white")
    constants.WIN.blit(time_text, (450, 8))

    # Render and display the shooting laser
    for laser in lasers:
        pygame.draw.rect(constants.WIN, "white", laser)

    # Render and display hit
    if hit:
        constants.WIN.blit(constants.HIT, (player.x, player.y - 30))
    
    # Render and display spaceship at the player's position
    constants.WIN.blit(constants.SPACESHIP, (player.x, player.y))
    # pygame.draw.rect(constants.WIN, (255, 0, 0), player, 2) # for debugging

    if shield_enabled:
        constants.WIN.blit(constants.SHIELD, (player.x, player.y))

    for extra_life_heart in extra_life_hearts:
        if life_hearts < 5:
            constants.WIN.blit(constants.LIFE_HEART, (extra_life_heart.x, extra_life_heart.y))
            constants.WIN.blit(constants.SHIELD, (extra_life_heart.x - 4, extra_life_heart.y - 8))
        else:
            hundred_points_text = constants.FONT.render("100", 1, "white")
            text_rect = hundred_points_text.get_rect()
            text_rect.topleft = (extra_life_heart.x, extra_life_heart.y)
            constants.WIN.blit(hundred_points_text, text_rect.topleft)
            constants.WIN.blit(constants.SHIELD_HUNDRED_POINTS, (extra_life_heart.x - 5, extra_life_heart.y - 6))

    pygame.display.update()


def draw_last_hit(player, elapsed_time):
    '''Draw last hit when shoconstants.WINg "Game over" text.'''

    constants.WIN.blit(constants.TOOLBAR, (0, 0))
    constants.WIN.blit(constants.BG, (0, 61))

    time_text = constants.FONT.render(f"Time: {round(elapsed_time)}s", 1, "white")
    constants.WIN.blit(time_text, (450, 8))

    constants.WIN.blit(constants.HIT, (player.x, player.y - 20))
    constants.WIN.blit(constants.SPACESHIP, (player.x, player.y))

    pygame.display.update()


def count_destroyed_missiles(last_minute, extra_points):

    if last_minute <= 1:
        extra_points.append("1")
    elif last_minute >= 2 and last_minute <= 4:
        extra_points.append("10")
    elif last_minute >= 5:
        extra_points.append("25")


def spawn_missiles(asteroids, missiles, min_distance):

    for _ in range(3): # spawn three missiles
        for _ in range(100): # attempts
            missile_x = random.randint(0, constants.WIDTH - constants.MISSILE_WIDTH)

            # Check spacing from existing missiles
            if all(abs(missile_x - m.x) >= min_distance for m in missiles):
                # Check vertical + horizontal space for asteroids
                safe_to_spawn = True
                for a in asteroids:
                    rect, hp = a
                    if rect.y + rect.height > -constants.MISSILE_HEIGHT and \
                    (missile_x + constants.MISSILE_WIDTH > rect.x and missile_x < rect.x + constants.ASTEROID_WIDTH):
                        safe_to_spawn = False
                        break

                if safe_to_spawn:
                    missile = pygame.Rect(missile_x, -constants.MISSILE_HEIGHT, constants.MISSILE_WIDTH, constants.MISSILE_HEIGHT)
                    missiles.append(missile)
                    break
    
    return missiles


def spawn_asteroids(asteroids, missiles, min_distance):
    if len(asteroids) < 2:
        for _ in range(100):
            asteroid_x = random.randint(0, constants.WIDTH - constants.ASTEROID_WIDTH)

            # check spacing from existing asteroids + missiles
            if all(abs(asteroid_x - a[0].x) >= min_distance for a in asteroids) and \
            all(abs(asteroid_x - m.x) >= min_distance for m in missiles):
                asteroid = [pygame.Rect(asteroid_x, -constants.ASTEROID_HEIGHT, constants.ASTEROID_WIDTH, constants.ASTEROID_HEIGHT), 10]
                asteroids.append(asteroid)
                break

    return asteroids


def update_asteroids(asteroids, player, life_hearts, shield_enabled, hit, combo_missile_destroyed, last_crash_time, extra_points, last_minute):
    """Update asteroid positions and handle collisions with the player."""
    for asteroid in asteroids[:]:
        rect, hp = asteroid
        rect.y += constants.ASTEROID_VEL  # move down

        # remove if it goes off screen
        if rect.y > constants.HEIGHT:
            asteroids.remove(asteroid)
            continue

        # collision with player
        if rect.colliderect(player):
            current_crash_time = time.time()
            if current_crash_time - last_crash_time >= 1.5:
                if shield_enabled:
                    shield_enabled = False
                    constants.DEACTIVATE_SHIELD_CHANNEL.play(sounds.deactivate_shield)
                else:
                    constants.GETTING_HIT_CHANNEL.play(sounds.getting_hit)
                    life_hearts -= 1
                    hit = True
                combo_missile_destroyed = 0
                count_destroyed_missiles(last_minute, extra_points)
                last_crash_time = current_crash_time
    return asteroids, life_hearts, shield_enabled, hit, combo_missile_destroyed, last_crash_time


def update_missiles(missiles, player, life_hearts, shield_enabled, hit, combo_missile_destroyed, last_crash_time, extra_points, last_minute, current_minute, last_minute_increment):
    """Update missile positions and handle collisions with the player."""
    for missile in missiles[:]:
        if current_minute > last_minute_increment:
            constants.MISSILE_VEL += 1
            last_minute_increment = current_minute

        missile.y += constants.MISSILE_VEL

        if missile.y > constants.HEIGHT:
            missiles.remove(missile)
        elif missile.x + missile.width > constants.WIDTH:
            missile.x = constants.WIDTH - missile.width
        elif missile.y + missile.height >= player.y and missile.colliderect(player):
            current_crash_time = time.time()
            if current_crash_time - last_crash_time >= 1.5:
                if shield_enabled:
                    shield_enabled = False
                    constants.DEACTIVATE_SHIELD_CHANNEL.play(sounds.deactivate_shield)
                else:
                    constants.GETTING_HIT_CHANNEL.play(sounds.getting_hit)
                    life_hearts -= 1
                    hit = True
                missiles.remove(missile)
                combo_missile_destroyed = 1
                count_destroyed_missiles(last_minute, extra_points)
                last_crash_time = current_crash_time
                break

    return missiles, life_hearts, shield_enabled, hit, combo_missile_destroyed, last_crash_time, last_minute_increment


def update_lasers_position(lasers):
    """Move lasers upward and remove if off-screen."""
    for laser in lasers[:]:
        laser.y -= constants.LASER_VEL
        if laser.y <= 60:
            try:
                lasers.remove(laser)
            except ValueError:
                pass
    return lasers


def handle_laser_asteroid_collisions(lasers, asteroids, combo_missile_destroyed, helper, shield_enabled):
    """Handle collisions between lasers and asteroids."""
    for laser in lasers[:]:
        for asteroid in asteroids[:]:
            rect, hp = asteroid
            if laser.colliderect(rect):
                asteroid[1] -= 1

                if laser in lasers:
                    lasers.remove(laser)

                constants.DESTROY_ASTEROID_CHANNEL.play(sounds.destroy_missile)

                if asteroid[1] <= 0:
                    asteroids.remove(asteroid)
                    combo_missile_destroyed += 3

                # Optional: update combo, shield, helper
                if combo_missile_destroyed == 15 and not helper:
                    constants.UPGRADE_CHANNEL.play(sounds.upgrade)
                if combo_missile_destroyed >= 15:
                    helper = True
                if combo_missile_destroyed >= 30 and not shield_enabled:
                    shield_enabled = True
                    constants.ACTIVATE_SHIELD_CHANNEL.play(sounds.activate_shield)

                break
    return lasers, asteroids, combo_missile_destroyed, helper, shield_enabled


def handle_laser_missile_collisions(lasers, missiles, combo_missile_destroyed, helper, shield_enabled, extra_life_heart_enabled, extra_points, last_minute):
    """Handle collisions between lasers and missiles."""
    for laser in lasers[:]:
        for missile in missiles[:]:
            if laser.colliderect(missile):
                count_destroyed_missiles(last_minute, extra_points)
                try:
                    missiles.remove(missile)
                    constants.DESTROY_MISSILE_CHANNEL.play(sounds.destroy_missile)
                    combo_missile_destroyed += 1

                    if combo_missile_destroyed == 15 and not helper:
                        constants.UPGRADE_CHANNEL.play(sounds.upgrade)
                    if combo_missile_destroyed >= 15:
                        helper = True
                    if combo_missile_destroyed >= 30 and not shield_enabled:
                        shield_enabled = True
                        constants.ACTIVATE_SHIELD_CHANNEL.play(sounds.activate_shield)
                    if combo_missile_destroyed % 50 == 0 and combo_missile_destroyed > 0:
                        extra_life_heart_enabled = True
                        constants.GENERATE_HEART_CHANNEL.play(sounds.generate_heart)

                except ValueError:
                    pass

                if laser in lasers:
                    try:
                        lasers.remove(laser)
                    except ValueError:
                        pass
                break
    return lasers, missiles, combo_missile_destroyed, helper, shield_enabled, extra_life_heart_enabled


def pause_game(player, elapsed_time, asteroids, missiles, lasers,
               life_hearts, hit, combo_missile_destroyed,
               shield_enabled, extra_life_hearts):
    """
    Pauses the game and shows a pause menu with Resume, Options, and Quit.
    Returns one of: "resume", "options", "quit".
    """
    constants.MENU_SONG_CHANNEL.play(sounds.menu_song, loops=-1)
    paused = True

    while paused:
        constants.WIN.blit(constants.BG, (0, 61))
        constants.WIN.blit(constants.TOOLBAR, (0, 0))
        draw(player, elapsed_time, asteroids, missiles, lasers,
             life_hearts, hit, combo_missile_destroyed,
             shield_enabled, extra_life_hearts)

        resume_clicked = images.resume_button.draw(constants.WIN)
        options_clicked = images.options_button.draw(constants.WIN)
        quit_clicked = images.quit_button.draw(constants.WIN)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return "quit"

        # --- Handle button clicks ---
        if resume_clicked:
            constants.MENU_SONG_CHANNEL.stop()
            # 3-2-1 countdown before resuming
            for _, text in zip(range(3, 0, -1),
                               [texts.three_text, texts.two_text, texts.one_text]):
                constants.COUNTDOWN_CHANNEL.play(sounds.countdown)
                constants.WIN.blit(constants.BG, (0, 61))
                constants.WIN.blit(constants.TOOLBAR, (0, 0))
                draw(player, elapsed_time, asteroids, missiles, lasers,
                     life_hearts, hit, combo_missile_destroyed,
                     shield_enabled, extra_life_hearts)
                constants.WIN.blit(
                    text,
                    (constants.WIDTH / 2 - text.get_width() / 2,
                     constants.HEIGHT / 2 - text.get_height() / 2)
                )
                pygame.display.update()
                pygame.time.delay(1000)

            return "resume"

        elif options_clicked:
            constants.MENU_SONG_CHANNEL.stop()
            return "options"

        elif quit_clicked:
            constants.MENU_SONG_CHANNEL.stop()
            return "quit"

        pygame.time.delay(50)


def game_over_animation(player, elapsed_time, extra_points):
    """
    Handles drawing the game over sequence, counting extra points,
    and displaying the rising total points animation.
    Returns the total points.
    """
    total_extra_points = 0

    pygame.time.delay(100)
    # Draw last hit
    draw_last_hit(player, elapsed_time)

    # Show lost text
    constants.WIN.blit(
        texts.lost_text,
        (constants.WIDTH / 2 - texts.lost_text.get_width() / 2,
         constants.HEIGHT / 2 - texts.lost_text.get_height() / 2)
    )
    pygame.display.update()

    # Play game over sound
    constants.GAME_OVER_CHANNEL.play(sounds.game_over)
    pygame.time.delay(5000)

    # Add extra points
    for point in extra_points:
        total_extra_points += int(point)

    # Animate points counting
    for _ in range(int(elapsed_time)):
        constants.WIN.blit(constants.TOOLBAR, (0, 0))
        constants.WIN.blit(constants.BG, (0, 61))
        total_extra_points += 1
        total_points_text = constants.FONT.render(f"Total points: {total_extra_points}", 1, "white")
        constants.WIN.blit(
            total_points_text,
            (constants.WIDTH / 2 - len(str(total_extra_points)) * 10 - texts.points_text.get_width() / 2,
             constants.HEIGHT / 2 - texts.points_text.get_height() / 2)
        )
        constants.COLLECT_POINTS_CHANNEL.play(sounds.collect_points)
        pygame.display.update()
        pygame.time.delay(10)

    # Rising text animation
    up_rising = 0
    for _ in range(100):
        up_rising += 1
        total_points_text = constants.FONT.render(f"Total points: {total_extra_points}", 1, "white")
        constants.WIN.blit(constants.TOOLBAR, (0, 0))
        constants.WIN.blit(constants.BG, (0, 61))
        constants.WIN.blit(
            total_points_text,
            (constants.WIDTH / 2 - len(str(total_extra_points)) * 10 - texts.points_text.get_width() / 2,
             constants.HEIGHT / 2 - texts.points_text.get_height() / 2 - up_rising)
        )
        constants.WIN.blit(
            texts.play_again_text,
            (constants.WIDTH/2 - texts.play_again_text.get_width()/2,
             constants.HEIGHT/2 - texts.play_again_text.get_height()/2 + 80 - up_rising)
        )
        constants.WIN.blit(
            texts.yes_text,
            (constants.WIDTH/2 - texts.yes_text.get_width()/2,
             constants.HEIGHT/2 - texts.yes_text.get_height()/2 + 140 - up_rising)
        )
        constants.WIN.blit(
            texts.no_text,
            (constants.WIDTH/2 - texts.no_text.get_width()/2,
             constants.HEIGHT/2 - texts.no_text.get_height()/2 + 180 - up_rising)
        )
        pygame.display.update()

    # Play menu song after animation
    constants.MENU_SONG_CHANNEL.play(sounds.menu_song, loops=-1)


def handle_game_over_input():
    """
    Waits for player input after game over.
    Returns:
        "restart" → player pressed Enter
        "quit"    → player pressed ESC or closed window
    """
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return "restart"
                elif event.key == pygame.K_ESCAPE:
                    return "quit"