import math
import button

# Temp class for writing
class Player:
    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, dog):
        self.__name = dog

    def __init__(self, name):
        self.name = name

    def __str__(self):

        return str(self.name)


# Exceptions when Trying to Build Road
class PlayerOwnsRoad(Exception):
    pass


class EdgeNotReal(Exception):
    pass


class TooCloseToStruc(Exception):
    pass


class Node:
    def __init__(self, name):
        self.name = name
        self.roads = list()
        self.player = 0
        self.city = False
        self.location = []
        self.button = None
        self.points = []
        self.resources = {}

    def __str__(self):
        return f"{self.name}"

    def avg_location(self, rad, screen):
        x = 0
        y = 0

        for i in self.location:
            x += i[0]
            y += i[1]



        x /= len(self.location)
        y /= len(self.location)

        self.location = (x, y)
        self.button = button.Button(screen, self.location[0] - rad, self.location[1] - rad, width=rad * 2,
                                    height=rad * 2)

        if self.city:
            pass
        else:
            self.house_points(x, y, rad)

    # House
    def house_points(self, center_x, center_y, radius):
        points = []
        for i in range(4):  # 4 sides in a diamond
            angle_deg = 90 * i - 45  # Start at -90° so that point is at the top
            angle_rad = math.radians(angle_deg)
            x = center_x + radius * math.cos(angle_rad)
            y = center_y + radius * math.sin(angle_rad)
            points.append((x, y))

        self.points = points


class Edge:

    @property
    def road(self):
        return self.__road

    @road.setter
    def road(self, val):
        if not val:
            self.__road = val
        elif isinstance(val, Player):
            self.__road = val
        else:
            raise TypeError

    def __init__(self, node_a: Node, node_b: Node, player: Player = False):
        self.nodes = [node_a, node_b]
        self.road = player
        self.player = 0
        self.points = []
        self.location = 0
        self.button = None
        node_a.roads.append(self)
        node_b.roads.append(self)

    def __str__(self):
        temp = list(self.nodes)
        txt = f"Between {str(temp[0])} and {str(temp[1])}"
        if self.road:
            txt = f"Road " + txt + f", Built by {self.road}"
        else:
            txt = "Path " + txt
        return txt

    def calc_road_points(self, screen, size):
        #points = [1, 2, 3, 4]
        points = []

        if not isinstance(self.nodes[0].location, tuple) or not isinstance(self.nodes[1].location, tuple):
            raise TypeError()

        if abs(self.nodes[1].location[0] - self.nodes[0].location[0]) > \
                abs(self.nodes[1].location[1] - self.nodes[0].location[1]):

            x = self.nodes[0].location[0]
            y = self.nodes[0].location[1]
            points += [(x, y+size),(x, y-size)]

            x = self.nodes[1].location[0]
            y = self.nodes[1].location[1]
            points += [(x, y - size), (x, y + size)]

        else:
            x = self.nodes[0].location[0]
            y = self.nodes[0].location[1]

            points += [(x + size, y), (x - size, y)]
            x = self.nodes[1].location[0]
            y = self.nodes[1].location[1]

            points += [(x - size, y), (x + size, y)]


        self.points = points

        x = 0
        y = 0
        for point in self.points:
            x += point[0]
            y += point[1]
        self.location = (x/4, y/4)
        self.button = button.Button(screen, self.location[0]-size, self.location[1]-size, width=size*2, height=size*2)


