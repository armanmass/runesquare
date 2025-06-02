import pygame
from typing import List

class InventoryUI:
    def __init__(self, font: pygame.font.Font, screen_size: tuple[int, int], width: int = 180, height: int = 300, margin: int = 20) -> None:
        self.font = font
        self.screen_width, self.screen_height = screen_size
        self.width = width
        self.height = height
        self.margin = margin
        self.bg_color = (30, 30, 30)
        self.border_color = (200, 200, 200)
        self.text_color = (255, 255, 255)

    def draw(self, surface: pygame.Surface, items: List[str]) -> None:
        x = self.screen_width - self.width - self.margin
        y = self.screen_height - self.height - self.margin
        # Draw background
        pygame.draw.rect(surface, self.bg_color, (x, y, self.width, self.height))
        pygame.draw.rect(surface, self.border_color, (x, y, self.width, self.height), 2)
        # Draw title
        title_surf = self.font.render("Inventory", True, self.text_color)
        surface.blit(title_surf, (x + 10, y + 10))
        # Draw items
        line_height = self.font.get_height() + 2
        for idx, item in enumerate(items):
            item_surf = self.font.render(item, True, self.text_color)
            surface.blit(item_surf, (x + 10, y + 40 + idx * line_height))
