"""

import pygame
import sys
from sudoku_generator import Board
from sudoku_generator import generate_sudoku

pygame.init()
screen = pygame.display.set_mode((540, 600))
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
        pygame.display.update()

    # Start the game with the selected difficulty
    board = Board(540, 600, screen, difficulty)

    # Main game loop
    game_running = True
    while game_running:
        screen.fill((255, 255, 255))  # Clear screen

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



"""
import pygame, sys
from sudoku_generator import *
from sudoku_generator import *

class Button:
    def __init__(self, text, screen, x, y, width=80, height=30, color=(50, 50, 100)):
        self.text = text
        self.screen = screen
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color

        self.button_font = pygame.font.Font(None, 30)
        self.button_text = self.button_font.render(self.text, 0, (255, 255, 255))
        self.button_surf = pygame.Surface((self.button_text.get_size()[0] + 20, self.button_text.get_size()[1] + 20))
        self.button_surf.fill((27, 38, 92))
        self.button_surf.blit(self.button_text, (10, 10))
        self.button_rect = self.button_surf.get_rect(center=(self.x, self.y))
        screen.blit(self.button_surf, self.button_rect)

    # Draw button
    def draw_button(self, surface):
        font = pygame.font.Font(None, 20)
        text = font.render(self.text, True, (255, 55, 255))
        text_rect = text.get_rect(center=(self.button_surf.get_width() / 2, self.button_surf.get_height() / 2))

        self.button_surf.blit(text, text_rect)
        surface.blit(self.button_surf, self.button_rect)

    def get_collide_point(self):
        rect = self.button_surf.get_rect()
        return self.button_rect

