import math, random
import pygame


# ananyaa sutaria
# crystal shao
# kushagra katiyar
# esha gokulram

import math, random

"""
This was adapted from a GeeksforGeeks article "Program for Sudoku Generator" by Aarti_Rathi and Ankur Trisal
https://www.geeksforgeeks.org/program-sudoku-generator/

"""


class SudokuGenerator:
    '''
	create a sudoku board - initialize class variables and set up the 2D board
	This should initialize:
	self.row_length		- the length of each row
	self.removed_cells	- the total number of cells to be removed
	self.board			- a 2D list of ints to represent the board
	self.box_length		- the square root of row_length

	Parameters:
    row_length is the number of rows/columns of the board (always 9 for this project)
    removed_cells is an integer value - the number of cells to be removed

	Return:
	None
    '''

    def __init__(self, row_length, removed_cells):
        self.row_length = 9
        self.removed_cells = removed_cells
        self.board = [[0 for i in range(self.row_length)]
                      for j in range(self.row_length)]
        self.box_length = int(math.sqrt(row_length))

    '''
	Returns a 2D python list of numbers which represents the board

	Parameters: None
	Return: list[list]
    '''

    def get_board(self):
        return self.board

    '''
	Displays the board to the console
    This is not strictly required, but it may be useful for debugging purposes

	Parameters: None
	Return: None
    '''

    def print_board(self):
        # Prints by Row
        for i in range(len(self.board)):
            print(self.board[i])

    '''
	Determines if num is contained in the specified row (horizontal) of the board
    If num is already in the specified row, return False. Otherwise, return True

	Parameters:
	row is the index of the row we are checking
	num is the value we are looking for in the row

	Return: boolean
    '''

    def valid_in_row(self, row, num):
        for count in range(len(self.board[row])):
            if num == self.board[row][count]:
                return False

        return True

    '''
	Determines if num is contained in the specified column (vertical) of the board
    If num is already in the specified col, return False. Otherwise, return True

	Parameters:
	col is the index of the column we are checking
	num is the value we are looking for in the column

	Return: boolean
    '''

    def valid_in_col(self, col, num):
        for count in range(len(self.board)):
            if num == self.board[count][col]:
                return False

        return True

    '''
	Determines if num is contained in the 3x3 box specified on the board
    If num is in the specified box starting at (row_start, col_start), return False.
    Otherwise, return True

	Parameters:
	row_start and col_start are the starting indices of the box to check
	i.e. the box is from (row_start, col_start) to (row_start+2, col_start+2)
	num is the value we are looking for in the box

	Return: boolean
    '''

    def valid_in_box(self, row_start, col_start, num):
        for i in range(row_start, row_start + 3):
            for p in range(col_start, col_start + 3):
                if num == self.board[i][p]:
                    return False

        return True

    '''
    Determines if it is valid to enter num at (row, col) in the board
    This is done by checking that num is unused in the appropriate, row, column, and box

	Parameters:
	row and col are the row index and col index of the cell to check in the board
	num is the value to test if it is safe to enter in this cell

	Return: boolean
    '''

    def is_valid(self, row, col, num):
        row_copy = row
        col_copy = col
        while row_copy != 0:
            if row_copy % 3 == 0:
                break
            row_copy -= 1
        while col_copy != 0:
            if col_copy % 3 == 0:
                break
            col_copy -= 1

        # Cols is working rows is not
        # Cols are valid when generating values
        if self.valid_in_row(row, num) is True:
            if self.valid_in_col(col, num) is True:
                if self.valid_in_box(row_copy, col_copy, num) is True:
                    return True
                else:
                    return False

        return False

    '''
    Fills the specified 3x3 box with values
    For each position, generates a random digit which has not yet been used in the box

	Parameters:
	row_start and col_start are the starting indices of the box to check
	i.e. the box is from (row_start, col_start) to (row_start+2, col_start+2)

	Return: None
    '''

    def fill_box(self, row_start, col_start):
        stack = []
        x_coordinate = row_start
        y_coordinate = col_start

        while True:
            value = random.randint(1, 9)
            if value in stack:
                pass
            else:
                stack.append(value)
                self.board[x_coordinate][y_coordinate] = value
                x_coordinate += 1
                if x_coordinate > row_start + 2:
                    x_coordinate = row_start
                    y_coordinate += 1
                    col_start += 1

                if len(stack) == 9:
                    break

    '''
    Fills the three boxes along the main diagonal of the board
    These are the boxes which start at (0,0), (3,3), and (6,6)

	Parameters: None
	Return: None
    '''

    def fill_diagonal(self):
        for t in range(0, 9, 3):
            self.fill_box(t, t)

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
        if (col >= self.row_length and row < self.row_length - 1):
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
        removed = 0
        while removed <= self.removed_cells - 1:
            x = random.randint(0, 8)
            y = random.randint(0, 8)

            if self.board[x][y] != 0:
                self.board[x][y] = 0
                removed += 1
            else:
                continue


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

    def set_sketched_value(self, value):
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

