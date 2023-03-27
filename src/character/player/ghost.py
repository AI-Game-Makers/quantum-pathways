import pygame
from src.character.player.player import Player

class Ghost(Player):
    def __init__(self, x, y):
        super().__init__(x, y, 'ghost.png')
        self.active = False

    def activate(self, x, y):
        self.set_position(x, y)
        self.active = True

    def deactivate(self):
        self.active = False

    def draw(self, screen):
        if self.active:
            super().draw(screen)

    def update(self, dt):
        if self.active:
            super().update(dt)

    def handle_keys(self, keys):
        if self.active:
            if keys[pygame.K_j]:
                self.accelerate((-1, 0))
            if keys[pygame.K_l]:
                self.accelerate((1, 0))
            if keys[pygame.K_i]:
                self.accelerate((0, -1))
            if keys[pygame.K_k]:
                self.accelerate((0, 1))