from src.character.character import Character

class EntangledPair(Character):
    def __init__(self, x, y):
        super().__init__(x, y, 'entangled_pair.png', (32, 32), 4, 1, 0.9)
