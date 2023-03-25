import pygame
from src.player import Player
from src.level import Level
from src.levels import level1, level2, level3, level4
from src.menu import Menu
from src.help_page import HelpPage
from src.utilities import draw_text

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()

        # Clock and timer
        self.clock = pygame.time.Clock()
        self.level_time_limit = 120  # Time limit in seconds
        self.timer = 0
        self.fps = 60
        self.running = True

        # Menu
        self.menu = Menu(self.screen)
        self.state = "menu"

        # Help Pages
        self.help_page = HelpPage(self.screen)

        # Game Levels
        self.current_level = 0
        self.all_levels = [level1, level2, level3, level4]
        self.load_level(self.all_levels[self.current_level])

        # Pause Menu
        self.paused = False
        self.pause_overlay = pygame.Surface((self.screen_width, self.screen_height))
        self.pause_overlay.set_alpha(128)
        self.pause_overlay.fill((0, 0, 0))

    def load_level(self, level_data):
        self.level = Level(self.screen)
        self.level.load_level(level_data)
        start_x, start_y = self.level.get_start_position()
        self.player = Player(start_x, start_y, "quarky.png")
        self.timer = 0

    def next_level(self):
        self.current_level += 1
        if self.current_level < len(self.all_levels):
            self.load_level(self.all_levels[self.current_level])
            self.timer = 0 
        else:
            self.state = "game_won"

    def main_loop(self):
        while self.running:
            if self.player.time_dilation_active:
                dt = self.clock.tick(self.fps / self.player.time_dilation_factor) / 1000.0
            else:
                dt = self.clock.tick(self.fps) / 1000.0

            self.handle_events()
            if not self.paused:
                self.update(dt)
            self.draw()

    def handle_events(self):
        keys = pygame.key.get_pressed()
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:
                if self.state == "game":
                    if event.key == pygame.K_p:
                        self.toggle_pause()
                elif self.state in ["game_won", "game_lost"]:
                    if event.key == pygame.K_h:
                        self.state = "menu"

            if self.state == "menu":
                menu_state = self.menu.handle_input(keys)
                if menu_state == "start":
                    self.current_level = 0
                    self.load_level(self.all_levels[self.current_level])
                    self.state = "game"
                elif menu_state == "quit":
                    self.running = False
                elif menu_state == "help":
                    self.state = "help"
                else:
                    self.state = "menu"

        if self.state == "game" and not self.paused:
            self.player.handle_input(events)

            if keys[pygame.K_q]:
                self.state = "menu"

        elif self.state == "help":
            if keys[pygame.K_q]:
                self.state = "menu"
            else:
                self.help_page.handle_events(events)

    def update(self, dt):
        if self.state == "game":
            if self.player.time_dilation_active:
                self.timer += dt / self.player.time_dilation_factor
            else:
                self.timer += dt
            if self.timer >= self.level_time_limit:
                self.state = "game_lost"
                self.timer = 0
            self.player.update(self.level)
            if not self.player.quantum_tunneling_active:
                if self.player.collides_with_goal(self.level.goal):
                    self.next_level()
        elif self.state == "menu":
            self.menu.update()

    def draw(self):
        self.screen.fill((0, 0, 50))
        if self.state == "game":
            self.level.draw()
            self.player.draw(self.screen)  # draw player before the UI elements
            self.draw_level_number()
            self.draw_timer()
            draw_text(self.screen, f"Score: {self.get_score()}", (25, 2), font_size=24,
                      font_variant="Bold", font_color=(255, 255, 255), align="left")

            if self.paused:
                self.draw_pause_overlay(self.screen)
        elif self.state == "menu":
            self.menu.draw()
        elif self.state == "game_won":
            self.game_won_screen()
        elif self.state == "game_lost":
            self.game_lost_screen()
        elif self.state == "help":
            self.help_page.draw()
        pygame.display.flip()

    def draw_timer(self):
        time_remaining = int(self.level_time_limit - self.timer)
        draw_text(self.screen, f"Time: {time_remaining}", ('center', 16), font_size=24,
                  font_variant="Bold", font_color=(255, 255, 255), align="center")

    def draw_level_number(self):
        level_text = f"Level: {self.current_level}"
        draw_text(self.screen, level_text, (self.screen_width - 25, 2), font_size=24,
                  font_variant="Bold", font_color=(255, 255, 255), align="right")

    def get_score(self):
        return self.player.collected_quarks

    def draw_pause_overlay(self, screen):
        if self.paused:
            screen.blit(self.pause_overlay, (0, 0))
            draw_text(self.screen, "Game Paused", font_size=36, font_variant="Bold", font_color=(255, 255, 255))

    def toggle_pause(self):
        self.paused = not self.paused

    def game_won_screen(self):
        draw_text(self.screen, "Congratulations! You won!", ("center", 100), font_size=30, font_variant="Bold", font_color=(0, 255, 0))
        draw_text(self.screen, f"Score: {self.get_score()}", ("center", 140), font_size=24, font_color=(255, 255, 255))
        draw_text(self.screen, "Press H to return home", ("center", self.screen_height - 100), 
                  font_size=14, font_color=(255, 255, 255))

    def game_lost_screen(self):
        draw_text(self.screen, "Game Over! You lost!", ("center", 100), font_size=30, font_variant="Bold", font_color=(255, 0, 0))
        draw_text(self.screen, f"Score: {self.get_score()}", ("center", 140), font_size=24, font_color=(255, 255, 255))
        draw_text(self.screen, "Press H to return home", ("center", self.screen_height - 100), 
                  font_size=14, font_color=(255, 255, 255))