class Graph:

    def __init__(self):
        self.node_list = [[Node("A" + num) for num in "123"], [Node("B" + num) for num in "1234"],
                          [Node("C" + num) for num in "1234"], [Node("D" + num) for num, in "12345"],
                          [Node("E" + num) for num in "12345"], [Node("F" + num) for num in "123456"],
                          [Node("G" + num) for num in "123456"], [Node("H" + num) for num, in "12345"],
                          [Node("I" + num) for num in "12345"], [Node("J" + num) for num in "1234"],
                          [Node("K" + num) for num in "1234"], [Node("L" + num) for num in "123"]]
        self.edge_list = list()
        for row in range(0, 6, 2):
            for node in range(len(self.node_list[row])):
                a = Edge(self.node_list[row][node], self.node_list[row + 1][node])
                b = Edge(self.node_list[row][node], self.node_list[row + 1][node + 1])
                self.edge_list.append(a)
                self.edge_list.append(b)

            for node in range(len(self.node_list[row + 1])):
                a = Edge(self.node_list[row + 1][node], self.node_list[row + 2][node])
                self.edge_list.append(a)

        for row in range(-1, -7, -2):
            for node in range(len(self.node_list[row])):
                a = Edge(self.node_list[row][node], self.node_list[row - 1][node])
                b = Edge(self.node_list[row][node], self.node_list[row - 1][node + 1])
                self.edge_list.append(a)
                self.edge_list.append(b)
            for node in range(len(self.node_list[row - 1])):
                if row != -5:
                    a = Edge(self.node_list[row - 1][node], self.node_list[row - 2][node])
                    self.edge_list.append(a)

    def build_road(self, node_a: Node, node_b: Node, player: Player):
        for edge in node_a.roads:
            if node_b in edge.nodes:
                if not edge.road:
                    edge.road = player
                    return True
                else:
                    raise PlayerOwnsRoad
        raise EdgeNotReal

    def build_structure(self, player: Player, node_a: Node):
        if node_a.structure is None:
            raise TooCloseToStruc
        for edge in node_a.roads:
            temp_set = list(edge.nodes)
            temp_set.remove(node_a)
            if temp_set[0].structure is not None:
                raise TooCloseToStruc

        node_a.structure = player

    # looks very bad rn, will update when player class exist
    def buildable_road(self, player):
        build_able = []
        nodes = []
        for row in self.node_list:
            for node in row:
                if node.player == player:
                    nodes.append(node)


        for road in self.edge_list:
            if road.player == player:
                for node in road.nodes:
                    if node.player == 0:
                        nodes.append(node)

        for node in nodes:
            for road in node.roads:
                if road.player == 0 and road not in build_able:
                    build_able.append(road)

        self.build_able = build_able

    # looks very bad rn, will update when player class exist
    def buildable_house(self, player):
        build_able = []

        for road in self.edge_list:
            if road.player == player:


                for node in road.nodes:

                    if self.status_buildable(node):
                        build_able.append(node)
        self.build_able = build_able

    def status_buildable(self, node: Node):
        for road in node.roads:
            if road.nodes[0].player != 0 or road.nodes[1].player != 0:
                return False
        return True

    def assign_tiles_to_nodes(self, tiles):
        for row in self.node_list:
            for col in row:
                col.resources = {}
        for num in range(len(tiles)):
            tile = tiles[num]
            if num < 3:
                mod = 0
                row = 0
            elif num < 7:
                mod = -3
                row = 2
            elif num < 12:
                mod = -7
                row = 4
            elif num < 16:
                mod = -12
                row = 6
            else:
                mod = -16
                row = 8
            if num <= 6:
                list_thing = [self.node_list[row][num+mod], self.node_list[row+1][num+mod+1], self.node_list[row+1][num+mod], self.node_list[row+2][num+mod+1], self.node_list[row+2][num+mod], self.node_list[row+3][num+mod+1]]

            elif num >= 12:
                list_thing = [self.node_list[row][num+mod+1], self.node_list[row+1][num+mod+1], self.node_list[row+1][num+mod], self.node_list[row+2][num+mod+1], self.node_list[row+2][num+mod], self.node_list[row+3][num+mod]]

            else:
                list_thing = [self.node_list[row][num+mod], self.node_list[row+1][num+mod+1], self.node_list[row+1][num+mod], self.node_list[row+2][num+mod+1], self.node_list[row+2][num+mod], self.node_list[row+3][num+mod]]

            for thing in list_thing:
                if tile[2] not in thing.resources:
                    thing.resources[tile[2]] = [tile[3]]
                else:
                    thing.resources[tile[2]].append(tile[3])