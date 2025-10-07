import pygame
import time
import random
from pygame.locals import *

import constants
import utils
from assets import sounds
from menus.start_menu import show_start_menu

pygame.display.set_caption(constants.GAME_NAME)

def main():

    run = True
    
    show_start_menu()

    player = pygame.Rect(480, constants.HEIGHT - constants.SPACESHIP_HEIGHT - 5, constants.SPACESHIP_WIDTH, constants.SPACESHIP_HEIGHT)
    clock = pygame.time.Clock()

    # FIXME The time to show minutes and seconds. Not only seconds
    start_time = time.time()
    elapsed_time = 0
    paused_time = 0

    asteroid_count = 0
    asteroid_add_increment = 3000 # Respawn time gap of falling asteroids
    missile_add_increment = 2000 # Starting respawn time gap of falling missiles
    missile_count = 0
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

    while run:
        dt = clock.tick(60)   # milliseconds since last frame
        missile_count += dt
        asteroid_count += dt
        elapsed_time = time.time() - start_time - paused_time

        # Earn extra lifes
        current_minute = int(elapsed_time // 60)  # Convert elapsed time to full minutes
        if current_minute > last_minute:
            if life_hearts < 5:
                life_hearts += 1
                activate_asteroids = True
            last_minute = current_minute

        if activate_asteroids and asteroid_count > asteroid_add_increment:
            utils.spawn_asteroids(asteroids, missiles, min_distance)
            asteroid_count = 0

        if missile_count > missile_add_increment:
            utils.spawn_missiles(asteroids, missiles, min_distance)
            missile_add_increment = max(250, missile_add_increment - 30)
            missile_count = 0

        # MOVE player - left, right, up and down
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x - constants.PLAYER_VEL - 5 >= 0:
            player.x -= constants.PLAYER_VEL
        if keys[pygame.K_RIGHT] and player.x + constants.PLAYER_VEL + player.width + 5 <= constants.WIDTH:
            player.x += constants.PLAYER_VEL
        if keys[pygame.K_UP] and player.y - constants.PLAYER_VEL - 65 >= 0:
            player.y -= constants.PLAYER_VEL
        if keys[pygame.K_DOWN] and player.y + constants.PLAYER_VEL + player.height + 5 <= constants.HEIGHT:
            player.y += constants.PLAYER_VEL
        if keys[pygame.K_SPACE]:
            current_time = time.time()
            if helper == False and ((len(lasers) <= 0 and current_time - last_shot_time >= 0.4) or current_time - last_shot_time >= 0.7):
                laser = pygame.Rect(player.x + constants.SPACESHIP_WIDTH // 2 - constants.LASER_WIDTH // 2, player.y, constants.LASER_WIDTH, constants.LASER_HEIGHT)
                constants.SHOOT_SINGLE_CHANNEL.play(sounds.shoot_single)
                lasers.append(laser)
                last_shot_time = current_time
            if helper and ((len(lasers) <= 1 and current_time - last_shot_time >= 0.4) or current_time - last_shot_time >= 0.7):
                laser1 = pygame.Rect(player.x + constants.SPACESHIP_WIDTH // 2 - constants.LASER_WIDTH // 2 - 7, player.y, constants.LASER_WIDTH, constants.LASER_HEIGHT)
                lasers.append(laser1)
                laser2 = pygame.Rect(player.x + constants.SPACESHIP_WIDTH // 2 - constants.LASER_WIDTH // 2 + 7, player.y, constants.LASER_WIDTH, constants.LASER_HEIGHT)
                constants.SHOOT_DOUBLE_CHANNEL.play(sounds.shoot_double)
                lasers.append(laser2)
                last_shot_time = current_time
        if keys[pygame.K_ESCAPE] or keys[pygame.K_p]:
            paused_duration = utils.pause_game(player, elapsed_time, asteroids, missiles, lasers, life_hearts, hit, combo_missile_destroyed, shield_enabled, extra_life_hearts)
            paused_time += paused_duration
        
        # Update asteroids and missiles
        asteroids, life_hearts, shield_enabled, hit, combo_missile_destroyed, last_crash_time = \
            utils.update_asteroids(asteroids, player, life_hearts, shield_enabled, hit, combo_missile_destroyed, last_crash_time, extra_points, last_minute)

        missiles, life_hearts, shield_enabled, hit, combo_missile_destroyed, last_crash_time, last_minute_increment = \
            utils.update_missiles(missiles, player, life_hearts, shield_enabled, hit, combo_missile_destroyed, last_crash_time, extra_points, last_minute, current_minute, last_minute_increment)

        if hit:
            if time.time() - current_hit_time >= 0.5:  # remove hit image after half a second after a hit
                hit = False
        
        # Generate shooting laser and remove lasers and asteroid/missile if hit
        lasers = utils.update_lasers_position(lasers)

        lasers, asteroids, combo_missile_destroyed, helper, shield_enabled = \
            utils.handle_laser_asteroid_collisions(lasers, asteroids, combo_missile_destroyed, helper, shield_enabled)

        lasers, missiles, combo_missile_destroyed, helper, shield_enabled, extra_life_heart_enabled = \
            utils.handle_laser_missile_collisions(lasers, missiles, combo_missile_destroyed, helper, shield_enabled, extra_life_heart_enabled, extra_points, last_minute)

        if extra_life_heart_enabled:
            extra_life_heart_x = random.randint(0, constants.WIDTH - constants.LIFE_HEART_WIDTH)
            extra_life_heart = pygame.Rect(extra_life_heart_x, 60, constants.LIFE_HEART_WIDTH, constants.LIFE_HEART_HEIGHT)
            extra_life_hearts.append(extra_life_heart)

        for extra_life_heart in extra_life_hearts[:]:
            extra_life_heart.y += constants.EXTRA_LIFE_HEART_VEL
            if extra_life_heart.y > constants.HEIGHT:
                extra_life_hearts.remove(extra_life_heart)
            if extra_life_heart.x + extra_life_heart.width > constants.WIDTH:
                extra_life_heart.x = constants.WIDTH - extra_life_heart.width
            if player.colliderect(extra_life_heart):
                extra_life_hearts.remove(extra_life_heart)
                constants.COLLECT_HEART_CHANNEL.play(sounds.collect_heart)
                if life_hearts < 5:
                    life_hearts += 1
                extra_points.append("100")
            extra_life_heart_enabled = False

        # Game Over
        if life_hearts == 0:
            utils.game_over_animation(player, elapsed_time, extra_points)
            action = utils.handle_game_over_input()

            if action == "restart":
                main()
            elif action == "quit":
                run = False

        # Exit game with "x" icon
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        utils.draw(player, elapsed_time, asteroids, missiles, lasers, life_hearts, hit, combo_missile_destroyed, shield_enabled, extra_life_hearts)

    pygame.quit()

if __name__ == "__main__":
    main()