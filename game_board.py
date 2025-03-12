import pygame
import math
import random
import Nodes_and_structures_map as Grid


class Board:
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

    # To make Diamonds for the board
    @staticmethod
    def __calculate_diamond(center_x, center_y, radius):
        points = []
        for i in range(4):  # 4 sides in a diamond
            angle_deg = 90 * i - 45  # Start at -90° so that point is at the top
            angle_rad = math.radians(angle_deg)
            x = center_x + radius * math.cos(angle_rad)
            y = center_y + radius * math.sin(angle_rad)
            points.append((x, y))
        return points

    def __init__(self, width, height):
        # Type checks inputs and Sets
        if (isinstance(width, int) or isinstance(width, float)) and (
                isinstance(height, int) or isinstance(height, float)):
            self.height = height
            self.width = width
        else:
            raise TypeError

        # List that will keep track of tile placement
        self.tile_list = ["O", "S", "Wo", "Wh", "B", "S", "B", "Wh", "Wo", "D",
                          "Wo", "O", "Wo", "O", "Wh", "S", "B", "Wh", "S"
                          ]

        # Grid of structures and roads
        self.grid = Grid.Graph()

        # The colors of each different material and player in a dictionary
        self.colors = {
            "Wo": (81, 125, 25),
            "B": (156, 67, 0),
            "Wh": (240, 173, 0),
            "O": (123, 111, 131),
            "S": (143, 206, 0),
            "D": (194, 178, 128),
            1: (255, 0, 0),
            2: (0, 255, 0),
            3: (0, 0, 255),
            4: (255, 255, 255)
        }

        # The numbers for each corresponding hexagon
        self.numbers = [10, 2, 9, 12, 6, 4, 10, 9, 11, 3, 8, 8, 3, 4, 5, 5, 6, 11]

        # Robber position
        self.robber_pos = None

        # Font info
        self.font = pygame.font.Font(None, 36)  # Default font, size 36 for text

        # Size info for the hexagon
        self.start_x = self.width * 0.35  # Starting x pos of the grid
        self.start_y = self.height / 6  # Starting y pos of the grid
        self.hex_size = self.height / 10  # Size of the hexagon
        self.hex_diff = self.hex_size * 1.875  # Difference between hexagons horizontally
        self.row_height = self.hex_diff - 21  # Difference between hexagons vertically
        self.point_lst = []

        # A list of tuples where (hex_count, row offset)
        self.rows = [
            (3, 0),
            (4, 1),
            (5, 2),
            (4, 3),
            (3, 4)
        ]

        self.generate_hexagons()
        self.create_buildings()

    def generate_hexagons(self):

        for hex_count, row_offset in self.rows:
            for i in range(hex_count):
                # The center x and y positions of the current hex
                x = self.start_x + self.hex_diff * i - (hex_count % 3) * self.hex_size + 5 * (hex_count % 3)
                y = self.start_y + self.row_height * row_offset

                # Make and draw the hexagon
                self.point_lst.append(list(self.__calculate_hexagon(x, y, self.hex_size)))

    # Method that will draw the game board
    def draw_board(self, screen, roll):
        # Color info for different parts of the board
        number_color = (0, 0, 0)  # Black color for numbers
        robber_color = (50, 50, 50)  # Dark gray for the robber

        # The index position for tiles and number lists
        tile_idx = 0
        num_idx = 0

        for point in self.point_lst:
            pygame.draw.polygon(screen, self.colors[self.tile_list[tile_idx]], point)

            x = sum([num[0] for num in point]) / 6
            y = sum([num[1] for num in point]) / 6

            # If it is the desert tile, move the robber, don't add number.
            if self.tile_list[tile_idx] == "D":

                self.robber_pos = [x, y]

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
        # Draws the robber after all the board is made. If the roll is 7,
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

    # Sets up the map of all buildings
    def create_buildings(self):

        # Loops for every hex - Finds center location betweens each hec for nodes
        for i in range(len(self.point_lst)):

            # Finds what row the top most node is in for each hex
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

            # Goes through every point in hex and sends cords to node
            print(type(self.grid.node_list[top_row][node].location))
            print(self.grid.node_list[top_row][node].location)
            if top_row < 6:

                self.grid.node_list[top_row][node].location.append(self.point_lst[i][0])
            else:
                self.grid.node_list[top_row][node + 1].location.append(self.point_lst[i][0])

            self.grid.node_list[top_row + 1][node].location.append(self.point_lst[i][5])
            self.grid.node_list[top_row + 1][node + 1].location.append(self.point_lst[i][1])
            self.grid.node_list[top_row + 2][node].location.append(self.point_lst[i][4])
            self.grid.node_list[top_row + 2][node + 1].location.append(self.point_lst[i][2])

            if top_row < 4:
                self.grid.node_list[top_row + 3][node + 1].location.append(self.point_lst[i][3])
            else:
                self.grid.node_list[top_row + 3][node].location.append(self.point_lst[i][3])

        # Tells all nodes to average out nodes
        for row in self.grid.node_list:
            for node in row:
                node.avg_location()

    # Prints all buildings to board
    def draw_building(self, screen):
        for row in self.grid.node_list:
            for node in row:
                if node.city:
                    pygame.draw.polygon(screen, self.colors[node.player],
                                        self.__calculate_hexagon(node.location[0], node.location[1], 20))
                elif node.player == 0:
                    break
                else:
                    pygame.draw.polygon(screen, self.colors[node.player],
                                        self.__calculate_diamond(node.location[0], node.location[1], 15))
