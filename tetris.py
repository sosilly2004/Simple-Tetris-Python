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
GRAY = (128, 128, 128)

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
        self.grid = [[0] * BOARD_WIDTH for _ in range(BOARD_HEIGHT)]

    def is_collision(self, shape, x, y):
        for row_index, row in enumerate(shape):
            for col_index, val in enumerate(row):
                if val and (self.grid[y + row_index][x + col_index] or 
                            x + col_index < 0 or 
                            x + col_index >= BOARD_WIDTH or 
                            y + row_index >= BOARD_HEIGHT):
                    return True
        return False

    def add_shape(self, shape, x, y):
        for row_index, row in enumerate(shape):
            for col_index, val in enumerate(row):
                if val:
                    self.grid[y + row_index][x + col_index] = 1

    def remove_full_rows(self):
        rows_to_remove = [i for i, row in enumerate(self.grid) if all(row)]
        for row_index in rows_to_remove:
            del self.grid[row_index]
            self.grid.insert(0, [0] * BOARD_WIDTH)

# Tetris game class
class Tetris:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Tetris")
        self.clock = pygame.time.Clock()
        self.board = Board()
        self.current_shape = self.get_random_shape()
        self.current_x = BOARD_WIDTH // 2 - len(self.current_shape[0]) // 2
        self.current_y = 0
        self.game_over = False
        self.score = 0
        self.level = 1
        self.fall_speed = 10
        self.soft_drop = False

    def get_random_shape(self):
        return random.choice(SHAPES)

    def rotate_shape(self, shape):
        return [list(row) for row in zip(*shape[::-1])]

    def draw_board(self):
        self.screen.fill(BLACK)
        for y, row in enumerate(self.board.grid):
            for x, val in enumerate(row):
                if val:
                    pygame.draw.rect(self.screen, GRAY, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
        for y, row in enumerate(self.current_shape):
            for x, val in enumerate(row):
                if val:
                    pygame.draw.rect(self.screen, WHITE, ((self.current_x + x) * BLOCK_SIZE, (self.current_y + y) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

    def draw_game_over_screen(self):
        font = pygame.font.SysFont(None, 48)
        game_over_text = font.render("Game Over", True, WHITE)
        score_text = font.render(f"Score: {self.score}", True, WHITE)
        restart_text = font.render("Press R to restart", True, WHITE)
        self.screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - 50))
        self.screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT // 2 + 50))

    def handle_soft_drop(self):
        if self.soft_drop:
            self.current_y += 1

    def run(self):
        while not self.game_over:
            self.clock.tick(self.fall_speed)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_over = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        if not self.board.is_collision(self.current_shape, self.current_x - 1, self.current_y):
                            self.current_x -= 1
                    elif event.key == pygame.K_RIGHT:
                        if not self.board.is_collision(self.current_shape, self.current_x + 1, self.current_y):
                            self.current_x += 1
                    elif event.key == pygame.K_DOWN:
                        self.soft_drop = True
                    elif event.key == pygame.K_UP:
                        rotated_shape = self.rotate_shape(self.current_shape)
                        if not self.board.is_collision(rotated_shape, self.current_x, self.current_y):
                            self.current_shape = rotated_shape
                    elif event.key == pygame.K_r and self.game_over:
                        self.__init__()  # Restart the game

                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_DOWN:
                        self.soft_drop = False

            self.handle_soft_drop()

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

            self.draw_board()

            if self.game_over:
                self.draw_game_over_screen()

            pygame.display.update()

        pygame.quit()

if __name__ == "__main__":
    game = Tetris()
    game.run()
