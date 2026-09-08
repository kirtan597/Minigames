"""
🎮 MINIGAMES CENTRAL - Arcade Dashboard Redesign
Advanced launcher with cyberpunk aesthetic and enhanced game cards
"""

import pygame
import sys
import os
import subprocess
import time
import math
import random

# Initialize Pygame
pygame.init()
pygame.font.init()

# Screen dimensions (Widescreen)
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

# Arcade Color Palette
COLOR_BG = (5, 8, 20)  # Deep space black
COLOR_BG_ACCENT = (15, 20, 35)  # Slightly lighter
COLOR_GRID = (56, 189, 248)  # Cyan grid
COLOR_TEXT = (229, 231, 235)  # Light gray
COLOR_TEXT_DARK = (100, 116, 139)  # Slate
COLOR_ACCENT = (34, 211, 238)  # Cyan glow

# Game Colors (Vibrant Arcade)
COLOR_FLAPPY = (56, 189, 248)  # Sky blue
COLOR_SNAKE = (52, 211, 153)  # Emerald
COLOR_PONG = (6, 182, 212)  # Cyan
COLOR_MONSTER = (245, 158, 11)  # Amber
COLOR_SPACE = (217, 70, 239)  # Fuchsia
COLOR_TETRIS = (59, 130, 246)  # Blue
COLOR_2048 = (250, 204, 21)  # Yellow
COLOR_BREAKOUT = (244, 63, 94)  # Rose


class Particle:
    def __init__(self, x, y, vx, vy, life, color, size=2):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.life = life
        self.max_life = life
        self.color = color
        self.size = size

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.06  # Slight gravity
        self.life -= 1

    def draw(self, screen):
        if self.life > 0:
            alpha = int(255 * (self.life / self.max_life))
            size = max(1, int(self.size * (self.life / self.max_life)))
            color = tuple(min(255, int(c * (self.life / self.max_life))) for c in self.color)
            pygame.draw.circle(screen, color, (int(self.x), int(self.y)), size)

    def is_alive(self):
        return self.life > 0


