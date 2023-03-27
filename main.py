import traceback

def main():
    import pygame
    from src.game_manager import GameManager

    gm = GameManager()
    gm.run()

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
            raise e
