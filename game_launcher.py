import pygame
import sys
import os
from enum import Enum
import subprocess
import time
import math

# Initialize Pygame
pygame.init()
pygame.font.init()

# Screen dimensions (Widescreen)
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

# Colors
COLOR_BG = (15, 23, 42)  # Deep navy blue
COLOR_PRIMARY = (30, 144, 255)  # Dodger blue
COLOR_SECONDARY = (255, 69, 0)  # Orange-red
COLOR_ACCENT = (34, 197, 94)  # Green
COLOR_WHITE = (255, 255, 255)
COLOR_TEXT = (229, 231, 235)  # Light gray
COLOR_HOVER = (59, 130, 246)  # Lighter blue
COLOR_SHADOW = (0, 0, 0)  # Shadow

class Particle:
    def __init__(self, x, y, vx, vy, life):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.life = life
        self.max_life = life
        self.color = (34, 197, 94)

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.1  # Gravity
        self.life -= 1

    def draw(self, screen):
        alpha = int(255 * (self.life / self.max_life))
        color = tuple(int(c * (self.life / self.max_life)) for c in self.color)
        pygame.draw.circle(screen, color, (int(self.x), int(self.y)), max(1, int(5 * (self.life / self.max_life))))

    def is_alive(self):
        return self.life > 0


class GameCard:
    def __init__(self, name, description, x, y, width, height, color, emoji):
        self.name = name
        self.description = description
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.hover_color = COLOR_HOVER
        self.base_color = color
        self.emoji = emoji
        self.hovered = False
        self.current_color = self.base_color
        self.scale = 1.0
        self.target_scale = 1.0
        self.particles = []

    def update(self, mouse_pos):
        self.hovered = self.rect.collidepoint(mouse_pos)
        
        if self.hovered:
            self.current_color = self.hover_color
            self.target_scale = 1.08
        else:
            self.current_color = self.base_color
            self.target_scale = 1.0

        # Smooth scale animation
        self.scale += (self.target_scale - self.scale) * 0.1

        # Update particles
        self.particles = [p for p in self.particles if p.is_alive()]
        for particle in self.particles:
            particle.update()

    def spawn_particle(self):
        if self.hovered and len(self.particles) < 5:
            angle = time.time() * 3
            vx = math.cos(angle) * 2
            vy = math.sin(angle) * 2 - 1
            particle = Particle(self.rect.centerx, self.rect.centery, vx, vy, 30)
            self.particles.append(particle)

    def draw(self, screen, font_title, font_desc):
        # Draw shadow
        shadow_rect = self.rect.copy()
        shadow_rect.y += 5
        pygame.draw.rect(screen, COLOR_SHADOW, shadow_rect, border_radius=15)

        # Calculate scaled rect
        scaled_width = int(self.rect.width * self.scale)
        scaled_height = int(self.rect.height * self.scale)
        offset_x = (self.rect.width - scaled_width) // 2
        offset_y = (self.rect.height - scaled_height) // 2
        scaled_rect = pygame.Rect(
            self.rect.x + offset_x,
            self.rect.y + offset_y,
            scaled_width,
            scaled_height
        )

        # Draw card background with rounded effect
        pygame.draw.rect(screen, self.current_color, scaled_rect, border_radius=15)
        border_color = COLOR_WHITE if self.hovered else (100, 100, 150)
        border_width = 3 if self.hovered else 2
        pygame.draw.rect(screen, border_color, scaled_rect, border_width, border_radius=15)

        # Draw glow effect if hovered
        if self.hovered:
            glow_rect = scaled_rect.inflate(10, 10)
            pygame.draw.rect(screen, (100, 150, 255), glow_rect, 1, border_radius=15)

        # Draw emoji
        emoji_surf = font_title.render(self.emoji, True, COLOR_WHITE)
        emoji_rect = emoji_surf.get_rect(center=(scaled_rect.centerx, scaled_rect.y + 30))
        screen.blit(emoji_surf, emoji_rect)

        # Draw game name
        name_surf = font_title.render(self.name, True, COLOR_WHITE)
        name_rect = name_surf.get_rect(center=(scaled_rect.centerx, scaled_rect.y + 80))
        screen.blit(name_surf, name_rect)

        # Draw description
        desc_lines = self.description.split('\n')
        y_offset = scaled_rect.y + 130
        for line in desc_lines:
            desc_surf = font_desc.render(line, True, COLOR_TEXT)
            desc_rect = desc_surf.get_rect(center=(scaled_rect.centerx, y_offset))
            screen.blit(desc_surf, desc_rect)
            y_offset += 25

        # Draw particles
        for particle in self.particles:
            particle.draw(screen)

    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)


