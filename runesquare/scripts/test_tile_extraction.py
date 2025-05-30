import pygame
from runesquare.utils.assets import load_tile

def main():
    pygame.init()
    screen = pygame.display.set_mode((64, 64))
    pygame.display.set_caption("Tile Extraction Test")

    # Load the new tileset
    tileset = pygame.image.load('runesquare/assets/images/environment/seasonal sample (spring).png').convert_alpha()
    # Extract the grass tile at pixel (0, 16), size 16x16
    # Since load_tile uses (row, col), and each tile is 16x16, (0, 1) is (0, 16)
    grass_tile = load_tile(tileset, row=1, col=0, tile_size=16)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 0, 0))
        # Draw the tile in the center
        screen.blit(grass_tile, (24, 24))
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main() 