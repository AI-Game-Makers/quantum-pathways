import pygame
from src.character.player.quarky import Quarky
from src.levels.level_manager import LevelManager
from src.ui import Label, COLORS
from src.scenes import Scene

class Game(Scene):
    def __init__(self, game_manager):
        super().__init__(game_manager)
        self.player = Quarky(0, 0)
        self.timer = 0

        self.game_ui = GameUI(self)
        self.level_manager = LevelManager(self)
        self.level = self.level_manager.current_level

    def update_level(self, level_manager):
        self.level = level_manager.current_level
        self.player.set_level(self.level)
        self.player.set_position(level_manager.start_x, level_manager.start_y)
        self.timer = 0

    def update(self, dt):
        self.timer += dt
        if self.timer >= self.level.time_limit:
            self.set_over(False, "Time's up!")

        self.player.update(dt)
        if not self.player.quantum_tunneling_active:
            if self.player.collides_with_goal(self.level.goal):
                self.level_manager.next_level()

    def handle_events(self, events):
        keys = pygame.key.get_pressed()
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    self.manager.pause()

                if keys[pygame.K_q]:
                    self.manager.main_menu()

        self.player.handle_input(events, keys)

    def draw(self, screen):
        self.level.draw()
        self.player.draw(screen)  # draw player before the UI elements
        self.game_ui.draw(screen)

    def get_score(self):
        return self.player.collected_quarks

    def set_over(self, won, reason=""):
        self.manager.game_over(won, reason)

class GameUI:
    def __init__(self, game):
        self.game = game
        self.score_label = Label("Score: 0", position=(25, 2), font_size=24, font_color=COLORS['white'],
                                 font_variant="Bold", align="left")
        self.timer_label = Label("Time: 0", position=("center", 16), font_size=24, font_color=COLORS['white'],
                                 font_variant="Bold", align="center")
        self.level_label = Label("Level: 0", position=(-25, 2), font_size=24, font_color=COLORS['white'],
                                 font_variant="Bold", align="right")

    def draw(self, screen):
        self.draw_level_number(screen)
        self.draw_timer(screen)
        self.draw_score(screen)

    def draw_score(self, screen):
        self.score_label.text = f"Score: {self.game.get_score()}"
        self.score_label.draw(screen)

    def draw_timer(self, screen):
        time_remaining = int(self.game.level.time_limit - self.game.timer)
        self.timer_label.text = f"Time: {time_remaining}"
        self.timer_label.draw(screen)

    def draw_level_number(self, screen):
        self.level_label.text = f"Level: {self.game.level_manager.current_level_id}"
        self.level_label.draw(screen)