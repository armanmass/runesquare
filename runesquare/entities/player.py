import pygame
from typing import Tuple

class Player:
    def __init__(self, position: Tuple[int, int], color: Tuple[int, int, int], size: int) -> None:
        self.position = list(position)  # [x, y]
        self.color = color
        self.size = size
        self.speed = 4

    def handle_input(self, keys: pygame.key.ScancodeWrapper) -> None:
        dx, dy = 0, 0
        if keys[pygame.K_w]:
            dy -= self.speed
        if keys[pygame.K_s]:
            dy += self.speed
        if keys[pygame.K_a]:
            dx -= self.speed
        if keys[pygame.K_d]:
            dx += self.speed
        self.position[0] += dx
        self.position[1] += dy

    def draw(self, surface: pygame.Surface) -> None:
        pygame.draw.rect(
            surface,
            self.color,
            (self.position[0], self.position[1], self.size, self.size)
        )
