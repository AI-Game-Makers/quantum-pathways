import pygame
from src.ghost import Ghost
from src.entangled_pair import EntangledPair
from path import get_asset_path

class Player:
    def __init__(self, x, y, sprite_path):
        # Sprite
        self.image = pygame.image.load(sprite_path)
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

        # Quark interactions (superposition, quantum tunneling, entanglement)
        self.ghost = None
        self.entangled_pair = None
        self.superposition_active = False
        self.entanglement_active = False
        self.quantum_tunneling_active = False
        self.collected_quarks = 0

    def collides_with_goal(self, goal):
        return self.rect.colliderect(goal.rect)
    
    def collides_with_quark(self, quarks):
        for quark in quarks:
            if self.rect.colliderect(quark.rect):
                return quark
        return None

    def create_ghost(self):
        if not self.ghost:
            self.ghost = Ghost(self.rect.x, self.rect.y, get_asset_path("assets/images/ghost.png"))

    def remove_ghost(self):
        self.ghost = None

    def merge_with_ghost(self):
        if self.ghost:
            self.rect.x = self.ghost.rect.x
            self.rect.y = self.ghost.rect.y
            self.remove_ghost()

    def draw_ghost(self, screen):
        if self.ghost:
            self.ghost.draw(screen)

    def create_entangled_pair(self):
        self.entangled_pair = EntangledPair(self.x, self.y, get_asset_path("assets/images/entangled_pair.png"))

    def teleport_to_entangled_pair(self):
        self.x, self.y = self.entangled_pair.x, self.entangled_pair.y
        self.rect.x = self.x
        self.rect.y = self.y

    def remove_entangled_pair(self):
        self.entangled_pair = None

    def draw_entangled_pair(self, screen):
        if self.entangled_pair:
            self.entangled_pair.draw(screen)

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)
        if self.ghost:
            self.draw_ghost(screen)
        if self.entangled_pair:
            self.draw_entangled_pair(screen)

    def handle_input(self, events):
        keys = pygame.key.get_pressed()
        for event in events:
            if event.type == pygame.KEYDOWN:
                if self.superposition_active and self.ghost:
                    self.ghost.handle_input(keys)
                    if event.key == pygame.K_m:
                        self.merge_with_ghost()
                        self.superposition_active = False
                
                if self.quantum_tunneling_active:
                    if event.key == pygame.K_t:
                        self.quantum_tunneling_active = False

                if self.entanglement_active:
                    if event.key == pygame.K_e:
                        if not self.entangled_pair:
                            self.create_entangled_pair()
                        else:
                            self.teleport_to_entangled_pair()
                            self.remove_entangled_pair()
                            self.entanglement_active = False

        if keys[pygame.K_LEFT]:
            self.vx -= self.acceleration
        if keys[pygame.K_RIGHT]:
            self.vx += self.acceleration
        if keys[pygame.K_UP]:
            self.vy -= self.acceleration
        if keys[pygame.K_DOWN]:
            self.vy += self.acceleration

    def handle_quark_interaction(self, quark, level):
        if quark.interaction == "superposition":
            self.superposition_active = True
            self.create_ghost()
        elif quark.interaction == "entanglement":
            self.entanglement_active = True
        elif quark.interaction == "quantum_tunneling":
            self.quantum_tunneling_active = True
        elif quark.interaction == "collect":
            self.collected_quarks += 1
            level.quarks.remove(quark)

    def update(self, level):
        new_x, new_y = self.x, self.y

        self.vx *= self.friction
        self.vy *= self.friction

        self.vx = max(-self.speed, min(self.speed, self.vx))
        self.vy = max(-self.speed, min(self.speed, self.vy))

        new_x += self.vx
        new_y += self.vy

        new_rect = pygame.Rect(new_x, self.y, self.rect.width, self.rect.height)
        if not level.collides_with_wall(new_rect, self.quantum_tunneling_active):
            self.x = new_x
            self.rect.x = new_x

        new_rect = pygame.Rect(self.x, new_y, self.rect.width, self.rect.height)
        if not level.collides_with_wall(new_rect, self.quantum_tunneling_active):
            self.y = new_y
            self.rect.y = new_y

        quark_collision = self.collides_with_quark(level.quarks)
        if quark_collision:
            self.handle_quark_interaction(quark_collision, level)
