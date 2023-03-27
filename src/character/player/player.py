from src.character.character import Character

class Player(Character):
    def __init__(self, x, y, sprite_path, size=(30, 30), max_speed_x=4, max_speed_y=4,
                 acceleration_x=4, acceleration_y=4, friction_coefficient=0.1, gravity=0, max_health=100):
        super().__init__(x, y, sprite_path, size, max_speed_x, max_speed_y,
                         acceleration_x, acceleration_y, friction_coefficient, gravity, max_health)
        self.collected_quarks = 0