# level1.py
import pygame
import os
import random

def run():
    pygame.init()

    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("November 1st - Explore the New Moon")

    background_image = pygame.image.load("moonview.png").convert()

    ground_image = pygame.image.load("ground.jpg").convert()
    ground_image = pygame.transform.scale(ground_image, (100, 30))

    rocket_image = pygame.image.load("rocket2.png").convert_alpha()
    rocket_image = pygame.transform.scale(rocket_image, (100, 100))

    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)

    font_path = os.path.join(os.getcwd(), "PressStart2P.ttf")
    font = pygame.font.Font(font_path, 24)
    button_font = pygame.font.Font(font_path, 18)

    level_width = 2000
    camera_x = 0
    player_x, player_y = 0, SCREEN_HEIGHT - 150 - 32
    player_speed = 5
    jump_power = 10
    gravity = 0.5
    player_vel_y = 0
    on_ground = False
    score = 0  # Initialize score to 0
    game_over = False
    time_limit = 15
    start_ticks = pygame.time.get_ticks()
    show_score = False

    ground_height = 30
    ground_y = SCREEN_HEIGHT - ground_height

    platforms = [
        (0, ground_y, 300, ground_height),
        (400, ground_y, 700, ground_height),
        (1250, ground_y, 350, ground_height)
    ]

    # Elevated platforms
    platforms += [
        (100, SCREEN_HEIGHT - 150, 200, 20),
        (400, SCREEN_HEIGHT - 200, 200, 20),
        (600, SCREEN_HEIGHT - 400, 200, 25),
        (750, SCREEN_HEIGHT - 250, 200, 20),
        (1200, SCREEN_HEIGHT - 150, 200, 20),
        (1600, SCREEN_HEIGHT - 200, 200, 20),
        (1800, SCREEN_HEIGHT - 300, 200, 20)
    ]

    # Load rock image
    rock_image = pygame.image.load("rock.png").convert_alpha()
    rock_image = pygame.transform.scale(rock_image, (50, 50))

    # Function to check for rock collisions with platforms
    def is_colliding_with_platforms(rock_rect):
        for plat_x, plat_y, plat_width, plat_height in platforms:
            tile_rect = pygame.Rect(plat_x, plat_y, plat_width, plat_height)
            if rock_rect.colliderect(tile_rect):
                return True
        return False

    # Function to generate random rocks
    def generate_rocks(num_rocks):
        rocks = []
        while len(rocks) < num_rocks:
            rock_x = random.randint(0, level_width - 50)
            rock_y = random.randint(0, ground_y - 50)
            rock_rect = pygame.Rect(rock_x, rock_y, 50, 50)
            if not is_colliding_with_platforms(rock_rect):
                rocks.append((rock_x, rock_y))
        return rocks

    rocks = generate_rocks(15)

    def draw_text(text, font, color, surface, x, y):
        text_obj = font.render(text, True, color)
        text_rect = text_obj.get_rect(center=(x, y))
        surface.blit(text_obj, text_rect)

    
    running = True
    game_started = False
    clock = pygame.time.Clock()
    jumping = False

    level_status = None  

    while running:
        seconds = (pygame.time.get_ticks() - start_ticks) / 1000
        remaining_time = time_limit - seconds

        if remaining_time <= 0 and not game_over:
            show_score = True
            game_over = True
            level_status = "next"

        if game_over:
            screen.fill(BLACK)
            if show_score:
                draw_text("Time's up!", font, WHITE, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50)
                draw_text(f"Level score: {score}", button_font, WHITE, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
            else:
                draw_text("Game Over", font, WHITE, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

            pygame.display.flip()
            clock.tick(30)


            pygame.time.wait(2000) 
            running = False
            continue

        if not game_started:
            screen.fill((0, 0, 30))
            draw_text("November 1st - New moon", font, WHITE, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100)
            draw_text("Press ENTER to Start", button_font, WHITE, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return "quit"
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    game_started = True
                    start_ticks = pygame.time.get_ticks()
                    score = 0

            pygame.display.flip()
            clock.tick(30)
        else:
            screen.blit(background_image, (0, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return "quit"

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                player_x -= player_speed
            if keys[pygame.K_RIGHT]:
                player_x += player_speed

            if keys[pygame.K_UP] and not jumping:
                if on_ground:
                    player_vel_y = -jump_power
                    on_ground = False
                else:
                    player_vel_y = -jump_power
                jumping = True

            if not keys[pygame.K_UP]:
                jumping = False

            player_vel_y += gravity
            player_y += player_vel_y

            player_rect = pygame.Rect(player_x, player_y, 100, 65)
            on_ground = False
            for plat_x, plat_y, plat_width, plat_height in platforms:
                tile_rect = pygame.Rect(plat_x, plat_y, plat_width, plat_height)
                if tile_rect.colliderect(player_rect.move(0, player_vel_y)):
                    if player_vel_y < 0:
                        player_y = tile_rect.bottom
                        player_vel_y = 0
                    elif player_vel_y >= 0:
                        player_y = tile_rect.top - 65
                        player_vel_y = 0
                        on_ground = True

            if player_y > SCREEN_HEIGHT:
                player_x, player_y = 0, SCREEN_HEIGHT - 150 - 32
                player_vel_y = 0

            if player_x < 0:
                player_x = 0
            elif player_x > level_width - 100:
                player_x = level_width - 100

            camera_x = max(0, min(player_x - SCREEN_WIDTH // 2, level_width - SCREEN_WIDTH))

            collected_rocks = []
            player_hitbox = pygame.Rect(player_x, player_y, 100, 100)
            for rock_x, rock_y in rocks:
                rock_rect = pygame.Rect(rock_x, rock_y, 50, 50)
                if player_hitbox.colliderect(rock_rect):
                    collected_rocks.append((rock_x, rock_y))

            for rock in collected_rocks:
                rocks.remove(rock)

            score = max(0, 2000 - (len(rocks) * 100))

            for plat_x, plat_y, plat_width, plat_height in platforms:
                for x in range(plat_width // 100):
                    screen.blit(ground_image, (plat_x - camera_x + x * 100, plat_y))

            screen.blit(rocket_image, (player_x - camera_x, player_y))

            for rock_x, rock_y in rocks:
                screen.blit(rock_image, (rock_x - camera_x, rock_y))

            draw_text(f"Time: {max(0, int(remaining_time))}", button_font, WHITE, screen, SCREEN_WIDTH // 2, 30)

            score_text = button_font.render(f"Level score: {score}", True, WHITE)
            screen.blit(score_text, (10, 10))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    return level_status, score
