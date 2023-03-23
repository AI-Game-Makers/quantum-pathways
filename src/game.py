import pygame
from src.player import Player
from src.level import Level
from src.levels import level1, level2, level3, level4
from src.menu import Menu
from path import get_asset_path

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()
        self.timer = 0
        self.running = True
        self.fps = 60
        self.clock = pygame.time.Clock()
        self.all_levels = [level1, level2, level3, level4]
        self.current_level = 0
        self.load_level(self.all_levels[self.current_level])
        self.menu = Menu(self.screen)
        self.state = "menu"
        self.font = pygame.font.Font(None, 36)

    def load_level(self, level_data):
        self.level = Level(self.screen)
        self.level.load_level(level_data)
        start_x, start_y = self.level.get_start_position()
        self.player = Player(start_x, start_y, get_asset_path("assets/images/quarky.png"))

    def next_level(self):
        self.current_level += 1
        if self.current_level < len(self.all_levels):
            self.load_level(self.all_levels[self.current_level])
        else:
            print("Congratulations! You've completed all levels!")
            self.running = False

    def main_loop(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(self.fps)

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
                else:
                    self.state = "menu"

        if self.state == "game":
            self.player.handle_input(events)

            if keys[pygame.K_q]:
                self.state = "menu"

    def update(self):
        if self.state == "game":
            self.timer += self.clock.tick(self.fps) / 1000.0
            self.player.update(self.level)  # Pass the level to the update method.
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
            self.draw_score()
        elif self.state == "menu":
            self.menu.draw()
        pygame.display.flip()

    def draw_timer(self):
        timer_text = f"Time: {int(self.timer)}s"
        timer_surface = self.font.render(timer_text, True, (255, 255, 255))
        self.screen.blit(timer_surface, (10, 50))

    def draw_level_number(self):
        level_text = f"Level: {self.current_level}"
        level_surface = self.font.render(level_text, True, (255, 255, 255))
        self.screen.blit(level_surface, (self.screen_width - 100, 10))

    def draw_score(self):
        font = pygame.font.Font(None, 36)
        score_text = f"Score: {self.player.collected_quarks}"
        score_surface = font.render(score_text, True, (255, 255, 255))
        self.screen.blit(score_surface, (10, 10))