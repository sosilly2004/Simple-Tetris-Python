import pygame
import random

# Initialize pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BLOCK_SIZE = 30
BOARD_WIDTH = 10
BOARD_HEIGHT = 20
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Shapes and their rotations
SHAPES = [
    [[1, 1, 1],
     [0, 1, 0]],
    
    [[1, 1, 0],
     [0, 1, 1]],
    
    [[1, 1],
     [1, 1]],
    
    [[1, 1, 1, 1]],
    
    [[1, 1, 1],
     [1, 0, 0]],
    
    [[1, 1, 1],
     [0, 0, 1]],
    
    [[1, 1, 1],
     [0, 1, 0]]
]

# Tetris board class
class Board:
    def __init__(self):
        # Initialize the game board grid
        self.grid = [[0] * BOARD_WIDTH for _ in range(BOARD_HEIGHT)]

    def is_collision(self, shape, x, y):
        # Check if the given shape collides with any existing blocks or borders
        for row_index, row in enumerate(shape):
            for col_index, val in enumerate(row):
                if val and (self.grid[y + row_index][x + col_index] or 
                            x + col_index < 0 or 
                            x + col_index >= BOARD_WIDTH or 
                            y + row_index >= BOARD_HEIGHT):
                    return True
        return False

    def add_shape(self, shape, x, y):
        # Add the given shape to the game board grid
        for row_index, row in enumerate(shape):
            for col_index, val in enumerate(row):
                if val:
                    self.grid[y + row_index][x + col_index] = 1

    def remove_full_rows(self):
        # Remove any full rows from the game board
        rows_to_remove = [i for i, row in enumerate(self.grid) if all(row)]
        for row_index in rows_to_remove:
            del self.grid[row_index]
            self.grid.insert(0, [0] * BOARD_WIDTH)

# Tetris game class
class Tetris:
    def __init__(self):
        # Initialize the game window, clock, board, and current shape
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Tetris")
        self.clock = pygame.time.Clock()
        self.board = Board()
        self.current_shape = self.get_random_shape()
        self.current_x = BOARD_WIDTH // 2 - len(self.current_shape[0]) // 2
        self.current_y = 0
        self.game_over = False

    def get_random_shape(self):
        # Return a random shape from the predefined shapes
        return random.choice(SHAPES)

    def rotate_shape(self, shape):
        # Rotate the given shape
        return [list(row) for row in zip(*shape[::-1])]

    def draw_board(self):
        # Draw the game board and the current falling shape
        self.screen.fill(BLACK)
        for y, row in enumerate(self.board.grid):
            for x, val in enumerate(row):
                if val:
                    pygame.draw.rect(self.screen, WHITE, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
        for y, row in enumerate(self.current_shape):
            for x, val in enumerate(row):
                if val:
                    pygame.draw.rect(self.screen, WHITE, ((self.current_x + x) * BLOCK_SIZE, (self.current_y + y) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
    
    def run(self):
        # Main game loop
        while not self.game_over:
            self.clock.tick(10)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_over = True
                elif event.type == pygame.KEYDOWN:
                    # Handle user input for moving and rotating the current shape
                    if event.key == pygame.K_LEFT:
                        if not self.board.is_collision(self.current_shape, self.current_x - 1, self.current_y):
                            self.current_x -= 1
                    elif event.key == pygame.K_RIGHT:
                        if not self.board.is_collision(self.current_shape, self.current_x + 1, self.current_y):
                            self.current_x += 1
                    elif event.key == pygame.K_DOWN:
                        if not self.board.is_collision(self.current_shape, self.current_x, self.current_y + 1):
                            self.current_y += 1
                    elif event.key == pygame.K_UP:
                        rotated_shape = self.rotate_shape(self.current_shape)
                        if not self.board.is_collision(rotated_shape, self.current_x, self.current_y):
                            self.current_shape = rotated_shape

            # Move the current shape down and handle collisions
            if self.board.is_collision(self.current_shape, self.current_x, self.current_y + 1):
                self.board.add_shape(self.current_shape, self.current_x, self.current_y)
                self.board.remove_full_rows()
                self.current_shape = self.get_random_shape()
                self.current_x = BOARD_WIDTH // 2 - len(self.current_shape[0]) // 2
                self.current_y = 0
                if self.board.is_collision(self.current_shape, self.current_x, self.current_y):
                    self.game_over = True
            else:
                self.current_y += 1

            # Draw the game board
            self.draw_board()
            pygame.display.update()

        pygame.quit()

if __name__ == "__main__":
    # Start the game
    game = Tetris()
    game.run()
