import pygame
import time
import random
pygame.font.init()

# Screen dimensions
WIDTH, HEIGHT = 1000, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Survivor")

# Load and scale background and toolbar
BG = pygame.transform.scale(pygame.image.load("resources/images/space_background.jpg"), (WIDTH, HEIGHT - 60))
TOOLBAR = pygame.transform.scale(pygame.image.load("resources/images/toolbar.png"), (WIDTH, HEIGHT - 740))

LIVE_HEART_WIDTH = 30
LIVE_HEART_HEIGHT = 35
LIVE_HEART = pygame.transform.scale(pygame.image.load("resources/images/lives.png"), (LIVE_HEART_WIDTH, LIVE_HEART_HEIGHT))

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

PLAYER_VEL = 5
MISSILE_VEL = 5
LASER_VEL = 10
EXTRA_LIVE_HEART_VEL = 3

MISSILE_WIDTH = 20
MISSILE_HEIGHT = 45
MISSILE = pygame.transform.scale(pygame.image.load("resources/images/missile.png"), (MISSILE_WIDTH, MISSILE_HEIGHT))

LASER_WIDTH = 2
LASER_HEIGHT = 20

# Font for rendering text
FONT = pygame.font.SysFont("comicsans", 25)

lost_text = FONT.render("Game over!", 1, "white")
points_text = FONT.render("Total points: ", 1, "white")
play_again_text = FONT.render("Play again?", 1, "white")
yes_text = FONT.render("Yes -> Press Enter", 1, "white")
no_text = FONT.render("No -> Press Esc", 1, "white")
pause_text = FONT.render("Pause - Press 'P' again or ESCAPE to resume game", 1, "white")
one_text = FONT.render("1", 1, "white")
two_text = FONT.render("2", 1, "white")
three_text = FONT.render("3", 1, "white")

def draw(player, elapsed_time, missiles, lasers, live_hearts, hit, combo_missile_destroyed, shield_enabled, extra_live_hearts):

    # Render and display background and toolbar
    WIN.blit(TOOLBAR, (0, 0))
    WIN.blit(BG, (0, 61))

    # Render and display destroyed missiles number
    if combo_missile_destroyed < 15:
        show_destroyed_missiles_number_text = FONT.render(f"{combo_missile_destroyed}", 1, "white")
    elif combo_missile_destroyed >= 15 and combo_missile_destroyed < 30:
        show_destroyed_missiles_number_text = FONT.render(f"{combo_missile_destroyed}", 1, "yellow")
    elif combo_missile_destroyed >= 30 and combo_missile_destroyed < 50:
        show_destroyed_missiles_number_text = FONT.render(f"{combo_missile_destroyed}", 1, "light blue")
    elif combo_missile_destroyed >= 50:
        show_destroyed_missiles_number_text = FONT.render(f"{combo_missile_destroyed}", 1, "green")   
    
    show_destroyed_missiles_text = FONT.render(f"Combo:", 1, "white")
    WIN.blit(show_destroyed_missiles_text, (830, 10))
    WIN.blit(show_destroyed_missiles_number_text, (920, 10))

    # Render and display live hearts
    for i in range(live_hearts):
        WIN.blit(LIVE_HEART, (23 + i * 40, 13))

    # Render and display elapsed time
    time_text = FONT.render(f"Time: {round(elapsed_time)}s", 1, "white")
    WIN.blit(time_text, (450, 8))

    # Render and display the falling missiles
    for missile in missiles:
        WIN.blit(MISSILE, (missile.x, missile.y))
        # pygame.draw.rect(WIN, (255, 0, 0), missile, 2) # for debugging

    # Render and display the shooting laser
    for laser in lasers:
        pygame.draw.rect(WIN, "white", laser)

    # Render and display hit
    if hit:
        WIN.blit(HIT, (player.x, player.y - 30))
    
    # Render and display spaceship at the player's position
    WIN.blit(SPACESHIP, (player.x, player.y))
    # pygame.draw.rect(WIN, (255, 0, 0), player, 2) # for debugging

    if shield_enabled:
        WIN.blit(SHIELD, (player.x, player.y))

    for extra_live_heart in extra_live_hearts:
        if live_hearts < 5:
            WIN.blit(LIVE_HEART, (extra_live_heart.x, extra_live_heart.y))
            WIN.blit(SHIELD, (extra_live_heart.x - 4, extra_live_heart.y - 8))
        else:
            hundred_points_text = FONT.render("100", 1, "white")
            text_rect = hundred_points_text.get_rect()
            text_rect.topleft = (extra_live_heart.x, extra_live_heart.y)
            WIN.blit(hundred_points_text, text_rect.topleft)
            WIN.blit(SHIELD_HUNDRED_POINTS, (extra_live_heart.x - 5, extra_live_heart.y - 6))

    pygame.display.update()


