# level3.py
import pygame
import random
import sys

def run():
    WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600
    GRID_SIZE = 20
    MAZE_WIDTH, MAZE_HEIGHT = WINDOW_WIDTH // GRID_SIZE, WINDOW_HEIGHT // GRID_SIZE

    PATH_COLOR = (0, 0, 0)
    EXIT_COLOR = (0, 255, 0)

    pygame.init()

    log_texture = pygame.image.load("pixil-frame-0.png") 
    beaver_sprite = pygame.image.load("pixil-frame-1.png") 

    sprite_width, sprite_height = 60, 60 
    beaver_sprite = pygame.transform.scale(beaver_sprite, (sprite_width, sprite_height))

    log_texture = pygame.transform.scale(log_texture, (GRID_SIZE, GRID_SIZE))

    def generate_maze():
        maze = [[1 for _ in range(MAZE_WIDTH)] for _ in range(MAZE_HEIGHT)]

        def carve_path(x, y):
            directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
            random.shuffle(directions) 
            for dx, dy in directions:
                nx, ny = x + dx * 2, y + dy * 2
                if 0 <= nx < MAZE_WIDTH and 0 <= ny < MAZE_HEIGHT and maze[ny][nx] == 1:
                    maze[y + dy][x + dx] = 0
                    maze[ny][nx] = 0
                    carve_path(nx, ny)

        start_x, start_y = random.randint(0, (MAZE_WIDTH - 1) // 2) * 2, random.randint(0, (MAZE_HEIGHT - 1) // 2) * 2
        maze[start_y][start_x] = 0
        carve_path(start_x, start_y)

        return maze

    def draw_background(screen):
        for y in range(0, WINDOW_HEIGHT, GRID_SIZE):
            for x in range(0, WINDOW_WIDTH, GRID_SIZE):
                screen.blit(log_texture, (x, y))

    def draw_maze_paths(screen, maze):
        for y in range(MAZE_HEIGHT):
            for x in range(MAZE_WIDTH):
                if maze[y][x] == 0:
                    pygame.draw.rect(screen, PATH_COLOR, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE))

    def draw_exit(screen, exit_pos):
        pygame.draw.rect(screen, EXIT_COLOR, (exit_pos[0] * GRID_SIZE, exit_pos[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))

    def show_win_message(screen, score):
        font = pygame.font.Font(None, 72)
        text = font.render(f"Level score: {score}", True, EXIT_COLOR)
        text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
        screen.fill((0, 0, 0)) 
        screen.blit(text, text_rect)
        pygame.display.flip()
        pygame.time.delay(2000)
        pygame.quit()
        return 'next', score

    def show_start_message(screen):
        font = pygame.font.Font(None, 48)
        text = font.render("Find the exit to the maze", True, (255, 255, 255))
        text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
        
        start_time = pygame.time.get_ticks()

        while pygame.time.get_ticks() - start_time < 3000:
            screen.fill((0, 0, 0))
            screen.blit(text, text_rect)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

        screen.fill((0, 0, 0))
        pygame.display.flip()

    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Beaver Maze Game - Level 3")
    clock = pygame.time.Clock()

    show_start_message(screen)

    maze = generate_maze()
    player_pos = [1, 1] 
    exit_pos = [MAZE_WIDTH - 2, MAZE_HEIGHT - 2] 
    score = 1000
    start_time = pygame.time.get_ticks()
    movement_delay = 100 
    last_move_time = pygame.time.get_ticks()

    running = True
    while running:
        elapsed_time = pygame.time.get_ticks() - start_time
        score = int(max(0, 1000 - elapsed_time * 0.01)) 

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        current_time = pygame.time.get_ticks()
        if current_time - last_move_time > movement_delay:
            keys = pygame.key.get_pressed()
            new_x, new_y = player_pos[0], player_pos[1]
            if keys[pygame.K_UP] and player_pos[1] > 0 and maze[player_pos[1] - 1][player_pos[0]] == 0:
                new_y -= 1
            elif keys[pygame.K_DOWN] and player_pos[1] < MAZE_HEIGHT - 1 and maze[player_pos[1] + 1][player_pos[0]] == 0:
                new_y += 1
            elif keys[pygame.K_LEFT] and player_pos[0] > 0 and maze[player_pos[1]][player_pos[0] - 1] == 0:
                new_x -= 1
            elif keys[pygame.K_RIGHT] and player_pos[0] < MAZE_WIDTH - 1 and maze[player_pos[1]][player_pos[0] + 1] == 0:
                new_x += 1

            if maze[new_y][new_x] == 0:
                player_pos = [new_x, new_y]
                last_move_time = current_time

        if player_pos == exit_pos or score == 0:
            result, final_score = show_win_message(screen, score)
            return result, final_score 

        draw_background(screen)

        draw_maze_paths(screen, maze)

        draw_exit(screen, exit_pos)

        screen.blit(beaver_sprite, 
                    (player_pos[0] * GRID_SIZE + (GRID_SIZE - sprite_width) // 2, 
                     player_pos[1] * GRID_SIZE + (GRID_SIZE - sprite_height) // 2))

        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Level score: {score}", True, (255, 255, 255))
        screen.blit(score_text, (WINDOW_WIDTH - 200, 10))

        pygame.display.flip()
        clock.tick(60) 

    pygame.quit()
    return 'quit', score

if __name__ == "__main__":
    result, score = run()
    print("Level 3 result:", result)
    print("Level 3 score:", score)
