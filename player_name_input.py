"""
Player Name Input Dialog for Minigames Central
"""

import pygame
import sys

# Colors
COLOR_BG = (15, 23, 42)
COLOR_INPUT_BG = (30, 40, 90)
COLOR_INPUT_BORDER = (100, 255, 218)
COLOR_TEXT = (229, 231, 235)
COLOR_WHITE = (255, 255, 255)
COLOR_BUTTON = (100, 255, 218)
COLOR_BUTTON_HOVER = (0, 255, 200)


class PlayerNameInput:
    def __init__(self, screen_width=1280, screen_height=720):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption("Enter Player Name - Minigames Central")
        
        # Fonts
        self.font_title = pygame.font.Font(None, 72)
        self.font_input = pygame.font.Font(None, 48)
        self.font_button = pygame.font.Font(None, 40)
        self.font_small = pygame.font.Font(None, 28)
        
        self.player_name = ""
        self.cursor_visible = True
        self.cursor_timer = 0
        self.button_rect = None

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if self.player_name.strip():
                        return self.player_name.strip()
                elif event.key == pygame.K_BACKSPACE:
                    self.player_name = self.player_name[:-1]
                elif event.key == pygame.K_ESCAPE:
                    return None
                elif len(self.player_name) < 20:
                    self.player_name += event.unicode
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.button_rect and self.button_rect.collidepoint(event.pos):
                    if self.player_name.strip():
                        return self.player_name.strip()
        
        return False  # Continue

    def update(self):
        self.cursor_timer += 1
        if self.cursor_timer > 30:
            self.cursor_visible = not self.cursor_visible
            self.cursor_timer = 0

    def draw(self):
        self.screen.fill(COLOR_BG)
        
        # Title
        title = self.font_title.render("🎮 Enter Your Name", True, COLOR_WHITE)
        title_rect = title.get_rect(center=(self.screen_width // 2, 100))
        self.screen.blit(title, title_rect)
        
        # Subtitle
        subtitle = self.font_small.render("What's your player name?", True, COLOR_TEXT)
        subtitle_rect = subtitle.get_rect(center=(self.screen_width // 2, 200))
        self.screen.blit(subtitle, subtitle_rect)
        
        # Input box
        input_box_width = 400
        input_box_height = 70
        input_box_x = (self.screen_width - input_box_width) // 2
        input_box_y = 300
        
        input_box = pygame.Rect(input_box_x, input_box_y, input_box_width, input_box_height)
        pygame.draw.rect(self.screen, COLOR_INPUT_BG, input_box)
        pygame.draw.rect(self.screen, COLOR_INPUT_BORDER, input_box, 3)
        
        # Display name with cursor
        display_text = self.player_name
        if self.cursor_visible and self.player_name:
            display_text += "|"
        elif not self.player_name:
            display_text = "Enter name..."
        
        text_color = COLOR_WHITE if self.player_name else COLOR_TEXT
        name_text = self.font_input.render(display_text, True, text_color)
        name_rect = name_text.get_rect(center=(self.screen_width // 2, input_box_y + input_box_height // 2))
        self.screen.blit(name_text, name_rect)
        
        # Play button
        button_width = 200
        button_height = 60
        button_x = (self.screen_width - button_width) // 2
        button_y = 450
        
        self.button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
        
        # Button color changes on hover
        mouse_pos = pygame.mouse.get_pos()
        button_color = COLOR_BUTTON_HOVER if self.button_rect.collidepoint(mouse_pos) else COLOR_BUTTON
        
        pygame.draw.rect(self.screen, button_color, self.button_rect)
        pygame.draw.rect(self.screen, COLOR_WHITE, self.button_rect, 2)
        
        button_text = self.font_button.render("PLAY", True, (0, 0, 0))
        button_text_rect = button_text.get_rect(center=self.button_rect.center)
        self.screen.blit(button_text, button_text_rect)
        
        # Instructions
        instructions = self.font_small.render("Press ENTER or click PLAY to start • ESC to cancel", True, COLOR_TEXT)
        instructions_rect = instructions.get_rect(center=(self.screen_width // 2, 600))
        self.screen.blit(instructions, instructions_rect)
        
        pygame.display.update()

    def run(self):
        pygame.init()
        clock = pygame.time.Clock()
        
        while True:
            result = self.handle_events()
            if result is not None:  # Either got a name or None (cancel/quit)
                pygame.quit()
                return result
            
            self.update()
            self.draw()
            clock.tick(60)


def get_player_name(screen_width=1280, screen_height=720):
    """Utility function to get player name"""
    dialog = PlayerNameInput(screen_width, screen_height)
    return dialog.run()


if __name__ == "__main__":
    pygame.init()
    name = get_player_name()
    if name:
        print(f"Player name: {name}")
    else:
        print("Cancelled")
