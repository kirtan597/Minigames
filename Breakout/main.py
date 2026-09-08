import pygame
import random
import sys
import math

pygame.init()

# Screen dimensions
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

# Colors
COLOR_BG = (15, 23, 42)
COLOR_TEXT = (229, 231, 235)
COLOR_WHITE = (255, 255, 255)
COLOR_PADDLE = (0, 255, 100)
COLOR_BALL = (255, 255, 0)
COLOR_BRICK = [(255, 50, 50), (255, 100, 50), (255, 150, 50), (255, 200, 50), (100, 200, 255)]

class Ball:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = 5
        self.vy = -5
        self.radius = 8

    def update(self):
        self.x += self.vx
        self.y += self.vy
        
        # Bounce off walls
        if self.x - self.radius < 0 or self.x + self.radius > SCREEN_WIDTH:
            self.vx = -self.vx
            self.x = max(self.radius, min(SCREEN_WIDTH - self.radius, self.x))
        
        if self.y - self.radius < 0:
            self.vy = -self.vy
            self.y = self.radius

    def draw(self, screen):
        pygame.draw.circle(screen, COLOR_BALL, (int(self.x), int(self.y)), self.radius)

class Paddle:
    def __init__(self):
        self.width = 100
        self.height = 15
        self.x = SCREEN_WIDTH // 2 - self.width // 2
        self.y = SCREEN_HEIGHT - 40
        self.speed = 7

    def move(self, direction):
        if direction == "LEFT":
            self.x = max(0, self.x - self.speed)
        elif direction == "RIGHT":
            self.x = min(SCREEN_WIDTH - self.width, self.x + self.speed)

    def draw(self, screen):
        pygame.draw.rect(screen, COLOR_PADDLE, (self.x, self.y, self.width, self.height), border_radius=5)

class Brick:
    def __init__(self, x, y, color_idx):
        self.x = x
        self.y = y
        self.width = 60
        self.height = 20
        self.color = COLOR_BRICK[color_idx % len(COLOR_BRICK)]
        self.alive = True

    def draw(self, screen):
        if self.alive:
            pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height), border_radius=3)
            pygame.draw.rect(screen, COLOR_WHITE, (self.x, self.y, self.width, self.height), 1, border_radius=3)

