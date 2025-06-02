from typing import Tuple
import pygame
import random
from runesquare.entities.skill_station import SkillStation

class Tree(SkillStation):
    def __init__(self, position: Tuple[int, int], sprite: pygame.Surface, size: int = 64) -> None:
        super().__init__(position, size)
        self.sprite = sprite # Store the sprite
        self.max_life = random.randint(2, 5)
        self.life = self.max_life

    def get_rect(self) -> Tuple[int, int, int, int]:
        # Keep the original interactive/collision rect based on position and size
        return (self.position[0], self.position[1], self.size, self.size)

    def take_damage(self, amount: int = 1) -> None:
        self.life -= amount

    def is_dead(self) -> bool:
        return self.life <= 0

    def draw(self, surface: pygame.Surface, camera_offset: Tuple[int, int]) -> None:
        # Calculate screen position based on tree's base position
        screen_x_base = self.position[0] - camera_offset[0]
        screen_y_base = self.position[1] - camera_offset[1]

        # Calculate offset to align sprite base with the tree's interactive area base
        # We want the bottom-center of the sprite to align with the bottom-center of the tree's size rect
        sprite_width, sprite_height = self.sprite.get_size()
        # Calculate the bottom-center of the tree's size rect
        tree_center_x = screen_x_base + self.size // 2
        tree_bottom_y = screen_y_base + self.size

        # Calculate the top-left corner to blit the sprite
        # Sprite's left edge should be tree_center_x - sprite_width // 2
        # Sprite's top edge should be tree_bottom_y - sprite_height
        sprite_screen_x = tree_center_x - sprite_width // 2
        sprite_screen_y = tree_bottom_y - sprite_height

        # Draw the sprite
        surface.blit(self.sprite, (sprite_screen_x, sprite_screen_y))

        # Draw life bar above tree (relative to sprite position)
        bar_width = 48 # Make life bar a fixed width, or scale based on tree size
        bar_height = 6
        filled = int(bar_width * (self.life / self.max_life))
        # Position life bar above the sprite, centered
        bar_x = sprite_screen_x + (sprite_width - bar_width) // 2
        bar_y = sprite_screen_y - bar_height - 5 # A little padding above the sprite
        pygame.draw.rect(surface, (139, 69, 19), (bar_x, bar_y, bar_width, bar_height))  # Brown background
        pygame.draw.rect(surface, (50, 205, 50), (bar_x, bar_y, filled, bar_height))  # Green life
        pygame.draw.rect(surface, (0, 0, 0), (bar_x, bar_y, bar_width, bar_height), 1)

    def get_skill_xp_reward(self) -> tuple[str, int]:
        return ("Woodcutting", 25)
