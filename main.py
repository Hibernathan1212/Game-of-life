import pygame
import sys
import random

# Grid dimensions
WIDTH, HEIGHT = 1400, 1400
ROWS, COLS = 280, 280
CELL_SIZE = WIDTH // COLS

# Colors
ALIVE_COLOR = (255, 255, 255)  # White
DEAD_COLOR = (0, 0, 0)         # Black
GRID_COLOR = (40, 40, 40)      # Grey for grid lines

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Conway's Game of Life")
clock = pygame.time.Clock()

# Create the initial board as a 2D array
def create_board(randomize=False):
    return [[random.randint(0, 1) if randomize else 0 for _ in range(COLS)] for _ in range(ROWS)]

# Draw the grid and cells
def draw_grid(board):
    screen.fill(DEAD_COLOR)
    for row in range(ROWS):
        for col in range(COLS):
            color = ALIVE_COLOR if board[row][col] == 1 else DEAD_COLOR
            pygame.draw.rect(screen, color, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            # Draw grid lines for clarity
            pygame.draw.rect(screen, GRID_COLOR, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)
    pygame.display.flip()

# Count neighbors for each cell
def count_neighbors(board, x, y):
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    count = 0
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if 0 <= nx < ROWS and 0 <= ny < COLS:
            count += board[nx][ny]
    return count

# Update the board based on Game of Life rules
def update_board(board):
    new_board = [[0 for _ in range(COLS)] for _ in range(ROWS)]
    for row in range(ROWS):
        for col in range(COLS):
            alive_neighbors = count_neighbors(board, row, col)
            if board[row][col] == 1:  # Cell is alive
                if alive_neighbors < 2 or alive_neighbors > 3:
                    new_board[row][col] = 0  # Dies
                else:
                    new_board[row][col] = 1  # Stays alive
            else:  # Cell is dead
                if alive_neighbors == 3:
                    new_board[row][col] = 1  # Becomes alive
    return new_board

# Main loop
def main():
    board = create_board(randomize=True)  # Randomize for an initial state
    running = False  # Start with the simulation paused

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    running = not running  # Toggle running state with space bar
                elif event.key == pygame.K_r:
                    board = create_board(randomize=True)  # Reset with random board
                elif event.key == pygame.K_c:
                    board = create_board(randomize=False)  # Clear the board

            elif pygame.mouse.get_pressed()[0]:  # Toggle cell state on left click
                mouse_x, mouse_y = pygame.mouse.get_pos()
                col, row = mouse_x // CELL_SIZE, mouse_y // CELL_SIZE
                board[row][col] = 1 - board[row][col]  # Toggle between 1 and 0

        if running:
            board = update_board(board)  # Update the board only if running

        draw_grid(board)
        clock.tick(100)

if __name__ == "__main__":
    main()