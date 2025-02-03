from random import randint


class Resource:
    pass


# temp name
class Value:

    def __init__(self, num, pos, resource):
        self.value = num
        self.pos = pos
        self.resource = resource

    def __str__(self):
        return f"Hex {self.pos}, has a value of {self.value}, and has {self.resource}"


class ValMap:

    def __init__(self, resource: list, default: bool = True):
        self.val_list = []
        self.roll_chart = {}
        self.resource = resource
        if default:
            # Creates Default Map
            self.default_map()

        else:
            # Randomly generates a map
            self.random_map()

    def default_map(self):
        self.map_gen([5, 2, 6, 3, 8, 10, 9, 12, 11, 4, 8, 10, 9, 4, 5, 6, 3, 11])

    def random_map(self):
        nums = [5, 2, 6, 3, 8, 10, 9, 12, 11, 4, 8, 10, 9, 4, 5, 6, 3, 11]
        new_numbs = []
        while len(nums) != 0:
            new_numbs.append(nums.pop(randint(0, len(nums))))
        self.map_gen(new_numbs)

    def map_gen(self, num_or: list):
        val_list = []

        order = ["A1", "B1", "C1", "D1", "E1", "E2", "E3", "D4", "C5", "B4",
                 "A3", "A2", "B2", "C2", "D2", "D3", "E4", "D3", "E3"]

        for x in range(len(order)):
            if self.resource[x] == "desert":
                num = 0
            else:
                num = num_or.pop(0)

            v = Value(num, order[x], self.resource[x])

            if num in self.roll_chart:
                self.roll_chart[num].append(v)
            else:
                self.roll_chart[num] = [v]

            val_list.append(v)

        self.val_list = val_list

    def roll_chart_return(self):
        for x in self.roll_chart:
            print(f"{x} grants {str(self.roll_chart[x])}")
        return self.roll_chart

    def val_list_return(self):
        return self.val_list

    def rolled_resources(self, rolled_num):
        return self.roll_chart[rolled_num]


if __name__ == "__main__":

    maps = ValMap(["desert", "grass", "stone", "water", "grass", "stone", "water", "grass", "stone", "water", "grass",
                   "stone", "water", "grass", "stone", "water", "grass", "stone", "water"])

    maps.roll_chart_return()


