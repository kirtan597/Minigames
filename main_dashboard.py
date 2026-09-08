"""
MINIGAMES CENTRAL - Exact Arcade Dashboard
Matches the design screenshot precisely
"""

import pygame
import sys
import os
import subprocess
import math
import random

pygame.init()
pygame.font.init()

# Screen - Widescreen 1280x720
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

# Colors from Design
BG_COLOR = (5, 8, 20)  # Deep dark blue
GRID_COLOR = (56, 189, 248)  # Cyan
TEXT_COLOR = (229, 231, 235)  # Light
TEXT_MUTED = (100, 116, 139)  # Muted gray
ACCENT_CYAN = (34, 211, 238)  # Bright cyan

# Game Card Colors (Exact from Screenshot)
COLOR_FLAPPY = (56, 189, 248)  # Cyan
COLOR_SNAKE = (52, 211, 153)  # Green
COLOR_PONG = (6, 182, 212)  # Dark Cyan
COLOR_MONSTER = (245, 158, 11)  # Amber
COLOR_SPACE = (217, 70, 239)  # Magenta
COLOR_TETRIS = (59, 130, 246)  # Blue
COLOR_2048 = (250, 204, 21)  # Yellow
COLOR_BREAKOUT = (244, 63, 94)  # Red


class GameCard:
    def __init__(self, x, y, name, subtitle, color, display_name, icon_text):
        self.x = x
        self.y = y
        self.width = 200
        self.height = 180
        self.name = name
        self.subtitle = subtitle
        self.color = color
        self.display_name = display_name
        self.icon_text = icon_text
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.hovered = False
        
    def update(self, mouse_pos):
        self.hovered = self.rect.collidepoint(mouse_pos)
        
    def draw(self, screen, font_label, font_title, font_desc, font_stat):
        # Background dark card
        pygame.draw.rect(screen, (15, 23, 42), self.rect, border_radius=12)
        
        # Border with game color
        border_width = 2 if self.hovered else 1
        pygame.draw.rect(screen, self.color, self.rect, border_width, border_radius=12)
        
        # Top bar with color
        top_bar = pygame.Rect(self.x, self.y, self.width, 30)
        pygame.draw.rect(screen, self.color, top_bar, border_radius=12)
        
        # Label tag (CLASSIC, RETRO, etc)
        label_surf = font_label.render(self.icon_text, True, self.color)
        screen.blit(label_surf, (self.x + 8, self.y + 8))
        
        # Stats tag (top right) - show score
        stat_text = "SCORE: 08" if self.name == "flappy_bird" else f"LEN: 14" if self.name == "snake" else f"WAVE 04" if self.name == "space" else "LINES: 24" if self.name == "tetris" else f"BEST: 2048" if self.name == "2048" else "SPD: 1.5x" if self.name == "monster" else "03" if self.name == "pong" else "x3 LIFE"
        stat_surf = font_stat.render(stat_text, True, self.color)
        screen.blit(stat_surf, (self.x + self.width - 65, self.y + 8))
        
        # Game display area
        game_area = pygame.Rect(self.x, self.y + 30, self.width, 90)
        pygame.draw.rect(screen, (10, 20, 40), game_area)
        
        # Game name
        name_surf = font_title.render(self.display_name, True, TEXT_COLOR)
        screen.blit(name_surf, (self.x + 10, self.y + 130))
        
        # Subtitle
        sub_surf = font_desc.render(self.subtitle, True, TEXT_MUTED)
        screen.blit(sub_surf, (self.x + 10, self.y + 150))
        
        # PLAY button
        button_rect = pygame.Rect(self.x + self.width - 60, self.y + 145, 50, 25)
        pygame.draw.rect(screen, self.color if self.hovered else (30, 60, 90), button_rect, border_radius=6)
        button_text = "PLAY →"
        btn_surf = font_stat.render(button_text, True, self.color if not self.hovered else TEXT_COLOR)
        screen.blit(btn_surf, (self.x + self.width - 55, self.y + 149))
    
    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)


