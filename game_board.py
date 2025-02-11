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

        # The colors of each different material in a dictionary
        self.colors = {
            "Wo": (81,125,25),
            "B": (156,67,0),
            "Wh": (240,173,0),
            "O": (123,111,131),
            "S": (143,206,0),
            "D": (194, 178, 128)
        }

        # The numbers for each corresponding hexagon
        self.numbers = [10, 2, 9, 12, 6, 4, 10, 9, 11, 3, 8, 8, 3, 4, 5, 5, 6, 11]
        self.robber_pos = None
        self.font = pygame.font.Font(None, 36)  # Default font, size 36 for text

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
    def draw_board(self, screen, roll):
        # Color info for different parts of the board
        number_color = (0, 0, 0)  # Black color for numbers
        robber_color = (50, 50, 50)  # Dark gray for the robber

        # Size info for the hexagon
        start_x = self.width * 0.35  # Starting x pos of the grid
        start_y = self.height / 6  # Starting y pos of the grid
        hex_size = self.height / 10  # Size of the hexagon
        hex_diff = hex_size * 1.875  # Difference between hexagons horizontally
        row_height = hex_diff - 25  # Difference between hexagons vertically

        # The index position for tiles and number lists
        tile_idx = 0
        num_idx = 0

        # A list of tuples where (hex_count, row offset)
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
                # The center x and y positions of the current hex
                x = start_x + hex_diff * i - (hex_count % 3) * hex_size + 5 * (hex_count % 3)
                y = start_y + row_height * row_offset

                # Make and draw the hexagon
                points = self.__calculate_hexagon(x, y, hex_size)
                pygame.draw.polygon(screen, self.colors[self.tile_list[tile_idx]], points)

                # If it is the desert tile, move the robber, don't add number.
                if self.tile_list[tile_idx] == "D":
                    self.robber_pos = (x,y)
                # Otherwise add the number like a normal tile
                else:
                    # Initialize the number
                    number_text = self.font.render(str(self.numbers[num_idx]), True, number_color)
                    text_rect = number_text.get_rect(center=(x, y))

                    # If the current tile equals the roll, highlight the chip.
                    if self.numbers[num_idx] == roll:
                        pygame.draw.circle(screen, (255, 0, 0), (x, y), int(hex_size * .4))

                    # Draws a game chip to make number more visible
                    pygame.draw.circle(screen, self.colors["D"], (x, y), int(hex_size * 0.3))

                    # "Draw" the number on screen
                    screen.blit(number_text, text_rect)

                    num_idx += 1
                tile_idx += 1
        # Draws the robber after all of the board is made. If the roll is 7,
        # highlight the robber.
        if roll == 7:
            pygame.draw.circle(screen, (255, 0, 0), self.robber_pos, int(hex_size * 0.4))
        pygame.draw.circle(screen, robber_color, self.robber_pos, int(hex_size * 0.3))


    # Shuffles the entire board and numbers
    def shuffle_board(self):
        random.shuffle(self.tile_list)
        random.shuffle(self.numbers)

    # Creates the beginner board
    def beginner_board(self):
        self.tile_list = ["O", "S", "Wo", "Wh", "B", "S", "B", "Wh", "Wo", "D",
                     "Wo", "O", "Wo", "O", "Wh", "S", "B", "Wh", "S"
                    ]
        self.numbers = [10, 2, 9, 12, 6, 4, 10, 9, 11, 3, 8, 8, 3, 4, 5, 5, 6, 11]
