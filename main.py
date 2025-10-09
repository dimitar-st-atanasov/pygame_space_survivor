# main.py
import sys
import pygame
import time
import random
from pygame.locals import *

import constants
import utils
from assets import sounds, images
from menus.start_menu import show_start_menu
from menus.options_menu import show_options_menu

pygame.display.set_caption(constants.GAME_NAME)


def run_game():
    """Main outer loop for menus."""
    while True:
        action = show_start_menu()
        if action == "play":
            game_loop()
        elif action == "options":
            show_options_menu()  # ignore "back" here, loop again to show start menu
        elif action == "quit":
            pygame.quit()
            sys.exit()


def game_loop():
    """Actual game logic loop."""
    # --- GAME INITIALIZATION ---
    player = pygame.Rect(480, constants.HEIGHT - constants.SPACESHIP_HEIGHT - 5,
                         constants.SPACESHIP_WIDTH, constants.SPACESHIP_HEIGHT)
    clock = pygame.time.Clock()
    start_time = time.time()
    paused_time = 0

    asteroid_count = 0
    missile_count = 0
    asteroid_add_increment = 3000
    missile_add_increment = 2000
    min_distance = constants.MISSILE_WIDTH * 2

    lasers = []
    asteroids = []
    missiles = []
    extra_points = []
    extra_life_hearts = []
    life_hearts = 3
    last_minute = 0
    last_shot_time = 0
    last_crash_time = 0
    current_hit_time = 0
    combo_missile_destroyed = 0
    hit = False
    helper = False
    activate_asteroids = False
    shield_enabled = False
    extra_life_heart_enabled = False
    last_minute_increment = 1

    run = True

    while run:
        dt = clock.tick(60)
        missile_count += dt
        asteroid_count += dt
        elapsed_time = time.time() - start_time - paused_time

        # --- handle minutes / extra lives ---
        current_minute = int(elapsed_time // 60)
        if current_minute > last_minute:
            if life_hearts < 5:
                life_hearts += 1
            activate_asteroids = True
            last_minute = current_minute

        # --- spawn asteroids / missiles ---
        if activate_asteroids and asteroid_count > asteroid_add_increment:
            utils.spawn_asteroids(asteroids, missiles, min_distance)
            asteroid_count = 0
        if missile_count > missile_add_increment:
            utils.spawn_missiles(asteroids, missiles, min_distance)
            missile_add_increment = max(250, missile_add_increment - 30)
            missile_count = 0

        # --- handle input ---
        keys = pygame.key.get_pressed()
        if keys[K_LEFT] and player.x - constants.PLAYER_VEL - 5 >= 0:
            player.x -= constants.PLAYER_VEL
        if keys[K_RIGHT] and player.x + constants.PLAYER_VEL + player.width + 5 <= constants.WIDTH:
            player.x += constants.PLAYER_VEL
        if keys[K_UP] and player.y - constants.PLAYER_VEL - 65 >= 0:
            player.y -= constants.PLAYER_VEL
        if keys[K_DOWN] and player.y + constants.PLAYER_VEL + player.height + 5 <= constants.HEIGHT:
            player.y += constants.PLAYER_VEL
        if keys[K_SPACE]:
            current_time = time.time()
            if not helper and ((len(lasers) <= 0 and current_time - last_shot_time >= 0.4) or current_time - last_shot_time >= 0.7):
                laser = pygame.Rect(player.x + constants.SPACESHIP_WIDTH // 2 - constants.LASER_WIDTH // 2,
                                    player.y, constants.LASER_WIDTH, constants.LASER_HEIGHT)
                constants.SHOOT_SINGLE_CHANNEL.play(sounds.shoot_single)
                lasers.append(laser)
                last_shot_time = current_time
            if helper and ((len(lasers) <= 1 and current_time - last_shot_time >= 0.4) or current_time - last_shot_time >= 0.7):
                laser1 = pygame.Rect(player.x + constants.SPACESHIP_WIDTH // 2 - constants.LASER_WIDTH // 2 - 7,
                                     player.y, constants.LASER_WIDTH, constants.LASER_HEIGHT)
                lasers.append(laser1)
                laser2 = pygame.Rect(player.x + constants.SPACESHIP_WIDTH // 2 - constants.LASER_WIDTH // 2 + 7,
                                     player.y, constants.LASER_WIDTH, constants.LASER_HEIGHT)
                constants.SHOOT_DOUBLE_CHANNEL.play(sounds.shoot_double)
                lasers.append(laser2)
                last_shot_time = current_time

        # --- Pause handling ---
        if keys[K_ESCAPE] or keys[K_p]:
            pause_start = time.time()
            while True:
                action = utils.pause_game(
                    player, elapsed_time, asteroids, missiles, lasers,
                    life_hearts, hit, combo_missile_destroyed,
                    shield_enabled, extra_life_hearts
                )

                if action == "resume":
                    break
                elif action == "options":
                    opt_action = show_options_menu()
                    if opt_action == "back":
                        continue # FIXME This doesn't work
                elif action == "quit":
                    run = False
                    break

            paused_time += time.time() - pause_start

        # --- update game state ---
        asteroids, life_hearts, shield_enabled, hit, combo_missile_destroyed, last_crash_time = \
            utils.update_asteroids(asteroids, player, life_hearts, shield_enabled,
                                   hit, combo_missile_destroyed, last_crash_time,
                                   extra_points, last_minute)
        missiles, life_hearts, shield_enabled, hit, combo_missile_destroyed, last_crash_time, last_minute_increment = \
            utils.update_missiles(missiles, player, life_hearts, shield_enabled,
                                  hit, combo_missile_destroyed, last_crash_time,
                                  extra_points, last_minute, current_minute, last_minute_increment)

        if hit and time.time() - current_hit_time >= 0.5:
            hit = False

        lasers = utils.update_lasers_position(lasers)
        lasers, asteroids, combo_missile_destroyed, helper, shield_enabled = \
            utils.handle_laser_asteroid_collisions(lasers, asteroids, combo_missile_destroyed, helper, shield_enabled)
        lasers, missiles, combo_missile_destroyed, helper, shield_enabled, extra_life_heart_enabled = \
            utils.handle_laser_missile_collisions(lasers, missiles, combo_missile_destroyed, helper,
                                                  shield_enabled, extra_life_heart_enabled, extra_points, last_minute)

        # --- handle extra life hearts ---
        if extra_life_heart_enabled:
            extra_life_heart_x = random.randint(0, constants.WIDTH - constants.LIFE_HEART_WIDTH)
            extra_life_heart = pygame.Rect(extra_life_heart_x, 60, constants.LIFE_HEART_WIDTH, constants.LIFE_HEART_HEIGHT)
            extra_life_hearts.append(extra_life_heart)
            extra_life_heart_enabled = False

        for heart in extra_life_hearts[:]:
            heart.y += constants.EXTRA_LIFE_HEART_VEL
            if heart.y > constants.HEIGHT:
                extra_life_hearts.remove(heart)
                continue
            if player.colliderect(heart):
                extra_life_hearts.remove(heart)
                constants.COLLECT_HEART_CHANNEL.play(sounds.collect_heart)
                if life_hearts < 5:
                    life_hearts += 1
                extra_points.append("100")

        # --- Game Over ---
        if life_hearts == 0:
            utils.game_over_animation(player, elapsed_time, extra_points)
            action = utils.handle_game_over_input()
            if action == "restart":
                return
            elif action == "quit":
                run = False

        # --- handle quit event ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # --- draw frame ---
        utils.draw(player, elapsed_time, asteroids, missiles, lasers,
                   life_hearts, hit, combo_missile_destroyed, shield_enabled, extra_life_hearts)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    run_game()
