import pygame
from src.ui import Button, Label, GradientBackground, COLORS
from src.scenes import Scene


class Menu(Scene):
    def __init__(self, game_manager):
        super().__init__(game_manager)
        self.options = ["Start", "Help", "Quit"]
        self.selected_option = 0

        self.background = GradientBackground(COLORS["dark_blue"], COLORS["purple"])
        self.title = Label("Quantum Pathways", position=('center', 100), font_color=COLORS["white"],
                           font_size=48, font_variant="BoldItalic")
        self.buttons = []
        for i, option in enumerate(self.options):
            button = Button(option, ('center', 250 + i * 50), padding=(20, 5), font_size=24, font_variant="Regular")
            self.buttons.append(button)

        self.footer_text = "Developed by Aria, a GPT-4 AI at AI Game Makers"
        self.footer = Label(self.footer_text, position=('center', -20), font_color=COLORS["white"],
                            font_size=12, font_variant="Italic")

    def update(self, dt):
        pass

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    self.navigate("down")
                elif event.key == pygame.K_UP:
                    self.navigate("up")
                elif event.key == pygame.K_RETURN:
                    self.select()

    def draw(self, screen):
        self.background.draw(screen)
        self.title.draw(screen)
        for i, button in enumerate(self.buttons):
            button.deselect()
            if i == self.selected_option:
                button.select()

            button.draw(screen)
        self.footer.draw(screen)

    def navigate(self, direction):
        if direction == "up":
            self.selected_option = (self.selected_option - 1) % len(self.options)
        elif direction == "down":
            self.selected_option = (self.selected_option + 1) % len(self.options)

    def select(self):
        if self.selected_option == 0:
            return self.manager.play()
        elif self.selected_option == 1:
            return self.manager.help()
        elif self.selected_option == 2:
            return self.manager.quit()

