"""
Flappy Bird - Minigames Central
A simple but challenging endless flying game
"""

import pygame
import random
import sys
import os
from data_manager import get_data_manager

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

# Colors
BG_COLOR = (20, 150, 200)
PIPE_COLOR = (76, 175, 80)
BIRD_COLOR = (255, 200, 50)
TEXT_COLOR = (255, 255, 255)

# Game settings - Optimized for playability
GRAVITY = 0.5  # Slightly gentler gravity
JUMP_POWER = -11  # Smoother jump
PIPE_WIDTH = 80
PIPE_GAP = 160  # More generous gap for children
PIPE_SPEED = -4  # Slower scrolling for better playability
FRAME_RATE = 60

class Bird:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.velocity = 0
        self.radius = 15
        self.alive = True

    def update(self):
        self.velocity += GRAVITY
        self.y += self.velocity
        
        # Boundary check
        if self.y + self.radius > SCREEN_HEIGHT or self.y - self.radius < 0:
            self.alive = False

    def jump(self):
        self.velocity = JUMP_POWER

    def draw(self, screen):
        pygame.draw.circle(screen, BIRD_COLOR, (int(self.x), int(self.y)), self.radius)
        # Draw eye
        pygame.draw.circle(screen, (0, 0, 0), (int(self.x + 5), int(self.y - 5)), 3)

    def get_rect(self):
        return pygame.Rect(self.x - self.radius, self.y - self.radius, 
                          self.radius * 2, self.radius * 2)


class Pipe:
    def __init__(self, x):
        self.x = x
        self.height = random.randint(100, SCREEN_HEIGHT - PIPE_GAP - 100)
        self.scored = False

    def update(self):
        self.x += PIPE_SPEED

    def draw(self, screen):
        # Top pipe
        pygame.draw.rect(screen, PIPE_COLOR, 
                        (self.x, 0, PIPE_WIDTH, self.height))
        # Bottom pipe
        pygame.draw.rect(screen, PIPE_COLOR,
                        (self.x, self.height + PIPE_GAP, PIPE_WIDTH, 
                         SCREEN_HEIGHT - self.height - PIPE_GAP))

    def is_off_screen(self):
        return self.x + PIPE_WIDTH < 0

    def check_collision(self, bird):
        bird_rect = bird.get_rect()
        
        # Top pipe collision
        if bird_rect.colliderect(pygame.Rect(self.x, 0, PIPE_WIDTH, self.height)):
            return True
        
        # Bottom pipe collision
        if bird_rect.colliderect(pygame.Rect(self.x, self.height + PIPE_GAP, PIPE_WIDTH,
                                             SCREEN_HEIGHT - self.height - PIPE_GAP)):
            return True
        
        return False

    def passed_bird(self, bird):
        return (self.x + PIPE_WIDTH < bird.x and not self.scored)


class FlappyBirdGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("🐦 Flappy Bird - Minigames Central")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 48)
        self.font_small = pygame.font.Font(None, 32)
        
        self.data_manager = get_data_manager()
        self.reset_game()

    def reset_game(self):
        self.bird = Bird(SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2)
        self.pipes = []
        self.score = 0
        self.game_over = False
        self.pipe_counter = 0
        self.start_time = pygame.time.get_ticks()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if self.game_over:
                        self.reset_game()
                    else:
                        self.bird.jump()
                elif event.key == pygame.K_ESCAPE:
                    return False
        return True

    def update(self):
        if not self.game_over:
            self.bird.update()
            
            # Spawn new pipes
            self.pipe_counter += 1
            if self.pipe_counter > 90:  # Spawn every 90 frames (~1.5 seconds)
                self.pipes.append(Pipe(SCREEN_WIDTH))
                self.pipe_counter = 0
            
            # Update pipes
            for pipe in self.pipes:
                pipe.update()
                
                # Check collision
                if pipe.check_collision(self.bird):
                    self.game_over = True
                
                # Check if bird passed pipe
                if pipe.passed_bird(self.bird):
                    self.score += 1
                    pipe.scored = True
            
            # Remove off-screen pipes
            self.pipes = [p for p in self.pipes if not p.is_off_screen()]

    def draw(self):
        self.screen.fill(BG_COLOR)
        
        # Draw pipes
        for pipe in self.pipes:
            pipe.draw(self.screen)
        
        # Draw bird
        self.bird.draw(self.screen)
        
        # Draw score
        score_text = self.font.render(f"Score: {self.score}", True, TEXT_COLOR)
        self.screen.blit(score_text, (20, 20))
        
        # Draw game over screen
        if self.game_over:
            elapsed_time = (pygame.time.get_ticks() - self.start_time) // 1000
            self.draw_game_over(elapsed_time)
        
        pygame.display.update()

    def draw_game_over(self, elapsed_time):
        # Semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))
        
        # Game over text
        game_over_text = self.font.render("GAME OVER", True, (255, 100, 100))
        game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 80))
        self.screen.blit(game_over_text, game_over_rect)
        
        # Final score
        final_score_text = self.font.render(f"Final Score: {self.score}", True, TEXT_COLOR)
        final_score_rect = final_score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(final_score_text, final_score_rect)
        
        # Time played
        time_text = self.font_small.render(f"Time: {elapsed_time}s", True, TEXT_COLOR)
        time_rect = time_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60))
        self.screen.blit(time_text, time_rect)
        
        # Restart instruction
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
        
        # Save score if game over
        if self.score > 0:
            self.data_manager.add_high_score("flappy_bird", "Player", self.score)
        
        pygame.quit()
        sys.exit()


def main():
    try:
        game = FlappyBirdGame()
        game.run()
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