# Start screen
def draw_game_start(screen):
    screen.fill("light blue")
    WIDTH = 540
    HEIGHT = 600
    LINE_COLOR = (0,0,0)

    # Welcome text
    welcome_text = pygame.font.Font(None, 50)
    welcome_surf = welcome_text.render('Welcome to Sudoku!', 0, LINE_COLOR)
    welcome_rect = welcome_surf.get_rect(center=(WIDTH // 2, HEIGHT // 3))

    # Button rectangle
    select_text = pygame.font.Font(None, 40)
    select_surf = select_text.render('Select Difficulty:', 0, LINE_COLOR)
    select_rect = select_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2))

    screen.blit(welcome_surf, welcome_rect)
    screen.blit(select_surf, select_rect)

    # Initialize and draw buttons
    easy_button = Button('Easy', screen, WIDTH // 3, 350)
    medium_button = Button('Medium', screen, WIDTH // 2, 350)
    hard_button = Button('Hard', screen, (WIDTH // 3) * 2, 350)

    # If button is clicked, return to main
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            # If user clicks on button
            if event.type == pygame.MOUSEBUTTONDOWN:

                # Easy
                if easy_button.get_collide_point().collidepoint(event.pos):
                    difficulty = 30
                    return difficulty
                # Medium
                if medium_button.get_collide_point().collidepoint(event.pos):
                    difficulty = 40
                    return difficulty
                # Hard
                if hard_button.get_collide_point().collidepoint(event.pos):
                    difficulty = 50
                    return difficulty
        pygame.display.update()


def draw_game_over(screen):
    BG_COLOR = "light blue"
    LINE_COLOR = (0,0,0)
    WIDTH = 540
    HEIGHT = 600

    game_over_font = pygame.font.Font(None, 40)
    screen.fill(BG_COLOR)

    if board.check_board():
        text = 'You win!'
    else:
        text = "You lost :("

    game_over_surf = game_over_font.render(text, 0, LINE_COLOR)
    game_over_rect = game_over_surf.get_rect(
        center=(WIDTH // 2, HEIGHT // 2 - 100))
    screen.blit(game_over_surf, game_over_rect)

    restart_button = Button('Restart', screen, 200, 400)

    quit_button = Button('Quit', screen, 400, 400)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            # If user clicks on button
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Restart
                if restart_button.get_collide_point().collidepoint(event.pos):
                    # If user wants to keep playing another game
                    return True

                # Quit
                if quit_button.get_collide_point().collidepoint(event.pos):
                    sys.exit()

        pygame.display.update()


if __name__ == '__main__':
    BG_COLOR = "light blue"
    LINE_COLOR = (0, 0, 0)
    WIDTH = 540
    HEIGHT = 600
    finished_game = False
    sketched_value = 0

    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Sudoku")

    # Main Game Loop
    while finished_game is False:
        game_over = False
        winner = False
        difficulty = draw_game_start(screen)  # Calls function to draw start screen

        # Start game board
        screen.fill(BG_COLOR)

        board = Board(9, 9, screen, difficulty)
        original_board = board
        board.draw()

        # Bottom row of buttons
        reset_button = Button('Reset', screen, (WIDTH // 3), 570)
        restart_button = Button('Restart', screen, WIDTH // 2, 570)
        exit_button = Button('Exit', screen, (WIDTH // 3) * 2, 570)

        # Constants
        x = 0
        y = 0
        while game_over is False:
            board.draw()

            for event in pygame.event.get():
                # If user presses x out button
                if event.type == pygame.QUIT:
                    sys.exit()

                # User clicks
                if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                    x, y = pygame.mouse.get_pos()

                    # User clicks quit
                    if exit_button.get_collide_point().collidepoint(event.pos):
                        finished_game = True
                        sys.exit()

                    # User clicks reset
                    if reset_button.get_collide_point().collidepoint(event.pos):
                        board.reset_to_original()

                    # User clicks restart
                    if restart_button.get_collide_point().collidepoint(event.pos):
                        screen.fill(BG_COLOR)
                        game_over = True
                        break

                    # User clicks on board
                    board_pos = board.click(x, y)
                    if board_pos is not None:
                        x, y = board_pos
                        board.select(x, y)

                # User enters valid keyboard input
                # help from: https://stackoverflow.com/questions/71672325/how-to-get-keyboard-input-in-pygame
                if event.type == pygame.KEYDOWN:

                    if (event.key == pygame.K_1 or
                            event.key == pygame.K_2 or
                            event.key == pygame.K_3 or
                            event.key == pygame.K_4 or
                            event.key == pygame.K_5 or
                            event.key == pygame.K_6 or
                            event.key == pygame.K_7 or
                            event.key == pygame.K_8 or
                            event.key == pygame.K_9):
                        sketched_value = event.key - 48
                        board.sketch(sketched_value)

                    # Clears spot on board if delete
                    if event.key == pygame.K_DELETE:
                        board.clear()

                    # User hits enter -> place sketched value
                    if event.key == pygame.K_RETURN and sketched_value != 0:
                        board.place_number(sketched_value)
                        board.update_board()
                        sketched_value = 0

                    # Arrow Navigation
                    if event.key == pygame.K_RIGHT:
                        # Counter Variables checks if it is the only available square in the row or col
                        counter = 0
                        if x < 8:
                            x += 1
                        else:
                            x = 0
                        # Section of Code goes till it finds a viable square
                        while True:
                            if board.select(x, y) is None:
                                if x < 8:
                                    x += 1
                                else:
                                    x = 0
                                    counter += 1
                                    if counter > 1:
                                        break
                            else:
                                break
                        board.select(x, y)
                    # Arrow Navigation
                    if event.key == pygame.K_LEFT:
                        # Counter Variables checks if it is the only available square in the row or col
                        counter = 0
                        if x > 0:
                            x -= 1
                        else:
                            x = 8
                        # Section of Code goes till it finds a viable square
                        while True:
                            if board.select(x, y) is None:
                                if x > 0:
                                    x -= 1
                                else:
                                    x = 8
                                    counter += 1
                                    if counter > 1:
                                        break
                            else:
                                break
                        board.select(x, y)
                    # Arrow Navigation
                    if event.key == pygame.K_UP:
                        # Counter Variables checks if it is the only available square in the row or col
                        counter = 0
                        if y > 0:
                            y -= 1
                        else:
                            y = 8
                        # Section of Code goes till it finds a viable square
                        while True:
                            if board.select(x, y) is None:
                                if y > 0:
                                    y -= 1
                                else:
                                    y = 8
                                    counter += 1
                                    if counter > 1:
                                        break
                            else:
                                break
                        board.select(x, y)
                    # Arrow Navigation
                    if event.key == pygame.K_DOWN:
                        # Counter Variables checks if it is the only available square in the row or col
                        counter = 0
                        if y < 8:
                            y += 1
                        else:
                            y = 0
                        # Section of Code goes till it finds a viable square
                        while True:
                            if board.select(x, y) is None:
                                if y < 8:
                                    y += 1
                                else:
                                    y = 0
                                    counter += 1
                                    if counter > 1:
                                        break
                            else:
                                break
                        board.select(x, y)

                    if board.is_full():
                        game_over = True
                        winner = True

            # Game is over and there is a winner/game is finished
            if game_over and winner:
                pygame.display.update()
                pygame.time.delay(1000)
                game_over = draw_game_over(screen)

            pygame.display.update()

