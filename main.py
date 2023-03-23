import traceback
import os

def main():
    import pygame
    from src.game import Game
    pygame.init()

    screen_width = 800
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Quantum Pathways")

    game = Game(screen)
    game.main_loop()

    pygame.quit()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        error_file = "error_log.txt"
        with open(error_file, "w") as f:
            f.write("Error encountered while running the game:\n")
            f.write(str(e))
            f.write("\n\nTraceback information:\n")
            traceback.print_exc(file=f)
        print(f"An error occurred. See {error_file} for details.")
        input("Press any key to exit...")
