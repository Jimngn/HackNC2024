# level2.py
import pygame
import random
import math
import sys
import numpy as np

def run():
    WIDTH, HEIGHT = 800, 600
    FPS = 60
    GAME_DURATION = 6000
    CAPTURE_RADIUS = 55

    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Explore the New Moon - Level 2")

    background_img = pygame.transform.scale(pygame.image.load("background.png"), (WIDTH, HEIGHT))
    telescope_img = pygame.transform.scale(pygame.image.load("telescope.png"), (80, 80))
    meteor_asteroid_img = pygame.transform.scale(pygame.image.load("meteor_asteroid.png"), (50, 50))
    meteor_asteroid_img = pygame.transform.rotate(meteor_asteroid_img, 45)
    meteor_comet_img = pygame.transform.scale(pygame.image.load("meteor_comet.png"), (50, 50))
    meteor_comet_img = pygame.transform.rotate(meteor_comet_img, -45)
    moon_img = pygame.transform.scale(pygame.image.load("moon.png"), (100, 100))
    explosion_img = pygame.transform.scale(pygame.image.load("explosion.png"), (50, 50))
    font = pygame.font.Font(None, 36)

    q_table = np.zeros((20, 2))
    alpha = 0.7
    gamma = 0.9
    epsilon = 0.9
    meteor_speed_range = [1.5, 3]
    meteor_spawn_interval = 1200
    current_state = 0
    capture_streak = 0

    def show_intro(messages):
        for message in messages:
            screen.fill((0, 0, 0))
            text = font.render(message, True, (255, 255, 255))
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - 40))
            pygame.display.flip()

            start_time = pygame.time.get_ticks()
            while pygame.time.get_ticks() - start_time < 2000:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

    def show_result_screen(score):
        screen.fill((0, 0, 0))
        text = font.render(f"Level score: {score}", True, (255, 255, 255))
        screen.blit(text, text.get_rect(center=(WIDTH // 2, HEIGHT // 2)))
        pygame.display.flip()

        start_time = pygame.time.get_ticks()
        while pygame.time.get_ticks() - start_time < 1000:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

    
                    
    def adjust_visibility(alpha_value):
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, int(alpha_value)))
        screen.blit(overlay, (0, 0))

    def update_q_table(state, action, reward, next_state):
        best_future_q = np.max(q_table[next_state])
        q_table[state, action] += alpha * (reward + gamma * best_future_q - q_table[state, action])


    show_intro([
        "November 4, 5 - Taurids Meteor Shower",
        "Collect the meteoroids with your telescope",
        "When the moon is bright, visibility will be reduced"
    ])

    telescope_x, telescope_y = WIDTH // 2, HEIGHT - 100
    meteors = []
    explosions = []
    meteor_timer = 0
    moon_brightness = 0  # Initial moon brightness
    moon_phase_direction = 1  # Direction for moon phase (1: brightening, -1: dimming)
    clock = pygame.time.Clock()
    start_time = pygame.time.get_ticks()
    score = 0
    capture_streak = 0

    class Meteor:
        def __init__(self):
            self.x = random.randint(100, WIDTH - 100)
            self.y = 0
            self.speed = random.uniform(*meteor_speed_range)
            self.type = random.choice(["asteroid", "comet"])
            self.image = meteor_asteroid_img if self.type == "asteroid" else meteor_comet_img

        def move(self):
            self.y += self.speed

        def draw(self):
            # Adjust brightness of meteors based on moon phase
            meteor_image = self.image.copy()
            meteor_image.set_alpha(255 - moon_brightness)
            screen.blit(meteor_image, (int(self.x), int(self.y)))

    class Explosion:
        def __init__(self, x, y):
            self.x = x
            self.y = y
            self.start_time = pygame.time.get_ticks()

        def draw(self):
            screen.blit(explosion_img, (self.x, self.y))

    running = True
    while running:
        elapsed_time = pygame.time.get_ticks() - start_time
        time_left = max(0, GAME_DURATION - elapsed_time)


        if time_left <= 0:
            show_result_screen(score)
            pygame.quit()
            return 'next', score 

        moon_brightness += moon_phase_direction * 0.1
        if moon_brightness >= 150:
            moon_phase_direction = -1
            moon_brightness = 150
        elif moon_brightness <= 0:
            moon_phase_direction = 1
            moon_brightness = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and telescope_x > 0:
            telescope_x -= 15
        if keys[pygame.K_RIGHT] and telescope_x < WIDTH - telescope_img.get_width():
            telescope_x += 15

        meteor_timer += clock.get_time()
        if meteor_timer >= meteor_spawn_interval:
            meteor_timer = 0
            if len(meteors) < 7:
                meteors.append(Meteor())

        for meteor in meteors[:]:
            meteor.move()
            if meteor.y > HEIGHT:
                meteors.remove(meteor)
                explosions.append(Explosion(meteor.x, HEIGHT - 50))
                capture_streak = max(0, capture_streak - 1)

            distance = math.hypot(meteor.x - telescope_x, meteor.y - telescope_y)
            if distance < CAPTURE_RADIUS:
                score += 10 
                meteors.remove(meteor)
                capture_streak += 1

                current_state = min(19, score // 50)
                if np.random.rand() < epsilon:
                    action = random.choice([0, 1])
                else:
                    action = np.argmax(q_table[current_state])

                if action == 0 and capture_streak > 3: 
                    meteor_speed_range[1] = min(10, meteor_speed_range[1] + 0.5)
                    meteor_spawn_interval = max(500, meteor_spawn_interval - 50)
                elif action == 1 and capture_streak < 1:
                    meteor_speed_range[1] = max(1.5, meteor_speed_range[1] - 0.5)
                    meteor_spawn_interval = min(2000, meteor_spawn_interval + 50)

                reward = 1 if capture_streak > 3 else -1
                next_state = min(19, score // 50)
                update_q_table(current_state, action, reward, next_state)
                current_state = next_state

                epsilon = max(0.1, epsilon * 0.995)

        screen.blit(background_img, (0, 0))
        for meteor in meteors:
            meteor.draw()
        screen.blit(telescope_img, (telescope_x, telescope_y))

        moon_surface = moon_img.copy()
        moon_surface.set_alpha(moon_brightness)
        screen.blit(moon_surface, (WIDTH - 110, 10))

        adjust_visibility(moon_brightness)

        time_text = font.render(f"Time Left: {time_left // 1000}s", True, (255, 255, 255))
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(time_text, (10, 10))
        screen.blit(score_text, (WIDTH - 150, 10))

        for explosion in explosions[:]:
            explosion.draw()
            if pygame.time.get_ticks() - explosion.start_time > 500:
                explosions.remove(explosion)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    return 'next', score 

if __name__ == "__main__":
    result, score = run()
    print("Level 2 result:", result)
    print("Level 2 score:", score)
