"""
Space Invaders - Minigames Central
Shoot down alien invaders
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
BG_COLOR = (0, 0, 30)
PLAYER_COLOR = (0, 255, 255)
ALIEN_COLOR = (255, 100, 100)
BULLET_COLOR = (255, 255, 0)
TEXT_COLOR = (255, 255, 255)

# Frame rate
FRAME_RATE = 60

class Player:
    def __init__(self):
        self.x = SCREEN_WIDTH // 2
        self.y = SCREEN_HEIGHT - 60
        self.width = 40
        self.height = 40
        self.speed = 7
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def move_left(self):
        if self.x > 0:
            self.x -= self.speed
            self.rect.x = self.x

    def move_right(self):
        if self.x + self.width < SCREEN_WIDTH:
            self.x += self.speed
            self.rect.x = self.x

    def draw(self, screen):
        # Ship body
        points = [
            (self.x + self.width // 2, self.y),
            (self.x, self.y + self.height),
            (self.x + self.width, self.y + self.height)
        ]
        pygame.draw.polygon(screen, PLAYER_COLOR, points)

    def get_rect(self):
        return self.rect


class Bullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 5
        self.height = 15
        self.speed = 10
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def update(self):
        self.y -= self.speed
        self.rect.y = self.y

    def draw(self, screen):
        pygame.draw.rect(screen, BULLET_COLOR, self.rect)

    def is_off_screen(self):
        return self.y < 0

    def get_rect(self):
        return self.rect


class Alien:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 40
        self.height = 40
        self.speed = random.randint(2, 5)
        self.direction = 1
        self.shoot_chance = 0.02
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def update(self):
        self.x += self.speed * self.direction
        self.rect.x = self.x
        
        # Bounce off edges
        if self.x <= 0 or self.x + self.width >= SCREEN_WIDTH:
            self.direction *= -1
            self.y += self.height

    def draw(self, screen):
        # Alien body
        pygame.draw.rect(screen, ALIEN_COLOR, self.rect)
        # Eyes
        pygame.draw.circle(screen, (0, 0, 0), (int(self.x + 10), int(self.y + 10)), 3)
        pygame.draw.circle(screen, (0, 0, 0), (int(self.x + 30), int(self.y + 10)), 3)

    def is_off_screen(self):
        return self.y > SCREEN_HEIGHT

    def get_rect(self):
        return self.rect

    def should_shoot(self):
        return random.random() < self.shoot_chance


class SpaceInvadersGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("👽 Space Invaders - Minigames Central")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 48)
        self.font_small = pygame.font.Font(None, 32)
        
        self.data_manager = get_data_manager()
        self.reset_game()

    def reset_game(self):
        self.player = Player()
        self.bullets = []
        self.aliens = []
        self.alien_bullets = []
        self.score = 0
        self.lives = 3
        self.game_over = False
        self.wave = 1
        self.spawn_aliens(5)
        self.start_time = pygame.time.get_ticks()

    def spawn_aliens(self, count):
        for i in range(count):
            x = random.randint(50, SCREEN_WIDTH - 100)
            y = random.randint(20, 150)
            self.aliens.append(Alien(x, y))

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
                        self.shoot()
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.player.move_left()
        if keys[pygame.K_RIGHT]:
            self.player.move_right()
        
        return True

    def shoot(self):
        self.bullets.append(Bullet(self.player.x + self.player.width // 2, self.player.y))

    def update(self):
        if not self.game_over:
            # Update bullets
            for bullet in self.bullets:
                bullet.update()
            
            self.bullets = [b for b in self.bullets if not b.is_off_screen()]
            
            # Update aliens
            for alien in self.aliens:
                alien.update()
                
                # Alien shoots
                if alien.should_shoot():
                    self.alien_bullets.append(Bullet(alien.x + alien.width // 2, alien.y + alien.height))
            
            # Remove off-screen aliens
            self.aliens = [a for a in self.aliens if not a.is_off_screen()]
            
            # Check collisions: bullets vs aliens
            for bullet in self.bullets:
                for alien in self.aliens:
                    if bullet.get_rect().colliderect(alien.get_rect()):
                        self.score += 10
                        self.bullets.remove(bullet)
                        self.aliens.remove(alien)
                        break
            
            # Update alien bullets
            for bullet in self.alien_bullets:
                bullet.y += bullet.speed
            
            self.alien_bullets = [b for b in self.alien_bullets if b.y < SCREEN_HEIGHT]
            
            # Check collisions: alien bullets vs player
            for bullet in self.alien_bullets:
                if bullet.get_rect().colliderect(self.player.get_rect()):
                    self.lives -= 1
                    self.alien_bullets.remove(bullet)
                    if self.lives <= 0:
                        self.game_over = True
            
            # Spawn new wave
            if len(self.aliens) == 0:
                self.wave += 1
                self.spawn_aliens(3 + self.wave)

    def draw(self):
        self.screen.fill(BG_COLOR)
        
        # Draw stars (background)
        for i in range(100):
            x = (i * 97 + self.score) % SCREEN_WIDTH
            y = (i * 73) % SCREEN_HEIGHT
            pygame.draw.circle(self.screen, (255, 255, 255), (x, y), 1)
        
        # Draw player
        self.player.draw(self.screen)
        
        # Draw bullets
        for bullet in self.bullets:
            bullet.draw(self.screen)
        
        # Draw alien bullets
        for bullet in self.alien_bullets:
            pygame.draw.rect(self.screen, (255, 0, 0), bullet.rect)
        
        # Draw aliens
        for alien in self.aliens:
            alien.draw(self.screen)
        
        # Draw HUD
        score_text = self.font.render(f"Score: {self.score}", True, TEXT_COLOR)
        self.screen.blit(score_text, (20, 20))
        
        lives_text = self.font_small.render(f"Lives: {self.lives}", True, TEXT_COLOR)
        self.screen.blit(lives_text, (20, 70))
        
        wave_text = self.font_small.render(f"Wave: {self.wave}", True, TEXT_COLOR)
        self.screen.blit(wave_text, (SCREEN_WIDTH - 200, 20))
        
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
            self.data_manager.add_high_score("space_invaders", "Player", self.score)
        
        pygame.quit()
        sys.exit()


def main():
    try:
        game = SpaceInvadersGame()
        game.run()
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
