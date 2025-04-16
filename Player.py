from card_bank import CardBank


class Player:
    def __init__(self, player_id: int, name: str, color: str):

        self.player_id = player_id
        self.name = name
        self.color = color

        # Initialize player's resource bank
        self.bank = CardBank('player')

        # Development cards
        self.development_cards = {
            'K': 0,  # Knight
            'V': 0,  # Victory Point
            'R': 0,  # Road Building
            'Y': 0,  # Year of Plenty
            'M': 0  # Monopoly
        }

        # Special achievements
        self.has_longest_road = False
        self.has_largest_army = False

        # Buildings
        self.settlements = []
        self.cities = []
        self.roads = []
        self.id = player_id # 1-4
        # Victory points
        self._victory_points = 0
        self._recalculate_victory_points()

    def _recalculate_victory_points(self):
        """Update victory points based on buildings and cards"""
        points = 0
        points += len(self.settlements)  # 1 VP per settlement
        points += 2 * len(self.cities)  # 2 VP per city
        points += self.development_cards['V']  # Victory point cards

        if self.has_longest_road:
            points += 2
        if self.has_largest_army:
            points += 2

        self._victory_points = points

    def add_resource(self, resource_type: str, amount: int = 1):
        """Add resources to player's bank"""
        self.bank.add_card(resource_type, amount)

    def remove_resource(self, resource_type: str, amount: int = 1):
        """Remove resources from player's bank"""
        self.bank.remove_card(resource_type, amount)

    def get_resource_count(self, resource_type: str) -> int:
        """Get count of a specific resource"""
        return self.bank.bank[resource_type]

    def add_development_card(self, card_type: str):
        """Add a development card to player's hand"""
        if card_type not in self.development_cards:
            raise ValueError(f"Invalid development card type: {card_type}")
        self.development_cards[card_type] += 1
        if card_type == 'V':
            self._recalculate_victory_points()

    def play_development_card(self, card_type: str):
        """Play a development card from hand"""
        if card_type not in self.development_cards:
            raise ValueError(f"Invalid development card type: {card_type}")
        if self.development_cards[card_type] < 1:
            raise ValueError(f"No {card_type} cards available")
        self.development_cards[card_type] -= 1

    def build_settlement(self, location, initial_setup=False):
        """
        Build a settlement at specified location

        Args:
            location: Settlement location identifier
            initial_setup: If True, skips resource payment
        """
        if not initial_setup:
            # Standard settlement cost
            self.bank.remove_card('Wo', 1)  # Wood
            self.bank.remove_card('B', 1)  # Brick
            self.bank.remove_card('S', 1)  # Sheep
            self.bank.remove_card('Wh', 1)  # Wheat

        self.settlements.append(location)
        self._recalculate_victory_points()

    def build_city(self, location):
        """
        Upgrade a settlement to a city

        Args:
            location: Must reference an existing settlement
        """
        if location not in self.settlements:
            raise ValueError("Cannot build city - no settlement at this location")

        # City cost
        self.bank.remove_card('Wh', 2)  # Wheat
        self.bank.remove_card('O', 3)  # Ore

        self.settlements.remove(location)
        self.cities.append(location)
        self._recalculate_victory_points()

    def build_road(self, location, initial_setup=False):
        """
        Build a road at specified location

        Args:
            location: Road location identifier
            initial_setup: If True, skips resource payment
        """
        if not initial_setup:
            # Road cost
            self.bank.remove_card('Wo', 1)  # Wood
            self.bank.remove_card('B', 1)  # Brick

        self.roads.append(location)

        # Check for longest road
        if len(self.roads) >= 5 and not self.has_longest_road:
            self.has_longest_road = True
            self._recalculate_victory_points()

    def play_knight_card(self):
        """Play a knight development card"""
        if self.development_cards['K'] < 1:
            raise ValueError("No knight cards available")

        self.play_development_card('K')
        self.development_cards['K'] += 1  # For tracking largest army

        # Check for largest army
        if self.development_cards['K'] >= 3 and not self.has_largest_army:
            self.has_largest_army = True
            self._recalculate_victory_points()

    def trade_with_bank(self, offer: dict, request: dict):
        """
        Trade resources with the bank

        Args:
            offer: Dict of resources to give (e.g., {'Wo': 4})
            request: Dict of resources to receive (e.g., {'O': 1})
        """
        # Remove offered resources
        for resource, amount in offer.items():
            self.bank.remove_card(resource, amount)

        # Add requested resources
        for resource, amount in request.items():
            self.bank.add_card(resource, amount)

    @property
    def victory_points(self):
        """Current victory points (read-only)"""
        return self._victory_points

    def __str__(self):
        """String representation of player state"""
        resources = [
            f"Wood: {self.bank.bank['Wo']}",
            f"Brick: {self.bank.bank['B']}",
            f"Sheep: {self.bank.bank['S']}",
            f"Wheat: {self.bank.bank['Wh']}",
            f"Ore: {self.bank.bank['O']}"
        ]

        cards = [f"{self._get_card_name(k)}: {v}"
                 for k, v in self.development_cards.items() if v > 0]

        return (f"Player {self.id} ({self.name}) - {self._victory_points} VP\n"
                f"Resources: {', '.join(resources)}\n"
                f"Dev Cards: {', '.join(cards) if cards else 'None'}\n"
                f"Buildings: {len(self.settlements)} settlements, {len(self.cities)} cities\n"
                f"Roads: {len(self.roads)} (Longest Road: {'Yes' if self.has_longest_road else 'No'})\n"
                f"Knights: {self.development_cards['K']} (Largest Army: {'Yes' if self.has_largest_army else 'No'})")

    def _get_card_name(self, card_code: str) -> str:
        """Convert card code to full name"""
        card_names = {
            'K': 'Knight',
            'V': 'Victory Point',
            'R': 'Road Building',
            'Y': 'Year of Plenty',
            'M': 'Monopoly'
        }
        return card_names.get(card_code, card_code)
