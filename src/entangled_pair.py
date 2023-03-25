import pygame
from src.utilities import load_image

class EntangledPair:
    def __init__(self, x, y, image_path='entangled_pair.png'):
        self.x = x
        self.y = y
        self.width = 32  # You may need to adjust this to match your tile size.
        self.height = 32  # You may need to adjust this to match your tile size.
        self.image = load_image(image_path)
        self.rect = pygame.Rect(x, y, self.width, self.height)

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def move_to(self, x, y):
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y
