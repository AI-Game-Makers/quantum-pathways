import pygame

class Quark:
    def __init__(self, x, y, width, height, image_path, interaction):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = pygame.image.load(image_path)
        self.rect = pygame.Rect(x, y, width, height)
        self.interaction = interaction

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def collides_with(self, rect):
        return self.rect.colliderect(rect)
