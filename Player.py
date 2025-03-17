class Player:
    def __init__(self, player_id, color):
        self.player_id = player_id
        self.color = color
        self.resources = {'Wo': 0, 'B': 0, 'S': 0, 'Wh': 0, 'O': 0}
        self.development_cards = {'K': 0, 'V': 0, 'P': 0}
        self.settlements = []
        self.cities = []
        self.roads = []
        self.victory_points = 0

    def add_resource(self, resource, amount=1):
        if resource in self.resources:
            self.resources[resource] += amount
        else:
            raise ValueError(f"Invalid resource: {resource}")

    def remove_resource(self, resource, amount=1):
        if resource in self.resources:
            if self.resources[resource] >= amount:
                self.resources[resource] -= amount
            else:
                raise ValueError(f"Not enough {resource} to remove.")
        else:
            raise ValueError(f"Invalid resource: {resource}")

    def add_development_card(self, card_type):
        if card_type in self.development_cards:
            self.development_cards[card_type] += 1
        else:
            raise ValueError(f"Invalid development card type: {card_type}")

    def build_settlement(self, location):
        required_resources = {'Wo': 1, 'B': 1, 'S': 1, 'Wh': 1}
        for resource, amount in required_resources.items():
            if self.resources[resource] < amount:
                raise ValueError(f"Not enough {resource} to build a settlement.")
        for resource, amount in required_resources.items():
            self.resources[resource] -= amount
        self.settlements.append(location)
        self.victory_points += 1

    def build_city(self, location):
        required_resources = {'Wh': 2, 'O': 3}
        for resource, amount in required_resources.items():
            if self.resources[resource] < amount:
                raise ValueError(f"Not enough {resource} to build a city.")
        for resource, amount in required_resources.items():
            self.resources[resource] -= amount
        if location in self.settlements:
            self.settlements.remove(location)
            self.cities.append(location)
        else:
            raise ValueError(f"No settlement at location {location} to upgrade.")
        self.victory_points += 1

    def build_road(self, location):
        required_resources = {'Wo': 1, 'B': 1}
        for resource, amount in required_resources.items():
            if self.resources[resource] < amount:
                raise ValueError(f"Not enough {resource} to build a road.")
        for resource, amount in required_resources.items():
            self.resources[resource] -= amount
        self.roads.append(location)

    def has_longest_road(self):
        return len(self.roads) >= 5

    def has_largest_army(self):
        return self.development_cards['K'] >= 3

    def update_victory_points(self):
        self.victory_points = len(self.settlements) + 2 * len(self.cities)
        self.victory_points += self.development_cards['V']
        if self.has_longest_road():
            self.victory_points += 2
        if self.has_largest_army():
            self.victory_points += 2

    def __str__(self):
        return (f"Player {self.player_id} ({self.color}):\n"
                f"Resources: {self.resources}\n"
                f"Development Cards: {self.development_cards}\n"
                f"Settlements: {self.settlements}\n"
                f"Cities: {self.cities}\n"
                f"Roads: {self.roads}\n"
                f"Victory Points: {self.victory_points}")
