from src.data.levels import level1, level2, level3, level4
from src.levels.level import Level


class LevelManager:
    def __init__(self, game):
        self.game = game
        self.levels = [level1, level2, level3, level4]
        self.current_level_id = 0
        self.load_level(self.current_level_id)
        self.more_levels = True

    def load_level(self, level_id):
        self.current_level_id = level_id
        self.current_level = Level(self.game.manager.screen, self.levels[level_id])
        self.start_x, self.start_y = self.current_level.get_start_position()
        self.game.update_level(self)

    def next_level(self):
        if self.current_level_id < len(self.levels) - 1:
            self.load_level(self.current_level_id + 1)
        else:
            self.more_levels = False
            self.game.set_over(True, "Congratulations! You finished the game!")
