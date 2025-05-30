from typing import Tuple
import pygame
from runesquare.entities.skill_station import SkillStation

class Tree(SkillStation):
    def __init__(self, position: Tuple[int, int], size: int = 64) -> None:
        super().__init__(position, size)

    def get_rect(self) -> Tuple[int, int, int, int]:
        return (self.position[0], self.position[1], self.size, self.size)

    def draw(self, surface: pygame.Surface, camera_offset: Tuple[int, int]) -> None:
        screen_x = self.position[0] - camera_offset[0]
        screen_y = self.position[1] - camera_offset[1]
        pygame.draw.rect(surface, (34, 139, 34), (screen_x, screen_y, self.size, self.size))  # Forest green
