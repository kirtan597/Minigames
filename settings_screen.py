"""
Settings Screen for Minigames Central
Theme selector, volume, difficulty, and preferences
"""

import pygame
import json
import os

# Colors for different themes
THEMES = {
    "dark": {
        "bg": (15, 23, 42),
        "text": (229, 231, 235),
        "accent": (100, 255, 218),
        "button": (50, 100, 150),
        "button_hover": (100, 150, 200),
    },
    "light": {
        "bg": (240, 245, 250),
        "text": (30, 40, 70),
        "accent": (0, 150, 255),
        "button": (200, 220, 240),
        "button_hover": (150, 200, 240),
    },
    "neon": {
        "bg": (0, 0, 20),
        "text": (0, 255, 150),
        "accent": (255, 0, 150),
        "button": (50, 50, 80),
        "button_hover": (100, 100, 150),
    },
    "retro": {
        "bg": (50, 50, 100),
        "text": (255, 200, 100),
        "accent": (255, 100, 50),
        "button": (100, 100, 150),
        "button_hover": (150, 150, 200),
    },
    "pastel": {
        "bg": (255, 240, 245),
        "text": (100, 80, 120),
        "accent": (200, 100, 200),
        "button": (230, 200, 230),
        "button_hover": (220, 150, 220),
    },
    "cyberpunk": {
        "bg": (15, 0, 25),
        "text": (200, 0, 255),
        "accent": (0, 255, 255),
        "button": (50, 0, 100),
        "button_hover": (100, 0, 200),
    },
}

DIFFICULTIES = ["Easy", "Normal", "Hard", "Nightmare"]
VOLUMES = ["Mute", "Low", "Medium", "High"]


class SettingsScreen:
    def __init__(self, screen_width=1280, screen_height=720):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption("⚙️ Settings - Minigames Central")
        
        # Fonts
        self.font_title = pygame.font.Font(None, 64)
        self.font_option = pygame.font.Font(None, 40)
        self.font_value = pygame.font.Font(None, 36)
        self.font_small = pygame.font.Font(None, 28)
        
        # Load settings
        self.settings = self.load_settings()
        self.theme_index = list(THEMES.keys()).index(self.settings.get("theme", "dark"))
        self.difficulty_index = DIFFICULTIES.index(self.settings.get("difficulty", "Normal"))
        self.volume_index = VOLUMES.index(self.settings.get("volume", "High"))
        
        self.selected_option = 0
        self.options = ["Theme", "Difficulty", "Volume"]

    def load_settings(self):
        if os.path.exists("settings.json"):
            try:
                with open("settings.json", "r") as f:
                    return json.load(f)
            except:
                return self.get_default_settings()
        return self.get_default_settings()

    def get_default_settings(self):
        return {
            "theme": "dark",
            "difficulty": "Normal",
            "volume": "High",
        }

    def save_settings(self):
        theme_name = list(THEMES.keys())[self.theme_index]
        settings = {
            "theme": theme_name,
            "difficulty": DIFFICULTIES[self.difficulty_index],
            "volume": VOLUMES[self.volume_index],
        }
        try:
            with open("settings.json", "w") as f:
                json.dump(settings, f, indent=2)
        except:
            pass

    def get_current_theme(self):
        theme_name = list(THEMES.keys())[self.theme_index]
        return THEMES[theme_name]

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.save_settings()
                    return "back"
                elif event.key == pygame.K_UP:
                    self.selected_option = (self.selected_option - 1) % len(self.options)
                elif event.key == pygame.K_DOWN:
                    self.selected_option = (self.selected_option + 1) % len(self.options)
                elif event.key == pygame.K_LEFT:
                    if self.selected_option == 0:  # Theme
                        self.theme_index = (self.theme_index - 1) % len(THEMES)
                    elif self.selected_option == 1:  # Difficulty
                        self.difficulty_index = (self.difficulty_index - 1) % len(DIFFICULTIES)
                    elif self.selected_option == 2:  # Volume
                        self.volume_index = (self.volume_index - 1) % len(VOLUMES)
                elif event.key == pygame.K_RIGHT:
                    if self.selected_option == 0:  # Theme
                        self.theme_index = (self.theme_index + 1) % len(THEMES)
                    elif self.selected_option == 1:  # Difficulty
                        self.difficulty_index = (self.difficulty_index + 1) % len(DIFFICULTIES)
                    elif self.selected_option == 2:  # Volume
                        self.volume_index = (self.volume_index + 1) % len(VOLUMES)
        
        return None

    def draw(self):
        theme = self.get_current_theme()
        self.screen.fill(theme["bg"])
        
        # Title
        title = self.font_title.render("⚙️ SETTINGS", True, theme["accent"])
        title_rect = title.get_rect(center=(self.screen_width // 2, 80))
        self.screen.blit(title, title_rect)
        
        # Options
        start_y = 200
        option_spacing = 120
        
        for i, option in enumerate(self.options):
            y = start_y + i * option_spacing
            
            # Highlight selected option
            if i == self.selected_option:
                highlight_rect = pygame.Rect(150, y - 10, self.screen_width - 300, 60)
                pygame.draw.rect(self.screen, theme["button_hover"], highlight_rect, border_radius=10)
            
            # Option label
            label_text = self.font_option.render(option, True, theme["text"])
            label_rect = label_text.get_rect(x=200, y=y)
            self.screen.blit(label_text, label_rect)
            
            # Option value
            if i == 0:  # Theme
                value = list(THEMES.keys())[self.theme_index].upper()
                nav_text = "◀ %s ▶" % value
            elif i == 1:  # Difficulty
                value = DIFFICULTIES[self.difficulty_index]
                nav_text = "◀ %s ▶" % value
            elif i == 2:  # Volume
                value = VOLUMES[self.volume_index]
                nav_text = "◀ %s ▶" % value
            
            value_text = self.font_value.render(nav_text, True, theme["accent"])
            value_rect = value_text.get_rect(right=self.screen_width - 200, y=y)
            self.screen.blit(value_text, value_rect)
        
        # Instructions
        instructions = self.font_small.render(
            "↑/↓ to select • ◀/▶ to change • ESC to save and exit",
            True,
            theme["text"]
        )
        instructions_rect = instructions.get_rect(center=(self.screen_width // 2, self.screen_height - 100))
        self.screen.blit(instructions, instructions_rect)
        
        # Theme preview box
        preview_y = start_y + len(self.options) * option_spacing + 50
        preview_text = self.font_small.render("Theme Preview:", True, theme["text"])
        self.screen.blit(preview_text, (200, preview_y))
        
        # Small color swatches
        colors_to_show = [
            ("BG", theme["bg"]),
            ("Text", theme["text"]),
            ("Accent", theme["accent"]),
        ]
        
        swatch_x = 200
        for label, color in colors_to_show:
            pygame.draw.rect(self.screen, color, (swatch_x, preview_y + 40, 40, 40))
            pygame.draw.rect(self.screen, theme["text"], (swatch_x, preview_y + 40, 40, 40), 1)
            color_label = self.font_small.render(label, True, theme["text"])
            self.screen.blit(color_label, (swatch_x - 10, preview_y + 85))
            swatch_x += 100
        
        pygame.display.update()

    def run(self):
        pygame.init()
        clock = pygame.time.Clock()
        
        while True:
            result = self.handle_events()
            if result:
                return result
            
            self.draw()
            clock.tick(60)


def open_settings():
    """Open settings screen"""
    settings_screen = SettingsScreen()
    return settings_screen.run()


if __name__ == "__main__":
    pygame.init()
    result = open_settings()
    print(f"Settings closed: {result}")
