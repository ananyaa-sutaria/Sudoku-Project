import pygame, sys
from sudoku_generator import *

# Start screen
def draw_game_start(screen):
    screen.fill("light blue")
    WIDTH = 540
    HEIGHT = 600
    LINE_COLOR = (0, 0, 0)

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

    # Define button properties with even less space
    button_width = 100
    button_height = 40
    button_y = 350
    padding = 5  # Even less space between buttons

    # Adjust button positions with minimal space between them and center them horizontally
    total_buttons_width = 3 * button_width + 2 * padding  # Total width of all buttons including space
    start_x = (WIDTH - total_buttons_width) // 2  # Center position for buttons

    easy_button_rect = pygame.Rect(start_x, button_y, button_width, button_height)
    medium_button_rect = pygame.Rect(start_x + button_width + padding, button_y, button_width, button_height)
    hard_button_rect = pygame.Rect(start_x + 2 * (button_width + padding), button_y, button_width, button_height)

    pygame.draw.rect(screen, (27, 38, 92), easy_button_rect)
    pygame.draw.rect(screen, (27, 38, 92), medium_button_rect)
    pygame.draw.rect(screen, (27, 38, 92), hard_button_rect)

    easy_text = pygame.font.Font(None, 30).render('Easy', 0, (255, 255, 255))
    medium_text = pygame.font.Font(None, 30).render('Medium', 0, (255, 255, 255))
    hard_text = pygame.font.Font(None, 30).render('Hard', 0, (255, 255, 255))

    screen.blit(easy_text, (easy_button_rect.x + (button_width - easy_text.get_width()) // 2, easy_button_rect.y + (button_height - easy_text.get_height()) // 2))
    screen.blit(medium_text, (medium_button_rect.x + (button_width - medium_text.get_width()) // 2, medium_button_rect.y + (button_height - medium_text.get_height()) // 2))
    screen.blit(hard_text, (hard_button_rect.x + (button_width - hard_text.get_width()) // 2, hard_button_rect.y + (button_height - hard_text.get_height()) // 2))

    # If button is clicked, return difficulty
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            # If user clicks on button
            if event.type == pygame.MOUSEBUTTONDOWN:
                if easy_button_rect.collidepoint(event.pos):
                    return 30
                if medium_button_rect.collidepoint(event.pos):
                    return 40
                if hard_button_rect.collidepoint(event.pos):
                    return 50
        pygame.display.update()

def draw_game_over(screen):
    BG_COLOR = "light blue"
    LINE_COLOR = (0, 0, 0)
    WIDTH = 540
    HEIGHT = 600

    game_over_font = pygame.font.Font(None, 40)
    screen.fill(BG_COLOR)

    if board.check_board():
        text = 'You win!'
    else:
        text = "You lost :("

    game_over_surf = game_over_font.render(text, 0, LINE_COLOR)
    game_over_rect = game_over_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 100))
    screen.blit(game_over_surf, game_over_rect)

    # Define bottom row buttons with minimal space
    button_width = 100
    button_height = 40
    padding = 5  # Even less space between buttons

    total_buttons_width = 3 * button_width + 2 * padding  # Total width of all buttons
    start_x = (WIDTH - total_buttons_width) // 2  # Center position for buttons

    restart_button_rect = pygame.Rect(start_x, 400, button_width, button_height)
    quit_button_rect = pygame.Rect(start_x + button_width + padding, 400, button_width, button_height)

    pygame.draw.rect(screen, (27, 38, 92), restart_button_rect)
    pygame.draw.rect(screen, (27, 38, 92), quit_button_rect)

    restart_text = pygame.font.Font(None, 30).render('Restart', 0, (255, 255, 255))
    quit_text = pygame.font.Font(None, 30).render('Quit', 0, (255, 255, 255))

    screen.blit(restart_text, (restart_button_rect.x + (button_width - restart_text.get_width()) // 2, restart_button_rect.y + (button_height - restart_text.get_height()) // 2))
    screen.blit(quit_text, (quit_button_rect.x + (button_width - quit_text.get_width()) // 2, quit_button_rect.y + (button_height - quit_text.get_height()) // 2))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            # If user clicks on button
            if event.type == pygame.MOUSEBUTTONDOWN:
                if restart_button_rect.collidepoint(event.pos):
                    return True
                if quit_button_rect.collidepoint(event.pos):
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

        # Define bottom row buttons with minimal space
        button_width = 100
        button_height = 40
        padding = 5  # Even less space between buttons

        total_buttons_width = 3 * button_width + 2 * padding  # Total width of all buttons
        start_x = (WIDTH - total_buttons_width) // 2  # Center position for buttons

        reset_button_rect = pygame.Rect(start_x, 570 - button_height // 2, button_width, button_height)
        restart_button_rect = pygame.Rect(start_x + button_width + padding, 570 - button_height // 2, button_width, button_height)
        exit_button_rect = pygame.Rect(start_x + 2 * (button_width + padding), 570 - button_height // 2, button_width, button_height)

        pygame.draw.rect(screen, (27, 38, 92), reset_button_rect)
        pygame.draw.rect(screen, (27, 38, 92), restart_button_rect)
        pygame.draw.rect(screen, (27, 38, 92), exit_button_rect)

        reset_text = pygame.font.Font(None, 30).render('Reset', 0, (255, 255, 255))
        restart_text = pygame.font.Font(None, 30).render('Restart', 0, (255, 255, 255))
        exit_text = pygame.font.Font(None, 30).render('Exit', 0, (255, 255, 255))

        screen.blit(reset_text, (reset_button_rect.x + (button_width - reset_text.get_width()) // 2, reset_button_rect.y + (button_height - reset_text.get_height()) // 2))
        screen.blit(restart_text, (restart_button_rect.x + (button_width - restart_text.get_width()) // 2, restart_button_rect.y + (button_height - restart_text.get_height()) // 2))
        screen.blit(exit_text, (exit_button_rect.x + (button_width - exit_text.get_width()) // 2, exit_button_rect.y + (button_height - exit_text.get_height()) // 2))

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
                    if exit_button_rect.collidepoint(event.pos):
                        finished_game = True
                        sys.exit()

                    # User clicks reset
                    if reset_button_rect.collidepoint(event.pos):
                        board.reset_to_original()

                    # User clicks restart
                    if restart_button_rect.collidepoint(event.pos):
                        screen.fill(BG_COLOR)
                        game_over = True
                        break

                    # User clicks on board
                    board_pos = board.click(x, y)
                    if board_pos is not None:
                        x, y = board_pos
                        board.select(x, y)

                # User enters valid keyboard input
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

                    if board.is_full():
                        game_over = True
                        winner = True

            # Game is over and there is a winner/game is finished
            if game_over and winner:
                pygame.display.update()
                pygame.time.delay(1000)
                game_over = draw_game_over(screen)

            pygame.display.update()
