import pygame
from runesquare.settings import WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE, BACKGROUND_COLOR
from runesquare.entities.player import Player

class GameManager:
    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption(WINDOW_TITLE)
        self.clock = pygame.time.Clock()
        self.running = True
        self.player = Player(
            position=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2),
            color=(255, 255, 0),  # Yellow
            size=32
        )

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
        keys = pygame.key.get_pressed()
        self.player.handle_input(keys)

    def _render(self) -> None:
        self.screen.fill(BACKGROUND_COLOR)
        self.player.draw(self.screen)
        pygame.display.flip()

    def quit(self) -> None:
        pygame.quit()
