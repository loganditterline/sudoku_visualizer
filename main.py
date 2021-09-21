import pygame
import random
from copy import copy, deepcopy

# Standard solved boards from which other boards are generated
base_board = [[1, 2, 3, 4, 5, 6, 7, 8, 9],
              [4, 5, 6, 7, 8, 9, 1, 2, 3],
              [7, 8, 9, 1, 2, 3, 4, 5, 6],
              [2, 3, 4, 5, 6, 7, 8, 9, 1],
              [5, 6, 7, 8, 9, 1, 2, 3, 4],
              [8, 9, 1, 2, 3, 4, 5, 6, 7],
              [3, 4, 5, 6, 7, 8, 9, 1, 2],
              [6, 7, 8, 9, 1, 2, 3, 4, 5],
              [9, 1, 2, 3, 4, 5, 6, 7, 8]]

# Board used for solving and displaying
sudoku_board = [[0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0]]
# Initialize
pygame.init()

width = 700
height = 1000

# Create screen of 500 x 800
screen = pygame.display.set_mode((width, height))

# Change title
pygame.display.set_caption('Sudoku')
icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)

# Colors and fonts
default_button = (200, 200, 200)
hovered_button = (100, 100, 100)
game_background = (255, 255, 255)
line_color = (0, 0, 0)
font = pygame.font.SysFont('lucidaconsole', 40)
font1 = pygame.font.SysFont('lucidaconsole', 30)
font2 = pygame.font.SysFont('lucidaconsole', 15)

# Solver information
delay = 30
removed = 50


# Generate board
def gen_board(num_remove):
    board = deepcopy(base_board)
    ctr = num_remove

    # Swap a solved board many times to create a random solved board
    # Swap rows
    for x in range(10000):
        offset = random.randint(0, 2) * 3
        row_one = random.randint(0, 2) + offset
        row_two = random.randint(0, 2) + offset
        if row_one != row_two:
            board = swap_row(board, row_one, row_two)

    # Swap columns
    for y in range(10000):
        offset = random.randint(0, 2) * 3
        col_one = random.randint(0, 2) + offset
        col_two = random.randint(0, 2) + offset
        if col_one != col_two:
            board = swap_column(board, col_one, col_two)

    # Swap block of rows
    for x in range(10000):
        row_one = random.randint(0, 2) * 3
        row_two = random.randint(0, 2) * 3
        if row_one != row_two:
            board = swap_row(board, row_one, row_two)
            board = swap_row(board, row_one + 1, row_two + 1)
            board = swap_row(board, row_one + 2, row_two + 2)

    # Swap block of columns
    for y in range(10000):
        col_one = random.randint(0, 2) * 3
        col_two = random.randint(0, 2) * 3
        if col_one != col_two:
            board = swap_column(board, col_one, col_two)
            board = swap_column(board, col_one + 1, col_two + 1)
            board = swap_column(board, col_one + 2, col_two + 2)

    # Remove 'ctr' numbers from the board
    while ctr > 0:
        row = random.randint(0, 8)
        col = random.randint(0, 8)
        if board[row][col] != 0:
            ctr -= 1
            board[row][col] = 0

    return board


# Swap row_one with row_two
def swap_row(board, row_one, row_two):
    board[row_one], board[row_two] = board[row_two], board[row_one]
    return board


# Swap col_one with col_two
def swap_column(board, col_one, col_two):
    for x in range(9):
        board[x][col_one], board[x][col_two] = board[x][col_two], board[x][col_one]
    return board