class Breakout:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("🧱 Breakout - Break Those Bricks!")
        self.clock = pygame.time.Clock()
        self.font_title = pygame.font.Font(None, 64)
        self.font_large = pygame.font.Font(None, 48)
        self.font_medium = pygame.font.Font(None, 36)
        self.font_small = pygame.font.Font(None, 24)
        
        self.paddle = Paddle()
        self.ball = Ball(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100)
        self.bricks = []
        self.score = 0
        self.lives = 3
        self.game_over = False
        self.won = False
        self.ball_attached = True
        
        self.create_bricks()

    def create_bricks(self):
        self.bricks = []
        brick_width = 60
        brick_height = 20
        rows = 4
        cols = 18
        gap = 5
        
        start_x = (SCREEN_WIDTH - (cols * (brick_width + gap))) // 2
        start_y = 50
        
        for row in range(rows):
            for col in range(cols):
                x = start_x + col * (brick_width + gap)
                y = start_y + row * (brick_height + gap)
                self.bricks.append(Brick(x, y, row))

    def check_collisions(self):
        # Paddle collision
        paddle_rect = pygame.Rect(self.paddle.x, self.paddle.y, self.paddle.width, self.paddle.height)
        ball_rect = pygame.Rect(self.ball.x - self.ball.radius, self.ball.y - self.ball.radius, 
                               self.ball.radius * 2, self.ball.radius * 2)
        
        if paddle_rect.colliderect(ball_rect):
            if self.ball.vy > 0:
                self.ball.vy = -abs(self.ball.vy)
                hit_pos = (self.ball.x - self.paddle.x) / self.paddle.width
                self.ball.vx = (hit_pos - 0.5) * 8

        # Brick collisions
        for brick in self.bricks:
            if brick.alive:
                brick_rect = pygame.Rect(brick.x, brick.y, brick.width, brick.height)
                
                if ball_rect.colliderect(brick_rect):
                    brick.alive = False
                    self.score += 10
                    
                    # Bounce
                    overlap_x = min(abs(ball_rect.right - brick_rect.left), 
                                   abs(ball_rect.left - brick_rect.right))
                    overlap_y = min(abs(ball_rect.bottom - brick_rect.top), 
                                   abs(ball_rect.top - brick_rect.bottom))
                    
                    if overlap_x < overlap_y:
                        self.ball.vx = -self.ball.vx
                    else:
                        self.ball.vy = -self.ball.vy

        # Check if ball falls
        if self.ball.y > SCREEN_HEIGHT:
            self.lives -= 1
            if self.lives <= 0:
                self.game_over = True
            else:
                self.ball_attached = True
                self.ball = Ball(self.paddle.x + self.paddle.width // 2, self.paddle.y - 20)

        # Check if won
        if all(not brick.alive for brick in self.bricks):
            self.won = True

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.paddle.move("LEFT")
        if keys[pygame.K_RIGHT]:
            self.paddle.move("RIGHT")
        
        if self.ball_attached:
            self.ball.x = self.paddle.x + self.paddle.width // 2
            self.ball.y = self.paddle.y - 20
        else:
            self.ball.update()
        
        if not self.game_over and not self.won:
            self.check_collisions()

    def draw(self):
        self.screen.fill(COLOR_BG)
        
        # Draw title
        title = self.font_title.render("🧱 BREAKOUT", True, (0, 255, 150))
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 20))
        self.screen.blit(title, title_rect)
        
        # Draw score and lives
        score_text = self.font_medium.render(f"Score: {self.score}", True, COLOR_WHITE)
        self.screen.blit(score_text, (20, 70))
        
        lives_text = self.font_medium.render(f"Lives: {self.lives}", True, (255, 100, 100))
        lives_rect = lives_text.get_rect(right=SCREEN_WIDTH - 20, top=70)
        self.screen.blit(lives_text, lives_rect)
        
        # Draw bricks
        for brick in self.bricks:
            brick.draw(self.screen)
        
        # Draw paddle
        self.paddle.draw(self.screen)
        
        # Draw ball
        self.ball.draw(self.screen)
        
        # Draw instructions
        if self.ball_attached:
            inst_text = self.font_small.render("SPACE to launch ball | Arrow keys to move", True, COLOR_TEXT)
            self.screen.blit(inst_text, (100, SCREEN_HEIGHT - 30))
        else:
            inst_text = self.font_small.render("Arrow keys to move | ESC to exit", True, COLOR_TEXT)
            self.screen.blit(inst_text, (150, SCREEN_HEIGHT - 30))
        
        # Draw game over
        if self.game_over:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(200)
            overlay.fill((0, 0, 0))
            self.screen.blit(overlay, (0, 0))
            
            game_over_text = self.font_title.render("GAME OVER!", True, (255, 100, 100))
            game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
            self.screen.blit(game_over_text, game_over_rect)
            
            final_score = self.font_large.render(f"Final Score: {self.score}", True, COLOR_WHITE)
            final_rect = final_score.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
            self.screen.blit(final_score, final_rect)
        
        # Draw won
        if self.won:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(150)
            overlay.fill((0, 0, 0))
            self.screen.blit(overlay, (0, 0))
            
            won_text = self.font_title.render("YOU WON! 🎉", True, (100, 255, 100))
            won_rect = won_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
            self.screen.blit(won_text, won_rect)
            
            final_score = self.font_large.render(f"Final Score: {self.score}", True, COLOR_WHITE)
            final_rect = final_score.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
            self.screen.blit(final_score, final_rect)

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
                    elif event.key == pygame.K_SPACE:
                        self.ball_attached = False
                    elif event.key == pygame.K_r and (self.game_over or self.won):
                        self.__init__()
            
            if not self.game_over and not self.won:
                self.update()
            
            self.draw()
            pygame.display.update()
        
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    breakout = Breakout()
    breakout.run()
