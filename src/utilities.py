import pygame
import os
from path import get_asset_path

font_registry = {}

def load_font(font_name, font_variant, font_size):
    font_id = f"{font_name}-{font_variant}-{font_size}"
    if font_id in font_registry:
        return font_registry[font_id]

    font_path = os.path.join("assets", "fonts", f"{font_name}-{font_variant}.ttf")
    font_path = get_asset_path(font_path)
    font = pygame.font.Font(font_path, font_size)
    font_registry[font_id] = font
    return font

def calculate_position(screen, position):
    width, height = screen.get_width(), screen.get_height()
    if position == 'center':
        return (width // 2, height // 2)
    elif (type(position) == tuple or type(position) == list) and len(position) == 2:
        if str(position[0]) == 'center' and type(position[1]) == int:
            return (width // 2, position[1])
        elif type(position[0]) == int and str(position[1]) == 'center':
            return (position[0], height // 2)
        elif str(position[0]) == 'center' and str(position[1]) == 'center':
            return (width // 2, height // 2)
    return position

def draw_text(screen, text, position='center', font_color=(255, 255, 255),
              font_name="SourceCodePro", font_variant="Regular", font_size=28,
              align="center"):
    font = load_font(font_name, font_variant, font_size)
    rendered_text = font.render(text, True, font_color)
    if align == "center":
        text_rect = rendered_text.get_rect(center=calculate_position(screen, position))
    elif align == "left":
        text_rect = rendered_text.get_rect(topleft=calculate_position(screen, position))
    elif align == "right":
        text_rect = rendered_text.get_rect(topright=calculate_position(screen, position))
    screen.blit(rendered_text, text_rect)

def draw_button(screen, text, position, font_name="SourceCodePro", font_variant="Regular",
                font_size=24, font_color=(255, 255, 255), bg_color=(50, 50, 50),
                border_color=(255, 255, 255), padding=(20, 10), radius=10, align="center"):
    font = load_font(font_name, font_variant, font_size)
    rendered_text = font.render(text, True, font_color)
    if align == "center":
        text_rect = rendered_text.get_rect(center=calculate_position(screen, position))
    elif align == "left":
        text_rect = rendered_text.get_rect(topleft=calculate_position(screen, position))
    elif align == "right":
        text_rect = rendered_text.get_rect(topright=calculate_position(screen, position))

    button_rect = pygame.Rect(text_rect.x - padding[0], text_rect.y - padding[1], text_rect.width + padding[0] * 2, text_rect.height + padding[1] * 2)
    pygame.draw.rect(screen, bg_color, button_rect, border_radius=radius)
    pygame.draw.rect(screen, border_color, button_rect, width=2, border_radius=radius)

    screen.blit(rendered_text, text_rect)

def load_image(image_path, size=None):
    image_path = os.path.join("assets", "images", image_path)
    image_path = get_asset_path(image_path)
    image = pygame.image.load(image_path)
    if size:
        image = pygame.transform.scale(image, size)
    return image

def vertical_gradient(screen, color1, color2):
    width, height = screen.get_size()
    for y in range(height):
        r = color1[0] + (color2[0] - color1[0]) * y / height
        g = color1[1] + (color2[1] - color1[1]) * y / height
        b = color1[2] + (color2[2] - color1[2]) * y / height
        pygame.draw.line(screen, (r, g, b), (0, y), (width, y))
