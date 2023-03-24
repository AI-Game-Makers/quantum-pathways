import pygame
from src.player import Player
from src.level import Level
from src.levels import level1, level2, level3, level4
from src.menu import Menu
from src.help_page import HelpPage
from path import get_asset_path

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()
        self.font = pygame.font.Font(None, 36)

        # Clock and timer
        self.clock = pygame.time.Clock()
        self.level_time_limit = 60  # Time limit in seconds
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

    def load_level(self, level_data):
        self.level = Level(self.screen)
        self.level.load_level(level_data)
        start_x, start_y = self.level.get_start_position()
        self.player = Player(start_x, start_y, get_asset_path("assets/images/quarky.png"))

    def next_level(self):
        self.current_level += 1
        if self.current_level < len(self.all_levels):
            self.load_level(self.all_levels[self.current_level])
            self.timer = 0 
        else:
            self.state = "game_over"

    def main_loop(self):
        while self.running:
            if self.player.time_dilation_active:
                dt = self.clock.tick(self.fps / self.player.time_dilation_factor) / 1000.0
            else:
                dt = self.clock.tick(self.fps) / 1000.0

            self.handle_events()
            self.update(dt)
            self.draw()

    def handle_events(self):
        keys = pygame.key.get_pressed()
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False

            if self.state == "menu":
                menu_state = self.menu.handle_input(keys)
                if menu_state == "start":
                    self.state = "game"
                elif menu_state == "quit":
                    self.running = False
                elif menu_state == "help":
                    self.state = "help"
                else:
                    self.state = "menu"

        if self.state == "game":
            self.player.handle_input(events)

            if keys[pygame.K_q]:
                self.state = "menu"

        elif self.state == "help":
            if keys[pygame.K_q]:
                self.state = "menu"

    def update(self, dt):
        if self.state == "game":
            if self.player.time_dilation_active:
                self.timer += dt / self.player.time_dilation_factor
            else:
                self.timer += dt
            if self.timer >= self.level_time_limit:
                self.state = "game_over"
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
            self.draw_text(f"Score: {self.get_score()}", (10, 10))
        elif self.state == "menu":
            self.menu.draw()
        elif self.state == "game_over":
            self.draw_text("Game Over", (300, 250))
        elif self.state == "help":
            self.help_page.draw()
        pygame.display.flip()

    def draw_text(self, text, position, color=(255, 255, 255)):
        text_surface = self.font.render(text, True, color)
        self.screen.blit(text_surface, position)

    def draw_timer(self):
        time_remaining = int(self.level_time_limit - self.timer)
        timer_color = (255, 0, 0) if time_remaining <= 10 else (255, 255, 255)
        self.draw_text(f"Time: {time_remaining}", (10, 50), timer_color)

    def draw_level_number(self):
        level_text = f"Level: {self.current_level}"
        level_surface = self.font.render(level_text, True, (255, 255, 255))
        self.screen.blit(level_surface, (self.screen_width - 100, 10))

    def get_score(self):
        return self.player.collected_quarks