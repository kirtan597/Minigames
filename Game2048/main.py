import pygame
import random
import sys

pygame.init()

# Screen dimensions
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

# Game constants
GRID_SIZE = 4
CELL_SIZE = 100
GRID_GAP = 10
GRID_WIDTH = GRID_SIZE * CELL_SIZE + (GRID_SIZE + 1) * GRID_GAP
GRID_HEIGHT = GRID_WIDTH

# Colors
COLOR_BG = (15, 23, 42)
COLOR_GRID_BG = (187, 173, 160)
COLOR_TEXT = (229, 231, 235)
COLOR_WHITE = (255, 255, 255)

TILE_COLORS = {
    2: (238, 228, 218),
    4: (237, 224, 200),
    8: (242, 177, 121),
    16: (245, 149, 99),
    32: (246, 124, 95),
    64: (246, 94, 59),
    128: (236, 206, 116),
    256: (236, 201, 75),
    512: (235, 195, 40),
    1024: (228, 155, 58),
    2048: (228, 155, 58),
    4096: (60, 58, 50),
}

TILE_TEXT_COLORS = {
    2: (119, 110, 101),
    4: (119, 110, 101),
    8: (249, 246, 242),
    16: (249, 246, 242),
    32: (249, 246, 242),
    64: (249, 246, 242),
    128: (249, 246, 242),
    256: (249, 246, 242),
    512: (249, 246, 242),
    1024: (249, 246, 242),
    2048: (249, 246, 242),
    4096: (249, 246, 242),
}

