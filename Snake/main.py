"""
Snake Game - Minigames Central
Classic snake gameplay with smooth movement and scoring
"""

import pygame
import random
import sys
from data_manager import get_data_manager
from enum import Enum

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

# Game grid
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Colors
BG_COLOR = (10, 20, 40)
SNAKE_COLOR = (76, 255, 127)
FOOD_COLOR = (255, 100, 100)
TEXT_COLOR = (255, 255, 255)
GRID_COLOR = (30, 40, 80)

# Frame rate - Balanced for playability
FRAME_RATE = 12  # Slightly faster for better responsiveness

class Direction(Enum):
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)

class SnakeGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("🐍 Snake - Minigames Central")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 48)
        self.font_small = pygame.font.Font(None, 32)
        
        self.data_manager = get_data_manager()
        self.reset_game()

    def reset_game(self):
        # Snake starts in center
        start_x = GRID_WIDTH // 2
        start_y = GRID_HEIGHT // 2
        
        self.snake = [
            (start_x, start_y),
            (start_x - 1, start_y),
            (start_x - 2, start_y)
        ]
        
        self.direction = Direction.RIGHT
        self.next_direction = Direction.RIGHT
        self.food = self.spawn_food()
        self.score = 0
        self.game_over = False
        self.start_time = pygame.time.get_ticks()

    def spawn_food(self):
        while True:
            x = random.randint(0, GRID_WIDTH - 1)
            y = random.randint(0, GRID_HEIGHT - 1)
            if (x, y) not in self.snake:
                return (x, y)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                elif event.key == pygame.K_UP and self.direction != Direction.DOWN:
                    self.next_direction = Direction.UP
                elif event.key == pygame.K_DOWN and self.direction != Direction.UP:
                    self.next_direction = Direction.DOWN
                elif event.key == pygame.K_LEFT and self.direction != Direction.RIGHT:
                    self.next_direction = Direction.LEFT
                elif event.key == pygame.K_RIGHT and self.direction != Direction.LEFT:
                    self.next_direction = Direction.RIGHT
                elif event.key == pygame.K_SPACE and self.game_over:
                    self.reset_game()
        return True

    def update(self):
        if not self.game_over:
            self.direction = self.next_direction
            
            # Calculate new head
            head_x, head_y = self.snake[0]
            dx, dy = self.direction.value
            new_head = (head_x + dx, head_y + dy)
            
            # Check collisions with walls
            if (new_head[0] < 0 or new_head[0] >= GRID_WIDTH or
                new_head[1] < 0 or new_head[1] >= GRID_HEIGHT):
                self.game_over = True
                return
            
            # Check collision with self
            if new_head in self.snake:
                self.game_over = True
                return
            
            # Add new head
            self.snake.insert(0, new_head)
            
            # Check if food eaten
            if new_head == self.food:
                self.score += 10
                self.food = self.spawn_food()
            else:
                self.snake.pop()

    def draw(self):
        self.screen.fill(BG_COLOR)
        
        # Draw grid
        for x in range(0, SCREEN_WIDTH, GRID_SIZE):
            pygame.draw.line(self.screen, GRID_COLOR, (x, 0), (x, SCREEN_HEIGHT))
        for y in range(0, SCREEN_HEIGHT, GRID_SIZE):
            pygame.draw.line(self.screen, GRID_COLOR, (0, y), (SCREEN_WIDTH, y))
        
        # Draw snake
        for i, (x, y) in enumerate(self.snake):
            rect = pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE - 2, GRID_SIZE - 2)
            color = tuple(min(255, c + 40) for c in SNAKE_COLOR) if i == 0 else SNAKE_COLOR
            pygame.draw.rect(self.screen, color, rect)
            pygame.draw.rect(self.screen, (200, 255, 200), rect, 2)
        
        # Draw food
        food_x, food_y = self.food
        food_rect = pygame.Rect(food_x * GRID_SIZE + 2, food_y * GRID_SIZE + 2,
                               GRID_SIZE - 4, GRID_SIZE - 4)
        pygame.draw.circle(self.screen, FOOD_COLOR,
                          (food_x * GRID_SIZE + GRID_SIZE // 2,
                           food_y * GRID_SIZE + GRID_SIZE // 2), GRID_SIZE // 2 - 2)
        
        # Draw score
        score_text = self.font.render(f"Score: {self.score}", True, TEXT_COLOR)
        self.screen.blit(score_text, (20, 20))
        
        # Draw game over
        if self.game_over:
            elapsed_time = (pygame.time.get_ticks() - self.start_time) // 1000
            self.draw_game_over(elapsed_time)
        
        pygame.display.update()

    def draw_game_over(self, elapsed_time):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))
        
        game_over_text = self.font.render("GAME OVER", True, (255, 100, 100))
        game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 80))
        self.screen.blit(game_over_text, game_over_rect)
        
        final_score_text = self.font.render(f"Final Score: {self.score}", True, TEXT_COLOR)
        final_score_rect = final_score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(final_score_text, final_score_rect)
        
        time_text = self.font_small.render(f"Time: {elapsed_time}s", True, TEXT_COLOR)
        time_rect = time_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60))
        self.screen.blit(time_text, time_rect)
        
        restart_text = self.font_small.render("Press SPACE to play again or ESC to exit", True, TEXT_COLOR)
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 120))
        self.screen.blit(restart_text, restart_rect)

    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FRAME_RATE)
        
        # Save score
        if self.score > 0:
            self.data_manager.add_high_score("snake", "Player", self.score)
        
        pygame.quit()
        sys.exit()


def main():
    try:
        game = SnakeGame()
        game.run()
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
