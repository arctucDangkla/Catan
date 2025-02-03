import pygame
import sys
import math

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Settlers of Catan")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Hexagon parameters
HEX_SIZE = 40
HEX_WIDTH = HEX_SIZE * 2
HEX_HEIGHT = int(HEX_SIZE * math.sqrt(3))

# Board dimensions
BOARD_ROWS = 5
BOARD_COLS = 5

# Hexagon grid
grid = []

def hex_corner(center, size, i):
    angle_deg = 60 * i
    angle_rad = math.pi / 180 * angle_deg
    return (center[0] + size * math.cos(angle_rad),
            center[1] + size * math.sin(angle_rad))

def draw_hexagon(surface, color, center, size):
    corners = [hex_corner(center, size, i) for i in range(6)]
    pygame.draw.polygon(surface, color, corners)
    pygame.draw.polygon(surface, BLACK, corners, 2)

def create_grid():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            x = col * HEX_WIDTH * 0.75
            y = row * HEX_HEIGHT
            if col % 2 == 1:
                y += HEX_HEIGHT / 2
            grid.append((x + HEX_WIDTH, y + HEX_HEIGHT))

def draw_grid():
    for center in grid:
        draw_hexagon(screen, WHITE, center, HEX_SIZE)

def main():
    clock = pygame.time.Clock()
    create_grid()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill(BLACK)
        draw_grid()
        pygame.display.flip()
        clock.tick(30)

if __name__ == "__main__":
    main()