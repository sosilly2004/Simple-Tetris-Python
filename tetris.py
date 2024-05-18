import pygame
import random

# Initialize pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PLAYABLE_WIDTH = int(SCREEN_WIDTH * 0.7)
TRACKING_WIDTH = int(SCREEN_WIDTH * 0.3)
BLOCK_SIZE = 30
BOARD_WIDTH = 10
BOARD_HEIGHT = 20
WHITE = (230, 230, 230)
BLACK = (60, 60, 60)
GRAY = (180, 180, 180)
PASTEL_BLUE = (132, 209, 229)
PASTEL_GREEN = (144, 238, 144)
PASTEL_PURPLE = (221, 160, 221)
PASTEL_PINK = (255, 182, 193)
PASTEL_ORANGE = (255, 190, 153)
PASTEL_TEAL = (175, 238, 238)

# Colors for shapes
SHAPE_COLORS = [
    PASTEL_BLUE,
    PASTEL_GREEN,
    PASTEL_PURPLE,
    PASTEL_PINK,
    PASTEL_ORANGE,
    PASTEL_TEAL
]

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
                if val and (x + col_index < 0 or 
                            x + col_index >= BOARD_WIDTH or 
                            y + row_index >= BOARD_HEIGHT or 
                            (y + row_index >= 0 and self.grid[y + row_index][x + col_index])):
                    return True
        return False

    def add_shape(self, shape, x, y, color):
        for row_index, row in enumerate(shape):
            for col_index, val in enumerate(row):
                if val and 0 <= y + row_index < BOARD_HEIGHT and 0 <= x + col_index < BOARD_WIDTH:
                    self.grid[y + row_index][x + col_index] = color

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
        self.playable_area = pygame.Rect(0, 0, PLAYABLE_WIDTH, SCREEN_HEIGHT)
        self.tracking_area = pygame.Rect(PLAYABLE_WIDTH, 0, TRACKING_WIDTH, SCREEN_HEIGHT)
        self.board = Board()
        self.current_shape = self.get_random_shape()
        self.next_shape = self.get_random_shape()
        self.current_color = self.get_color_for_shape(self.current_shape)
        self.next_color = self.get_color_for_shape(self.next_shape)
        self.current_x = BOARD_WIDTH // 2 - len(self.current_shape[0]) // 2
        self.current_y = 0
        self.game_over = False
        self.score = 0
        self.level = 1
        self.fall_speed = 10
        self.soft_drop = False
        self.try_again_button = pygame.Rect(PLAYABLE_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 50, 200, 50)
        self.splash_screen = True
        self.play_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2, 200, 50)

    def get_random_shape(self):
        return random.choice(SHAPES)

    def get_color_for_shape(self, shape):
        shape_index = SHAPES.index(shape)
        return SHAPE_COLORS[shape_index % len(SHAPE_COLORS)]

    def rotate_shape(self, shape):
        return [list(row) for row in zip(*shape[::-1])]

    def draw_playable_area(self):
        pygame.draw.rect(self.screen, WHITE, self.playable_area)
        for y, row in enumerate(self.board.grid):
            for x, val in enumerate(row):
                if val:
                    pygame.draw.rect(self.screen, val, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
        for y, row in enumerate(self.current_shape):
            for x, val in enumerate(row):
                if val:
                    pygame.draw.rect(self.screen, self.current_color, ((self.current_x + x) * BLOCK_SIZE, (self.current_y + y) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

    def draw_tracking_area(self):
        pygame.draw.rect(self.screen, PASTEL_YELLOW, self.tracking_area)
        font = pygame.font.SysFont(None, 24)
        score_text = font.render(f"Score: {self.score}", True, BLACK)
        level_text = font.render(f"Level: {self.level}", True, BLACK)
        next_piece_text = font.render("Next Piece:", True, BLACK)
        self.screen.blit(score_text, (PLAYABLE_WIDTH + 10, 50))
        self.screen.blit(level_text, (PLAYABLE_WIDTH + 10, 100))
        self.screen.blit(next_piece_text, (PLAYABLE_WIDTH + 10, 150))
        self.draw_shape(self.next_shape, PLAYABLE_WIDTH + 10, 200, self.next_color)

    def draw_shape(self, shape, x, y, color):
        for i, row in enumerate(shape):
            for j, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(self.screen, color, (x + j * BLOCK_SIZE, y + i * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

    def draw_game_over_screen(self):
        pygame.draw.rect(self.screen, PASTEL_PINK, self.playable_area)
        font = pygame.font.SysFont(None, 48)
        game_over_text = font.render("Game Over", True, BLACK)
        score_text = font.render(f"Score: {self.score}", True, BLACK)
        restart_text = font.render("Try Again", True, BLACK)
        self.screen.blit(game_over_text, (PLAYABLE_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - 50))
        self.screen.blit(score_text, (PLAYABLE_WIDTH // 2 - score_text.get_width() // 2, SCREEN_HEIGHT // 2))
        pygame.draw.rect(self.screen, GRAY, self.try_again_button)
        self.screen.blit(restart_text, (PLAYABLE_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT // 2 + 60))

    def draw_splash_screen(self):
        self.screen.fill(PASTEL_BLUE)
        font = pygame.font.SysFont(None, 72)
        title_text = font.render("Tetris", True, BLACK)
        self.screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, SCREEN_HEIGHT // 2 - 150))
        pygame.draw.rect(self.screen, PASTEL_GREEN, self.play_button)
        play_text = font.render("Play", True, BLACK)
        self.screen.blit(play_text, (self.play_button.x + (self.play_button.width - play_text.get_width()) // 2, self.play_button.y + (self.play_button.height - play_text.get_height()) // 2))

    def handle_soft_drop(self):
        if self.soft_drop:
            self.current_y += 1

    def run(self):
        while True:
            if self.splash_screen:
                self.draw_splash_screen()
                pygame.display.update()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        return
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_pos = event.pos
                        if self.play_button.collidepoint(mouse_pos):
                            self.splash_screen = False
            elif self.game_over:
                self.draw_playable_area()
                self.draw_game_over_screen()
                pygame.display.update()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        return
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_pos = event.pos
                        if self.try_again_button.collidepoint(mouse_pos):
                            self.__init__()
                            self.splash_screen = False
                            break
            else:
                self.clock.tick(self.fall_speed)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        return
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
                            self.__init__()
                            self.splash_screen = False

                    elif event.type == pygame.KEYUP:
                        if event.key == pygame.K_DOWN:
                            self.soft_drop = False

                self.handle_soft_drop()

                if self.board.is_collision(self.current_shape, self.current_x, self.current_y + 1):
                    self.board.add_shape(self.current_shape, self.current_x, self.current_y, self.current_color)
                    self.board.remove_full_rows()
                    self.current_shape = self.next_shape
                    self.current_color = self.next_color
                    self.next_shape = self.get_random_shape()
                    self.next_color = self.get_color_for_shape(self.next_shape)
                    self.current_x = BOARD_WIDTH // 2 - len(self.current_shape[0]) // 2
                    self.current_y = 0
                    if self.board.is_collision(self.current_shape, self.current_x, self.current_y):
                        self.game_over = True
                else:
                    self.current_y += 1

                self.draw_playable_area()
                self.draw_tracking_area()

                pygame.display.update()

if __name__ == "__main__":
    game = Tetris()
    game.run()
