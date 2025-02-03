#To make the actual board for Catan
import math
import pygame
import random

# Screen Size
SCREENWIDTH = 1000
SCREENHEIGHT = SCREENWIDTH * .80 #800 pixels

# The list of tiles and what material it produces.
# This default value is the recommended order to place the tiles, from top row to bottom, left to right.
tile_list = ["O", "S", "Wo", "Wh", "B", "S", "B", "Wh", "Wo", "D", "Wo", "O", "Wo", "O", "Wh", "S", "B", "Wh", "S"]


# pygame setup
pygame.init()
screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
pygame.display.set_caption("Catan")
running = True


# To make the hexagons for the board
def calculate_hexagon(center_x, center_y, radius):
    points = []
    for i in range(6):  # 6 sides in a hexagon
        angle_deg = 60 * i -90 # Start at -90° so that point is at the top
        angle_rad = math.radians(angle_deg)
        x = center_x + radius * math.cos(angle_rad)
        y = center_y + radius * math.sin(angle_rad)
        points.append((x, y))
    return points
# Function that will check the color of the inputed color in the form of a string
# Wo = wood (dark green), B = brick (reddish brown), Wh = wheat (yellow), O = ore (grey), S = sheep (light green)
# D = desert (tan)
def color_check(color):
    if color == "Wo":
        return (81,125,25)
    elif color == "B":
        return (156,67,0)
    elif color == "Wh":
        return (240,173,0)
    elif color == "O":
        return (123,111,131)
    elif color == "S":
        return (143,206,0)
    elif color == "D":
        return (194, 178, 128)
    else:
        return (255,255,255)

# Function that will maintain the look of the board
def game_board():
    # Colors for the board
    bg_color = (79, 166, 235)
    # Size info for the hexagon
    start_x = SCREENWIDTH * 0.35
    start_y = SCREENHEIGHT / 6
    hex_size = SCREENHEIGHT / 10
    hex_diff = 150

    # The index position for tile_list
    idx = 0

    screen.fill(bg_color)
    # First row
    for i in range(3):
        pygame.draw.polygon(screen, color_check(tile_list[idx]), calculate_hexagon(start_x + hex_diff * i, start_y, hex_size))
        idx += 1
    # Second row
    for i in range(4):
        pygame.draw.polygon(screen, color_check(tile_list[idx]), calculate_hexagon(start_x - hex_size + 5 + hex_diff * i, start_y + 125, hex_size))
        idx += 1
    # Third row
    for i in range (5):
        pygame.draw.polygon(screen, color_check(tile_list[idx]), calculate_hexagon(start_x - hex_size * 2 + 10 + hex_diff * i, start_y + 250, hex_size))
        idx += 1
    # Fourth row
    for i in range (4):
        pygame.draw.polygon(screen, color_check(tile_list[idx]), calculate_hexagon(start_x - hex_size + 5 + hex_diff * i, start_y + 375, hex_size))
        idx += 1
    # Fifth row
    for i in range (3):
        pygame.draw.polygon(screen, color_check(tile_list[idx]), calculate_hexagon(start_x + hex_diff * i, start_y + 500, hex_size))
        idx += 1

while running:
    # Check for events, such as closing game.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    # draws the game board
    game_board()

    pygame.display.update()

# Closes the game safely
pygame.quit()