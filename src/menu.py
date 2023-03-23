import pygame

class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.options = ["Start Game", "Tutorial", "Quit"]
        self.selected_option = 0
        self.state = "menu"
        self.font = pygame.font.Font(None, 36)

    def draw(self):
        if self.state == "menu":
            self.draw_menu()
        elif self.state == "tutorial":
            self.draw_tutorial()

    def draw_menu(self):
        y = 250
        for i, item in enumerate(self.options):
            if i == self.selected_option:
                color = (255, 255, 0)  # Yellow color for the selected menu item
            else:
                color = (255, 255, 255)  # White color for the non-selected menu items

            text = self.font.render(item, True, color)
            text_rect = text.get_rect(center=(self.screen.get_width() // 2, y))
            self.screen.blit(text, text_rect)
            y += 50

    def draw_tutorial(self):
        lines = [
            "Welcome to Quantum Pathways!",
            "Use arrow keys to move Quarky.",
            "Press SPACE to switch platforms.",
            "Collect quarks to gain new abilities.",
            "Reach the goal area to complete a level.",
            "",
            "Press Q to return to the main menu.",
        ]

        y = 50
        for line in lines:
            text = self.font.render(line, True, (255, 255, 255))
            text_rect = text.get_rect(center=(self.screen.get_width() // 2, y))
            self.screen.blit(text, text_rect)
            y += 40

    def update(self):
        pass

    def handle_input(self, keys):
        if self.state == "menu":
            return self.handle_menu_input(keys)
        elif self.state == "tutorial":
            return self.handle_tutorial_input(keys)

    def handle_menu_input(self, keys):
        if keys[pygame.K_DOWN]:
            self.navigate("down")
        elif keys[pygame.K_UP]:
            self.navigate("up")
        elif keys[pygame.K_RETURN]:
            return self.select()

    def handle_tutorial_input(self, keys):
        if keys[pygame.K_q]:
            self.state = "menu"

    def navigate(self, direction):
        if direction == "up":
            self.selected_option = (self.selected_option - 1) % len(self.options)
        elif direction == "down":
            self.selected_option = (self.selected_option + 1) % len(self.options)

    def select(self):
        if self.selected_option == 0:
            return "start"
        elif self.selected_option == 1:
            self.state = "tutorial"
            return "tutorial"
        elif self.selected_option == 2:
            return "quit"