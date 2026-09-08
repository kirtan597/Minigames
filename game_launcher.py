import pygame
import sys
import os
import subprocess
import time
import math

# Initialize Pygame
pygame.init()
pygame.font.init()

# Screen dimensions (Widescreen)
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

# Modern Vibrant Color Palette
COLOR_BG = (20, 24, 82)  # Deep purple-blue
COLOR_BG_LIGHT = (30, 35, 100)  # Slightly lighter purple-blue

# Game Colors - Pure & Vibrant
COLOR_BIRD = (255, 107, 107)  # Vibrant Red
COLOR_SNAKE = (76, 255, 127)  # Lime Green
COLOR_PONG = (255, 215, 0)  # Gold Yellow
COLOR_MONSTER = (147, 112, 255)  # Bright Purple
COLOR_SPACE = (0, 255, 255)  # Cyan
COLOR_TETRIS = (0, 255, 255)  # Cyan
COLOR_2048 = (255, 200, 50)  # Orange
COLOR_BREAKOUT = (255, 100, 100)  # Red

# UI Colors
COLOR_WHITE = (255, 255, 255)
COLOR_TEXT = (240, 240, 255)  # Almost white with blue tint
COLOR_TEXT_DARK = (100, 100, 150)  # Darker text
COLOR_SHADOW = (0, 0, 20)  # Dark shadow
COLOR_ACCENT = (100, 255, 218)  # Bright teal


class Particle:
    def __init__(self, x, y, vx, vy, life, color):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.life = life
        self.max_life = life
        self.color = color
        self.size = 4

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.08  # Gravity
        self.life -= 1

    def draw(self, screen):
        alpha = int(255 * (self.life / self.max_life))
        color = tuple(min(255, int(c * (self.life / self.max_life) + 20)) for c in self.color)
        size = max(1, int(self.size * (self.life / self.max_life)))
        pygame.draw.circle(screen, color, (int(self.x), int(self.y)), size)

    def is_alive(self):
        return self.life > 0


class GameCard:
    def __init__(self, name, x, y, width, height, color, emoji, game_color):
        self.name = name
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.game_color = game_color
        self.emoji = emoji
        
        self.rect = pygame.Rect(x, y, width, height)
        self.hovered = False
        self.current_color = color
        self.scale = 1.0
        self.target_scale = 1.0
        self.particles = []
        self.hover_time = 0

    def update(self, mouse_pos):
        self.hovered = self.rect.collidepoint(mouse_pos)
        
        if self.hovered:
            self.target_scale = 1.12
            self.hover_time = min(self.hover_time + 1, 30)
            # Blend color towards game color when hovered
            blend = self.hover_time / 30.0
            self.current_color = tuple(
                int(self.color[i] * (1 - blend) + self.game_color[i] * blend)
                for i in range(3)
            )
        else:
            self.target_scale = 1.0
            self.hover_time = max(self.hover_time - 1, 0)
            blend = self.hover_time / 30.0
            self.current_color = tuple(
                int(self.color[i] * (1 - blend) + self.game_color[i] * blend)
                for i in range(3)
            )

        # Smooth scale animation
        self.scale += (self.target_scale - self.scale) * 0.12

        # Update particles
        self.particles = [p for p in self.particles if p.is_alive()]
        for particle in self.particles:
            particle.update()

    def spawn_particles(self):
        if self.hovered and len(self.particles) < 8:
            angle = time.time() * 5
            vx = math.cos(angle) * 2.5
            vy = math.sin(angle) * 2.5 - 1
            particle = Particle(self.rect.centerx, self.rect.centery, vx, vy, 40, self.game_color)
            self.particles.append(particle)

    def draw(self, screen, font_title, font_name):
        # Calculate scaled rect
        scaled_width = int(self.width * self.scale)
        scaled_height = int(self.height * self.scale)
        offset_x = (self.width - scaled_width) // 2
        offset_y = (self.height - scaled_height) // 2
        scaled_rect = pygame.Rect(
            self.x + offset_x,
            self.y + offset_y,
            scaled_width,
            scaled_height
        )

        # Draw shadow behind card
        shadow_offset = int(8 * self.scale)
        shadow_rect = scaled_rect.copy()
        shadow_rect.y += shadow_offset
        pygame.draw.rect(screen, COLOR_SHADOW, shadow_rect, border_radius=20)

        # Draw main card with gradient effect (simulated with border)
        pygame.draw.rect(screen, self.current_color, scaled_rect, border_radius=20)
        
        # Draw border
        border_color = self.game_color if self.hovered else (100, 100, 180)
        border_width = 4 if self.hovered else 2
        pygame.draw.rect(screen, border_color, scaled_rect, border_width, border_radius=20)

        # Draw inner glow
        if self.hovered:
            inner_rect = scaled_rect.inflate(-6, -6)
            pygame.draw.rect(screen, tuple(min(255, c + 50) for c in self.current_color), 
                           inner_rect, 1, border_radius=18)

        # Draw emoji - Large and centered
        emoji_surf = font_title.render(self.emoji, True, COLOR_WHITE)
        emoji_rect = emoji_surf.get_rect(center=(scaled_rect.centerx, scaled_rect.y + 35))
        screen.blit(emoji_surf, emoji_rect)

        # Draw game name - Clean typography
        name_surf = font_name.render(self.name, True, COLOR_WHITE)
        name_rect = name_surf.get_rect(center=(scaled_rect.centerx, scaled_rect.y + 95))
        screen.blit(name_surf, name_rect)

        # Draw particles
        for particle in self.particles:
            particle.draw(screen)

    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)


