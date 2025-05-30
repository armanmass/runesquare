import pygame
from typing import Tuple

def load_tile(tileset: pygame.Surface, row: int, col: int, tile_size: int) -> pygame.Surface:
    """Extract a tile from a tileset image by row and column."""
    x = col * tile_size
    y = row * tile_size
    return tileset.subsurface((x, y, tile_size, tile_size)).copy() 