class Dashboard:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("MINIGAMES CENTRAL")
        self.clock = pygame.time.Clock()
        
        # Fonts
        self.font_header = pygame.font.Font(None, 80)
        self.font_label = pygame.font.Font(None, 14)
        self.font_title = pygame.font.Font(None, 20)
        self.font_desc = pygame.font.Font(None, 13)
        self.font_stat = pygame.font.Font(None, 12)
        self.font_info = pygame.font.Font(None, 12)
        
        # Create game cards - 2 rows of 4
        self.cards = [
            # Row 1
            GameCard(47, 220, "flappy_bird", "Endless Flight", COLOR_FLAPPY, "Flappy Bird", "CLASSIC"),
            GameCard(327, 220, "snake", "Cyber Slither", COLOR_SNAKE, "Snake", "RETRO"),
            GameCard(607, 220, "pong", "Twin Neon Paddle", COLOR_PONG, "Pong", "ARCADE 1972"),
            GameCard(887, 220, "monster", "Lava Runner", COLOR_MONSTER, "Monster Run", "ACTION"),
            # Row 2
            GameCard(47, 450, "space", "Alien Defense", COLOR_SPACE, "Space Invaders", "GALAXY"),
            GameCard(327, 450, "tetris", "Block Stacker", COLOR_TETRIS, "Tetris", "PUZZLE"),
            GameCard(607, 450, "2048", "Tile Synthesis", COLOR_2048, "2048 Puzzle", "LOGIC"),
            GameCard(887, 450, "breakout", "Brick Demolition", COLOR_BREAKOUT, "Breakout", "BREAKOUT"),
        ]
        
        self.running = True
        self.game_process = None

    def draw_background(self):
        self.screen.fill(BG_COLOR)
        
        # Grid pattern
        line_color = (25, 35, 75)
        for i in range(0, SCREEN_WIDTH, 80):
            pygame.draw.line(self.screen, line_color, (i, 0), (i, SCREEN_HEIGHT), 1)
        for i in range(0, SCREEN_HEIGHT, 80):
            pygame.draw.line(self.screen, line_color, (0, i), (SCREEN_WIDTH, i), 1)

    def draw_header(self):
        # Top status bar
        status_text = "● ONLINE CORE v2.4  ·  14ms"
        status_surf = self.font_info.render(status_text, True, TEXT_MUTED)
        self.screen.blit(status_surf, (50, 12))
        
        engines_text = "8 / 8 ENGINES LOADED"
        engines_surf = self.font_info.render(engines_text, True, TEXT_MUTED)
        self.screen.blit(engines_surf, (SCREEN_WIDTH - 200, 12))
        
        # Player badge
        badge_text = "● ARCADE MASTER"
        badge_surf = self.font_info.render(badge_text, True, ACCENT_CYAN)
        self.screen.blit(badge_surf, (SCREEN_WIDTH - 150, 12))
        
        # Main title
        title = "MINIGAMES "
        title_surf = self.font_header.render(title, True, TEXT_COLOR)
        title_rect = title_surf.get_rect(center=(SCREEN_WIDTH // 2 - 100, 80))
        self.screen.blit(title_surf, title_rect)
        
        # Central (in cyan)
        central = "CENTRAL"
        central_surf = self.font_header.render(central, True, ACCENT_CYAN)
        central_rect = central_surf.get_rect(center=(SCREEN_WIDTH // 2 + 100, 80))
        self.screen.blit(central_surf, central_rect)
        
        # Tagline
        tagline = "PLAY ♦ LEARN ♦ EXPLORE"
        tagline_surf = self.font_desc.render(tagline, True, TEXT_MUTED)
        tagline_rect = tagline_surf.get_rect(center=(SCREEN_WIDTH // 2, 145))
        self.screen.blit(tagline_surf, tagline_rect)
        
        # Line under title
        pygame.draw.line(self.screen, ACCENT_CYAN, (300, 165), (980, 165), 2)

    def draw_footer(self):
        # Footer bar background
        footer_bg = pygame.Rect(200, 680, 880, 40)
        pygame.draw.rect(self.screen, (15, 25, 45), footer_bg, border_radius=8)
        pygame.draw.rect(self.screen, (50, 100, 150), footer_bg, 1, border_radius=8)
        
        # Footer buttons
        footer_text = "CLICK: Select & Play   ·   L: Leaderboard   ·   S: Settings   ·   ESC: Quit"
        footer_surf = self.font_info.render(footer_text, True, TEXT_MUTED)
        footer_rect = footer_surf.get_rect(center=(SCREEN_WIDTH // 2, 700))
        self.screen.blit(footer_surf, footer_rect)

    def run(self):
        while self.running:
            self.clock.tick(60)
            mouse_pos = pygame.mouse.get_pos()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                    elif event.key == pygame.K_l:
                        self.open_leaderboard()
                    elif event.key == pygame.K_s:
                        self.open_settings()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    for card in self.cards:
                        if card.is_clicked(mouse_pos):
                            self.launch_game(card.name)
            
            # Update cards
            for card in self.cards:
                card.update(mouse_pos)
            
            # Draw
            self.draw_background()
            self.draw_header()
            
            for card in self.cards:
                card.draw(self.screen, self.font_label, self.font_title, self.font_desc, self.font_stat)
            
            self.draw_footer()
            pygame.display.update()

    def launch_game(self, game_name):
        game_paths = {
            "flappy_bird": "FlappyBird\\main.py",
            "snake": "Snake\\main.py",
            "pong": "Pong\\main.py",
            "monster": "MonsterRun\\main.py",
            "space": "SpaceInvaders\\main.py",
            "tetris": "Tetris\\main.py",
            "2048": "Game2048\\main.py",
            "breakout": "Breakout\\main.py",
        }
        
        if game_name in game_paths:
            try:
                self.game_process = subprocess.Popen(
                    [sys.executable, game_paths[game_name]],
                    cwd=os.path.dirname(os.path.abspath(__file__))
                )
                self.game_process.wait()
            except Exception as e:
                print(f"Error: {e}")

    def open_leaderboard(self):
        try:
            subprocess.Popen(
                [sys.executable, "leaderboard_screen.py"],
                cwd=os.path.dirname(os.path.abspath(__file__))
            ).wait()
        except:
            pass

    def open_settings(self):
        try:
            subprocess.Popen(
                [sys.executable, "settings_screen.py"],
                cwd=os.path.dirname(os.path.abspath(__file__))
            ).wait()
        except:
            pass


def main():
    dashboard = Dashboard()
    dashboard.run()
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