class GameLauncher:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("🎮 MINIGAMES CENTRAL - Play. Learn. Explore.")
        self.clock = pygame.time.Clock()
        
        # Fonts - Clean and modern
        self.font_title = pygame.font.Font(None, 72)  # Large emoji
        self.font_name = pygame.font.Font(None, 40)   # Game names
        self.font_header = pygame.font.Font(None, 72) # Main title
        self.font_small = pygame.font.Font(None, 24)  # Small text
        
        self.running = True
        self.game_process = None
        self.background_particles = []
        self.time_elapsed = 0
        
        # Create game cards - 8 games (4 original + 3 new)
        self.cards = [
            GameCard("Flappy Bird", 50, 100, 200, 220, (80, 90, 160), "🐦", COLOR_BIRD),
            GameCard("Snake", 300, 100, 200, 220, (80, 90, 160), "🐍", COLOR_SNAKE),
            GameCard("Pong", 550, 100, 200, 220, (80, 90, 160), "🏓", COLOR_PONG),
            GameCard("Monster Run", 800, 100, 200, 220, (80, 90, 160), "👾", COLOR_MONSTER),
            GameCard("Space Invaders", 1050, 100, 200, 220, (80, 90, 160), "👽", COLOR_SPACE),
            GameCard("Tetris", 175, 380, 200, 220, (80, 90, 160), "🧩", COLOR_TETRIS),
            GameCard("2048 Puzzle", 425, 380, 200, 220, (80, 90, 160), "🔢", COLOR_2048),
            GameCard("Breakout", 675, 380, 200, 220, (80, 90, 160), "🧱", COLOR_BREAKOUT),
        ]
        
        # Initialize background particles
        for _ in range(15):
            self.create_background_particle()

    def create_background_particle(self):
        import random
        x = random.randint(0, SCREEN_WIDTH)
        y = random.randint(0, SCREEN_HEIGHT)
        vx = random.uniform(-0.5, 0.5)
        vy = random.uniform(-0.5, 0.5)
        color = random.choice([COLOR_ACCENT, COLOR_BIRD, COLOR_SNAKE, COLOR_PONG])
        particle = Particle(x, y, vx, vy, 200, color)
        particle.size = random.uniform(2, 4)
        self.background_particles.append(particle)

    def draw_background(self):
        # Main background
        self.screen.fill(COLOR_BG)
        
        # Subtle grid pattern
        line_color = (40, 50, 120)
        for i in range(0, SCREEN_WIDTH, 80):
            pygame.draw.line(self.screen, line_color, (i, 0), (i, SCREEN_HEIGHT), 1)
        for i in range(0, SCREEN_HEIGHT, 80):
            pygame.draw.line(self.screen, line_color, (0, i), (SCREEN_WIDTH, i), 1)
        
        # Update and draw background particles
        self.background_particles = [p for p in self.background_particles if p.is_alive()]
        if len(self.background_particles) < 15:
            self.create_background_particle()
        
        for particle in self.background_particles:
            particle.update()
            particle.draw(self.screen)

    def draw_header(self):
        # Main title with glow
        header_text = "🎮 MINIGAMES CENTRAL"
        header_surf = self.font_header.render(header_text, True, COLOR_WHITE)
        header_rect = header_surf.get_rect(center=(SCREEN_WIDTH // 2, 30))
        self.screen.blit(header_surf, header_rect)
        
        # Animated underline
        pulse = int(2 + 3 * math.sin(self.time_elapsed / 800))
        pygame.draw.line(
            self.screen,
            COLOR_ACCENT,
            (SCREEN_WIDTH // 2 - 200, 70),
            (SCREEN_WIDTH // 2 + 200, 70),
            pulse
        )

    def draw_footer(self):
        footer_text = "Click to play • ESC to quit"
        footer_surf = self.font_small.render(footer_text, True, COLOR_TEXT_DARK)
        footer_rect = footer_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 20))
        self.screen.blit(footer_surf, footer_rect)

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
                    if event.button == 1:
                        for card in self.cards:
                            if card.is_clicked(mouse_pos):
                                self.launch_game(card.name)

            # Update
            for card in self.cards:
                card.update(mouse_pos)
                card.spawn_particles()

            # Draw
            self.draw_background()
            self.draw_header()
            
            for card in self.cards:
                card.draw(self.screen, self.font_title, self.font_name)
            
            self.draw_footer()
            pygame.display.update()

    def launch_game(self, game_name):
        game_paths = {
            "Flappy Bird": "Flappy Bird\\main.py",
            "Snake": "SnakeGame\\main.py",
            "Pong": "Pong-Game\\main.py",
            "Monster Run": "monster_run\\main.py",
            "Space Invaders": "SpaceShip\\main.py",
            "Tetris": "Tetris\\main.py",
            "2048 Puzzle": "Game2048\\main.py",
            "Breakout": "Breakout\\main.py",
        }

        if game_name in game_paths:
            game_path = game_paths[game_name]
            try:
                self.game_process = subprocess.Popen(
                    [sys.executable, game_path],
                    cwd=os.path.dirname(os.path.abspath(__file__))
                )
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
