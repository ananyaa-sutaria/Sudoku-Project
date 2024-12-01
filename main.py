import pygame
import sys
from sudoku_generator import Board
from sudoku_generator import SudokuGenerator

pygame.init()
screen = pygame.display.set_mode((576, 576))
pygame.display.set_caption("Sudoku")

#inital screen shown when user starts or resets game
def game_start_screen():
    font = pygame.font.SysFont('Times New Roman', 30)
    start_text = font.render("Select Difficulty:", True, (255, 255, 255))
    screen.blit(start_text, (150, 100))

    easy_button = pygame.Rect(60, 200, 120, 50)
    medium_button = pygame.Rect(210, 200, 120, 50)
    hard_button = pygame.Rect(360, 200, 120, 50)

    pygame.draw.rect(screen, (0, 255, 0), easy_button)
    pygame.draw.rect(screen, (255, 255, 0), medium_button)
    pygame.draw.rect(screen, (255, 0, 0), hard_button)

    easy_text = font.render("Easy", True, (0, 0, 0))
    medium_text = font.render("Medium", True, (0, 0, 0))
    hard_text = font.render("Hard", True, (0, 0, 0))

    screen.blit(easy_text, (80, 215))
    screen.blit(medium_text, (220, 215))
    screen.blit(hard_text, (380, 215))

    pygame.display.flip()

    return easy_button, medium_button, hard_button

#reset, restart, and exit buttons when the game has started
def draw_buttons():
    font = pygame.font.SysFont('Times New Roman', 24)

    reset_button = pygame.Rect(50, 540, 120, 50)
    restart_button = pygame.Rect(200, 540, 120, 50)
    exit_button = pygame.Rect(350, 540, 120, 50)

    pygame.draw.rect(screen, (0, 255, 0), reset_button)
    pygame.draw.rect(screen, (0, 0, 255), restart_button)
    pygame.draw.rect(screen, (255, 0, 0), exit_button)

    reset_text = font.render("Reset", True, (255, 255, 255))
    restart_text = font.render("Restart", True, (255, 255, 255))
    exit_text = font.render("Exit", True, (255, 255, 255))

    screen.blit(reset_text, (reset_button.x + 35, reset_button.y + 10))
    screen.blit(restart_text, (restart_button.x + 20, restart_button.y + 10))
    screen.blit(exit_text, (exit_button.x + 35, exit_button.y + 10))

    pygame.display.flip()

    return reset_button, restart_button, exit_button


def main():
    clock = pygame.time.Clock()

    easy_button, medium_button, hard_button = game_start_screen()

    difficulty = 30

    game_running = True
    while game_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if easy_button.collidepoint(mouse_x, mouse_y):
                    difficulty = 30
                elif medium_button.collidepoint(mouse_x, mouse_y):
                    difficulty = 40
                elif hard_button.collidepoint(mouse_x, mouse_y):
                    difficulty = 50
                game_running = False

        pygame.display.flip()

    board = Board(576, 576, screen, difficulty)

    # Main game loop
    game_running = True
    while game_running:
        screen.fill(("light blue"))  # Clear screen

        board.draw()

        reset_button, restart_button, exit_button = draw_buttons()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                row, col = board.click(mouse_x, mouse_y)
                board.select(row, col)

                if reset_button.collidepoint(mouse_x, mouse_y):
                    board.reset_to_original()
                elif restart_button.collidepoint(mouse_x, mouse_y):
                    screen.fill((0, 0, 0))
                    main()
                    return
                elif exit_button.collidepoint(mouse_x, mouse_y):
                    game_running = False

            if event.type == pygame.KEYDOWN:
                if board.selected_cell:
                    if event.key == pygame.K_RETURN:
                        board.place_number(board.selected_cell.sketched_value)
                    elif event.key == pygame.K_BACKSPACE:
                        board.selected_cell.set_sketched_value(0)
                    elif pygame.K_1 <= event.key <= pygame.K_9:
                        board.selected_cell.set_sketched_value(event.key - pygame.K_0)

        pygame.display.flip()

        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()