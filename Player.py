class Player:
    def __init__(self, player_id: int, name: str, color: tuple):
        """
        Initialize a player with basic attributes and empty resources/buildings
        
        Args:
            player_id: Unique integer identifier (1-4)
            name: Player's name
            color: RGB tuple for player color (e.g., (255,0,0) for red)
        """
        self.player_id = player_id
        self.name = name
        self.color = color
        
        # Resources
        self.resources = {
            'wood': 0,
            'brick': 0,
            'sheep': 0,
            'wheat': 0,
            'ore': 0
        }
        
        # Development cards
        self.development_cards = {
            'knight': 0,
            'victory_point': 0,
            'road_building': 0,
            'year_of_plenty': 0,
            'monopoly': 0
        }
        
        # Special cards
        self.has_longest_road = False
        self.has_largest_army = False
        
        # Buildings
        self.settlements = []
        self.cities = []
        self.roads = []
        
        # Victory points (base + special cards)
        self._victory_points = 0
        self._recalculate_victory_points()

    def _recalculate_victory_points(self):
        """Update victory points based on buildings and cards"""
        points = 0
        points += len(self.settlements)  # 1 VP per settlement
        points += 2 * len(self.cities)   # 2 VP per city
        points += self.development_cards['victory_point']
        
        if self.has_longest_road:
            points += 2
        if self.has_largest_army:
            points += 2
            
        self._victory_points = points

    def add_resource(self, resource_type: str, amount: int = 1):
        """Add resources to player's hand"""
        if resource_type not in self.resources:
            raise ValueError(f"Invalid resource type: {resource_type}")
        self.resources[resource_type] += amount

    def remove_resource(self, resource_type: str, amount: int = 1):
        """Remove resources from player's hand with validation"""
        if resource_type not in self.resources:
            raise ValueError(f"Invalid resource type: {resource_type}")
        if self.resources[resource_type] < amount:
            raise ValueError(f"Not enough {resource_type} (has {self.resources[resource_type]}, needs {amount})")
        self.resources[resource_type] -= amount

    def add_development_card(self, card_type: str):
        """Add a development card to player's hand"""
        if card_type not in self.development_cards:
            raise ValueError(f"Invalid development card type: {card_type}")
        self.development_cards[card_type] += 1
        if card_type == 'victory_point':
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
            location: Tuple of coordinates or node reference
            initial_setup: If True, skips resource payment (for game setup)
        """
        if not initial_setup:
            # Standard settlement cost
            required_resources = {'wood': 1, 'brick': 1, 'sheep': 1, 'wheat': 1}
            for res, amount in required_resources.items():
                self.remove_resource(res, amount)
                
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
        required_resources = {'wheat': 2, 'ore': 3}
        for res, amount in required_resources.items():
            self.remove_resource(res, amount)
            
        self.settlements.remove(location)
        self.cities.append(location)
        self._recalculate_victory_points()

    def build_road(self, location, initial_setup=False):
        """
        Build a road at specified location
        
        Args:
            location: Tuple of coordinates or edge reference
            initial_setup: If True, skips resource payment (for game setup)
        """
        if not initial_setup:
            # Road cost
            required_resources = {'wood': 1, 'brick': 1}
            for res, amount in required_resources.items():
                self.remove_resource(res, amount)
                
        self.roads.append(location)
        
        # Check for longest road
        if len(self.roads) >= 5 and not self.has_longest_road:
            self.has_longest_road = True
            self._recalculate_victory_points()

    def play_knight_card(self):
        """Play a knight development card"""
        if self.development_cards['knight'] < 1:
            raise ValueError("No knight cards available")
            
        self.play_development_card('knight')
        self.development_cards['knight'] += 1  # For tracking largest army
        
        # Check for largest army
        if self.development_cards['knight'] >= 3 and not self.has_largest_army:
            self.has_largest_army = True
            self._recalculate_victory_points()

    def trade_with_bank(self, offer: dict, request: dict):
        """
        Trade resources with the bank
        
        Args:
            offer: Dict of resources to give (e.g., {'wood': 4})
            request: Dict of resources to receive (e.g., {'ore': 1})
        """
        # Validate offer
        for res, amount in offer.items():
            self.remove_resource(res, amount)
            
        # Add requested resources
        for res, amount in request.items():
            self.add_resource(res, amount)

    @property
    def victory_points(self):
        """Current victory points (read-only)"""
        return self._victory_points

    def __str__(self):
        """String representation of player state"""
        resources = ", ".join([f"{k}:{v}" for k, v in self.resources.items() if v > 0])
        cards = ", ".join([f"{k}:{v}" for k, v in self.development_cards.items() if v > 0])
        
        return (f"Player {self.player_id} ({self.name}) - {self._victory_points} VP\n"
                f"Resources: {resources or 'None'}\n"
                f"Dev Cards: {cards or 'None'}\n"
                f"Buildings: {len(self.settlements)} settlements, {len(self.cities)} cities\n"
                f"Roads: {len(self.roads)} (Longest Road: {'Yes' if self.has_longest_road else 'No'})\n"
                f"Knights: {self.development_cards['knight']} (Largest Army: {'Yes' if self.has_largest_army else 'No'})")
