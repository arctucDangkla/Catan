import pygame
import math
import random


class Board:
    def __init__(self, width, height):
        # List that will keep track of tile placement
        self.tile_list = ["O", "S", "Wo", "Wh", "B", "S", "B", "Wh", "Wo", "D",
                     "Wo", "O", "Wo", "O", "Wh", "S", "B", "Wh", "S"
                    ]
        self.height = height
        self.width = width
        # The color for the board game
        bg_color = (79, 166, 235)
        # The colors of each different material in a dictionary
        self.colors = {
            "Wo": (81,125,25),
            "B": (156,67,0),
            "Wh": (240,173,0),
            "O": (123,111,131),
            "S": (143,206,0),
            "D": (194, 178, 128)
        }

    # To make the hexagons for the board
    @staticmethod
    def __calculate_hexagon(center_x, center_y, radius):
        points = []
        for i in range(6):  # 6 sides in a hexagon
            angle_deg = 60 * i - 90  # Start at -90° so that point is at the top
            angle_rad = math.radians(angle_deg)
            x = center_x + radius * math.cos(angle_rad)
            y = center_y + radius * math.sin(angle_rad)
            points.append((x, y))
        return points

    # Method that will draw the game board
    def draw_board(self, screen):
        # Size info for the hexagon
        start_x = self.width * 0.35  # Starting x pos of the grid
        start_y = self.height / 6  # Starting y pos of the grid
        hex_size = self.height / 10  # Size of the hexagon
        hex_diff = hex_size * 1.875  # Difference between hexagons horizontally
        row_height = hex_diff - 25  # Difference between hexagons vertically

        # The index position for tile_list
        idx = 0

        # A list of tuples where (# of hexes, row offset)
        rows = [
            (3, 0),
            (4, 1),
            (5, 2),
            (4, 3),
            (3, 4)
        ]

        # Loop through each hex in each row
        for hex_count, row_offset in rows:
            for i in range(hex_count):
                x = start_x + hex_diff * i - (hex_count % 3) * hex_size + 5 * (hex_count % 3)
                y = start_y + row_height * row_offset
                points = self.__calculate_hexagon(x, y, hex_size)
                pygame.draw.polygon(screen, self.colors[self.tile_list[idx]], points)
                idx += 1

    # Shuffles the entire board
    def shuffle_board(self):
        random.shuffle(self.tile_list)
        # TO add number randomization:

    # Creates the beginner board
    def beginner_board(self):
        self.tile_list = ["O", "S", "Wo", "Wh", "B", "S", "B", "Wh", "Wo", "D",
                     "Wo", "O", "Wo", "O", "Wh", "S", "B", "Wh", "S"
                    ]
        # To add number ordering:
