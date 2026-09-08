import pygame
import random
import sys
import math

pygame.init()

# Screen dimensions (Widescreen)
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

# Tetris field dimensions
FIELD_WIDTH = 10
FIELD_HEIGHT = 20
CELL_SIZE = 30

# Colors
COLOR_BG = (15, 23, 42)
COLOR_FIELD_BG = (20, 30, 50)
COLOR_BORDER = (100, 150, 255)
COLOR_TEXT = (229, 231, 235)
COLOR_WHITE = (255, 255, 255)
COLOR_RED = (255, 59, 48)
COLOR_CYAN = (0, 255, 255)
COLOR_BLUE = (0, 0, 255)
COLOR_ORANGE = (255, 140, 0)
COLOR_YELLOW = (255, 255, 0)
COLOR_GREEN = (0, 255, 0)
COLOR_PURPLE = (128, 0, 128)

# Tetromino shapes
TETROMINOES = {
    'I': [[1, 1, 1, 1]],
    'O': [[1, 1], [1, 1]],
    'T': [[0, 1, 0], [1, 1, 1]],
    'S': [[0, 1, 1], [1, 1, 0]],
    'Z': [[1, 1, 0], [0, 1, 1]],
    'J': [[1, 0, 0], [1, 1, 1]],
    'L': [[0, 0, 1], [1, 1, 1]]
}

TETROMINO_COLORS = {
    'I': COLOR_CYAN,
    'O': COLOR_YELLOW,
    'T': COLOR_PURPLE,
    'S': COLOR_GREEN,
    'Z': COLOR_RED,
    'J': COLOR_BLUE,
    'L': COLOR_ORANGE
}

