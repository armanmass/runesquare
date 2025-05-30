import pygame
import random
from runesquare.settings import WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE, BACKGROUND_COLOR, WATER_COLOR, ISLAND_COLOR, ISLAND_ELLIPSE, WORLD_WIDTH, WORLD_HEIGHT
from runesquare.entities.player import Player
from runesquare.entities.tree import Tree
from runesquare.systems.renderer import load_tiles, draw_island
from runesquare.entities.player import is_inside_ellipse
from typing import Tuple

class GameManager:
    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption(WINDOW_TITLE)
        self.clock = pygame.time.Clock()
        self.running = True
        self.player = Player(
            position=(WORLD_WIDTH // 2, WORLD_HEIGHT // 2),
            color=(255, 255, 0),  # Yellow
            size=32
        )
        self.camera_offset = (0, 0)
        self.tiles = load_tiles()
        self.trees = self._generate_trees(num_trees=12, tree_size=64)

    def _generate_trees(self, num_trees: int, tree_size: int) -> list:
        trees = []
        attempts = 0
        while len(trees) < num_trees and attempts < num_trees * 10:
            x = random.randint(0, WORLD_WIDTH - tree_size)
            y = random.randint(0, WORLD_HEIGHT - tree_size)
            tree_rect = (x, y, tree_size, tree_size)
            if is_inside_ellipse(tree_rect, ISLAND_ELLIPSE):
                px, py = WORLD_WIDTH // 2, WORLD_HEIGHT // 2
                if abs(x - px) > tree_size and abs(y - py) > tree_size:
                    trees.append(Tree((x, y), size=tree_size))
            attempts += 1
        return trees

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
        tree_rects = [tree.get_rect() for tree in self.trees]
        self.player.handle_input(keys, tree_rects)
        self.camera_offset = self._calculate_camera_offset()

    def _calculate_camera_offset(self) -> Tuple[int, int]:
        px, py, pw, ph = self.player.get_rect()
        # Center camera on player
        cam_x = px + pw // 2 - WINDOW_WIDTH // 2
        cam_y = py + ph // 2 - WINDOW_HEIGHT // 2
        # Clamp to world bounds
        cam_x = max(0, min(cam_x, WORLD_WIDTH - WINDOW_WIDTH))
        cam_y = max(0, min(cam_y, WORLD_HEIGHT - WINDOW_HEIGHT))
        return (cam_x, cam_y)

    def _render(self) -> None:
        self.screen.fill(WATER_COLOR)
        draw_island(self.screen, self.camera_offset, self.tiles)
        for tree in self.trees:
            tree.draw(self.screen, self.camera_offset)
        self.player.draw(self.screen, self.camera_offset)
        pygame.display.flip()

    def quit(self) -> None:
        pygame.quit()
