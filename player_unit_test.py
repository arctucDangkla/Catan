import unittest
from player import Player


class TestPlayer(unittest.TestCase):
    def setUp(self):
        """Create a test player before each test"""
        self.player = Player(player_id=1, name="Test Player", color="blue")

    def test_initialization(self):
        """Test player initialization with correct values"""
        self.assertEqual(self.player.player_id, 1)
        self.assertEqual(self.player.name, "Test Player")
        self.assertEqual(self.player.color, "blue")
        self.assertEqual(self.player.victory_points, 0)

        # Verify initial resource counts are zero
        for resource in ['Wo', 'B', 'S', 'Wh', 'O']:
            self.assertEqual(self.player.get_resource_count(resource), 0)

        # Verify no development cards initially
        for card in self.player.development_cards.values():
            self.assertEqual(card, 0)

    def test_add_and_remove_resource(self):
        """Test adding and removing resources"""
        # Test adding resources
        self.player.add_resource('Wo', 3)
        self.assertEqual(self.player.get_resource_count('Wo'), 3)

        self.player.add_resource('Wh')
        self.assertEqual(self.player.get_resource_count('Wh'), 1)

        # Test removing resources
        self.player.add_resource('B', 2)
        self.player.remove_resource('B')
        self.assertEqual(self.player.get_resource_count('B'), 1)

        # Test removing non-existent resource
        with self.assertRaises(Exception):
            self.player.remove_resource('O')

    def test_build_settlement(self):
        """Test building a settlement with resource cost"""
        # Add required resources
        for resource in ['Wo', 'B', 'S', 'Wh']:
            self.player.add_resource(resource, 1)

        self.player.build_settlement("A1")

        # Verify resources were deducted
        for resource in ['Wo', 'B', 'S', 'Wh']:
            self.assertEqual(self.player.get_resource_count(resource), 0)

        # Verify settlement was added and VP increased
        self.assertEqual(len(self.player.settlements), 1)
        self.assertEqual(self.player.victory_points, 1)

        # Test insufficient resources
        with self.assertRaises(Exception):
            self.player.build_settlement("B2")

    def test_build_settlement_initial_setup(self):
        """Test building settlement during initial setup (no resource cost)"""
        self.player.build_settlement("B2", initial_setup=True)

        # Verify no resources were deducted
        for resource in ['Wo', 'B', 'S', 'Wh']:
            self.assertEqual(self.player.get_resource_count(resource), 0)

        # Verify settlement was added
        self.assertEqual(len(self.player.settlements), 1)

    def test_build_city(self):
        """Test upgrading a settlement to a city"""
        # Setup - build a settlement first
        self.player.build_settlement("C3", initial_setup=True)

        # Add resources needed for city
        self.player.add_resource('Wh', 2)
        self.player.add_resource('O', 3)

        self.player.build_city("C3")

        # Verify resources were deducted
        self.assertEqual(self.player.get_resource_count('Wh'), 0)
        self.assertEqual(self.player.get_resource_count('O'), 0)

        # Verify city was added and settlement removed
        self.assertEqual(len(self.player.settlements), 0)
        self.assertEqual(len(self.player.cities), 1)
        self.assertEqual(self.player.victory_points, 2)  # Cities give 2 VP

        # Test building city without settlement
        with self.assertRaises(ValueError):
            self.player.build_city("D4")

    def test_build_road(self):
        """Test building a road with resource cost"""
        # Add required resources
        self.player.add_resource('Wo', 1)
        self.player.add_resource('B', 1)

        self.player.build_road("R1")

        # Verify resources were deducted
        self.assertEqual(self.player.get_resource_count('Wo'), 0)
        self.assertEqual(self.player.get_resource_count('B'), 0)

        # Verify road was added
        self.assertEqual(len(self.player.roads), 1)

        # Test insufficient resources
        with self.assertRaises(Exception):
            self.player.build_road("R2")

    def test_build_road_initial_setup(self):
        """Test building road during initial setup (no resource cost)"""
        self.player.build_road("R1", initial_setup=True)

        # Verify no resources were deducted
        self.assertEqual(self.player.get_resource_count('Wo'), 0)
        self.assertEqual(self.player.get_resource_count('B'), 0)

        # Verify road was added
        self.assertEqual(len(self.player.roads), 1)

    def test_development_cards(self):
        """Test adding and playing development cards"""
        # Test adding cards
        self.player.add_development_card('K')  # Knight
        self.player.add_development_card('V')  # Victory Point

        self.assertEqual(self.player.development_cards['K'], 1)
        self.assertEqual(self.player.development_cards['V'], 1)
        self.assertEqual(self.player.victory_points, 1)  # VP card should count

        # Test playing cards
        self.player.play_development_card('K')
        self.assertEqual(self.player.development_cards['K'], 0)

        # Test playing non-existent card
        with self.assertRaises(ValueError):
            self.player.play_development_card('M')  # No monopoly card

        # Victory points should decrease when VP card is played
        self.player.play_development_card('V')
        self.assertEqual(self.player.development_cards['V'], 0)
        self.assertEqual(self.player.victory_points, 0)

    def test_play_knight_card(self):
        """Test playing knight card and tracking largest army"""
        self.player.add_development_card('K')
        self.player.add_development_card('K')
        self.player.add_development_card('K')

        # Play first knight (should trigger largest army)
        self.player.play_knight_card()
        self.assertEqual(self.player.development_cards['K'], 2)  # 3-1=2 (but +1 when played)
        self.assertTrue(self.player.has_largest_army)
        self.assertEqual(self.player.victory_points, 2)

        # Play second knight
        self.player.play_knight_card()
        self.assertEqual(self.player.development_cards['K'], 1)  # 2-1=1 (but +1 when played)

        # Play third knight (should drop below 3)
        self.player.play_knight_card()
        self.assertEqual(self.player.development_cards['K'], 0)  # 1-1=0 (but +1 when played)
        self.assertFalse(self.player.has_largest_army)
        self.assertEqual(self.player.victory_points, 0)

    def test_trade_with_bank(self):
        """Test trading resources with the bank"""
        # Setup resources
        self.player.add_resource('Wo', 4)
        self.player.add_resource('S', 2)

        # Trade 4 wood for 1 ore
        self.player.trade_with_bank({'Wo': 4}, {'O': 1})

        # Verify trade
        self.assertEqual(self.player.get_resource_count('Wo'), 0)
        self.assertEqual(self.player.get_resource_count('O'), 1)
        self.assertEqual(self.player.get_resource_count('S'), 2)  # Unchanged

        # Test insufficient resources for trade
        with self.assertRaises(Exception):
            self.player.trade_with_bank({'Wo': 1}, {'B': 1})

    def test_victory_points_calculation(self):
        """Test victory point calculation with various sources"""
        # Add settlement
        self.player.build_settlement("A1", initial_setup=True)
        self.assertEqual(self.player.victory_points, 1)

        # Add city
        self.player.build_settlement("B2", initial_setup=True)
        self.player.add_resource('Wh', 2)
        self.player.add_resource('O', 3)
        self.player.build_city("B2")
        self.assertEqual(self.player.victory_points, 3)  # 1 (settlement) + 2 (city)

        # Add VP card
        self.player.add_development_card('V')
        self.assertEqual(self.player.victory_points, 4)

        # Add longest road
        for i in range(5):
            self.player.build_road(f"R{i}", initial_setup=True)
        self.assertTrue(self.player.has_longest_road)
        self.assertEqual(self.player.victory_points, 6)

        # Add largest army
        for i in range(3):
            self.player.add_development_card('K')
            self.player.play_knight_card()
        self.assertTrue(self.player.has_largest_army)
        self.assertEqual(self.player.victory_points, 8)


if __name__ == '__main__':
    unittest.main()