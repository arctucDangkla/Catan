import unittest
from Player import Player


class TestPlayerInitialization(unittest.TestCase):
    def test_player_creation(self):
        """Test basic player creation"""
        player = Player(player_id=1, name="Alice", color="red")
        self.assertEqual(player.player_id, 1)
        self.assertEqual(player.name, "Alice")
        self.assertEqual(player.color, "red")
        self.assertEqual(player.victory_points, 0)


class TestResourceManagement(unittest.TestCase):
    def setUp(self):
        self.player = Player(player_id=1, name="Bob", color="blue")

    def test_add_resources(self):
        """Test adding resources"""
        self.player.add_resource('Wo', 2)  # Wood
        self.player.add_resource('Wh')  # Wheat (default 1)
        self.assertEqual(self.player.get_resource_count('Wo'), 2)
        self.assertEqual(self.player.get_resource_count('Wh'), 1)

    def test_remove_resources(self):
        """Test removing resources"""
        self.player.add_resource('S', 3)  # Sheep
        self.player.remove_resource('S', 2)
        self.assertEqual(self.player.get_resource_count('S'), 1)

        with self.assertRaises(Exception):
            self.player.remove_resource('O', 1)  # No ore

    def test_development_card_invalid_card(self):
        with self.assertRaises(Exception):
            self.player.play_development_card('Wo')
        with self.assertRaises(Exception):
            self.player.add_development_card('Wo')
    def test_development_card_not_enough(self):
        with self.assertRaises(Exception):
            self.player.play_development_card('K')
    def test_development_card_played(self):
        self.player.add_development_card('K')
        self.assertEqual(self.player.development_cards['K'], 1)
        self.player.play_development_card('K')
        self.assertEqual(self.player.development_cards['K'], 0)
        self.player.has_longest_road = True
        self.player.has_largest_army = True
        self.player._recalculate_victory_points()
        self.assertEqual(self.player.victory_points, 4)


class TestBuilding(unittest.TestCase):
    def setUp(self):
        self.player = Player(player_id=1, name="Charlie", color="green")
        # Add resources needed for buildings
        self.player.add_resource('Wo', 10)
        self.player.add_resource('B', 10)  # Brick
        self.player.add_resource('S', 10)  # Sheep
        self.player.add_resource('Wh', 10)  # Wheat
        self.player.add_resource('O', 10)  # Ore

    def test_build_settlement(self):
        """Test settlement building"""
        self.player.build_settlement("A1")
        self.assertEqual(len(self.player.settlements), 1)
        self.assertEqual(self.player.victory_points, 1)

        # Verify resource costs
        self.assertEqual(self.player.get_resource_count('Wo'), 9)
        self.assertEqual(self.player.get_resource_count('B'), 9)
        self.assertEqual(self.player.get_resource_count('S'), 9)
        self.assertEqual(self.player.get_resource_count('Wh'), 9)

    def test_build_city(self):
        """Test city building"""
        # Need a settlement first
        self.player.build_settlement("B2", initial_setup=True)
        self.player.build_city("B2")
        self.assertEqual(len(self.player.settlements), 0)
        self.assertEqual(len(self.player.cities), 1)
        self.assertEqual(self.player.victory_points, 2)


class TestDevelopmentCards(unittest.TestCase):
    def setUp(self):
        self.player = Player(player_id=1, name="Dana", color="orange")

    def test_add_development_card(self):
        """Test adding development cards"""
        self.player.add_development_card('K')  # Knight
        self.player.add_development_card('V')  # Victory Point
        self.assertEqual(self.player.development_cards['K'], 1)
        self.assertEqual(self.player.development_cards['V'], 1)
        self.assertEqual(self.player.victory_points, 1)

