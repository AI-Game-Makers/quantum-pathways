import pygame
from src.utilities import draw_text, vertical_gradient

class HelpPage:
    def __init__(self, screen):
        self.screen = screen
        self.current_page = 1
        instructions = "# Welcome to Quantum Pathways!\n" + \
        "\n" + \
        "## Objective:\n" + \
        "Guide Quarky to the flag within the time limit to complete a level. Collect quarks to gain points and unlock quantum abilities.\n" + \
        "\newpage" + \
        "## Controls:\n" + \
        "- Arrow keys: Move Quarky\n" + \
        "- `I` `J` `K` `L` : Control ghost when superimposed\n" + \
        "\n" + \
        "## Navigation:\n" + \
        "Press `P` to pause or unpause the game, and `Q` to return to the main menu.\n" + \
        "\newpage" + \
        "## Quantum Abilities:\n" + \
        "1. **Superposition** (Red Quark): Creates a ghost that can be controlled separately. Press `M` to merge with the ghost.\n" + \
        "2. **Quantum Tunneling** (Blue Quark): Enables Quarky to pass through walls. Press `T` to toggle tunneling on/off.\n" + \
        "3. **Entanglement** (Green Quark): Press `E` to create an entangled pair and teleport to its location.\n" + \
        "\newpage" + \
        "## Collectibles:\n" + \
        "- Orange Quark: Collect to gain points\n" + \
        "\newpage" + \
        "## Tips:\n" + \
        "- Utilize quantum interactions to overcome obstacles and solve puzzles. Be cautious when disabling tunneling to avoid trapping yourself. Observe your environment and think ahead before using your abilities, as they can sometimes have unintended consequences. Experiment with different strategies to find the most effective solutions."
        self.pages = instructions.split("\newpage")

        from pygame_markdown import MarkdownRenderer
        self.markdowns = []
        for page in self.pages:
            md = MarkdownRenderer()
            md.set_markdown_from_string(md_string=page)
            md.set_area(self.screen, 0, 0, self.screen.get_width(), self.screen.get_height())
            md.set_color_background(r=0, g=0, b=50)
            md.set_color_font(r=255, g=255, b=255)
            self.markdowns.append(md)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if self.current_page > 1:
                        self.current_page -= 1

                if event.key == pygame.K_RIGHT:
                    if self.current_page < len(self.pages):
                        self.current_page += 1

    def draw(self):
        """ Draw the help page. """
        vertical_gradient(self.screen, (0, 0, 50), (128, 0, 128))  # Dark blue to purple gradient
        page_text = self.markdowns[self.current_page - 1]
        self.draw_markdown(page_text)
        self.draw_arrows()

    def draw_markdown(self, markdown):
        """ Parse and draw markdown text to the screen.  """
        pygame_events = pygame.event.get()
        mouse_x, mouse_y = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()
        markdown.display(pygame_events, mouse_x, mouse_y, mouse_pressed)

    def draw_arrows(self):
        """ Draw page navigation arrows in the bottom left and right corners using text. """
        y = self.screen.get_height() - 20
        footer_font_variant = "Regular"
        footer_font_color = (255, 255, 255)

        # Draw arrows
        if self.current_page > 1:
            draw_text(self.screen, "<", (30, y), font_color=footer_font_color,
                      font_size=30, font_variant=footer_font_variant)
        if self.current_page < len(self.pages):
            draw_text(self.screen, ">", (self.screen.get_width() - 30, y),
                      font_color=footer_font_color, font_size=30, font_variant=footer_font_variant)

        # Add footer text
        footer_1 = str(self.current_page) + " of " + str(len(self.pages))
        draw_text(self.screen, footer_1, ('center', y - 8), font_color=footer_font_color,
                  font_size=14, font_variant=footer_font_variant)

        footer_2 = "Press Q to return to main menu"
        draw_text(self.screen, footer_2, ('center', y + 8), font_color=footer_font_color,
                  font_size=12, font_variant=footer_font_variant)