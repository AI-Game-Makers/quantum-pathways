import pygame

class Ghost:
    def __init__(self, x, y, image_path):
        # Sprite
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect(topleft=(x, y))

        # Position
        self.x = x             # x position in pixels
        self.y = y             # y position in pixels

        # Movement
        self.speed = 4         # Speed in pixels per frame
        self.acceleration = 1  # Acceleration in pixels per frame per frame
        self.friction = 0.9    # Friction multiplier (0.0 - 1.0)
        self.vx = 0            # Velocity in the x direction
        self.vy = 0            # Velocity in the y direction

    def collides_with_goal(self, goal):
        return self.rect.colliderect(goal.rect)

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)

    def handle_input(self, keys):
        new_x, new_y = self.x, self.y

        if keys[pygame.K_j]:
            self.vx -= self.acceleration
        if keys[pygame.K_l]:
            self.vx += self.acceleration
        if keys[pygame.K_i]:
            self.vy -= self.acceleration
        if keys[pygame.K_k]:
            self.vy += self.acceleration

        self.vx *= self.friction
        self.vy *= self.friction

        self.vx = max(-self.speed, min(self.speed, self.vx))
        self.vy = max(-self.speed, min(self.speed, self.vy))

        new_x += self.vx
        new_y += self.vy
