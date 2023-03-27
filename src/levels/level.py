from src.objects.quark import Quark
from src.ui import Image, Tile

class Level:
    def __init__(self, screen, level_data, tile_size=32):
        self.screen = screen
        self.tile_size = tile_size
        self.tile_images = {tile_type: Image(f"tiles/{tile_type}.png", (tile_size, tile_size)) for tile_type in ["E", "W", "X", "Y", "Z"]}
        self.quarks = []
        self.quark_interactions = {
            'R': 'superposition',
            'G': 'entanglement',
            'B': 'quantum_tunneling',
            'T': 'time_dilation',
            'Q': 'collect'
        }
        self.load_level(level_data)
        self.time_limit = 120

    def load_level(self, level_data):
        self.level_data = level_data
        self.rows = len(level_data)
        self.cols = len(level_data[0])
        self.tiles = []

        for i, row in enumerate(level_data):
            tile_row = []
            for j, tile_value in enumerate(row):
                x = j * self.tile_size
                y = i * self.tile_size

                try:
                    if tile_value in self.quark_interactions.keys():
                        quark_image = f"quarks/{tile_value}.png"
                        quark_interaction = self.quark_interactions[tile_value]
                        quark = Quark(x, y, self.tile_size, self.tile_size, quark_image, quark_interaction)
                        self.quarks.append(quark)
                        tile = None  # Set tile to None when it's a quark.
                    else:
                        tile_image = self.tile_images[tile_value]
                        tile = Tile(x, y, self.tile_size, self.tile_size, tile_image)

                    if tile_value == "E":
                        self.goal = tile
                except KeyError:
                    tile = None  # Ignore unknown tile values.

                tile_row.append(tile)
            self.tiles.append(tile_row)

    def draw_quarks(self):
        for quark in self.quarks:
            quark.draw(self.screen)

    def draw(self):
        for row in self.tiles:
            for tile in row:
                if tile is not None:
                    tile.draw(self.screen)

        self.draw_quarks()

    def collides_with_wall(self, rect):
        for row in self.tiles:
            for tile in row:
                if tile is not None and tile.collides_with(rect) and tile != self.goal:
                    return True
        return False

    def get_start_position(self):
        for row in range(self.rows):
            for col in range(self.cols):
                if self.level_data[row][col] == "S":
                    return col * self.tile_size, row * self.tile_size
        return 0, 0
