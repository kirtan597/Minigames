"""
Pong Game - Minigames Central
Classic Pong gameplay: Player vs Computer AI
"""

import pygame
import sys
from data_manager import get_data_manager

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

# Colors
BG_COLOR = (10, 20, 40)
PADDLE_COLOR = (255, 215, 0)
BALL_COLOR = (255, 255, 255)
TEXT_COLOR = (255, 255, 255)

# Paddle
PADDLE_WIDTH = 15
PADDLE_HEIGHT = 100
PADDLE_SPEED = 8

# Ball
BALL_SIZE = 12
BALL_SPEED_X = 6
BALL_SPEED_Y = 6
MAX_BALL_SPEED = 10

# Frame rate
FRAME_RATE = 60

class Paddle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = PADDLE_WIDTH
        self.height = PADDLE_HEIGHT
        self.speed = PADDLE_SPEED
        self.rect = pygame.Rect(x, y, self.width, self.height)

    def move_up(self):
        if self.y > 0:
            self.y -= self.speed
            self.rect.y = self.y

    def move_down(self):
        if self.y + self.height < SCREEN_HEIGHT:
            self.y += self.speed
            self.rect.y = self.y

    def draw(self, screen):
        pygame.draw.rect(screen, PADDLE_COLOR, self.rect)

    def get_rect(self):
        return self.rect


class Ball:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = BALL_SPEED_X
        self.vy = BALL_SPEED_Y
        self.size = BALL_SIZE

    def update(self):
        self.x += self.vx
        self.y += self.vy
        
        # Wall collisions (top/bottom)
        if self.y - self.size < 0 or self.y + self.size > SCREEN_HEIGHT:
            self.vy = -self.vy

    def draw(self, screen):
        pygame.draw.circle(screen, BALL_COLOR, (int(self.x), int(self.y)), self.size)

    def check_paddle_collision(self, paddle):
        ball_rect = pygame.Rect(self.x - self.size, self.y - self.size,
                               self.size * 2, self.size * 2)
        
        if ball_rect.colliderect(paddle.get_rect()):
            self.vx = -self.vx
            self.x = self.x + self.vx * 2  # Move ball away from paddle
            
            # Add spin based on paddle hit location
            paddle_center = paddle.y + PADDLE_HEIGHT // 2
            diff = (self.y - paddle_center) / PADDLE_HEIGHT
            self.vy += diff * 4
            
            # Cap speed
            if abs(self.vy) > MAX_BALL_SPEED:
                self.vy = MAX_BALL_SPEED if self.vy > 0 else -MAX_BALL_SPEED
            
            return True
        return False

    def is_out_of_bounds(self):
        return self.x < 0 or self.x > SCREEN_WIDTH

    def reset(self):
        self.x = SCREEN_WIDTH // 2
        self.y = SCREEN_HEIGHT // 2
        self.vx = BALL_SPEED_X
        self.vy = BALL_SPEED_Y


class PongGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("🏓 Pong - Minigames Central")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 64)
        self.font_small = pygame.font.Font(None, 32)
        
        self.data_manager = get_data_manager()
        self.reset_game()

    def reset_game(self):
        self.player = Paddle(SCREEN_WIDTH - PADDLE_WIDTH - 20, SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2)
        self.ai = Paddle(20, SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2)
        self.ball = Ball(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        
        self.player_score = 0
        self.ai_score = 0
        self.game_over = False
        self.start_time = pygame.time.get_ticks()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                elif event.key == pygame.K_SPACE and self.game_over:
                    self.reset_game()
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.player.move_up()
        if keys[pygame.K_DOWN]:
            self.player.move_down()
        
        return True

    def update_ai(self):
        # Simple AI: move towards ball
        ai_center = self.ai.y + PADDLE_HEIGHT // 2
        
        if ai_center < self.ball.y - 20:
            self.ai.move_down()
        elif ai_center > self.ball.y + 20:
            self.ai.move_up()

    def update(self):
        if not self.game_over:
            self.ball.update()
            self.update_ai()
            
            # Check paddle collisions
            self.ball.check_paddle_collision(self.player)
            self.ball.check_paddle_collision(self.ai)
            
            # Check scoring
            if self.ball.is_out_of_bounds():
                if self.ball.x < 0:
                    self.player_score += 1
                else:
                    self.ai_score += 1
                
                self.ball.reset()
            
            # Check win condition (first to 11)
            if self.player_score >= 11 or self.ai_score >= 11:
                self.game_over = True

    def draw(self):
        self.screen.fill(BG_COLOR)
        
        # Draw center line
        for y in range(0, SCREEN_HEIGHT, 20):
            pygame.draw.line(self.screen, (100, 100, 150), 
                            (SCREEN_WIDTH // 2, y), 
                            (SCREEN_WIDTH // 2, y + 10), 2)
        
        # Draw paddles and ball
        self.player.draw(self.screen)
        self.ai.draw(self.screen)
        self.ball.draw(self.screen)
        
        # Draw scores
        player_score_text = self.font.render(str(self.player_score), True, TEXT_COLOR)
        ai_score_text = self.font.render(str(self.ai_score), True, TEXT_COLOR)
        
        self.screen.blit(player_score_text, (SCREEN_WIDTH - 100, 30))
        self.screen.blit(ai_score_text, (100, 30))
        
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
        
        winner = "You Win!" if self.player_score > self.ai_score else "AI Wins!"
        winner_color = (100, 255, 100) if self.player_score > self.ai_score else (255, 100, 100)
        
        winner_text = self.font.render(winner, True, winner_color)
        winner_rect = winner_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 80))
        self.screen.blit(winner_text, winner_rect)
        
        score_text = self.font.render(f"{self.player_score} - {self.ai_score}", True, TEXT_COLOR)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(score_text, score_rect)
        
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
        
        # Save score (use player score as final score)
        if self.player_score > 0:
            self.data_manager.add_high_score("pong", "Player", self.player_score)
        
        pygame.quit()
        sys.exit()


def main():
    try:
        game = PongGame()
        game.run()
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
