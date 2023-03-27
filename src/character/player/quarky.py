import pygame
from src.character.player.player import Player
from src.character.player.ghost import Ghost
from src.character.entangled_pair import EntangledPair

class Quarky(Player):
    def __init__(self, x, y):
        super().__init__(x, y, 'quarky.png')
        self.level = None

        # Quarky has a 'ghost` that is a temporary copy of himself
        # and appears when he uses the superposition ability
        self.superposition_active = False
        self.ghost = Ghost(self.bbox.x, self.bbox.y)

        # Quarky can get entangled with another instance of himself
        # and teleport to his entangled pair when he uses the
        # entanglement ability
        self.entanglement_active = False
        self.entangled_pair = None

        # Quarky can use quantum tunneling to tunnel through
        # solid objects when he uses the quantum tunneling ability
        self.quantum_tunneling_active = False

    def set_level(self, level):
        self.level = level

    def collides_with_goal(self, goal):
        return self.bbox.colliderect(goal.rect)
    
    def collides_with_quark(self, quarks):
        for quark in quarks:
            if self.bbox.colliderect(quark.bbox):
                return quark
        return None

    def merge_with_ghost(self):
        self.set_position(self.ghost.bbox.x, self.ghost.bbox.y)
        self.ghost.deactivate()

    def draw(self, screen):
        if self.entangled_pair:
            self.entangled_pair.draw(screen)
        super().draw(screen)
        self.ghost.draw(screen)

    def activate_superposition(self):
        self.superposition_active = True
        self.ghost.activate(self.x, self.y)

    def deactivate_superposition(self):
        if self.superposition_active:
            self.superposition_active = False
            self.merge_with_ghost()

    def activate_entanglement(self):
        self.entanglement_active = True

    def toggle_entanglement(self):
        if self.entanglement_active:
            if self.entangled_pair:
                self.set_position(self.entangled_pair.x, self.entangled_pair.y)
                self.entangled_pair = None
                self.entanglement_active = False
            else:
                self.entangled_pair = EntangledPair(self.x, self.y)

    def activate_quantum_tunneling(self):
        self.quantum_tunneling_active = True

    def deactivate_quantum_tunneling(self):
        if self.quantum_tunneling_active:
            self.quantum_tunneling_active = False

    def handle_events(self, events):
        super().handle_events(events)
        actions = {
            pygame.K_m: self.deactivate_superposition,
            pygame.K_t: self.deactivate_quantum_tunneling,
            pygame.K_e: self.toggle_entanglement,
        }

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key in actions:
                    actions[event.key]()

    def handle_keys(self, keys):
        super().handle_keys(keys)
        self.ghost.handle_keys(keys)
        if keys[pygame.K_LEFT]:
            self.accelerate((-1, 0))
        if keys[pygame.K_RIGHT]:
            self.accelerate((1, 0))
        if keys[pygame.K_UP]:
            self.accelerate((0, -1))
        if keys[pygame.K_DOWN]:
            self.accelerate((0, 1))

    def handle_quark_interaction(self, quark, level):
        if quark.interaction == "superposition":
            self.activate_superposition()
        elif quark.interaction == "entanglement":
            self.activate_entanglement()
        elif quark.interaction == "quantum_tunneling":
            self.quantum_tunneling_active = True
        elif quark.interaction == "collect":
            self.collected_quarks += 1

        level.quarks.remove(quark)

    def update(self, dt):
        if self.level:
            # Update the player's position while checking for collisions
            new_x, new_y = self.compute_new_position(dt)
            if self.quantum_tunneling_active:
                self.set_position(new_x, new_y)
            else:
                new_bbox = pygame.Rect(new_x, self.y, self.bbox.width, self.bbox.height)
                if not self.level.collides_with_wall(new_bbox):
                    self.set_position(new_x, self.y)

                new_bbox = pygame.Rect(self.x, new_y, self.bbox.width, self.bbox.height)
                if not self.level.collides_with_wall(new_bbox):
                    self.set_position(self.x, new_y)

            # Quarks can be collected regardless of quantum tunneling
            quark_collision = self.collides_with_quark(self.level.quarks)
            if quark_collision:
                self.handle_quark_interaction(quark_collision, self.level)
            
            # Update the ghost if superposition is active
            if self.superposition_active:
                self.ghost.update(dt)
