import pygame

class HelpPage:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 28)
        self.text_color = (255, 255, 255)

    def draw(self):
        lines = [
            ["Welcome to Quantum Pathways!", ""],
            ["", ""],
            ["Controls:", "Objectives:"],
            ["Use arrow keys to move Quarky.", "Collect quarks to gain points and access"],
            ["Use I, J, K, L keys to control", "quantum abilities. Reach the flag within"],
            ["the ghost when superimposed. ",  "the time limit to complete a level."],
            ["", ""],
            ["Quantum Interactions:", "Quarks:"],
            ["Superposition: Collect the Red Quark", "Red Quark: Superposition"],
            ["to create a ghost, and press 'M' to", "Blue Quark: Quantum Tunneling"],
            ["merge with the ghost.", "Green Quark: Entanglement"],
            ["Quantum Tunneling: Collect the Blue", "Orange Quark: Collectible (gives points)"],
            ["Quark to enable tunneling, and", ""],
            ["press 'T' to disable tunneling.", "Tips:"],
            ["Entanglement: Collect the Green Quark,", "Use quantum interactions to overcome"],
            ["then press 'E' to create an", "obstacles and solve puzzles."],
            ["entangled pair and teleport to its", "Be mindful when disabling tunneling"],
            ["location.", "to avoid trapping yourself."],
            ["", ""],
            ["", "Press Q to return to the main menu."]
        ]

        y = 40
        x1 = self.screen.get_width() // 4
        x2 = (self.screen.get_width() * 3) // 4

        for line in lines:
            left_text = self.font.render(line[0], True, self.text_color)
            left_text_rect = left_text.get_rect(center=(x1, y))
            self.screen.blit(left_text, left_text_rect)

            right_text = self.font.render(line[1], True, self.text_color)
            right_text_rect = right_text.get_rect(center=(x2, y))
            self.screen.blit(right_text, right_text_rect)

            y += 30