# main.py
import pygame
import sys
import level1
import level2 
import level3  
import level4 
from flask import Flask
app = Flask(__name__)


def show_landing_page():
    pygame.init()
    SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("November Astronomical Events")
    font_title = pygame.font.Font(None, 74)
    font_button = pygame.font.Font(None, 50)
    clock = pygame.time.Clock()


    title_text = font_title.render("November Astronomical Events", True, (255, 255, 255))
    title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100))


    button_text = font_button.render("Start", True, (0, 0, 0))
    button_rect = pygame.Rect(0, 0, 200, 80)
    button_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)
    button_color = (255, 255, 255)


    while True:
        screen.fill((0, 0, 0)) 
        screen.blit(title_text, title_rect)


        pygame.draw.rect(screen, button_color, button_rect)
        screen.blit(button_text, button_text.get_rect(center=button_rect.center))
        pygame.display.flip()


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    pygame.mixer.music.stop()
                    return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    pygame.mixer.music.stop()
                    return

        clock.tick(30)

def show_congratulations_screen(total_score):
    pygame.init() 
    SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Game Completed")
    font_large = pygame.font.Font(None, 74)
    font_small = pygame.font.Font(None, 36)
    clock = pygame.time.Clock()

    congrats_text = font_large.render("Congratulations!", True, (255, 255, 255))
    levels_complete_text = font_large.render("You've completed all levels!", True, (255, 255, 255))
    total_score_text = font_small.render(f"Total Score: {total_score}", True, (255, 255, 255))
    continue_text = font_small.render("Press ESC to exit", True, (255, 255, 255))


    congrats_rect = congrats_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100))
    levels_complete_rect = levels_complete_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 30))
    total_score_rect = total_score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40))
    continue_rect = continue_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100))


    while True:
        screen.fill((0, 0, 0)) 
        screen.blit(congrats_text, congrats_rect)
        screen.blit(levels_complete_text, levels_complete_rect)
        screen.blit(total_score_text, total_score_rect)
        screen.blit(continue_text, continue_rect)
        pygame.display.flip()


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    return

        clock.tick(30)

def main():
    show_landing_page()

    total_score = 0

    while True:

        print("Starting Level 1...")
        level_status, score = level1.run()
        total_score += score 

        if level_status == "next":
            print("Level 1 completed! Starting Level 2...")
            level_status, score = level2.run() 
            total_score += score 


            if level_status == "next":
                print("Level 2 completed! Starting Level 3...")
                level_status, score = level3.run()
                total_score += score


                if level_status == "next":
                    print("Level 3 completed! Starting Level 4...")
                    level_status, score = level4.run()
                    total_score += score 


                    if level_status == "next":
                        print("Congratulations! You've completed all levels!")
                        show_congratulations_screen(total_score)
                        break 
                else:
                    print("You lost in Level 3. Restarting from Level 1...")
            else:
                print("You lost in Level 2. Restarting from Level 1...")
        else:
            print("You lost in Level 1. Restarting from Level 1...")

if __name__ == "__main__":
    main()