class Tetris:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("🧱 Tetris - Widescreen Edition")
        self.clock = pygame.time.Clock()
        self.font_title = pygame.font.Font(None, 64)
        self.font_large = pygame.font.Font(None, 48)
        self.font_medium = pygame.font.Font(None, 36)
        self.font_small = pygame.font.Font(None, 24)
        
        # Calculate field position (centered)
        self.field_x = (SCREEN_WIDTH - FIELD_WIDTH * CELL_SIZE) // 2
        self.field_y = (SCREEN_HEIGHT - FIELD_HEIGHT * CELL_SIZE) // 2
        
        # Initialize game state
        self.field = [[0 for _ in range(FIELD_WIDTH)] for _ in range(FIELD_HEIGHT)]
        self.current_piece = None
        self.current_color = None
        self.piece_x = 0
        self.piece_y = 0
        self.score = 0
        self.level = 1
        self.lines_cleared = 0
        self.game_over = False
        self.paused = False
        self.fall_time = 0
        self.fall_speed = 500  # ms
        
        self.spawn_new_piece()

    def spawn_new_piece(self):
        piece_type = random.choice(list(TETROMINOES.keys()))
        self.current_piece = TETROMINOES[piece_type]
        self.current_color = TETROMINO_COLORS[piece_type]
        self.piece_x = FIELD_WIDTH // 2 - len(self.current_piece[0]) // 2
        self.piece_y = 0
        
        # Check if piece can spawn (game over if not)
        if not self.can_place():
            self.game_over = True

    def can_place(self):
        for y, row in enumerate(self.current_piece):
            for x, cell in enumerate(row):
                if cell:
                    board_x = self.piece_x + x
                    board_y = self.piece_y + y
                    
                    if board_x < 0 or board_x >= FIELD_WIDTH or board_y >= FIELD_HEIGHT:
                        return False
                    if board_y >= 0 and self.field[board_y][board_x]:
                        return False
        return True

    def place_piece(self):
        for y, row in enumerate(self.current_piece):
            for x, cell in enumerate(row):
                if cell:
                    board_x = self.piece_x + x
                    board_y = self.piece_y + y
                    if 0 <= board_y < FIELD_HEIGHT:
                        self.field[board_y][board_x] = 1

    def clear_lines(self):
        lines_to_clear = []
        for y in range(FIELD_HEIGHT):
            if all(self.field[y]):
                lines_to_clear.append(y)
        
        for y in reversed(lines_to_clear):
            del self.field[y]
            self.field.insert(0, [0] * FIELD_WIDTH)
        
        if lines_to_clear:
            cleared = len(lines_to_clear)
            self.lines_cleared += cleared
            
            # Score calculation
            line_multipliers = {1: 100, 2: 300, 3: 500, 4: 800}
            self.score += line_multipliers.get(cleared, 800) * self.level
            
            # Level up every 10 lines
            self.level = 1 + self.lines_cleared // 10
            self.fall_speed = max(100, 500 - self.level * 30)

    def move_piece(self, dx, dy):
        self.piece_x += dx
        self.piece_y += dy
        
        if not self.can_place():
            self.piece_x -= dx
            self.piece_y -= dy
            return False
        return True

    def rotate_piece(self):
        # Rotate 90 degrees clockwise
        rotated = list(zip(*self.current_piece[::-1]))
        rotated = [list(row) for row in rotated]
        
        old_piece = self.current_piece
        self.current_piece = rotated
        
        if not self.can_place():
            self.current_piece = old_piece
            return False
        return True

    def update(self, dt):
        if self.game_over or self.paused:
            return
        
        self.fall_time += dt
        
        if self.fall_time >= self.fall_speed:
            self.fall_time = 0
            if not self.move_piece(0, 1):
                self.place_piece()
                self.clear_lines()
                self.spawn_new_piece()

    def draw(self):
        self.screen.fill(COLOR_BG)
        
        # Draw title
        title = self.font_title.render("🧱 TETRIS", True, (0, 255, 255))
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 30))
        self.screen.blit(title, title_rect)
        
        # Draw field background
        field_rect = pygame.Rect(
            self.field_x - 5,
            self.field_y - 5,
            FIELD_WIDTH * CELL_SIZE + 10,
            FIELD_HEIGHT * CELL_SIZE + 10
        )
        pygame.draw.rect(self.screen, COLOR_FIELD_BG, field_rect)
        pygame.draw.rect(self.screen, COLOR_BORDER, field_rect, 2)
        
        # Draw field cells
        for y in range(FIELD_HEIGHT):
            for x in range(FIELD_WIDTH):
                if self.field[y][x]:
                    rect = pygame.Rect(
                        self.field_x + x * CELL_SIZE,
                        self.field_y + y * CELL_SIZE,
                        CELL_SIZE - 1,
                        CELL_SIZE - 1
                    )
                    pygame.draw.rect(self.screen, (100, 100, 100), rect)
                    pygame.draw.rect(self.screen, (150, 150, 150), rect, 1)
        
        # Draw current piece
        if self.current_piece and not self.game_over:
            for y, row in enumerate(self.current_piece):
                for x, cell in enumerate(row):
                    if cell:
                        rect = pygame.Rect(
                            self.field_x + (self.piece_x + x) * CELL_SIZE,
                            self.field_y + (self.piece_y + y) * CELL_SIZE,
                            CELL_SIZE - 1,
                            CELL_SIZE - 1
                        )
                        pygame.draw.rect(self.screen, self.current_color, rect)
                        pygame.draw.rect(self.screen, COLOR_WHITE, rect, 2)
        
        # Draw stats panel
        stats_x = self.field_x + FIELD_WIDTH * CELL_SIZE + 50
        
        score_text = self.font_large.render(f"Score: {self.score}", True, (0, 255, 100))
        self.screen.blit(score_text, (stats_x, 100))
        
        level_text = self.font_medium.render(f"Level: {self.level}", True, (100, 200, 255))
        self.screen.blit(level_text, (stats_x, 180))
        
        lines_text = self.font_medium.render(f"Lines: {self.lines_cleared}", True, (255, 150, 0))
        self.screen.blit(lines_text, (stats_x, 250))
        
        # Draw controls
        controls_y = 400
        controls = [
            "CONTROLS:",
            "← → Move",
            "↑ Rotate",
            "↓ Drop",
            "P Pause",
            "ESC Menu"
        ]
        for i, text in enumerate(controls):
            control_text = self.font_small.render(text, True, COLOR_TEXT)
            self.screen.blit(control_text, (stats_x, controls_y + i * 30))
        
        # Draw game over
        if self.game_over:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(200)
            overlay.fill((0, 0, 0))
            self.screen.blit(overlay, (0, 0))
            
            game_over_text = self.font_title.render("GAME OVER!", True, COLOR_RED)
            game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
            self.screen.blit(game_over_text, game_over_rect)
            
            final_score = self.font_large.render(f"Final Score: {self.score}", True, COLOR_WHITE)
            final_rect = final_score.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
            self.screen.blit(final_score, final_rect)
        
        # Draw paused
        if self.paused:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(150)
            overlay.fill((0, 0, 0))
            self.screen.blit(overlay, (0, 0))
            
            paused_text = self.font_title.render("PAUSED", True, COLOR_WHITE)
            paused_rect = paused_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            self.screen.blit(paused_text, paused_rect)

    def run(self):
        running = True
        
        while running:
            dt = self.clock.tick(60)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key == pygame.K_LEFT:
                        self.move_piece(-1, 0)
                    elif event.key == pygame.K_RIGHT:
                        self.move_piece(1, 0)
                    elif event.key == pygame.K_DOWN:
                        self.move_piece(0, 1)
                    elif event.key == pygame.K_UP:
                        self.rotate_piece()
                    elif event.key == pygame.K_SPACE:
                        while self.move_piece(0, 1):
                            pass
                    elif event.key == pygame.K_p:
                        self.paused = not self.paused
                    elif event.key == pygame.K_r and self.game_over:
                        self.__init__()
            
            self.update(dt)
            self.draw()
            pygame.display.update()
        
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    tetris = Tetris()
    tetris.run()