import pygame
from sudoku_generator import *


# The Board class and its attributes are established.
class Board:
    def __init__(self, width, height, screen, difficulty):
        self.width = width
        self.height = height
        self.screen = screen
        self.difficulty = difficulty
        #This is the original Board
        self.board = generate_sudoku(9, difficulty)
        self.original_board = [[self.board[row][col] for col in range(self.width)] for row in range(self.height)]
        # The b_cells and chosen_cell attributes are established. They will come into use later.
        self.b_cells = [[Cell(self.board[row][col], row, col, screen) for col in range(self.width)] for row in range(self.height)]
        self.chosen_cell = None
        self.past_row = -1
        self.past_col = -1


    # The sudoku board grid will be drawn.
    def draw(self):
        cell_size = 60
        # Each cell is drawn.
        for row in range(self.height):
            for col in range(self.width):
                b_cell = self.b_cells[row][col]
                b_cell.draw()

        # Lines are drawn, with 3 by 3 grids getting put in bold.
        for cell in range(self.width + 1):
            line_thickness = 3 if cell % 3 == 0 else 1  # thicker lines for box boundaries
            pygame.draw.line(self.screen, (0, 0, 0), (cell * cell_size, 0), (cell * cell_size, self.height * cell_size),
                             line_thickness)
            pygame.draw.line(self.screen, (0, 0, 0), (0, cell * cell_size), (self.width * cell_size, cell * cell_size),
                             line_thickness)

    # A cell on the board is marked as selected.
    def select(self, row, col):
        if self.original_board[col][row] != 0:
            self.chosen_cell = None
            pass
        else:
            self.chosen_cell = self.b_cells[col][row]

            # Unselecting previous cell
            if self.past_row != -1 and self.past_col != -1:
                self.b_cells[self.past_col][self.past_row].selected = False
                self.b_cells[self.past_col][self.past_col].draw()

            """
            Sets the cell to selected being true if the cell can be changed
            Changed validation to check if original board is 0 above
            """
            self.past_row, self.past_col = row, col
            self.b_cells[col][row].selected = True
        return self.chosen_cell

    # The coordinates of a chosen cell are retrieved.
    def click(self, x, y):
        #Cell Size is 50 ---> changed to 60 for better formatting
        x_cord = x // 60
        y_cord = y // 60
        if x_cord > 8 or y_cord > 8:
            return None
        return x_cord, y_cord

    # The chosen cell, should it exist, is cleared.
    def clear(self):
        if self.chosen_cell:
            self.chosen_cell.set_cell_value(0)
            self.chosen_cell.set_sketched_value(0)

    # The chosen cell, should it exist, is given a sketched value.
    def sketch(self, value):
        if self.chosen_cell:
            self.chosen_cell.set_sketched_value(value)

    # The chosen cell, should it exist, has their value set.
    def place_number(self, value):
        if self.chosen_cell:
            self.chosen_cell.set_cell_value(value)
            #Sets sketched value back to 0
            self.chosen_cell.set_sketched_value(0)
            #After number is input, makes it no longer selected
            self.chosen_cell.draw()
            self.chosen_cell.selected = False

    #Board is set to original Board
    #B_Cells is set to original board values
    def reset_to_original(self):
        for row in range(self.height):
            for col in range(self.width):
                self.board[row][col] = self.original_board[row][col]
        self.b_cells = [[Cell(self.board[row][col], row, col, self.screen) for col in range(self.width)] for row in
                        range(self.height)]


    # The program will check if the board is full or not.
    def is_full(self):
        for row in range(self.height):
            for col in range(self.width):
                # If any of the cells are empty, the program returns False.
                if self.b_cells[row][col].value == 0:
                    return False
        # If no cells have a value of 0, the board is full and the program returns True.
        return True

    # The underlying 2D board is updated.
    def update_board(self):
        """
        Sets the board cell at chosen cells row, col to be the chosen cells value
        """
        if self.chosen_cell != None:
            self.b_cells[self.chosen_cell.row][self.chosen_cell.col].value = self.chosen_cell.value
            self.board[self.chosen_cell.row][self.chosen_cell.col] = self.chosen_cell.value
            #Keeps original board as original
            self.original_board[self.chosen_cell.row][self.chosen_cell.col] = 0

    # The program looks for an empty cell.
    def find_empty(self):
        for row in range(self.height):
            for col in range(self.width):
                # If the cell is empty, its coordinates are returned as a tuple.
                if self.b_cells[row][col].value == 0:
                    return row, col
        return None

    # The program checks if the board is correctly solved.
    def check_board(self):
        #Uses Validation Functions from Sudoku Generator to see if the numbers input are valid
        def valid_in_row(row, num):
            counter = 0
            for count in range(len(self.board[row])):
                if num == self.board[row][count]:
                    counter += 1
                    if counter > 1:
                        return False
            return True
        def valid_in_col(col, num):
            counter = 0
            for count in range(len(self.board)):
                if num == self.board[count][col] and count != col:
                    counter += 1
                    if counter > 1:
                        return False
            return True
        def valid_in_box(row_start, col_start, num):
            counter = 0
            for i in range(row_start, row_start + 3):
                for p in range(col_start, col_start + 3):
                    if num == self.board[i][p]:
                        counter += 1
                        if counter > 1:
                            return False
            return True

        def is_valid(row, col, num):
            row_copy = row
            col_copy = col
            while row_copy != 0:
                if row_copy % 3 == 0:
                    break
                row_copy -= 1
            while col_copy != 0:
                if col_copy % 3 == 0:
                    break
                col_copy -= 1
            if valid_in_row(row, num) is True:
                if valid_in_col(col, num) is True:
                    if valid_in_box(row_copy, col_copy, num) is True:
                        return True
                    else:
                        return False
                else:
                    return False
            else:
                return False


        for row in range(self.height):
            for col in range(self.width):
                if is_valid(row, col, self.board[row][col]):
                    pass
                else:
                    return False
        return True

    #used for debugging
    def print_board(self):
        for i in range(len(self.board)):
            print(self.board[i])
        print("------")

    def get_cell_value(self, row, col):
        return self.b_cells[col][row].get_value()


"""
class Board:
    def __init__(self, width, height, screen, difficulty):
        self.width = width
        self.height = height
        self.screen = screen
        self.difficulty = difficulty
        self.gameState = [[0 for i in range(9)] for i in range(9)]
        self.selected_cell = None
        #self.board = generate_sudoku(9, difficulty)
        #self.original_board = [[self.board[row][col] for col in range(self.width)] for row in range(self.height)]

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
"""



