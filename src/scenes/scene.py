class Scene:
    """ Base class for all scenes. """
    MAIN_MENU = "main_menu"
    HELP_PAGE = "help_page"
    GAME_PLAYING = "game_playing"
    GAME_PAUSED = "game_paused"
    GAME_OVER = "game_over"

    def __init__(self, game_manager):
        self.manager = game_manager

    def update(self, dt):
        pass

    def handle_events(self, events):
        pass

    def draw(self, screen):
        pass