class ArcadeGameCard:
    def __init__(self, name, x, y, width, height, color, emoji, description):
        self.name = name
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.emoji = emoji
        self.description = description
        
        self.rect = pygame.Rect(x, y, width, height)
        self.hovered = False
        self.current_color = color
        self.scale = 1.0
        self.target_scale = 1.0
        self.particles = []
        self.hover_time = 0
        self.glow_intensity = 0.0
        self.score_counter = random.randint(1, 20) * 4  # Random starting score display

    def update(self, mouse_pos):
        self.hovered = self.rect.collidepoint(mouse_pos)
        
        if self.hovered:
            self.target_scale = 1.08
            self.hover_time = min(self.hover_time + 1, 30)
            self.glow_intensity = min(self.glow_intensity + 0.05, 1.0)
        else:
            self.target_scale = 1.0
            self.hover_time = max(self.hover_time - 1, 0)
            self.glow_intensity = max(self.glow_intensity - 0.03, 0.0)

        # Smooth scale animation
        self.scale += (self.target_scale - self.scale) * 0.15

        # Update particles
        self.particles = [p for p in self.particles if p.is_alive()]
        for particle in self.particles:
            particle.update()

    def spawn_particles(self):
        if self.hovered and len(self.particles) < 12:
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(1.5, 3.5)
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed - 0.5
            
            particle = Particle(
                self.rect.centerx, self.rect.centery,
                vx, vy, 50, self.color, random.uniform(1.5, 3)
            )
            self.particles.append(particle)

    def draw(self, screen, font_emoji, font_title, font_desc, font_stat):
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

        # Draw glow background
        if self.glow_intensity > 0:
            glow_rect = scaled_rect.inflate(int(20 * self.glow_intensity), int(20 * self.glow_intensity))
            glow_color = tuple(int(c * self.glow_intensity * 0.3) for c in self.color)
            pygame.draw.ellipse(screen, glow_color, glow_rect)

        # Draw shadow
        shadow_offset = int(6 * self.scale)
        shadow_rect = scaled_rect.copy()
        shadow_rect.y += shadow_offset
        pygame.draw.rect(screen, (0, 0, 10), shadow_rect, border_radius=12)

        # Draw main card background (glassmorphic)
        pygame.draw.rect(screen, COLOR_BG_ACCENT, scaled_rect, border_radius=16)
        
        # Draw border with glow
        border_color = tuple(int(c * (0.5 + self.glow_intensity * 0.5)) for c in self.color)
        border_width = 2 if self.hovered else 1
        pygame.draw.rect(screen, border_color, scaled_rect, border_width, border_radius=16)

        # Draw top bar with color
        top_bar_height = int(30 * self.scale)
        top_bar = pygame.Rect(scaled_rect.x, scaled_rect.y, scaled_rect.width, top_bar_height)
        pygame.draw.rect(screen, self.color, top_bar, border_radius=16)
        
        # Draw emoji on top bar
        emoji_surf = font_emoji.render(self.emoji, True, COLOR_TEXT)
        emoji_rect = emoji_surf.get_rect(center=(scaled_rect.centerx, scaled_rect.y + top_bar_height // 2))
        screen.blit(emoji_surf, emoji_rect)

        # Draw game name
        name_surf = font_title.render(self.name, True, COLOR_TEXT)
        name_rect = name_surf.get_rect(center=(scaled_rect.centerx, scaled_rect.y + top_bar_height + 18))
        screen.blit(name_surf, name_rect)

        # Draw description
        desc_surf = font_desc.render(self.description, True, COLOR_TEXT_DARK)
        desc_rect = desc_surf.get_rect(center=(scaled_rect.centerx, scaled_rect.y + top_bar_height + 42))
        screen.blit(desc_surf, desc_rect)

        # Draw score tag
        score_text = f"BEST: {self.score_counter}"
        score_surf = font_stat.render(score_text, True, self.color)
        score_rect = score_surf.get_rect(bottomright=(scaled_rect.right - 8, scaled_rect.bottom - 8))
        screen.blit(score_surf, score_rect)

        # Draw particles
        for particle in self.particles:
            particle.draw(screen)

    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)


class ArcadeLauncher:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("🎮 MINIGAMES CENTRAL - Arcade Redesign")
        self.clock = pygame.time.Clock()
        
        # Fonts
        self.font_emoji = pygame.font.Font(None, 48)
        self.font_title = pygame.font.Font(None, 32)
        self.font_desc = pygame.font.Font(None, 16)
        self.font_stat = pygame.font.Font(None, 14)
        self.font_header = pygame.font.Font(None, 80)
        self.font_subheader = pygame.font.Font(None, 24)
        self.font_info = pygame.font.Font(None, 14)
        
        self.running = True
        self.game_process = None
        self.background_particles = []
        self.time_elapsed = 0
        
        # Create game cards
        self.cards = [
            ArcadeGameCard("Flappy Bird", 30, 120, 220, 200, COLOR_FLAPPY, "🐦", "Endless Flight"),
            ArcadeGameCard("Snake", 290, 120, 220, 200, COLOR_SNAKE, "🐍", "Cyber Slither"),
            ArcadeGameCard("Pong", 550, 120, 220, 200, COLOR_PONG, "🏓", "Twin Neon"),
            ArcadeGameCard("Monster Run", 810, 120, 220, 200, COLOR_MONSTER, "👾", "Lava Runner"),
            ArcadeGameCard("Space Invaders", 1050, 120, 220, 200, COLOR_SPACE, "👽", "Alien Defense"),
            ArcadeGameCard("Tetris", 160, 360, 220, 200, COLOR_TETRIS, "🧩", "Block Stacker"),
            ArcadeGameCard("2048 Puzzle", 420, 360, 220, 200, COLOR_2048, "🔢", "Tile Synthesis"),
            ArcadeGameCard("Breakout", 680, 360, 220, 200, COLOR_BREAKOUT, "🧱", "Brick Breaker"),
        ]
        
        # Initialize background particles
        for _ in range(30):
            self.create_background_particle()

    def create_background_particle(self):
        x = random.randint(0, SCREEN_WIDTH)
        y = random.randint(0, SCREEN_HEIGHT)
        vx = random.uniform(-0.3, 0.3)
        vy = random.uniform(-0.5, 0.1)
        color = random.choice([COLOR_FLAPPY, COLOR_SNAKE, COLOR_PONG, COLOR_ACCENT])
        particle = Particle(x, y, vx, vy, 150, color, random.uniform(0.5, 2))
        self.background_particles.append(particle)

    def draw_background(self):
        # Main background
        self.screen.fill(COLOR_BG)
        
        # Subtle grid pattern
        line_color = (30, 40, 80)
        line_alpha = 15
        for i in range(0, SCREEN_WIDTH, 60):
            pygame.draw.line(self.screen, line_color, (i, 0), (i, SCREEN_HEIGHT), 1)
        for i in range(0, SCREEN_HEIGHT, 60):
            pygame.draw.line(self.screen, line_color, (0, i), (SCREEN_WIDTH, i), 1)
        
        # Update and draw background particles
        self.background_particles = [p for p in self.background_particles if p.is_alive()]
        if len(self.background_particles) < 30:
            self.create_background_particle()
        
        for particle in self.background_particles:
            particle.update()
            particle.draw(self.screen)

    def draw_header(self):
        # System status bar
        status_surf = self.font_info.render("● ONLINE CORE v2.4 • 14ms • 8/8 ENGINES LOADED", True, COLOR_TEXT_DARK)
        self.screen.blit(status_surf, (20, 10))

        # Main title
        title_text = "MINIGAMES"
        title_surf = self.font_header.render(title_text, True, COLOR_TEXT)
        title_rect = title_surf.get_rect(center=(SCREEN_WIDTH // 2, 50))
        self.screen.blit(title_surf, title_rect)

        # Central subtitle
        central_text = "CENTRAL"
        central_surf = self.font_header.render(central_text, True, COLOR_ACCENT)
        central_rect = central_surf.get_rect(center=(SCREEN_WIDTH // 2, 50))
        
        # Draw cyan glow effect behind central text
        glow_rect = central_rect.inflate(40, 20)
        pygame.draw.ellipse(self.screen, (34, 211, 238, 30), glow_rect)
        self.screen.blit(central_surf, central_rect)

        # Tagline
        tagline = "PLAY ♦ LEARN ♦ EXPLORE"
        tagline_surf = self.font_subheader.render(tagline, True, COLOR_TEXT_DARK)
        tagline_rect = tagline_surf.get_rect(center=(SCREEN_WIDTH // 2, 100))
        self.screen.blit(tagline_surf, tagline_rect)

        # Decorative line
        pygame.draw.line(self.screen, COLOR_ACCENT, (SCREEN_WIDTH // 2 - 150, 110), (SCREEN_WIDTH // 2 + 150, 110), 2)

    def draw_footer(self):
        footer_text = "L: Leaderboard • S: Settings • ESC: Quit"
        footer_surf = self.font_info.render(footer_text, True, COLOR_TEXT_DARK)
        footer_rect = footer_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 15))
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
                    elif event.key == pygame.K_l:
                        self.show_leaderboard()
                    elif event.key == pygame.K_s:
                        self.show_settings()
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
                card.draw(self.screen, self.font_emoji, self.font_title, self.font_desc, self.font_stat)
            
            self.draw_footer()
            pygame.display.update()

    def launch_game(self, game_name):
        game_paths = {
            "Flappy Bird": "FlappyBird\\main.py",
            "Snake": "Snake\\main.py",
            "Pong": "Pong\\main.py",
            "Monster Run": "MonsterRun\\main.py",
            "Space Invaders": "SpaceInvaders\\main.py",
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

    def show_leaderboard(self):
        """Open leaderboard screen"""
        try:
            leaderboard_path = os.path.join(
                os.path.dirname(os.path.abspath(__file__)),
                "leaderboard_screen.py"
            )
            subprocess.Popen(
                [sys.executable, leaderboard_path],
                cwd=os.path.dirname(os.path.abspath(__file__))
            ).wait()
        except Exception as e:
            print(f"Error opening leaderboard: {e}")

    def show_settings(self):
        """Open settings screen"""
        try:
            settings_path = os.path.join(
                os.path.dirname(os.path.abspath(__file__)),
                "settings_screen.py"
            )
            subprocess.Popen(
                [sys.executable, settings_path],
                cwd=os.path.dirname(os.path.abspath(__file__))
            ).wait()
        except Exception as e:
            print(f"Error opening settings: {e}")


def main():
    try:
        launcher = ArcadeLauncher()
        launcher.run()
    except Exception as e:
        print(f"Error running arcade launcher: {e}")
        import traceback
        traceback.print_exc()
    finally:
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    main()
