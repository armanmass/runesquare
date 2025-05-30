from typing import Tuple
import pygame

class SkillStation:
    def __init__(self, position: Tuple[int, int], size: int = 32) -> None:
        self.position = position  # (x, y) in world coordinates
        self.size = size

    def draw(self, surface: pygame.Surface, camera_offset: Tuple[int, int]) -> None:
        # Placeholder: draw as a gray square
        screen_x = self.position[0] - camera_offset[0]
        screen_y = self.position[1] - camera_offset[1]
        pygame.draw.rect(surface, (128, 128, 128), (screen_x, screen_y, self.size, self.size))
