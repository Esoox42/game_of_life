import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 700
ROWS, COLS = 16, 16
CELL_SIZE = WIDTH // COLS

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (169, 169, 169)
GREEN = (0, 140, 0)
RED = (255, 0, 0)

# Create the game board
board = [[WHITE] * COLS for _ in range(ROWS)]

# Create the Pygame window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game of Life")

font = pygame.font.Font(None, 36)

def draw_board():
    for row in range(ROWS):
        for col in range(COLS):
            pygame.draw.rect(screen, board[row][col], (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE), 0)
            pygame.draw.line(screen, BLACK, (col * CELL_SIZE, 0), (col * CELL_SIZE, HEIGHT - 100))
            pygame.draw.line(screen, BLACK, (0, row * CELL_SIZE), (WIDTH, row * CELL_SIZE))

def toggle_cell_color(row, col):
    if board[row][col] == WHITE:
        board[row][col] = BLACK
    else:
        board[row][col] = WHITE

def count_living_neighbors(row, col):
    count = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue
            new_row, new_col = row + i, col + j
            if 0 <= new_row < ROWS and 0 <= new_col < COLS and board[new_row][new_col] == BLACK:
                count += 1
    return count

def update_board():
    new_board = [[WHITE] * COLS for _ in range(ROWS)]
    for row in range(ROWS):
        for col in range(COLS):
            living_neighbors = count_living_neighbors(row, col)
            if board[row][col] == BLACK:
                # Cell is alive
                if living_neighbors == 2 or living_neighbors == 3:
                    new_board[row][col] = BLACK
            else:
                # Cell is dead
                if living_neighbors == 3:
                    new_board[row][col] = BLACK
    return new_board

def draw_start_button():
    pygame.draw.rect(screen, GREEN, (WIDTH // 2 - 150, HEIGHT - 90, 100, 40), 0)
    start_text = font.render("Start", True, WHITE)
    screen.blit(start_text, (WIDTH // 2 - 130, HEIGHT - 80))

def draw_end_button():
    pygame.draw.rect(screen, RED, (WIDTH // 2 - 50, HEIGHT - 90, 100, 40), 0)
    end_text = font.render("End", True, WHITE)
    screen.blit(end_text, (WIDTH // 2 - 30, HEIGHT - 80))

def draw_reset_button():
    pygame.draw.rect(screen, GRAY, (WIDTH // 2 + 50, HEIGHT - 90, 100, 40), 0)
    reset_text = font.render("Reset", True, WHITE)
    screen.blit(reset_text, (WIDTH // 2 + 70, HEIGHT - 80))

def draw_step_button():
    pygame.draw.rect(screen, BLACK, (WIDTH // 2 + 150, HEIGHT - 90, 100, 40), 0)
    step_text = font.render("Step", True, WHITE)
    screen.blit(step_text, (WIDTH // 2 + 170, HEIGHT - 80))

# Game loop
setup_phase = True  # Flag to indicate whether the game is in setup phase
running_simulation = False  # Flag to indicate whether the simulation is running
iteration_count = 0
prev_board = None
step_mode = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouseX, mouseY = pygame.mouse.get_pos()
            clicked_row = mouseY // CELL_SIZE
            clicked_col = mouseX // CELL_SIZE

            if setup_phase and mouseY < HEIGHT - 100:
                toggle_cell_color(clicked_row, clicked_col)
            elif WIDTH // 2 - 150 <= mouseX <= WIDTH // 2 - 50 and HEIGHT - 90 <= mouseY <= HEIGHT - 50:
                running_simulation = not running_simulation
                setup_phase = not running_simulation
                step_mode = False
            elif WIDTH // 2 - 50 <= mouseX <= WIDTH // 2 + 50 and HEIGHT - 90 <= mouseY <= HEIGHT - 50:
                running_simulation = False
                setup_phase = True
            elif WIDTH // 2 + 50 <= mouseX <= WIDTH // 2 + 150 and HEIGHT - 90 <= mouseY <= HEIGHT - 50:
                board = [[WHITE] * COLS for _ in range(ROWS)]
                iteration_count = 0
                prev_board = None
                step_mode = False

    screen.fill(WHITE)
    draw_board()
    draw_start_button()
    draw_end_button()
    draw_reset_button()
    draw_step_button()

    if setup_phase or (running_simulation and not step_mode):
        pass  # Add setup phase logic here if needed
    elif running_simulation or step_mode:
        board = update_board()
        iteration_count += 1

        # Check for a stable state
        if board == prev_board:
            running_simulation = False
        else:
            prev_board = [row[:] for row in board]  # Copy the new board state

        if step_mode:
            running_simulation = False

# Display the iteration count
    iteration_text = font.render(f"Iteration: {iteration_count}", True, BLACK)
    screen.blit(iteration_text, (10, HEIGHT - 80))

    pygame.display.flip()
    pygame.time.delay(500)  # Add a delay to make the simulation visible