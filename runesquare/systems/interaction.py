from typing import List, Optional, Tuple

def find_nearby_tree(player_rect: Tuple[int, int, int, int], tree_rects: List[Tuple[int, int, int, int]], threshold: int = 8) -> Optional[int]:
    px, py, pw, ph = player_rect
    for i, (tx, ty, tw, th) in enumerate(tree_rects):
        # Check if player is overlapping or within threshold pixels of the tree
        if (px + pw > tx - threshold and px < tx + tw + threshold and
            py + ph > ty - threshold and py < ty + th + threshold):
            return i  # Return the index of the nearby tree
    return None
