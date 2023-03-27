import pygame
import os
from path import get_asset_path


class FontManager:
    """ A singleton class to manage fonts. """

    __instance = None

    @staticmethod
    def get_instance():
        """ Static access method. """
        if FontManager.__instance == None:
            FontManager()
        return FontManager.__instance
    
    def __init__(self):
        """ Virtually private constructor. """
        if FontManager.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            FontManager.__instance = self
            self.font_cache = {}
    
    def get_font_id(self, font_name, font_variant, font_size):
        return f"{font_name}-{font_variant}-{font_size}"

    def get_cached_font(self, font_name, font_variant, font_size):
        font_id = self.get_font_id(font_name, font_variant, font_size)
        return self.font_cache[font_id]

    def get_font(self, font_name, font_variant, font_size):
        if not self.has_font(font_name, font_variant, font_size):
            self.load_font(font_name, font_variant, font_size)

        return self.get_cached_font(font_name, font_variant, font_size)

    def has_font(self, font_name, font_variant, font_size):
        font_id = self.get_font_id(font_name, font_variant, font_size)
        return font_id in self.font_cache

    def load_font(self, font_name, font_variant, font_size):
        font_path = os.path.join("assets", "fonts", f"{font_name}-{font_variant}.ttf")
        font_path = get_asset_path(font_path)
        font = pygame.font.Font(font_path, font_size)
        self.update_cache(font_name, font_variant, font_size, font)
    
    def update_cache(self, font_name, font_variant, font_size, font):
        font_id = self.get_font_id(font_name, font_variant, font_size)
        self.font_cache[font_id] = font
    