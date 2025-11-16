import pygame
import math

import settings


class LoadingScreen:
    def __init__(self, width: int = settings.SCREEN_WIDTH, height: int = settings.SCREEN_HEIGHT):
        pygame.init()

        self.running = True

        self.window = pygame.display.set_mode((width, height))

        self.clock = pygame.time.Clock()

        color_white = pygame.Color(255,255,255)
        waiting_font = pygame.font.SysFont("Comic Sans MS", 80)
        waiting_surface = waiting_font.render("Waiting for players...", True, color_white)
        time_font = pygame.font.SysFont("Comic Sans MS", 36)

        self.background = pygame.Surface(self.window.get_size())
        self._load_background_asset()
        waiting_dest = (self.window.get_width() * 0.5 - waiting_surface.get_width() * 0.5, self.window.get_height() * 0.15)
        arc_rect = pygame.Rect(0, 0, self.window.get_height() * 0.15, self.window.get_height() * 0.15)
        arc_rect.center = (int(self.window.get_width() * 0.5), int(self.window.get_height() * 0.5))

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.window.blit(self.background, (0, 0))
            self.window.blit(waiting_surface, waiting_dest)

            time_surface = time_font.render(f"Elapsed time: {int(pygame.time.get_ticks() / 1000)} seconds", True, color_white)
            time_dest = (self.window.get_width() * 0.5 - time_surface.get_width() * 0.5, self.window.get_height() * 0.7)
            self.window.blit(time_surface, time_dest)

            angle = pygame.time.get_ticks() / 200
            arc_length = math.pi * (math.sin(pygame.time.get_ticks() / 800) + 1.2) / 1.2
            pygame.draw.arc(self.window, color_white, arc_rect, angle, angle + arc_length, 10)

            pygame.display.flip()

            self.clock.tick(settings.FPS)


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

    def quit(self):
        self.running = False


def main():
    LoadingScreen()


if __name__ == "__main__":
    main()
