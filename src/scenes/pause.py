import pygame
from src.ui import Label, GradientBackground, COLORS
from src.scenes import Scene

class GamePausedScene(Scene):
    def __init__(self, game_manager):
        super().__init__(game_manager)
        self.background = GradientBackground(COLORS["dark_blue"], COLORS["purple"])
        self.pause_label = Label("Game Paused", position="center", font_size=24,
                                 font_variant="Bold", font_color=COLORS['white'])

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    self.manager.play()

    def draw(self, screen):
        self.background.draw(screen)
        self.pause_label.draw(screen)
