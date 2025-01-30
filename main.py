import pygame
import random

pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 300, 600
SIDE_PANEL_WIDTH = 150
GRID_SIZE = 30
COLUMNS, ROWS = SCREEN_WIDTH // GRID_SIZE, SCREEN_HEIGHT // GRID_SIZE

BLACK = (20, 20, 20)
WHITE = (255, 255, 255)
GRAY = (70, 70, 70)
DARK_GRAY = (40, 40, 40)
COLORS = [
    (255, 0, 0),
    (0, 255, 0),
    (0, 0, 255),
    (255, 255, 0),
    (0, 255, 255),
    (255, 0, 255),
    (128, 128, 255),
]

SHAPES = [
    [[1, 1, 1, 1]],
    [[1, 1], [1, 1]],
    [[0, 1, 0], [1, 1, 1]],
    [[1, 0, 0], [1, 1, 1]],
    [[0, 0, 1], [1, 1, 1]],
    [[0, 1, 1], [1, 1, 0]],
    [[1, 1, 0], [0, 1, 1]],
]

screen = pygame.display.set_mode((SCREEN_WIDTH + SIDE_PANEL_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tetris")
clock = pygame.time.Clock()
font = pygame.font.Font(pygame.font.get_default_font(), 20)

class Tetrimino:
    def __init__(self):
        self.shape = random.choice(SHAPES)
        self.color = random.choice(COLORS)
        self.x = COLUMNS // 2 - len(self.shape[0]) // 2
        self.y = 0

    def rotate(self):
        self.shape = [list(row) for row in zip(*self.shape[::-1])]

def check_collision(grid, shape, offset_x, offset_y):
    for y, row in enumerate(shape):
        for x, cell in enumerate(row):
            if cell:
                new_x = x + offset_x
                new_y = y + offset_y
                if (
                    new_x < 0
                    or new_x >= COLUMNS
                    or new_y >= ROWS
                    or (new_y >= 0 and grid[new_y][new_x])
                ):
                    return True
    return False

def merge_tetrimino(grid, tetrimino):
    for y, row in enumerate(tetrimino.shape):
        for x, cell in enumerate(row):
            if cell:
                grid[tetrimino.y + y][tetrimino.x + x] = tetrimino.color

def clear_rows(grid):
    full_rows = [i for i, row in enumerate(grid) if all(row)]
    for row in full_rows:
        del grid[row]
        grid.insert(0, [None] * COLUMNS)
    return len(full_rows)

def draw_grid(surface, grid):
    surface.fill(BLACK)
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell:
                pygame.draw.rect(
                    surface,
                    cell,
                    (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE),
                )
                pygame.draw.rect(
                    surface,
                    BLACK,
                    (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE),
                    2,
                )
    for x in range(COLUMNS):
        pygame.draw.line(surface, GRAY, (x * GRID_SIZE, 0), (x * GRID_SIZE, SCREEN_HEIGHT))
    for y in range(ROWS):
        pygame.draw.line(surface, GRAY, (0, y * GRID_SIZE), (SCREEN_WIDTH, y * GRID_SIZE))

def draw_tetrimino(surface, tetrimino):
    for y, row in enumerate(tetrimino.shape):
        for x, cell in enumerate(row):
            if cell:
                pygame.draw.rect(
                    surface,
                    tetrimino.color,
                    (
                        (tetrimino.x + x) * GRID_SIZE,
                        (tetrimino.y + y) * GRID_SIZE,
                        GRID_SIZE,
                        GRID_SIZE,
                    ),
                )
                pygame.draw.rect(
                    surface,
                    DARK_GRAY,
                    (
                        (tetrimino.x + x) * GRID_SIZE,
                        (tetrimino.y + y) * GRID_SIZE,
                        GRID_SIZE,
                        GRID_SIZE,
                    ),
                    2,
                )

def draw_next_tetrimino(surface, next_tetrimino):
    label = font.render("Next: ", True, WHITE)
    surface.blit(label, (SCREEN_WIDTH + 10, 10))
    for y, row in enumerate(next_tetrimino.shape):
        for x, cell in enumerate(row):
            if cell:
                pygame.draw.rect(
                    surface,
                    next_tetrimino.color,
                    (
                        SCREEN_WIDTH + 10 + x * GRID_SIZE,
                        30 + y * GRID_SIZE,
                        GRID_SIZE,
                        GRID_SIZE,
                    ),
                )
                pygame.draw.rect(
                    surface,
                    DARK_GRAY,
                    (
                        SCREEN_WIDTH + 10 + x * GRID_SIZE,
                        30 + y * GRID_SIZE,
                        GRID_SIZE,
                        GRID_SIZE,
                    ),
                    2,
                )

def draw_score(surface, score):
    label = font.render(f"Score: {score}", True, WHITE)
    surface.blit(label, (SCREEN_WIDTH + 10, 150))

def draw_level(surface, level):
    label = font.render(f"Level: {level}", True, WHITE)
    surface.blit(label, (SCREEN_WIDTH + 10, 200))

def main():
    grid = [[None for _ in range(COLUMNS)] for _ in range(ROWS)]
    tetrimino = Tetrimino()
    next_tetrimino = Tetrimino()
    fall_time = 0
    level = 1
    fall_speed = 500
    score = 0
    lines_cleared = 0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if not check_collision(grid, tetrimino.shape, tetrimino.x - 1, tetrimino.y):
                        tetrimino.x -= 1
                if event.key == pygame.K_RIGHT:
                    if not check_collision(grid, tetrimino.shape, tetrimino.x + 1, tetrimino.y):
                        tetrimino.x += 1
                if event.key == pygame.K_DOWN:
                    if not check_collision(grid, tetrimino.shape, tetrimino.x, tetrimino.y + 1):
                        tetrimino.y += 1
                if event.key == pygame.K_UP:
                    old_shape = tetrimino.shape[:]
                    tetrimino.rotate()
                    if check_collision(grid, tetrimino.shape, tetrimino.x, tetrimino.y):
                        tetrimino.shape = old_shape

        fall_time += clock.get_rawtime()
        clock.tick()

        if fall_time > fall_speed:
            fall_time = 0
            if not check_collision(grid, tetrimino.shape, tetrimino.x, tetrimino.y + 1):
                tetrimino.y += 1
            else:
                merge_tetrimino(grid, tetrimino)
                lines_cleared += clear_rows(grid)
                score += lines_cleared * 10
                level = lines_cleared // 10 + 1
                fall_speed = max(50, 500 - (level - 1) * 50)
                tetrimino = next_tetrimino
                next_tetrimino = Tetrimino()

                if check_collision(grid, tetrimino.shape, tetrimino.x, tetrimino.y):
                    print("Game Over! Final Score:", score)
                    running = False

        draw_grid(screen, grid)
        draw_tetrimino(screen, tetrimino)
        draw_next_tetrimino(screen, next_tetrimino)
        draw_score(screen, score)
        draw_level(screen, level)
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
