import os
import pygame
from src.ui import FontManager
from src.ui.colors import COLORS
from path import get_asset_path

class Widget:
    def __init__(self):
        self.fm = FontManager.get_instance()

    def calculate_position(self, screen, position):
        width, height = screen.get_width(), screen.get_height()
        x, y = 0, 0
        if position == 'center':
            x, y = (width // 2, height // 2)
        elif (type(position) == tuple or type(position) == list) and len(position) == 2:
            if str(position[0]) == 'center' and type(position[1]) == int:
                x, y = (width // 2, position[1])
            elif type(position[0]) == int and str(position[1]) == 'center':
                x, y = (position[0], height // 2)
            elif str(position[0]) == 'center' and str(position[1]) == 'center':
                x, y = (width // 2, height // 2)
            elif type(position[0]) == int and type(position[1]) == int:
                x, y = position[0], position[1]

        if x < 0:
            x = width + x
        if y < 0:
            y = height + y

        return x, y


class Label(Widget):

    def __init__(self, text, position='center', font_color=COLORS["white"],
                 font_name="SourceCodePro", font_variant="Regular", font_size=28,
                 align="center"):
        super().__init__()
        self.text = text
        self.position = position
        self.align = align
        self.font_name = font_name
        self.font_color = font_color
        self.font_size = font_size
        self.font = self.fm.get_font(font_name, font_variant, font_size)

    def _draw(self, screen):
        """ Internal method to draw the label """
        rendered_text = self.font.render(self.text, True, self.font_color)
        if self.align == "center":
            text_rect = rendered_text.get_rect(center=self.calculate_position(screen, self.position))
        elif self.align == "left":
            text_rect = rendered_text.get_rect(topleft=self.calculate_position(screen, self.position))
        elif self.align == "right":
            text_rect = rendered_text.get_rect(topright=self.calculate_position(screen, self.position))
        return rendered_text, text_rect

    def draw(self, screen):
        """ Draw the label """
        rendered_text, text_rect = self._draw(screen)     
        screen.blit(rendered_text, text_rect)


class Button(Label):

    def __init__(self, text, position='center', font_color=COLORS["white"],
                 font_name="SourceCodePro", font_variant="Regular", font_size=28,
                 bg_color=COLORS["gray"], border_color=COLORS["white"],
                 padding=(20, 10), radius=10, align="center"):
        super().__init__(text, position, font_color, font_name, font_variant, font_size, align)
        self.bg_color = bg_color
        self.border_color = border_color
        self.padding = padding
        self.radius = radius

    def select(self):
        self.bg_color = COLORS["white"]
        self.border_color = COLORS["gray"]
        self.font_color = COLORS["dark_blue"]
        self.font = self.fm.get_font(self.font_name, "Bold", self.font_size)

    def deselect(self):
        self.bg_color = COLORS["gray"]
        self.border_color = COLORS["white"]
        self.font_color = COLORS["white"]
        self.font = self.fm.get_font(self.font_name, "Regular", self.font_size)

    def draw(self, screen):
        rendered_text, text_rect = self._draw(screen)

        button_rect = pygame.Rect(text_rect.x - self.padding[0], text_rect.y - self.padding[1],
                                 text_rect.width + self.padding[0] * 2, text_rect.height + self.padding[1] * 2)
        pygame.draw.rect(screen, self.bg_color, button_rect, border_radius=self.radius)
        pygame.draw.rect(screen, self.border_color, button_rect, width=2, border_radius=self.radius)

        screen.blit(rendered_text, text_rect)


class GradientBackground(Widget):

    def __init__(self, color_start, color_end, direction="vertical"):
        super().__init__()
        self.color_start = color_start
        self.color_end = color_end
        self.direction = direction

    def draw(self, screen):
        if self.direction == 'vertical':
            self.draw_vertical(screen, self.color_start, self.color_end)
        elif self.direction == 'horizontal':
            self.draw_horizontal(screen, self.color_start, self.color_end)

    def draw_vertical(self, screen, color1, color2):
        width, height = screen.get_size()
        for y in range(height):
            r = color1[0] + (color2[0] - color1[0]) * y / height
            g = color1[1] + (color2[1] - color1[1]) * y / height
            b = color1[2] + (color2[2] - color1[2]) * y / height
            pygame.draw.line(screen, (r, g, b), (0, y), (width, y))

    def draw_horizontal(self, screen, color1, color2):
        width, height = screen.get_size()
        for x in range(width):
            r = color1[0] + (color2[0] - color1[0]) * x / width
            g = color1[1] + (color2[1] - color1[1]) * x / width
            b = color1[2] + (color2[2] - color1[2]) * x / width
            pygame.draw.line(screen, (r, g, b), (x, 0), (x, height))


class Image(Widget):

    def __init__(self, image_path, size, position=(0, 0)):
        super().__init__()
        image_path = os.path.join("assets", "images", image_path)
        image_path = get_asset_path(image_path)
        image = pygame.image.load(image_path)
        if size:
            image = pygame.transform.scale(image, size)

        # Convert image to the same format as the display surface for faster blitting
        self.image = image.convert_alpha() if image_path.endswith(".png") else image.convert()
        self.position = position

    def get_rect(self, **kwargs):
        return self.image.get_rect(**kwargs)

    def draw(self, screen):
        screen.blit(self.image, self.position)