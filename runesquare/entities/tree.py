from typing import Tuple
import pygame
import random
from runesquare.entities.skill_station import SkillStation

class Tree(SkillStation):
    def __init__(self, position: Tuple[int, int], size: int = 64) -> None:
        super().__init__(position, size)
        self.max_life = random.randint(2, 5)
        self.life = self.max_life

    def get_rect(self) -> Tuple[int, int, int, int]:
        return (self.position[0], self.position[1], self.size, self.size)

    def take_damage(self, amount: int = 1) -> None:
        self.life -= amount

    def is_dead(self) -> bool:
        return self.life <= 0

    def draw(self, surface: pygame.Surface, camera_offset: Tuple[int, int]) -> None:
        screen_x = self.position[0] - camera_offset[0]
        screen_y = self.position[1] - camera_offset[1]
        pygame.draw.rect(surface, (34, 139, 34), (screen_x, screen_y, self.size, self.size))  # Forest green
        # Draw life bar above tree
        bar_width = self.size
        bar_height = 6
        filled = int(bar_width * (self.life / self.max_life))
        bar_x = screen_x
        bar_y = screen_y - 10
        pygame.draw.rect(surface, (139, 69, 19), (bar_x, bar_y, bar_width, bar_height))  # Brown background
        pygame.draw.rect(surface, (50, 205, 50), (bar_x, bar_y, filled, bar_height))  # Green life
        pygame.draw.rect(surface, (0, 0, 0), (bar_x, bar_y, bar_width, bar_height), 1)
