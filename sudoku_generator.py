import math, random
import pygame


# ananyaa sutaria
# crystal shao
# kushagra katiyar
# esha gokulram

class SudokuGenerator:

    def __init__(self, removed_cells, row_length=9):
        self.row_length = row_length
        self.removed_cells = removed_cells
        self.board = []
        self.box_length = math.pow(self.row_length, 1 / 2)

        return None

    def get_board(self):
        for row in range(self.row_length):
            new_row = []
            for col in range(self.row_length):
                new_row.append(0)
            self.board.append(new_row)

        return self.board

    def print_board(self):
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                print(self.board[row][col], end=' ')
            print()

        return None

    def valid_in_row(self, row, num):
        if num in self.board[row]:
            return False
        return True

    def valid_in_col(self, col, num):
        for row in range(self.row_length):
            if self.board[row][col] == num:
                return False
        return True

    def valid_in_box(self, row_start, col_start, num):
        for row in range(row_start, row_start + 3):
            for col in range(col_start, col_start + 3):
                if self.board[row][col] == num:
                    return False
        return True

    def is_valid(self, row, col, num):
        row_start = (row // 3) * 3
        col_start = (col // 3) * 3

        if self.valid_in_row(row, num) == False:
            return False
        elif self.valid_in_col(col, num) == False:
            return False
        elif self.valid_in_box(row_start, col_start, num) == False:
            return False
        else:
            return True

    def fill_box(self, row_start, col_start):
        num_set = []

        for i in range(row_start, row_start + 3):
            for j in range(col_start, col_start + 3):
                num = random.randint(1, 9)
                while num in num_set:
                    num = random.randint(1, 9)
                num_set.append(num)
                self.board[i][j] = num

        return None

    def fill_diagonal(self):
        for i in range(0, self.row_length, 3):
            self.fill_box(i, i)

        return None

    '''
    DO NOT CHANGE
    Provided for students
    Fills the remaining cells of the board
    Should be called after the diagonal boxes have been filled

	Parameters:
	row, col specify the coordinates of the first empty (0) cell

	Return:
	boolean (whether or not we could solve the board)
    '''

    def fill_remaining(self, row, col):
        if col >= self.row_length and row < self.row_length - 1:
            row += 1
            col = 0
        if row >= self.row_length and col >= self.row_length:
            return True
        if row < self.box_length:
            if col < self.box_length:
                col = self.box_length
        elif row < self.row_length - self.box_length:
            if col == int(row // self.box_length * self.box_length):
                col += self.box_length
        else:
            if col == self.row_length - self.box_length:
                row += 1
                col = 0
                if row >= self.row_length:
                    return True

        for num in range(1, self.row_length + 1):
            if self.is_valid(row, col, num):
                self.board[row][col] = num
                if self.fill_remaining(row, col + 1):
                    return True
                self.board[row][col] = 0
        return False

    '''
    DO NOT CHANGE
    Provided for students
    Constructs a solution by calling fill_diagonal and fill_remaining

	Parameters: None
	Return: None
    '''

    def fill_values(self):
        self.fill_diagonal()
        self.fill_remaining(0, self.box_length)

    '''
    Removes the appropriate number of cells from the board
    This is done by setting some values to 0
    Should be called after the entire solution has been constructed
    i.e. after fill_values has been called

    NOTE: Be careful not to 'remove' the same cell multiple times
    i.e. if a cell is already 0, it cannot be removed again

	Parameters: None
	Return: None
    '''

    def remove_cells(self):
        removed_count = 0
        while removed_count < self.removed_cells:
            row = random.randint(0, self.row_length - 1)
            col = random.randint(0, self.row_length - 1)
            if self.board[row][col] != 0:
                self.board[row][col] = 0
                removed_count += 1
        return None



'''
DO NOT CHANGE
Provided for students
Given a number of rows and number of cells to remove, this function:
1. creates a SudokuGenerator
2. fills its values and saves this as the solved state
3. removes the appropriate number of cells
4. returns the representative 2D Python Lists of the board and solution

Parameters:
size is the number of rows/columns of the board (9 for this project)
removed is the number of cells to clear (set to 0)

Return: list[list] (a 2D Python list to represent the board)
'''


def generate_sudoku(size, removed):
    sudoku = SudokuGenerator(size, removed)
    sudoku.fill_values()
    board = sudoku.get_board()
    sudoku.remove_cells()
    board = sudoku.get_board()
    return board


class Cell:
    def __init__(self, value, row, col, screen):
        self.value = value
        self.row = row
        self.col = col
        self.screen = screen
        self.sketched_value = 0
        self.selected = False

    def set_cell_value(self, value):
        self.value = value

    def sketched_value(self, value):
        self.sketched_value = value

    def draw(self):
        cell_size = 60
        x = self.col * cell_size
        y = self.row * cell_size
        pygame.draw.rect(self.screen, (255, 255, 255), (x, y, cell_size, cell_size))
        if self.selected:
            pygame.draw.rect(self.screen, (255, 0, 0), (x, y, cell_size, cell_size), 3)
        else:
            pygame.draw.rect(self.screen, (0, 0, 0), (x, y, cell_size, cell_size), 1)
        if self.value != 0:
            font = pygame.font.Font(None, cell_size // 2)
            text = font.render(str(self.value), True, (0, 0, 0))
            text_rect = text.get_rect(center=(x + cell_size // 2, y + cell_size // 2))
            self.screen.blit(text, text_rect)
        elif self.sketched_value != 0:
            font = pygame.font.Font(None, cell_size // 3)
            text = font.render(str(self.sketched_value), True, (128, 128, 128))
            text_rect = text.get_rect(topleft=(x + 5, y + 5))
            self.screen.blit(text, text_rect)


class Board:
    def __init__(self, width, height, screen, difficulty):
        self.width = width
        self.height = height
        self.screen = screen
        self.difficulty = difficulty
        self.gameState = [[0 for i in range(9)] for i in range(9)]
        self.selected_cell = None

    def draw(self):

        for i in range(1, 10):
            pygame.draw.line(self.screen, (0, 0, 0), (0, i * 64), (576, i * 64))
        for i in range(1, 10):
            pygame.draw.line(self.screen, (0, 0, 0), (i * 64, 0), (i * 64, 576))
        for i in range(3, 9, 3):  # bold lines
            pygame.draw.line(self.screen, (0, 0, 0), (i * 64, 0), (i * 64, 576), 5)
            pygame.draw.line(self.screen, (0, 0, 0), (0, i * 64), (576, i * 64), 5)
        if self.selected_cell:
            row, col = self.selected_cell
            pygame.draw.rect(self.screen, (255, 0, 0), (col * 64, row * 64, 64, 64), 5)

    def select(self, row, col):
        self.selected_cell = (row, col)

    def click(self, x, y):
        if 0 <= x < self.width and 0 <= y < self.height:
            row = y // (self.height // 9)
            col = x // (self.width // 9)
            return (row, col)
        return None

    def clear(self):
        if self.selected_cell:
            row, col = self.selected_cell
            self.gameState[row][col] = 0

    def sketch(self, value):
        if self.selected_cell:
            row, col = self.selected_cell
            self.gameState[row][col] = value

    def place_number(self, value):
        if self.selected_cell:
            row, col = self.selected_cell
            self.gameState[row][col] = value

    def reset_to_original(self):
        for row in range(9):
            for col in range(9):
                if self.gameState[row][col] != 0:
                    self.gameState[row][col] = self.gameState[row][col]
                else:
                    self.gameState[row][col] = 0

    def is_full(self):
        for row in range(9):
            for col in range(9):
                if self.gameState[row][col] == 0:
                    return False
        return True

    def update_board(self):
        for row in range(9):
            for col in range(9):
                self.gameState[row][col] = self.gameState[row][col]

    def find_empty(self):
        for row in range(9):
            for col in range(9):
                if self.gameState[row][col] == 0:
                    return (row, col)
        return None

    def check_board(self):
        for row in range(9):
            if len(set(self.gameState[row])) != len([i for i in self.gameState[row] if i != 0]):
                return False
        for col in range(9):
            column = [self.gameState[row][col] for row in range(9)]
            if len(set(column)) != len([i for i in column if i != 0]):
                return False
        for row_start in range(0, 9, 3):
            for col_start in range(0, 9, 3):
                box = [self.gameState[row][col] for row in range(row_start, row_start + 3)
                       for col in range(col_start, col_start + 3)]
                if len(set(box)) != len([i for i in box if i != 0]):
                    return False
        return True




