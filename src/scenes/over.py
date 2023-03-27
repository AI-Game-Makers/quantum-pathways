import pygame
from src.ui import Label, GradientBackground, COLORS
from src.scenes import Scene


class GameOverScene(Scene):
    def __init__(self, game_manager):
        super().__init__(game_manager)
        self.background = GradientBackground(COLORS["dark_blue"], COLORS["purple"])
        self.reason_label = Label("", ("center", 100), font_size=30, font_variant="Bold", font_color=COLORS['white'])
        self.score_label = Label("Score: 0", position=("center", 140), font_size=24, font_color=COLORS['white'])
        self.home_label = Label("Press H to return home", position=("center", -100),
                                font_size=14, font_color=COLORS['white'])
        self.game_score = game_manager.game.get_score()
        self.won, self.reason = None, None

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_h:
                    self.manager.main_menu()

    def draw(self, screen):
        self.background.draw(screen)
        self.reason_label.draw(screen)
        self.score_label.text = f"Score: {self.game_score}"
        self.score_label.draw(screen)
        self.home_label.draw(screen)

    def set_over(self, won, reason=""):
        self.reason_label.text = reason
        self.reason_label.font_color = COLORS['green'] if won else COLORS['red']