# Sudoku board
def create_board():
    screen.fill(game_background)
    horz_offset = 0.086
    horz_spacing = 0.092
    vert_offset = 0.0602
    vert_spacing = 0.0644

    # Draw lines for the board with relative orientation
    for n in range(10):
        if n % 3 == 0:
            thickness = 5
        else:
            thickness = 2

        x_level = (horz_offset + horz_spacing * n) * width
        pygame.draw.line(screen, line_color, (x_level, 0.0602 * height), (x_level, 0.6398 * height), thickness)

        y_level = (vert_offset + vert_spacing * n) * height
        pygame.draw.line(screen, line_color, (0.086 * width, y_level), (0.914 * width, y_level), thickness)

    # Write numbers into board
    horz_value_offset = 0.066
    vert_value_offset = 0.0462
    for row in range(9):
        for col in range(9):
            value = str(sudoku_board[row][col]) if sudoku_board[row][col] != 0 else ""
            text = font.render(value, 1, (0, 0, 0))
            x_val = (horz_value_offset + horz_spacing * (col + 0.5)) * width
            y_val = (vert_value_offset + vert_spacing * (row + 0.5)) * height
            screen.blit(text, (x_val, y_val))

    # Information on screen for user

    delay_label = font1.render("Delay: " + str(delay) + "ms", 1, "black")
    screen.blit(delay_label, (0.1 * width, 0.7 * height))

    removed_label = font1.render("Numbers Removed: " + str(removed) + " numbers", 1 ,"black")
    screen.blit(removed_label, (0.1 * width, 0.75 * height))

    space_info_label = font2.render("SPACE to Solve", 1, "black")
    screen.blit(space_info_label, (0.1 * width, 0.8 * height))

    reset_info_label = font2.render("R to Reset Solved Puzzle", 1, "black")
    screen.blit(reset_info_label, (0.1 * width, 0.83 * height))

    generate_info_label = font2.render("G to Generate New Puzzle", 1, "black")
    screen.blit(generate_info_label, (0.1 * width, 0.86 * height))

    remove_info_label = font2.render("RIGHT / LEFT Arrows to Remove MORE / LESS Numbers", 1, "black")
    screen.blit(remove_info_label, (0.1 * width, 0.89 * height))

    delay_info_label = font2.render("D/S to INCREASE / DECREASE Delay", 1, "black")
    screen.blit(delay_info_label, (0.1 * width, 0.92 * height))


def valid(board, row, col, val):
    for i in range(9):
        if board[row][i] == val or board[i][col] == val:
            return False
    start_row = row // 3 * 3
    start_col = col // 3 * 3
    for row_offset in range(3):
        for col_offset in range(3):
            if board[start_row + row_offset][start_col + col_offset] == val:
                return False
    return True


def solve_sudoku(board, row, col, delay):
    while board[row][col] != 0:
        # If not on final row, advance to next row
        if row < 8:
            row += 1
        # If at end of rows, move to next column and start from beginning
        elif row == 8 and col < 8:
            row = 0
            col += 1
        # Otherwise, we are done
        else:
            return True
    pygame.event.pump()
    # Try all values 1-9 until valid
    for val in range(1, 10):
        if valid(board, row, col, val):
            # Fill square with value and show on board
            board[row][col] = val
            screen.fill((255, 255, 255))
            create_board()
            pygame.display.update()
            pygame.time.delay(delay)
            # If there is a solution with this value in this square, recursively solve
            if solve_sudoku(board, row, col, delay) == 1:
                return True
            # Otherwise, backtrack
            else:
                board[row][col] = 0
            # Display change on GUI
            screen.fill((255, 255, 255))
            create_board()
            pygame.display.update()
            pygame.time.delay(delay)


# Generate and display board and copy it
sudoku_board = gen_board(removed)
temp_board = deepcopy(sudoku_board)
create_board()

# Keep program running until X button is hit
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            # If g is pressed, generate a new board, make a copy, and display it
            if event.key == pygame.K_g:
                sudoku_board = gen_board(removed)
                temp_board = deepcopy(sudoku_board)
                create_board()
            # If SPACE is pressed, solve the board
            if event.key == pygame.K_SPACE:
                solve_sudoku(sudoku_board, 0, 0, delay)
            # If R is pressed, reset the board
            if event.key == pygame.K_r:
                sudoku_board = temp_board
                create_board()
            # If D is pressed, decrease the delay
            if event.key == pygame.K_d:
                delay = delay - 10
                if delay < 0:
                    delay = 0
                create_board()
            # If S is pressed, increase the delay
            if event.key == pygame.K_s:
                delay = delay + 10
                if delay > 500:
                    delay = 500
                create_board()
            # If RIGHT is pressed, increase numbers removed
            if event.key == pygame.K_RIGHT:
                removed += 1
                if removed > 64:
                    removed = 64
                create_board()
            # If LEFT is pressed, decrease numbers removed
            if event.key == pygame.K_LEFT:
                removed -= 1
                if removed < 1:
                    removed = 1
                create_board()

    pygame.display.flip()
pygame.display.update()
