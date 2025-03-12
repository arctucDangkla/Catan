import pygame
import math
import random
import Nodes_and_structures_map as grid


class Board:
    def __init__(self, width, height):
        # List that will keep track of tile placement
        self.tile_list = ["O", "S", "Wo", "Wh", "B", "S", "B", "Wh", "Wo", "D",
                     "Wo", "O", "Wo", "O", "Wh", "S", "B", "Wh", "S"
                    ]

        self.grid = grid.Graph()

        # Type checks inputs and Sets
        if (isinstance(width, int) or isinstance(width, float)) and (isinstance(height, int) or isinstance(height, float)):
            self.height = height
            self.width = width
        else:
            raise TypeError

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

    @staticmethod
    def __calculate_diamond(center_x, center_y, radius):
        points = []
        for i in range(4):  # 4 sides in a diamond
            angle_deg = 90 * i- 45   # Start at -90° so that point is at the top
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
        self.start_x = self.width * 0.35  # Starting x pos of the grid
        self.start_y = self.height / 6  # Starting y pos of the grid
        self.hex_size = self.height / 10  # Size of the hexagon
        self.hex_diff = self.hex_size * 1.875  # Difference between hexagons horizontally
        self.row_height = self.hex_diff - 21 # Difference between hexagons vertically





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


        self.point_lst = []
        for hex_count, row_offset in rows:
            for i in range(hex_count):
                # The center x and y positions of the current hex
                x = self.start_x + self.hex_diff * i - (hex_count % 3) * self.hex_size + 5 * (hex_count % 3)
                y = self.start_y + self.row_height * row_offset

                # Make and draw the hexagon
                points = self.__calculate_hexagon(x, y, self.hex_size)
                self.point_lst.append(points)
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
                        pygame.draw.circle(screen, (255, 0, 0), (x, y), int(self.hex_size * .4))

                    # Draws a game chip to make number more visible
                    pygame.draw.circle(screen, self.colors["D"], (x, y), int(self.hex_size * 0.3))

                    # "Draw" the number on screen
                    screen.blit(number_text, text_rect)

                    num_idx += 1
                tile_idx += 1
        # Draws the robber after all of the board is made. If the roll is 7,
        # highlight the robber.
        if roll == 7:
            pygame.draw.circle(screen, (255, 0, 0), self.robber_pos, int(self.hex_size * 0.4))
        pygame.draw.circle(screen, robber_color, self.robber_pos, int(self.hex_size * 0.3))


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

        # Loop through each hex in each row

    def create_buildings(self):

        """# Builds all the exterior houses
        order = [[0, 5], [0], [0, 1], [5], [1], [4, 5], [1, 2], [4], [2], [3, 4], [3], [2, 3]]
        order_b = [0, 1, 2, 3, 6, 7, 11, 12, 15, 16, 17, 18]
        count = -1
        for i in order_b:
            count += 1
            for d in order[count]:
                x = self.point_lst[i][d][0]
                y = self.point_lst[i][d][1]
                pygame.draw.polygon(screen, (100, 20, 50), self.__calculate_diamond(x, y, 10))"""

        for i in range(len(self.point_lst)):
            if i <= 2:
                top_row = 0
                node = i
            elif i <= 6:
                top_row = 2
                node = i - 3
            elif i <= 11:
                top_row = 4
                node = i - 7
            elif i <= 15:
                top_row = 6
                node = i - 12
            else:
                node = i - 16
                top_row = 8

            if top_row < 6:
                self.grid.node_list[top_row][node].location.append(self.point_lst[i][0])
                print(f'hex {i} add {self.point_lst[i][0]} to {self.grid.node_list[top_row][node]}')
            else:
                self.grid.node_list[top_row][node + 1].location.append(self.point_lst[i][0])
                print(f'hex {i} add {self.point_lst[i][0]} to {self.grid.node_list[top_row][node + 1]}')

            self.grid.node_list[top_row + 1][node].location.append(self.point_lst[i][5])
            print(f'hex {i} add {self.point_lst[i][5]} to {self.grid.node_list[top_row + 1][node]}')

            self.grid.node_list[top_row + 1][node + 1].location.append(self.point_lst[i][1])
            print(f'hex {i} add {self.point_lst[i][1]} to {self.grid.node_list[top_row + 1][node + 1]}')

            self.grid.node_list[top_row + 2][node].location.append(self.point_lst[i][4])
            print(f'hex {i} add {self.point_lst[i][4]} to {self.grid.node_list[top_row + 2][node]}')

            self.grid.node_list[top_row + 2][node + 1].location.append(self.point_lst[i][2])
            print(f'hex {i} add {self.point_lst[i][2]} to {self.grid.node_list[top_row + 2][node + 1]}')

            if top_row < 4:
                self.grid.node_list[top_row + 3][node + 1].location.append(self.point_lst[i][3])

            else:
                self.grid.node_list[top_row + 3][node].location.append(self.point_lst[i][3])





        for row in self.grid.node_list:
            for node in row:
                node.avg_location()


    def draw_building(self, screen):
        for row in self.grid.node_list:
            for node in row:
                pygame.draw.polygon(screen, (100, 20, 50), self.__calculate_diamond(node.location[0], node.location[1], 10))






