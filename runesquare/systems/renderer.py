import pygame
from runesquare.utils.assets import load_tile
from runesquare.settings import ISLAND_ELLIPSE, WORLD_WIDTH, WORLD_HEIGHT
from runesquare.entities.player import is_inside_ellipse
from typing import Tuple

def load_tiles() -> dict:
    tileset = pygame.image.load('runesquare/assets/images/environment/seasonal sample (spring).png').convert_alpha()
    return {
        "grass": load_tile(tileset, row=1, col=0, tile_size=16),
        "water": load_tile(tileset, row=13, col=11, tile_size=16)
    }

TILE_SIZE = 16

def draw_island(surface: pygame.Surface, camera_offset: Tuple[int, int], tiles: dict) -> None:
    for y in range(0, WORLD_HEIGHT, TILE_SIZE):
        for x in range(0, WORLD_WIDTH, TILE_SIZE):
            tile_rect = (x, y, TILE_SIZE, TILE_SIZE)
            screen_x = x - camera_offset[0]
            screen_y = y - camera_offset[1]
            # Draw water everywhere
            surface.blit(tiles["water"], (screen_x, screen_y))
            # Draw grass only inside the island
            if is_inside_ellipse(tile_rect, ISLAND_ELLIPSE):
                surface.blit(tiles["grass"], (screen_x, screen_y))
