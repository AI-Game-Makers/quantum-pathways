from src.levels.level import Level
from src.levels.procedural_level import ProceduralLevel


class LevelManager:
    def __init__(self, game):
        self.game = game
        self.NUM_LEVELS = 100
        self.current_level_id = 1
        self.load_level(self.current_level_id)
        self.more_levels = True

    def load_level(self, level_id):
        WIDTH = 800 // 32
        HEIGHT = 600 // 32
        self.current_level_id = level_id
        level_data = str(ProceduralLevel(level_id, WIDTH, HEIGHT)).splitlines()
        self.current_level = Level(self.game.manager.screen, level_data)
        self.start_x, self.start_y = self.current_level.get_start_position()
        self.game.update_level(self)

    def next_level(self):
        if self.current_level_id < self.NUM_LEVELS:
            self.load_level(self.current_level_id + 1)
        else:
            self.more_levels = False
            self.game.set_over(True, "Congratulations! You finished the game!")
