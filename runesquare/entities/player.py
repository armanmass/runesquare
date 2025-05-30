import pygame
from typing import Tuple, List
from runesquare.settings import ISLAND_ELLIPSE

def is_inside_ellipse(rect: Tuple[int, int, int, int], ellipse: Tuple[int, int, int, int]) -> bool:
    rx, ry, rw, rh = rect
    ex, ey, ew, eh = ellipse
    px = rx + rw / 2
    py = ry + rh / 2
    cx = ex + ew / 2
    cy = ey + eh / 2
    nx = (px - cx) / (ew / 2)
    ny = (py - cy) / (eh / 2)
    return nx * nx + ny * ny <= 1

def collides_with_any(rect: Tuple[int, int, int, int], obstacles: List[Tuple[int, int, int, int]]) -> bool:
    rx, ry, rw, rh = rect
    for ox, oy, ow, oh in obstacles:
        if rx < ox + ow and rx + rw > ox and ry < oy + oh and ry + rh > oy:
            return True
    return False

class Player:
    def __init__(self, position: Tuple[int, int], color: Tuple[int, int, int], size: int) -> None:
        self.position = list(position)  # [x, y] in world coordinates
        self.color = color
        self.size = size
        self.speed = 4

    def handle_input(self, keys: pygame.key.ScancodeWrapper, tree_rects: List[Tuple[int, int, int, int]]) -> None:
        dx, dy = 0, 0
        if keys[pygame.K_w]:
            dy -= self.speed
        if keys[pygame.K_s]:
            dy += self.speed
        if keys[pygame.K_a]:
            dx -= self.speed
        if keys[pygame.K_d]:
            dx += self.speed
        new_rect = (
            self.position[0] + dx,
            self.position[1] + dy,
            self.size,
            self.size
        )
        if is_inside_ellipse(new_rect, ISLAND_ELLIPSE) and not collides_with_any(new_rect, tree_rects):
            self.position[0] += dx
            self.position[1] += dy

    def get_rect(self) -> Tuple[int, int, int, int]:
        return (self.position[0], self.position[1], self.size, self.size)

    def draw(self, surface: pygame.Surface, camera_offset: Tuple[int, int]) -> None:
        screen_x = self.position[0] - camera_offset[0]
        screen_y = self.position[1] - camera_offset[1]
        pygame.draw.rect(
            surface,
            self.color,
            (screen_x, screen_y, self.size, self.size)
        )
