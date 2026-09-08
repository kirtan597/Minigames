"""
Monster Run - Minigames Central
Jump over obstacles and collect coins
"""

import pygame
import random
import sys
from data_manager import get_data_manager

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

# Colors
BG_COLOR = (50, 200, 255)
GROUND_COLOR = (100, 200, 100)
PLAYER_COLOR = (150, 100, 255)
OBSTACLE_COLOR = (200, 100, 100)
COIN_COLOR = (255, 255, 0)
TEXT_COLOR = (255, 255, 255)

# Physics
GRAVITY = 0.6
JUMP_POWER = -18
GROUND_Y = SCREEN_HEIGHT - 100

# Frame rate
FRAME_RATE = 60

class Player:
    def __init__(self):
        self.x = 100
        self.y = GROUND_Y - 40
        self.width = 40
        self.height = 40
        self.velocity_y = 0
        self.on_ground = True
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def jump(self):
        if self.on_ground:
            self.velocity_y = JUMP_POWER
            self.on_ground = False

    def update(self):
        # Apply gravity
        self.velocity_y += GRAVITY
        self.y += self.velocity_y
        
        # Ground collision
        if self.y + self.height >= GROUND_Y:
            self.y = GROUND_Y - self.height
            self.velocity_y = 0
            self.on_ground = True
        
        self.rect.y = self.y

    def draw(self, screen):
        # Body
        pygame.draw.rect(screen, PLAYER_COLOR, self.rect)
        # Eyes
        pygame.draw.circle(screen, (0, 0, 0), (self.x + 10, self.y + 10), 3)
        pygame.draw.circle(screen, (0, 0, 0), (self.x + 30, self.y + 10), 3)

    def get_rect(self):
        return self.rect


class Obstacle:
    def __init__(self, x):
        self.x = x
        self.y = GROUND_Y - 40
        self.width = 30
        self.height = 40
        self.speed = 8
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def update(self):
        self.x -= self.speed
        self.rect.x = self.x

    def draw(self, screen):
        pygame.draw.rect(screen, OBSTACLE_COLOR, self.rect)
        # Draw angry face
        pygame.draw.line(screen, (0, 0, 0), (self.x + 5, self.y + 5), (self.x + 10, self.y + 5), 2)
        pygame.draw.line(screen, (0, 0, 0), (self.x + 20, self.y + 5), (self.x + 25, self.y + 5), 2)

    def is_off_screen(self):
        return self.x + self.width < 0

    def get_rect(self):
        return self.rect


class Coin:
    def __init__(self, x):
        self.x = x
        self.y = random.randint(GROUND_Y - 200, GROUND_Y - 100)
        self.radius = 8
        self.collected = False

    def draw(self, screen):
        pygame.draw.circle(screen, COIN_COLOR, (int(self.x), int(self.y)), self.radius)
        pygame.draw.circle(screen, (200, 200, 0), (int(self.x), int(self.y)), self.radius, 2)

    def check_collision(self, player):
        dist = ((self.x - player.x) ** 2 + (self.y - (player.y + player.height // 2)) ** 2) ** 0.5
        return dist < self.radius + 20

    def is_off_screen(self):
        return self.x < 0


class MonsterRunGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("👾 Monster Run - Minigames Central")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 48)
        self.font_small = pygame.font.Font(None, 32)
        
        self.data_manager = get_data_manager()
        self.reset_game()

    def reset_game(self):
        self.player = Player()
        self.obstacles = []
        self.coins = []
        self.score = 0
        self.game_over = False
        self.obstacle_counter = 0
        self.coin_counter = 0
        self.start_time = pygame.time.get_ticks()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                elif event.key == pygame.K_SPACE:
                    if self.game_over:
                        self.reset_game()
                    else:
                        self.player.jump()
        return True

    def update(self):
        if not self.game_over:
            self.player.update()
            
            # Spawn obstacles
            self.obstacle_counter += 1
            if self.obstacle_counter > 100:
                self.obstacles.append(Obstacle(SCREEN_WIDTH))
                self.obstacle_counter = 0
            
            # Spawn coins
            self.coin_counter += 1
            if self.coin_counter > 80:
                self.coins.append(Coin(SCREEN_WIDTH))
                self.coin_counter = 0
            
            # Update obstacles
            for obstacle in self.obstacles:
                obstacle.update()
                
                # Check collision
                if obstacle.get_rect().colliderect(self.player.get_rect()):
                    self.game_over = True
            
            # Remove off-screen obstacles
            self.obstacles = [o for o in self.obstacles if not o.is_off_screen()]
            
            # Update coins
            for coin in self.coins:
                if coin.check_collision(self.player):
                    coin.collected = True
                    self.score += 10
            
            # Remove collected/off-screen coins
            self.coins = [c for c in self.coins if not c.collected and not c.is_off_screen()]

    def draw(self):
        self.screen.fill(BG_COLOR)
        
        # Draw ground
        pygame.draw.rect(self.screen, GROUND_COLOR,
                        (0, GROUND_Y, SCREEN_WIDTH, SCREEN_HEIGHT - GROUND_Y))
        
        # Draw obstacles
        for obstacle in self.obstacles:
            obstacle.draw(self.screen)
        
        # Draw coins
        for coin in self.coins:
            coin.draw(self.screen)
        
        # Draw player
        self.player.draw(self.screen)
        
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
            self.data_manager.add_high_score("monster_run", "Player", self.score)
        
        pygame.quit()
        sys.exit()


def main():
    try:
        game = MonsterRunGame()
        game.run()
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
