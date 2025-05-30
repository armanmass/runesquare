import pygame
from runesquare.settings import WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE, BACKGROUND_COLOR

class GameManager:
    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption(WINDOW_TITLE)
        self.clock = pygame.time.Clock()
        self.running = True

    def run(self) -> None:
        while self.running:
            self._handle_events()
            self._update()
            self._render()
            self.clock.tick(60)

    def _handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def _update(self) -> None:
        pass  # Game logic will go here

    def _render(self) -> None:
        self.screen.fill(BACKGROUND_COLOR)
        pygame.display.flip()

    def quit(self) -> None:
        pygame.quit()
