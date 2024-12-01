import pygame
import sys
from sudoku_generator import generate_sudoku  # Import the function

# Initialize PyGame
pygame.init()

# Define constants for the game window size and colors
WIDTH, HEIGHT = 600, 600
LINE_WIDTH = 3
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

# Set up the screen and fonts
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sudoku Game")
font = pygame.font.SysFont("Arial", 32)


def draw_grid():
    """Draw the main grid and subgrid lines"""
    block_size = WIDTH // 9
    for i in range(1, 9):
        thickness = LINE_WIDTH if i % 3 != 0 else 6
        pygame.draw.line(screen, BLACK, (i * block_size, 0), (i * block_size, HEIGHT), thickness)
        pygame.draw.line(screen, BLACK, (0, i * block_size), (WIDTH, i * block_size), thickness)


def draw_numbers(board):
    """Draw the numbers on the Sudoku board"""
    block_size = WIDTH // 9
    for i in range(9):
        for j in range(9):
            num = board[i][j]
            if num != 0:
                text = font.render(str(num), True, BLACK)
                screen.blit(text, (j * block_size + block_size // 3, i * block_size + block_size // 4))


def game_loop():
    """Main game loop"""
    # Define difficulty and removed cells
    difficulty = 'medium'
    removed_cells = 40 if difficulty == 'medium' else 30 if difficulty == 'easy' else 50

    # Generate the Sudoku puzzle
    board = generate_sudoku(9, removed_cells)  # Call the generate_sudoku() function

    selected_cell = None
    running = True

    while running:
        screen.fill(WHITE)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Handle cell selection (left click)
                mouse_x, mouse_y = pygame.mouse.get_pos()
                row = mouse_y // (HEIGHT // 9)
                col = mouse_x // (WIDTH // 9)
                selected_cell = (row, col)

            elif event.type == pygame.KEYDOWN:
                # Handle number input and cell selection
                if selected_cell:
                    row, col = selected_cell
                    if event.key == pygame.K_1:
                        board[row][col] = 1
                    elif event.key == pygame.K_2:
                        board[row][col] = 2
                    elif event.key == pygame.K_3:
                        board[row][col] = 3
                    elif event.key == pygame.K_4:
                        board[row][col] = 4
                    elif event.key == pygame.K_5:
                        board[row][col] = 5
                    elif event.key == pygame.K_6:
                        board[row][col] = 6
                    elif event.key == pygame.K_7:
                        board[row][col] = 7
                    elif event.key == pygame.K_8:
                        board[row][col] = 8
                    elif event.key == pygame.K_9:
                        board[row][col] = 9

        # Draw the grid, numbers, and selected cell
        draw_grid()
        draw_numbers(board)

        if selected_cell:
            row, col = selected_cell
            block_size = WIDTH // 9
            pygame.draw.rect(screen, RED, (col * block_size, row * block_size, block_size, block_size), 3)

        pygame.display.flip()

    pygame.quit()
    sys.exit()


# Run the game
if __name__ == "__main__":
    game_loop()