def draw_last_hit(player, elapsed_time, live_hearts, extra_points):
    '''Draw last hit when showing "Game over" text.'''

    WIN.blit(TOOLBAR, (0, 0))
    WIN.blit(BG, (0, 61))

    show_hits = FONT.render(f"Remaining lives:", 1, "white")
    WIN.blit(show_hits, (25, 8))

    for i in range(live_hearts):
        WIN.blit(LIVE_HEART, (210 + i * 40, 10))

    time_text = FONT.render(f"Time: {round(elapsed_time)}s", 1, "white")
    WIN.blit(time_text, (450, 8))

    show_destroyed_missiles = FONT.render(f"Destroyed missiles: {len(extra_points)}", 1, "white")
    WIN.blit(show_destroyed_missiles, (700, 8))

    WIN.blit(HIT, (player.x, player.y - 20))
    WIN.blit(SPACESHIP, (player.x, player.y))

    pygame.display.update()

def count_destroyed_missiles(last_minute, extra_points):
    if last_minute <= 1:
        extra_points.append("1")
    elif last_minute >= 2 and last_minute <= 4:
        extra_points.append("10")
    elif last_minute >= 5:
        extra_points.append("25")

def main():
    global MISSILE_VEL

    run = True

    player = pygame.Rect(480, HEIGHT - SPACESHIP_HEIGHT - 5, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    clock = pygame.time.Clock()

    # FIXME The time to show minutes and seconds. Not only seconds
    start_time = time.time()
    elapsed_time = 0
    paused_time = 0
    pause_start = None

    missile_add_increment = 2000 # Starting respawn time gap of falling missiles
    missile_count = 0

    lasers = []
    missiles = []
    live_hearts = 3
    last_minute = 0
    extra_points = []
    total_extra_points = 0

    last_shot_time = 0

    current_hit_time = 0
    hit = False
    helper = False
    combo_missile_destroyed = 0
    shield_enabled = False
    extra_live_heart_enabled = False
    extra_live_hearts = []

    last_minute_increment = 0

    while run:
        missile_count += clock.tick(60)
        elapsed_time = time.time() - start_time - paused_time

        # Earn extra lives
        current_minute = int(elapsed_time // 60)  # Convert elapsed time to full minutes
        if current_minute > last_minute:
            if live_hearts < 5:
                live_hearts += 1
            last_minute = current_minute

        if missile_count > missile_add_increment:
            for _ in range(3):
                missile_x = random.randint(0, WIDTH - MISSILE_WIDTH)
                if missile_x < 10:
                    missile_x = 10
                elif missile_x > 975:
                    missile_x = 975
                missile = pygame.Rect(missile_x, 60, MISSILE_WIDTH, MISSILE_HEIGHT)
                missiles.append(missile)

            missile_add_increment = max(250, missile_add_increment - 30)
            missile_count = 0

        pause = False

        # MOVE player - left, right, up and down
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x - PLAYER_VEL - 5 >= 0:
            player.x -= PLAYER_VEL
        if keys[pygame.K_RIGHT] and player.x + PLAYER_VEL + player.width + 5 <= WIDTH:
            player.x += PLAYER_VEL
        if keys[pygame.K_UP] and player.y - PLAYER_VEL - 65 >= 0:
            player.y -= PLAYER_VEL
        if keys[pygame.K_DOWN] and player.y + PLAYER_VEL + player.height + 5 <= HEIGHT:
            player.y += PLAYER_VEL
        if keys[pygame.K_SPACE]:
            current_time = time.time()
            if helper == False:
                if len(lasers) <= 0:
                    laser = pygame.Rect(player.x + SPACESHIP_WIDTH // 2 - LASER_WIDTH // 2, player.y, LASER_WIDTH, LASER_HEIGHT)
                    lasers.append(laser)
            if helper == True and int(current_time) - int(last_shot_time) >= 0.3:
                if len(lasers) <= 1:
                    laser1 = pygame.Rect(player.x + SPACESHIP_WIDTH // 2 - LASER_WIDTH // 2 - 7, player.y, LASER_WIDTH, LASER_HEIGHT)
                    lasers.append(laser1)
                    laser2 = pygame.Rect(player.x + SPACESHIP_WIDTH // 2 - LASER_WIDTH // 2 + 7, player.y, LASER_WIDTH, LASER_HEIGHT)
                    lasers.append(laser2)
                    last_shot_time = current_time
        if keys[pygame.K_ESCAPE] or keys[pygame.K_p]:
            pause = True

        # Pause/unpause the game with "P" or ESC key
        if pause:
            pause_start = time.time()
            WIN.blit(pause_text, (WIDTH / 2 - pause_text.get_width() / 2, HEIGHT / 2 - pause_text.get_height() / 2))
            pygame.display.update()
            while pause:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False
                        pause = False
                        break

                    if event.type == pygame.KEYDOWN and (event.key == pygame.K_p or event.key == pygame.K_ESCAPE):
                        pause = False
                        for _, text in zip(range(3, 0, -1), [three_text, two_text, one_text]):
                            WIN.blit(BG, (0, 61))
                            WIN.blit(TOOLBAR, (0, 0))
                            draw(player, elapsed_time, missiles, lasers, live_hearts, hit, combo_missile_destroyed, shield_enabled, extra_live_hearts)
                            
                            WIN.blit(text, (WIDTH / 2 - text.get_width() / 2, HEIGHT / 2 - text.get_height() / 2))
                            pygame.display.update()
                            pygame.time.delay(1000)
                        paused_time += time.time() - pause_start
                        break
        
        # Generate falling missiles and remove them if hit spaceship
        for missile in missiles[:]:
            if current_minute > last_minute_increment:
                MISSILE_VEL += 1
                last_minute_increment = current_minute
            missile.y += MISSILE_VEL
            if missile.y > HEIGHT:
                missiles.remove(missile)
            elif missile.x + missile.width > WIDTH:
                missile.x = WIDTH - missile.width
            elif missile.y + missile.height >= player.y and missile.colliderect(player):
                if shield_enabled:
                    shield_enabled = False
                else:
                    live_hearts -= 1
                    helper = False
                    hit = True
                    current_hit_time = time.time()
                missiles.remove(missile)
                combo_missile_destroyed = 1
                count_destroyed_missiles(last_minute, extra_points)
                break

        if hit:
            if time.time() - current_hit_time >= 0.5:  # remove hit image after half a second after a hit
                hit = False
        
        # Generate shooting laser and remove laser and missile if hit
        for laser in lasers[:]:
            laser.y -= LASER_VEL
            if laser.y <= 60:
                try:
                    lasers.remove(laser)
                except ValueError:
                    pass
                
            for missile in missiles[:]:
                if laser.colliderect(missile):
                    count_destroyed_missiles(last_minute, extra_points)
                    try:
                        missiles.remove(missile)
                        combo_missile_destroyed += 1
                        if combo_missile_destroyed >= 15:
                            helper = True
                        if combo_missile_destroyed >= 30:
                            shield_enabled = True
                        if combo_missile_destroyed % 50 == 0 and combo_missile_destroyed > 0:
                            extra_live_heart_enabled = True

                    except ValueError:
                        pass

                    if len(lasers) > 0:
                        try:
                            lasers.remove(laser)
                        except ValueError:
                            pass
                    break

        if extra_live_heart_enabled:
            extra_live_heart_x = random.randint(0, WIDTH - LIVE_HEART_WIDTH)
            extra_live_heart = pygame.Rect(extra_live_heart_x, 60, LIVE_HEART_WIDTH, LIVE_HEART_HEIGHT)
            extra_live_hearts.append(extra_live_heart)

        for extra_live_heart in extra_live_hearts[:]:
            extra_live_heart.y += EXTRA_LIVE_HEART_VEL
            if extra_live_heart.y > HEIGHT:
                extra_live_hearts.remove(extra_live_heart)
            if extra_live_heart.x + extra_live_heart.width > WIDTH:
                extra_live_heart.x = WIDTH - extra_live_heart.width
            if player.colliderect(extra_live_heart):
                extra_live_hearts.remove(extra_live_heart)
                if live_hearts < 5:
                    live_hearts += 1
                extra_points.append("100")
            extra_live_heart_enabled = False

        # Game Over
        if live_hearts == 0:
            draw_last_hit(player, elapsed_time, live_hearts, extra_points)
            WIN.blit(lost_text, (WIDTH/2 - lost_text.get_width()/2, HEIGHT/2 - lost_text.get_height()/2))
            pygame.display.update()
            pygame.time.delay(2500)

            for point in extra_points:
                total_extra_points += int(point)

            for _ in range(int(elapsed_time)):
                WIN.blit(TOOLBAR, (0, 0))
                WIN.blit(BG, (0, 61))
                total_extra_points += 1
                # To center the text according the length of the string text + total_extra_points
                total_points_text = FONT.render(f"Total points: {total_extra_points}", 1, "white")
                WIN.blit(total_points_text, (WIDTH / 2 - len(str(total_extra_points)) * 10 - points_text.get_width() / 2, HEIGHT / 2 - points_text.get_height() / 2))
                pygame.display.update()
                pygame.time.delay(10)

            # raise smoothly whole text with 100 pixels
            up_rising = 0
            for _ in range(100):
                up_rising += 1
                total_points_text = FONT.render(f"Total points: {total_extra_points}", 1, "white")
                WIN.blit(TOOLBAR, (0, 0))
                WIN.blit(BG, (0, 61))
                WIN.blit(total_points_text, (WIDTH / 2 - len(str(total_extra_points)) * 10 - points_text.get_width() / 2, HEIGHT / 2 - points_text.get_height() / 2 - up_rising))
                WIN.blit(play_again_text, (WIDTH/2 - play_again_text.get_width()/2, HEIGHT/2 - play_again_text.get_height()/2 + 80 - up_rising))
                WIN.blit(yes_text, (WIDTH/2 - yes_text.get_width()/2, HEIGHT/2 - yes_text.get_height()/2 + 140 - up_rising))
                WIN.blit(no_text, (WIDTH/2 - no_text.get_width()/2, HEIGHT/2 - no_text.get_height()/2 + 180 - up_rising))
                pygame.display.update()
            
            given_answer = False
            while not given_answer:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        given_answer = True
                        run = False
                        break

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            given_answer = True
                            main()
                        elif event.key == pygame.K_ESCAPE:
                            given_answer = True
                            pygame.quit()
                            exit() 

        # Exit game with "x" icon
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        draw(player, elapsed_time, missiles, lasers, live_hearts, hit, combo_missile_destroyed, shield_enabled, extra_live_hearts)

    pygame.quit()

if __name__ == "__main__":
    main()