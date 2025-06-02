import pygame
import random
from runesquare.settings import WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE, BACKGROUND_COLOR, WATER_COLOR, ISLAND_COLOR, ISLAND_ELLIPSE, WORLD_WIDTH, WORLD_HEIGHT
from runesquare.entities.player import Player
from runesquare.entities.tree import Tree
from runesquare.systems.renderer import load_tiles, draw_island
from runesquare.entities.player import is_inside_ellipse
from typing import Tuple
from runesquare.systems.interaction import find_nearby_tree

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
        self.action = None  # e.g., {"type": "cutting", "target_idx": int, "progress": float}

    def _generate_trees(self, num_trees: int, tree_size: int) -> list:
        trees = []
        attempts = 0
        tree_sprite = self.tiles["tree"] # Get the tree sprite
        while len(trees) < num_trees and attempts < num_trees * 10:
            x = random.randint(0, WORLD_WIDTH - tree_size)
            y = random.randint(0, WORLD_HEIGHT - tree_size)
            tree_rect = (x, y, tree_size, tree_size)
            if is_inside_ellipse(tree_rect, ISLAND_ELLIPSE):
                px, py = WORLD_WIDTH // 2, WORLD_HEIGHT // 2
                if abs(x - px) > tree_size and abs(y - py) > tree_size:
                    trees.append(Tree((x, y), sprite=tree_sprite, size=tree_size)) # Pass the sprite
            attempts += 1
        return trees

    def run(self) -> None:
        while self.running:
            self._handle_events()
            dt = self.clock.tick(60) / 1000.0  # Delta time in seconds
            self._update(dt)
            self._render()

    def _handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                if self.action is None:
                    tree_rects = [tree.get_rect() for tree in self.trees]
                    player_rect = self.player.get_rect()
                    idx = find_nearby_tree(player_rect, tree_rects)
                    if idx is not None and not self.trees[idx].is_dead():
                        self.action = {
                            "type": "cutting",
                            "target_idx": idx,
                            "progress": 0.0,
                            "target_life": self.trees[idx].life,
                        }
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.action = None  # Allow canceling action

    def _update(self, dt: float) -> None:
        keys = pygame.key.get_pressed()
        tree_rects = [tree.get_rect() for tree in self.trees]
        self.player.handle_input(keys, tree_rects)
        self.camera_offset = self._calculate_camera_offset()
        CHOP_TIME = 1.0  # seconds per chop, can be moved/configured per station
        # Continuous action system
        if self.action is not None and self.action["type"] == "cutting":
            idx = self.action["target_idx"]
            if 0 <= idx < len(self.trees):
                tree = self.trees[idx]
                player_rect = self.player.get_rect()
                # Check proximity and if tree is alive
                if not tree.is_dead() and find_nearby_tree(player_rect, [tree.get_rect()]) == 0:
                    self.action["progress"] += dt  # Use real time, not frames
                    if self.action["progress"] >= CHOP_TIME:
                        tree.take_damage(1)
                        self.action["progress"] = 0.0
                        self.action["target_life"] = tree.life
                        # Use the station's skill/XP reward interface
                        skill_name, xp_amount = tree.get_skill_xp_reward()
                        leveled_up = self.player.add_xp(skill_name, xp_amount)
                        xp = self.player.get_skill_xp(skill_name)
                        level = self.player.get_skill_level(skill_name)
                        print(f"{skill_name} XP: {xp}, Level: {level}{' (Level Up!)' if leveled_up else ''}")
                        if tree.is_dead():
                            # Remove dead tree and spawn a new one
                            self.trees.pop(idx)
                            self.trees.append(self._spawn_tree(tree_size=64))
                            self.action = None
                else:
                    self.action = None  # Cancel if out of range or tree dead
            else:
                self.action = None

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
        # Draw progress bar if cutting
        if self.action is not None and self.action["type"] == "cutting":
            px, py, pw, ph = self.player.get_rect()
            bar_width = 48
            bar_height = 8
            progress = min(self.action["progress"], 1.0)
            filled = int(bar_width * progress)
            screen_x = px - self.camera_offset[0] + (pw - bar_width) // 2
            screen_y = py - self.camera_offset[1] - 16
            # Draw background
            pygame.draw.rect(self.screen, (60, 60, 60), (screen_x, screen_y, bar_width, bar_height))
            # Draw filled portion
            pygame.draw.rect(self.screen, (50, 205, 50), (screen_x, screen_y, filled, bar_height))
            # Draw border
            pygame.draw.rect(self.screen, (0, 0, 0), (screen_x, screen_y, bar_width, bar_height), 2)
        pygame.display.flip()

    def _spawn_tree(self, tree_size: int) -> Tree:
        attempts = 0
        tree_sprite = self.tiles["tree"] # Get the tree sprite
        while attempts < 100:
            x = random.randint(0, WORLD_WIDTH - tree_size)
            y = random.randint(0, WORLD_HEIGHT - tree_size)
            tree_rect = (x, y, tree_size, tree_size)
            if is_inside_ellipse(tree_rect, ISLAND_ELLIPSE):
                px, py = WORLD_WIDTH // 2, WORLD_HEIGHT // 2
                if abs(x - px) > tree_size and abs(y - py) > tree_size:
                    # Avoid overlapping other trees
                    for t in self.trees:
                        tx, ty, tw, th = t.get_rect()
                        if (x < tx + tw and x + tree_size > tx and y < ty + th and y + tree_size > ty):
                            break
                    else:
                        return Tree((x, y), sprite=tree_sprite, size=tree_size) # Pass the sprite
            attempts += 1
        # Fallback: just return a tree at center
        return Tree((WORLD_WIDTH // 2, WORLD_HEIGHT // 2), sprite=tree_sprite, size=tree_size) # Pass the sprite

    def quit(self) -> None:
        pygame.quit()
