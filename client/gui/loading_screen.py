import pygame

import settings


class LoadingScreen:
    def __init__(self, width: int = settings.SCREEN_WIDTH, height: int = settings.SCREEN_HEIGHT):
        pygame.init()

        self.running = True

        self.window = pygame.display.set_mode((width, height))

        self.font = pygame.font.SysFont("Comic Sans MS", 100)
        self.font_surface = self.font.render("Waiting for players...", True, pygame.Color(255,255,255))

        self.background = pygame.Surface(self.window.get_size())
        self._load_background_asset()
        self.window.blit(self.background, (0, 0))
        self.window.blit(self.font_surface, (0, 0))
        pygame.display.flip()
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False



    def _load_background_asset(self) -> None:
        """Loads the background image or creates a fallback."""
        try:
            self.background = pygame.image.load("assets/loading_background.jpg").convert()
            self.background = pygame.transform.scale(self.background, self.window.get_size())
            print("[INFO] Background loaded successfully.")
        except Exception as e:
            print(f"[ERROR] Could not load background.jpg: {e}. Using fallback solid color.")
            self.background = pygame.Surface(self.window.get_size())
            self.background.fill((40, 40, 50))


def main():
    LoadingScreen()


if __name__ == "__main__":
    main()
