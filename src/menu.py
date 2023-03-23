import pygame

class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.options = ["Start", "Help", "Quit"]
        self.selected_option = 0
        self.font = pygame.font.Font(None, 36)

    def draw(self):
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