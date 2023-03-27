import pygame
from src.scenes import Scene, Menu, HelpPage, Game, GameOverScene, GamePausedScene

class GameManager:
    WINDOW_WIDTH = 800
    WINDOW_HEIGHT = 600
    BACKGROUND_COLOR = (0, 0, 50)

    def __init__(self, title="Quantum Pathways"):
        pygame.init()
        self.screen = pygame.display.set_mode((GameManager.WINDOW_WIDTH, GameManager.WINDOW_HEIGHT))
        pygame.display.set_caption(title)
        self.width = self.screen.get_width()
        self.height = self.screen.get_height()
        self.game  = Game(self)
        self.scenes = {
            Scene.MAIN_MENU: Menu(self),
            Scene.HELP_PAGE: HelpPage(self),
            Scene.GAME_PLAYING: self.game,
            Scene.GAME_PAUSED: GamePausedScene(self),
            Scene.GAME_OVER: GameOverScene(self)
        }
        self.current_scence_name = Scene.MAIN_MENU
        self.current_scence = self.scenes[self.current_scence_name]
        self.clock = pygame.time.Clock()
        self.fps = 60
        self.running = True

    def run(self):
        while self.running:
            dt = self.clock.tick(self.fps) / 1000.0
            self.handle_events()
            self.update(dt)
            self.draw()

    def update(self, dt):
        self.current_scence.update(dt)

    def draw(self):
        self.screen.fill(GameManager.BACKGROUND_COLOR)
        self.current_scence.draw(self.screen)
        pygame.display.flip()

    def handle_events(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.quit()

        self.current_scence.handle_events(events)

    def toggle_pause(self):
        self.paused = not self.paused
        if self.paused:
            self.current_scence_name = Scene.GAME_PAUSED
        else:
            self.current_scence_name = Scene.GAME_PLAYING

    def main_menu(self):
        self.current_scence_name = Scene.MAIN_MENU
        self.current_scence = self.scenes[self.current_scence_name]

    def help(self):
        self.current_scence_name = Scene.HELP_PAGE
        self.current_scence = self.scenes[self.current_scence_name]

    def play(self):
        self.current_scence_name = Scene.GAME_PLAYING
        self.current_scence = self.scenes[self.current_scence_name]

    def pause(self):
        self.current_scence_name = Scene.GAME_PAUSED
        self.current_scence = self.scenes[self.current_scence_name]

    def game_over(self, won, reason=""):
        self.current_scence_name = Scene.GAME_OVER
        self.current_scence = self.scenes[self.current_scence_name]
        self.current_scence.set_over(won, reason)

    def quit(self):
        self.running = False
