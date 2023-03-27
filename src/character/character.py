from src.ui import Image

class Character:
    def __init__(self, x, y, sprite_path, size, max_speed_x, max_speed_y,
                 acceleration_x=0, acceleration_y=0, friction_coefficient=0.0, gravity=0, max_health=100):
        self.sprite = Image(sprite_path, size)
        self.bbox = self.sprite.get_rect(topleft=(x, y))

        self.x, self.y = x, y
        self.max_speed_x, self.max_speed_y = max_speed_x, max_speed_y
        self.acceleration_x, self.acceleration_y = acceleration_x, acceleration_y
        self.friction_coefficient = friction_coefficient
        self.gravity = gravity
        self.vx, self.vy = 0, 0
        self.max_health, self.health = max_health, max_health

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.defeated()

    def defeated(self):
        pass

    def accelerate(self, direction):
        self.vx += self.acceleration_x * direction[0]
        self.vy += self.acceleration_y * direction[1]

    def apply_friction(self, dt):
        friction_x = -self.friction_coefficient * self.vx
        friction_y = -self.friction_coefficient * self.vy

        self.vx += friction_x #* dt
        self.vy += friction_y #* dt

    def compute_new_position(self, dt):
        self.apply_friction(dt)
        self.vx = max(-self.max_speed_x, min(self.max_speed_x, self.vx))
        self.vy = max(-self.max_speed_y, min(self.max_speed_y, self.vy))
        self.vy += self.gravity * dt
        new_x = self.x + self.vx #* dt
        new_y = self.y + self.vy #* dt
        return new_x, new_y
    
    def set_position(self, x, y):
        self.x, self.y = x, y
        self.bbox.x, self.bbox.y = self.x, self.y
        self.sprite.position = (self.x, self.y)

    def clamp_position(self, screen):
        self.x = max(0, min(screen.get_width() - self.bbox.width, self.x))
        self.y = max(24, min(screen.get_height() - self.bbox.height, self.y))
        self.bbox.x, self.bbox.y = self.x, self.y

    def update(self, dt):
        new_x, new_y = self.compute_new_position(dt)
        self.set_position(new_x, new_y)

    def draw(self, screen):
        self.clamp_position(screen)
        self.sprite.draw(screen)

    def handle_input(self, events, keys):
        self.handle_events(events)
        self.handle_keys(keys)

    def handle_events(self, events):
        pass

    def handle_keys(self, keys):
        pass