class GameLauncher:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("🎮 Minigames Launcher - Game Central")
        self.clock = pygame.time.Clock()
        self.font_title = pygame.font.Font(None, 48)
        self.font_desc = pygame.font.Font(None, 28)
        self.font_large = pygame.font.Font(None, 72)
        self.font_header = pygame.font.Font(None, 64)
        
        self.running = True
        self.current_game = None
        self.game_process = None
        self.background_particles = []
        self.time_elapsed = 0
        
        # Create game cards
        self.cards = [
            GameCard(
                "Flappy Bird",
                "Navigate through pipes\nSmooth & Relaxing",
                100, 120, 220, 240,
                COLOR_PRIMARY, "🐦"
            ),
            GameCard(
                "Snake Game",
                "Classic snake action\nGrow and survive",
                380, 120, 220, 240,
                COLOR_SECONDARY, "🐍"
            ),
            GameCard(
                "Pong Game",
                "Retro two-player action\nTest your reflexes",
                660, 120, 220, 240,
                COLOR_ACCENT, "🏓"
            ),
            GameCard(
                "Monster Run",
                "Jump and dodge\nFun platformer",
                940, 120, 220, 240,
                (100, 200, 255), "👾"
            ),
            GameCard(
                "Space Invaders",
                "Defend against aliens\nShoot and survive",
                540, 400, 220, 240,
                (255, 100, 200), "👽"
            ),
        ]
        
        # Initialize background particles
        for _ in range(20):
            self.create_background_particle()

    def create_background_particle(self):
        x = pygame.time.get_ticks() % SCREEN_WIDTH
        y = pygame.time.get_ticks() % SCREEN_HEIGHT
        vx = (pygame.time.get_ticks() % 20 - 10) * 0.01
        vy = (pygame.time.get_ticks() % 20 - 10) * 0.01
        particle = Particle(x, y, vx, vy, 100)
        particle.color = (34, 197, 94)
        self.background_particles.append(particle)

    def draw_background(self):
        self.screen.fill(COLOR_BG)
        
        # Draw animated gradient lines
        for i in range(0, SCREEN_HEIGHT, 40):
            wave = math.sin(self.time_elapsed / 500 + i / 100) * 5
            pygame.draw.line(
                self.screen,
                (50, 100, 150),
                (0 + wave, i),
                (SCREEN_WIDTH + wave, i),
                1
            )
        
        # Update and draw background particles
        self.background_particles = [p for p in self.background_particles if p.is_alive()]
        if len(self.background_particles) < 20:
            self.create_background_particle()
        
        for particle in self.background_particles:
            particle.update()
            particle.draw(self.screen)

    def draw_header(self):
        # Animated title with color shift
        color_shift = int((math.sin(self.time_elapsed / 1000) + 1) * 50 + 150)
        title_color = (color_shift, 144, 255)
        
        header_text = "🎮 MINIGAMES CENTRAL"
        header_surf = self.font_header.render(header_text, True, title_color)
        header_rect = header_surf.get_rect(center=(SCREEN_WIDTH // 2, 40))
        self.screen.blit(header_surf, header_rect)
        
        # Draw animated decorative line
        line_width = int(300 + 100 * math.sin(self.time_elapsed / 1500))
        start_x = SCREEN_WIDTH // 2 - line_width // 2
        end_x = SCREEN_WIDTH // 2 + line_width // 2
        pygame.draw.line(self.screen, COLOR_ACCENT, (start_x, 70), (end_x, 70), 3)

    def draw_footer(self):
        footer_text = "Select a game to play | ESC to quit"
        footer_surf = self.font_desc.render(footer_text, True, COLOR_TEXT)
        footer_rect = footer_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 30))
        self.screen.blit(footer_surf, footer_rect)
        
        # Draw pulsing border
        pulse = int(3 + 2 * math.sin(self.time_elapsed / 500))
        pygame.draw.line(self.screen, COLOR_ACCENT, (0, SCREEN_HEIGHT - 50), (SCREEN_WIDTH, SCREEN_HEIGHT - 50), pulse)

    def run(self):
        while self.running:
            self.time_elapsed += self.clock.tick(60)
            mouse_pos = pygame.mouse.get_pos()

            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left click
                        for card in self.cards:
                            if card.is_clicked(mouse_pos):
                                self.launch_game(card.name)

            # Update
            for card in self.cards:
                card.update(mouse_pos)
                card.spawn_particle()

            # Draw
            self.draw_background()
            self.draw_header()
            
            for card in self.cards:
                card.draw(self.screen, self.font_title, self.font_desc)
            
            self.draw_footer()
            pygame.display.update()

    def launch_game(self, game_name):
        game_paths = {
            "Flappy Bird": "Flappy Bird\\main.py",
            "Snake Game": "SnakeGame\\main.py",
            "Pong Game": "Pong-Game\\main.py",
            "Monster Run": "monster_run\\main.py",
            "Space Invaders": "SpaceShip\\main.py",
        }

        if game_name in game_paths:
            game_path = game_paths[game_name]
            try:
                # Launch game as subprocess
                self.game_process = subprocess.Popen(
                    [sys.executable, game_path],
                    cwd=os.path.dirname(os.path.abspath(__file__))
                )
                # Wait for game to finish
                self.game_process.wait()
                self.game_process = None
            except Exception as e:
                print(f"Error launching {game_name}: {e}")


def main():
    try:
        launcher = GameLauncher()
        launcher.run()
    except Exception as e:
        print(f"Error running launcher: {e}")
        import traceback
        traceback.print_exc()
    finally:
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    main()
