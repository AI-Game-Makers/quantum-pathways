import pygame
from src.ui import Label, GradientBackground, COLORS
from src.scenes import Scene


class HelpPage(Scene):
    def __init__(self, game_manager):
        super().__init__(game_manager)
        self.screen = game_manager.screen
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

        self.background = GradientBackground(COLORS["dark_blue"], COLORS["purple"])

        font_variant = "Regular"
        font_color = COLORS["white"]
        y = -20

        self.left_label = Label("<", (30, y), font_color=font_color, font_size=30, font_variant=font_variant)
        self.right_label = Label(">", (- 30, y), font_color=font_color, font_size=30, font_variant=font_variant)
        
        pages = str(self.current_page) + " of " + str(len(self.pages))
        self.footer_1 = Label(pages, ('center', y - 8), font_color=font_color, font_size=14, font_variant=font_variant)

        menu = "Press Q to return to main menu"
        self.footer_2 = Label(menu, ('center', y + 8), font_color=font_color, font_size=12, font_variant=font_variant)


    def update(self, dt):
        pass

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if self.current_page > 1:
                        self.current_page -= 1

                if event.key == pygame.K_RIGHT:
                    if self.current_page < len(self.pages):
                        self.current_page += 1

                if event.key == pygame.K_q:
                    self.manager.main_menu()

    def draw(self, screen):
        """ Draw the help page. """
        self.background.draw(screen)
        page_text = self.markdowns[self.current_page - 1]
        self.draw_markdown(page_text)
        self.draw_arrows(screen)
        self.footer_1.draw(screen)
        self.footer_2.draw(screen)

    def draw_markdown(self, markdown):
        """ Parse and draw markdown text to the screen.  """
        pygame_events = pygame.event.get()
        mouse_x, mouse_y = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()
        markdown.display(pygame_events, mouse_x, mouse_y, mouse_pressed)

    def draw_arrows(self, screen):
        if self.current_page > 1:
            self.left_label.draw(screen)
        if self.current_page < len(self.pages):
            self.right_label.draw(screen)
        