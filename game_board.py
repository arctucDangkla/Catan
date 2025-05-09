import pygame
import math
import random
import Nodes_and_structures_map as Grid
from dice import Dice
import button
import card_bank


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

    def __init__(self, screen, width, height):
        self.screen = screen
        self.background = []
        self.hex_boarder = []
        self.cur_player = 1
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
            "Wo": (50, 90, 10),
            "B": (136, 57, 10),
            "Wh": (230, 153, 0),
            "O": (123, 111, 131),
            "S": (143, 206, 0),
            "D": (194, 178, 128),
            1: (255, 0, 0),
            2: (0, 255, 0),
            3: (0, 0, 255),
            4: (155, 155, 155)
        }

        # The numbers for each corresponding hexagon
        self.numbers = [10, 2, 9, 12, 6, 4, 10, 9, 11, 3, 8, 8, 3, 4, 5, 5, 6, 11]

        # Robber position
        self.robber_pos = None

        # Font info
        self.font = pygame.font.Font(None, 36)  # Default font, size 36 for text

        # Dice info
        self.dice_vals = Dice(self.width, self.height, board=self)
        self.dice_button = button.Button(screen, self.dice_vals.x, self.dice_vals.y, "none", self.dice_vals.total_width, self.dice_vals.size)

        # Size info for the hexagon
        self.start_x = self.width * 0.35  # Starting x pos of the grid
        self.start_y = self.height / 8  # Starting y pos of the grid
        self.hex_size = self.height / 10  # Size of the hexagon
        self.hex_diff = self.hex_size * 1.875  # Difference between hexagons horizontally
        self.row_height = self.hex_diff - 21  # Difference between hexagons vertically
        self.point_lst = []
        self.player_list = []

        # A list of tuples where (hex_count, row offset)
        self.rows = [
            (3, 0),
            (4, 1),
            (5, 2),
            (4, 3),
            (3, 4)
        ]

        self.generate_hexagons()
        self.create_buildings(self.width / 50 + (1/3))
        self.calculate_roads(self.screen, self.width / 125)   # self.width / 5 / (5+(1/3)))

        self.card_bank = card_bank.CardBank("game")
        self.dice_rolled = False

    def generate_hexagons(self):
        num_count = 0
        tile_count = 0
        self.point_lst = []
        for hex_count, row_offset in self.rows:

            for i in range(hex_count):
                # The center x and y positions of the current hex
                x = self.start_x + self.hex_diff * i - (hex_count % 3) * self.hex_size + 5 * (hex_count % 3)
                y = self.start_y + self.row_height * row_offset


                # Make and draw the hexagon
                if self.tile_list[tile_count] == "D":
                    self.point_lst.append([self.__calculate_hexagon(x, y, self.hex_size), True, 0, self.tile_list[tile_count]])
                else:
                    self.point_lst.append([self.__calculate_hexagon(x, y, self.hex_size), False, self.numbers[num_count], self.tile_list[tile_count]])
                    num_count += 1
                tile_count += 1

                self.background.append(list(self.__calculate_hexagon(x, y, self.hex_size*1.1)))
                self.hex_boarder.append(list(self.__calculate_hexagon(x, y, self.hex_size * 1.025)))
        self.grid.assign_tiles_to_nodes(self.point_lst)

    # Method that will draw the game board
    def draw_board(self, screen):
        # Color info for different parts of the board
        number_color = (0, 0, 0)  # Black color for numbers
        robber_color = (50, 50, 50)  # Dark gray for the robber

        # The index position for tiles and number lists
        tile_idx = 0
        num_idx = 0

        # Draws Sandy Background
        for point in self.background:
            pygame.draw.polygon(screen, (194, 178, 128), point)
        for point in self.hex_boarder:
            pygame.draw.polygon(screen, (0, 0, 0), point)


        for point in self.point_lst:
            pygame.draw.polygon(screen, self.colors[point[3]], point[0])
            x = sum([num[0] for num in point[0]]) / 6
            y = sum([num[1] for num in point[0]]) / 6

            # If it is the desert tile, move the robber, don't add number.
            if point[3] == 'D':
                self.robber_pos = [x, y]


            # Otherwise add the number like a normal tile
            else:
                # Initialize the number
                number_text = self.font.render(str(point[2]), True, number_color)
                text_rect = number_text.get_rect(center=(x, y))

                # If the current tile equals the roll, highlight the chip.
                if point[2] == self.dice_vals.result:
                    pygame.draw.circle(screen, (255, 255, 255), (x, y), int(self.hex_size * .4))

                # Draws a game chip to make number more visible
                pygame.draw.circle(screen, self.colors["D"], (x, y), int(self.hex_size * 0.3))

                # "Draw" the number on screen
                screen.blit(number_text, text_rect)


        # Draws the robber after all the board is made. If the roll is 7,
        # highlight the robber.
        if self.dice_vals.result == 7:
            pygame.draw.circle(screen, (255, 255, 255), self.robber_pos, int(self.hex_size * 0.4))
        pygame.draw.circle(screen, robber_color, self.robber_pos, int(self.hex_size * 0.3))


        # Draw the dice
        self.dice_vals.draw_die(screen, self.dice_vals.x, self.dice_vals.y, self.dice_vals.size,
                                self.dice_vals.values[0])  # Draw first die
        self.dice_vals.draw_die(screen, self.dice_vals.x + self.dice_vals.size + self.dice_vals.spacing,
                                self.dice_vals.y, self.dice_vals.size,
                                self.dice_vals.values[1])  # Draw second die
        # Checks for dice roll
        if self.dice_button.draw():
            self.dice_vals.roll_dice()

    # Shuffles the entire board and numbers
    def shuffle_board(self):
        self.tile_list = ["O", "S", "Wo", "Wh", "B", "S", "B", "Wh", "Wo", "D",
                          "Wo", "O", "Wo", "O", "Wh", "S", "B", "Wh", "S"
                          ]
        self.numbers = [10, 2, 9, 12, 6, 4, 10, 9, 11, 3, 8, 8, 3, 4, 5, 5, 6, 11]

        random.shuffle(self.tile_list)

        random.shuffle(self.numbers)
        self.generate_hexagons()

    # Creates the beginner board
    def beginner_board(self):
        self.tile_list = ["O", "S", "Wo", "Wh", "B", "S", "B", "Wh", "Wo", "D",
                          "Wo", "O", "Wo", "O", "Wh", "S", "B", "Wh", "S"
                          ]
        self.numbers = [10, 2, 9, 12, 6, 4, 10, 9, 11, 3, 8, 8, 3, 4, 5, 5, 6, 11]

        # Loop through each hex in each row

    # Sets up the map of all buildings
    def create_buildings(self, size):

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
            if top_row < 6:

                self.grid.node_list[top_row][node].location.append(self.point_lst[i][0][0])
            else:
                self.grid.node_list[top_row][node + 1].location.append(self.point_lst[i][0][0])

            self.grid.node_list[top_row + 1][node].location.append(self.point_lst[i][0][5])
            self.grid.node_list[top_row + 1][node + 1].location.append(self.point_lst[i][0][1])
            self.grid.node_list[top_row + 2][node].location.append(self.point_lst[i][0][4])
            self.grid.node_list[top_row + 2][node + 1].location.append(self.point_lst[i][0][2])

            if top_row < 4:
                self.grid.node_list[top_row + 3][node + 1].location.append(self.point_lst[i][0][3])
            else:
                self.grid.node_list[top_row + 3][node].location.append(self.point_lst[i][0][3])

        # Tells all nodes to average out nodes
        for row in self.grid.node_list:
            for node in row:
                node.avg_location(size, self.screen)

    # Prints all buildings to board
    def draw_building(self, screen):
        for row in self.grid.node_list:
            for node in row:
                if node.city:
                    pygame.draw.polygon(screen, self.colors[node.player],
                                        node.points)
                elif node.player == 0:
                    pass
                else:
                    pygame.draw.polygon(screen, self.colors[node.player],
                                        node.points)

    # Finds the points between all the nodes
    def calculate_roads(self, screen, size):
        for edge in self.grid.edge_list:
            edge.calc_road_points(screen, size)

    # Prints all buildings to board
    def draw_roads(self, screen):

        for edge in self.grid.edge_list:

            if edge.player == 0:
                pass
            else:
                color = (0, 0, 0)
                if edge.player == 1:
                    color = (155, 0, 0)
                elif edge.player == 2:
                    color = (0, 155, 0)
                elif edge.player == 3:
                    color = (0, 0, 155)
                elif edge.player == 4:
                    color = (55, 55, 55)

                pygame.draw.polygon(screen, color, edge.points)

    def next_player(self):
        self.cur_player += 1
        if self.cur_player > 4:
            self.cur_player = 1

    # Shows all spots where a player can build
    def find_buildable_road(self, player):
        if self.player_list[player-1].get_resource_count('Wo') > 0 and self.player_list[player-1].get_resource_count('B') > 0:
            self.grid.buildable_road(player)
        else:
            self.grid.build_able = []

    def find_buildable_house(self, player):
        self.grid.buildable_house(player)
        if self.player_list[player-1].get_resource_count('Wo') > 0 and self.player_list[player-1].get_resource_count('B') > 0 and self.player_list[player-1].get_resource_count('Wh') > 0 and self.player_list[player-1].get_resource_count('S') > 0:
            self.grid.buildable_house(player)
        else:
            self.grid.build_able = []

    # Print Buildable
    def draw_buildable(self, build, screen):
        for item in build:
            pygame.draw.circle(screen, (135, 206, 235), item.location, int(self.hex_size * 0.15))

    def awards_players(self, roll):
        for row in self.grid.node_list:
            for node in row:
                if node.player != 0 and roll in node.resources:
                    for tile in node.resources[roll]:
                        if node.city:
                            if self.card_bank.bank[tile] >= 2:
                                self.player_list[node.player - 1].add_resource(tile, 2)
                                self.card_bank.remove_card(tile, 2)
                            elif self.card_bank.bank[tile] == 1:
                                self.player_list[node.player - 1].add_resource(tile)
                                self.card_bank.remove_card(tile)
                        else:
                            if self.card_bank.bank[tile] >= 1:
                                self.player_list[node.player - 1].add_resource(tile)
                                self.card_bank.remove_card(tile)



