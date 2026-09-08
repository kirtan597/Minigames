"""
Leaderboard Screen for Minigames Central
Displays global and personal high scores for all games
"""

import pygame
import sys
from data_manager import get_data_manager

# Colors
COLOR_BG = (15, 23, 42)
COLOR_TEXT = (229, 231, 235)
COLOR_WHITE = (255, 255, 255)
COLOR_ACCENT = (0, 255, 200)
COLOR_GOLD = (255, 215, 0)
COLOR_SILVER = (192, 192, 192)
COLOR_BRONZE = (205, 127, 50)

class LeaderboardScreen:
    def __init__(self, screen_width=1280, screen_height=720):
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption("🏆 Leaderboards - Minigames Central")
        self.clock = pygame.time.Clock()
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # Fonts
        self.font_title = pygame.font.Font(None, 64)
        self.font_game = pygame.font.Font(None, 40)
        self.font_rank = pygame.font.Font(None, 36)
        self.font_score = pygame.font.Font(None, 32)
        self.font_small = pygame.font.Font(None, 24)
        
        self.data_manager = get_data_manager()
        self.games = [
            "flappy_bird",
            "snake",
            "pong",
            "monster_run",
            "space_invaders",
            "tetris",
            "2048",
            "breakout"
        ]
        self.game_displays = {
            "flappy_bird": "🐦 Flappy Bird",
            "snake": "🐍 Snake",
            "pong": "🏓 Pong",
            "monster_run": "👾 Monster Run",
            "space_invaders": "👽 Space Invaders",
            "tetris": "🧩 Tetris",
            "2048": "🔢 2048",
            "breakout": "🧱 Breakout"
        }
        self.current_game_index = 0

    def draw_leaderboard(self, game_name: str):
        """Draw leaderboard for a specific game"""
        self.screen.fill(COLOR_BG)
        
        # Title
        title = self.font_title.render("🏆 LEADERBOARDS", True, COLOR_ACCENT)
        title_rect = title.get_rect(center=(self.screen_width // 2, 30))
        self.screen.blit(title, title_rect)
        
        # Game name
        game_display = self.game_displays.get(game_name, game_name)
        game_title = self.font_game.render(game_display, True, COLOR_WHITE)
        game_rect = game_title.get_rect(center=(self.screen_width // 2, 100))
        self.screen.blit(game_title, game_rect)
        
        # Get scores
        scores = self.data_manager.get_high_scores(game_name, limit=10)
        
        # Draw scores
        start_y = 160
        y_offset = 0
        
        if not scores:
            no_scores = self.font_score.render("No scores yet. Be the first!", True, COLOR_TEXT)
            self.screen.blit(no_scores, (self.screen_width // 2 - 200, start_y))
        else:
            for rank, score_data in enumerate(scores, 1):
                y = start_y + y_offset
                
                # Rank with medal
                if rank == 1:
                    medal = "🥇"
                    rank_color = COLOR_GOLD
                elif rank == 2:
                    medal = "🥈"
                    rank_color = COLOR_SILVER
                elif rank == 3:
                    medal = "🥉"
                    rank_color = COLOR_BRONZE
                else:
                    medal = f"#{rank}"
                    rank_color = COLOR_TEXT
                
                rank_text = self.font_rank.render(f"{medal} {rank}.", True, rank_color)
                self.screen.blit(rank_text, (100, y))
                
                # Player name
                name_text = self.font_score.render(score_data["player"], True, COLOR_WHITE)
                self.screen.blit(name_text, (300, y))
                
                # Score
                score_text = self.font_score.render(f"{score_data['score']}", True, COLOR_ACCENT)
                score_rect = score_text.get_rect(right=self.screen_width - 100, top=y)
                self.screen.blit(score_text, score_rect)
                
                # Date
                date_text = self.font_small.render(score_data["date"], True, COLOR_TEXT)
                date_rect = date_text.get_rect(right=self.screen_width - 100, top=y + 35)
                self.screen.blit(date_text, date_rect)
                
                y_offset += 55
        
        # Navigation info
        nav_text = self.font_small.render(
            f"← Previous | {self.current_game_index + 1}/{len(self.games)} | Next →",
            True,
            COLOR_TEXT
        )
        nav_rect = nav_text.get_rect(center=(self.screen_width // 2, self.screen_height - 50))
        self.screen.blit(nav_text, nav_rect)
        
        # Controls
        controls = self.font_small.render("ESC: Back to Menu", True, COLOR_TEXT)
        self.screen.blit(controls, (50, self.screen_height - 30))

    def run(self):
        """Run leaderboard screen"""
        running = True
        
        while running:
            self.clock.tick(60)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key == pygame.K_LEFT:
                        self.current_game_index = (self.current_game_index - 1) % len(self.games)
                    elif event.key == pygame.K_RIGHT:
                        self.current_game_index = (self.current_game_index + 1) % len(self.games)
            
            current_game = self.games[self.current_game_index]
            self.draw_leaderboard(current_game)
            pygame.display.update()
        
        pygame.quit()
        sys.exit()


def main():
    pygame.init()
    screen = LeaderboardScreen()
    screen.run()


if __name__ == "__main__":
    main()