class Game2048:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("2048 - Puzzle Game")
        self.clock = pygame.time.Clock()
        self.font_title = pygame.font.Font(None, 64)
        self.font_score = pygame.font.Font(None, 40)
        self.font_tile = pygame.font.Font(None, 48)
        self.font_small = pygame.font.Font(None, 24)
        
        # Grid position
        self.grid_x = (SCREEN_WIDTH - GRID_WIDTH) // 2
        self.grid_y = (SCREEN_HEIGHT - GRID_HEIGHT) // 2 + 50
        
        # Game state
        self.grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.score = 0
        self.best_score = 0
        self.game_over = False
        self.won = False
        self.moved = False
        
        self.add_tile()
        self.add_tile()

    def add_tile(self):
        empty_cells = []
        for y in range(GRID_SIZE):
            for x in range(GRID_SIZE):
                if self.grid[y][x] == 0:
                    empty_cells.append((x, y))
        
        if empty_cells:
            x, y = random.choice(empty_cells)
            self.grid[y][x] = 2 if random.random() < 0.9 else 4

    def move(self, direction):
        if direction == "LEFT":
            self.grid = [self.slide_left(row) for row in self.grid]
        elif direction == "RIGHT":
            self.grid = [self.slide_right(row) for row in self.grid]
        elif direction == "UP":
            self.grid = list(zip(*[self.slide_left(list(col)) for col in zip(*self.grid)]))
            self.grid = [list(row) for row in self.grid]
        elif direction == "DOWN":
            self.grid = list(zip(*[self.slide_right(list(col)) for col in zip(*self.grid)]))
            self.grid = [list(row) for row in self.grid]
        
        if self.moved:
            self.add_tile()
            self.check_game_state()

    def slide_left(self, row):
        def merge(arr):
            merged = []
            skip = False
            for i in range(len(arr)):
                if skip:
                    skip = False
                    continue
                if i + 1 < len(arr) and arr[i] == arr[i + 1]:
                    merged.append(arr[i] * 2)
                    self.score += arr[i] * 2
                    skip = True
                elif arr[i] != 0:
                    merged.append(arr[i])
            return merged + [0] * (len(arr) - len(merged))
        
        new_row = [val for val in row if val != 0]
        new_row = merge(new_row)
        self.moved = new_row != row
        return new_row

    def slide_right(self, row):
        reversed_row = row[::-1]
        result = self.slide_left(reversed_row)
        return result[::-1]

    def check_game_state(self):
        # Check for win
        for row in self.grid:
            if 2048 in row:
                self.won = True
        
        # Check for possible moves
        for y in range(GRID_SIZE):
            for x in range(GRID_SIZE):
                if self.grid[y][x] == 0:
                    return
                
                current = self.grid[y][x]
                
                if x < GRID_SIZE - 1 and self.grid[y][x + 1] == current:
                    return
                if y < GRID_SIZE - 1 and self.grid[y + 1][x] == current:
                    return
        
        self.game_over = True
        self.best_score = max(self.best_score, self.score)

    def draw(self):
        self.screen.fill(COLOR_BG)
        
        # Draw title
        title = self.font_title.render("2048 PUZZLE", True, (0, 255, 200))
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 30))
        self.screen.blit(title, title_rect)
        
        # Draw scores
        score_text = self.font_score.render(f"Score: {self.score}", True, COLOR_WHITE)
        self.screen.blit(score_text, (50, 60))
        
        best_text = self.font_score.render(f"Best: {self.best_score}", True, COLOR_WHITE)
        best_rect = best_text.get_rect(right=SCREEN_WIDTH - 50, top=60)
        self.screen.blit(best_text, best_rect)
        
        # Draw grid background
        grid_rect = pygame.Rect(self.grid_x, self.grid_y, GRID_WIDTH, GRID_HEIGHT)
        pygame.draw.rect(self.screen, COLOR_GRID_BG, grid_rect, border_radius=10)
        
        # Draw tiles
        for y in range(GRID_SIZE):
            for x in range(GRID_SIZE):
                tile_x = self.grid_x + x * (CELL_SIZE + GRID_GAP) + GRID_GAP
                tile_y = self.grid_y + y * (CELL_SIZE + GRID_GAP) + GRID_GAP
                
                value = self.grid[y][x]
                
                if value == 0:
                    color = (205, 192, 180)
                else:
                    color = TILE_COLORS.get(value, (100, 100, 100))
                
                tile_rect = pygame.Rect(tile_x, tile_y, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(self.screen, color, tile_rect, border_radius=5)
                
                if value > 0:
                    text_color = TILE_TEXT_COLORS.get(value, COLOR_WHITE)
                    tile_text = self.font_tile.render(str(value), True, text_color)
                    text_rect = tile_text.get_rect(center=(tile_x + CELL_SIZE // 2, tile_y + CELL_SIZE // 2))
                    self.screen.blit(tile_text, text_rect)
        
        # Draw instructions
        controls_y = self.grid_y + GRID_HEIGHT + 30
        instructions = [
            "Arrow Keys: Move tiles | N: New Game | ESC: Menu"
        ]
        for i, text in enumerate(instructions):
            inst_text = self.font_small.render(text, True, COLOR_TEXT)
            self.screen.blit(inst_text, (50, controls_y + i * 30))
        
        # Draw game over
        if self.game_over:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(200)
            overlay.fill((0, 0, 0))
            self.screen.blit(overlay, (0, 0))
            
            game_over_text = self.font_title.render("GAME OVER!", True, (255, 100, 100))
            game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
            self.screen.blit(game_over_text, game_over_rect)
            
            final_score = self.font_score.render(f"Final Score: {self.score}", True, COLOR_WHITE)
            final_rect = final_score.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
            self.screen.blit(final_score, final_rect)
        
        # Draw won message
        if self.won:
            won_text = self.font_title.render("YOU WON! 🎉", True, (100, 255, 100))
            won_rect = won_text.get_rect(center=(SCREEN_WIDTH // 2, 200))
            self.screen.blit(won_text, won_rect)

    def run(self):
        running = True
        
        while running:
            self.clock.tick(60)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key == pygame.K_LEFT:
                        self.move("LEFT")
                    elif event.key == pygame.K_RIGHT:
                        self.move("RIGHT")
                    elif event.key == pygame.K_UP:
                        self.move("UP")
                    elif event.key == pygame.K_DOWN:
                        self.move("DOWN")
                    elif event.key == pygame.K_n:
                        self.__init__()
            
            self.draw()
            pygame.display.update()
        
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = Game2048()
    game.run()
