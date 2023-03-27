import pygame
from enum import Enum
from src.ui import Image

class Quark:
    def __init__(self, x, y, width, height, image_path, interaction):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = Image(image_path, (width, height))
        self.bbox = pygame.Rect(x, y, width, height)
        self.interaction = interaction

    def draw(self, screen):
        self.image.position = (self.x, self.y)
        self.image.draw(screen)

    def collides_with(self, rect):
        return self.bbox.colliderect(rect)

class QuarkType(Enum):
    SUPERPOSITION = "superposition"
    ENTANGLEMENT = "entanglement"
    QUANTUM_TUNNELING = "quantum_tunneling"
    TIME_DILATION = "time_dilation"
    COLLECT = "collect"
