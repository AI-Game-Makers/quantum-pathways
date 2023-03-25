import pygame
from src.utilities import draw_button, draw_text, vertical_gradient, load_image

class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.options = ["Start", "Help", "Quit"]
        self.selected_option = 0

    def draw(self):
        vertical_gradient(self.screen, (0, 0, 50), (128, 0, 128))  # Dark blue to purple gradient
        draw_text(self.screen, "Quantum Pathways", position=('center', 100), 
                  font_color=(255, 255, 255), font_size=48, font_variant="BoldItalic")
        y = 250
        for i, item in enumerate(self.options):
            bg_color = (80, 80, 80) # Gray
            border_color = (255, 255, 255) # White
            text_color = (255, 255, 255) # White
            font_variant = "Regular"
            if i == self.selected_option:
                bg_color = (255, 255, 255) # White
                border_color = (80, 80, 80) # Gray
                text_color = (0, 0, 50) # Dark blue
                font_variant = "Bold"

            draw_button(self.screen, item, ('center', y), font_color=text_color, padding=(20, 5),
                        bg_color=bg_color, border_color=border_color, font_variant=font_variant)
            y += 50
        draw_text(self.screen, "Developed by Aria, a GPT-4 AI at AI Game Makers", position=('center', 580), 
                  font_color=(255, 255, 255), font_size=12, font_variant="Italic")

    def update(self):
        pass

    def handle_input(self, keys):
        if keys[pygame.K_DOWN]:
            self.navigate("down")
        elif keys[pygame.K_UP]:
            self.navigate("up")
        elif keys[pygame.K_RETURN]:
            return self.select()

    def navigate(self, direction):
        if direction == "up":
            self.selected_option = (self.selected_option - 1) % len(self.options)
        elif direction == "down":
            self.selected_option = (self.selected_option + 1) % len(self.options)

    def select(self):
        if self.selected_option == 0:
            return "start"
        elif self.selected_option == 1:
            return "help"
        elif self.selected_option == 2:
            return "quit"