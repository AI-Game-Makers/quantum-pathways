import pygame
from src.tile import Tile
from src.quark import Quark
from path import get_asset_path

class Level:
    def __init__(self, screen, tile_size=32):
        self.screen = screen
        self.tile_size = tile_size
        self.tile_images = {
            'E': pygame.image.load(get_asset_path("assets/images/tiles/end.png")),
            'W': pygame.image.load(get_asset_path("assets/images/tiles/lime.png")),
            'X': pygame.image.load(get_asset_path("assets/images/tiles/light_green.png")),
            'Y': pygame.image.load(get_asset_path("assets/images/tiles/sky_blue.png")),
            'Z': pygame.image.load(get_asset_path("assets/images/tiles/dark_green.png")),
        }
        self.walls = ['W', 'X', 'Y', 'Z']
        self.quarks = []
        self.quark_interactions = {
            'R': 'superposition',
            'G': 'entanglement',
            'B': 'quantum_tunneling',
            'Q': 'collect'
        }

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
                        quark_image = get_asset_path(f"assets/images/quarks/{tile_value}.png")
                        quark_interaction = self.quark_interactions[tile_value]
                        quark = Quark(x, y, self.tile_size, self.tile_size, quark_image, quark_interaction)
                        self.quarks.append(quark)
                        tile = None  # Set tile to None when it's a quark.
                    else:
                        tile_image = self.tile_images[tile_value]
                        if tile_image is not None:
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

    def collides_with_wall(self, rect, quantum_tunneling_active):
        if quantum_tunneling_active:
            return False

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
