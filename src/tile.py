import pygame

class Tile(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, image):
        super().__init__()
        self.image = image
        self.rect = pygame.Rect(x, y, width, height)

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)

    def collides_with(self, rect):
        return self.rect.colliderect(rect)
